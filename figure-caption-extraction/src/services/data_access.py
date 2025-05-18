import pandas as pd
from typing import List, Dict, Optional
from ..core.database import db

class DataAccessService:
    @staticmethod
    def export_to_csv():
        """Export current database state to CSV files"""
        try:
            # Create data directory if it doesn't exist
            import os
            data_dir = 'data'
            os.makedirs(data_dir, exist_ok=True)

            # Set proper file permissions before writing
            for file_name in ['papers.csv', 'figures.csv', 'entities.csv']:
                file_path = os.path.join(data_dir, file_name)
                # Ensure the file is writable or create it if it doesn't exist
                try:
                    with open(file_path, 'a') as f:
                        pass
                    os.chmod(file_path, 0o666)  # Set read/write permissions for everyone
                except Exception as e:
                    print(f"Error setting permissions for {file_name}: {str(e)}")

            # Export the data
            papers_df = db.conn.execute("SELECT * FROM papers").df()
            papers_df.to_csv('data/papers.csv', index=False)
            
            figures_df = db.conn.execute("SELECT * FROM figures").df()
            figures_df.to_csv('data/figures.csv', index=False)
            
            entities_df = db.conn.execute("SELECT * FROM entities").df()
            entities_df.to_csv('data/entities.csv', index=False)
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")

    @staticmethod
    async def save_paper(paper_data: Dict) -> str:
        """Save paper information in database and update CSVs"""
        paper_id = paper_data["paper_id"]
        title = paper_data.get("title", "")  
        abstract = paper_data.get("abstract", "")  
        source_type = paper_data.get("source_type", "pubmed")
        
        # Check if paper exists
        existing = db.conn.execute("SELECT 1 FROM papers WHERE paper_id = ?", (paper_id,)).fetchone()
        
        if existing:
            # Update existing paper
            db.conn.execute("""
                UPDATE papers 
                SET title = ?, abstract = ?, source_type = ?
                WHERE paper_id = ?
            """, (title, abstract, source_type, paper_id))
            
            # Delete existing figures and their entities
            figures = db.conn.execute("SELECT figure_id FROM figures WHERE paper_id = ?", (paper_id,)).fetchall()
            for (figure_id,) in figures:
                db.conn.execute("DELETE FROM entities WHERE figure_id = ?", (figure_id,))
            db.conn.execute("DELETE FROM figures WHERE paper_id = ?", (paper_id,))
        else:
            # Insert new paper
            db.conn.execute("""
                INSERT INTO papers (paper_id, title, abstract, source_type)
                VALUES (?, ?, ?, ?)
            """, (paper_id, title, abstract, source_type))
        
        # Export updated data to CSVs
        DataAccessService.export_to_csv()
        return paper_id

    @staticmethod
    async def save_figure(paper_id: str, figure_data: Dict) -> str:
        """Save figure information and update CSVs"""
        figure_id = figure_data["figure_id"]
        db.conn.execute("""
            INSERT INTO figures (figure_id, paper_id, caption, url)
            VALUES (?, ?, ?, ?)
        """, (figure_id, paper_id, figure_data["caption"], figure_data["url"]))
        
        # Export updated data to CSVs
        DataAccessService.export_to_csv()
        return figure_id

    @staticmethod
    async def save_entities(figure_id: str, entities: List[Dict]):
        """Save entity information and update CSVs"""
        for entity in entities:
            db.conn.execute("""
                INSERT INTO entities (entity_id, figure_id, entity_type, entity_text)
                VALUES (?, ?, ?, ?)
            """, (entity["entity_id"], figure_id, entity["entity_type"], entity["entity_text"]))
        
        # Export updated data to CSVs
        DataAccessService.export_to_csv()

    @staticmethod
    async def get_paper(paper_id: str) -> Optional[Dict]:
        """Retrieve paper information from database"""
        result = db.conn.execute("""
            SELECT p.paper_id, p.title, p.abstract, p.source_type,
                   f.figure_id, f.caption, f.url,
                   e.entity_type, e.entity_text
            FROM papers p
            LEFT JOIN figures f ON p.paper_id = f.paper_id
            LEFT JOIN entities e ON f.figure_id = e.figure_id
            WHERE p.paper_id = ?
        """, (paper_id,))
        paper_data = result.fetchall()
        
        if not paper_data:
            return None
            
        # Get column names from cursor description
        columns = [description[0] for description in result.description]
        
        # Convert first row to dictionary
        first_row = dict(zip(columns, paper_data[0]))
        
        # Check if we need to fetch from API (when title and abstract are empty)
        if (not first_row['title'] and not first_row['abstract']) or not first_row['figure_id']:
            # Import PubMedService here to avoid circular imports
            from ..services.pubmed import PubMedService
            pubmed_service = PubMedService()
            try:
                api_data = await pubmed_service.get_paper_data(paper_id)
                if api_data:
                    # Update the database with API data
                    await DataAccessService.save_paper(api_data)
                    for figure in api_data.get('figures', []):
                        await DataAccessService.save_figure(paper_id, figure)
                    return api_data
            except Exception as e:
                print(f"Failed to fetch from API: {e}")
        
        # Organize the results into a structured format
        paper = {
            "paper_id": first_row['paper_id'],
            "title": first_row['title'],
            "abstract": first_row['abstract'],
            "source_type": first_row['source_type'],
            "figures": []
        }
        
        # Group figures and their entities
        figures_dict = {}
        for row in paper_data:
            row_dict = dict(zip(columns, row))
            figure_id = row_dict['figure_id']
            if figure_id:
                if figure_id not in figures_dict:
                    figures_dict[figure_id] = {
                        "figure_id": figure_id,
                        "caption": row_dict['caption'],
                        "url": row_dict['url'],
                        "entities": []
                    }
                if row_dict['entity_type']:
                    figures_dict[figure_id]["entities"].append({
                        "entity_type": row_dict['entity_type'],
                        "entity_text": row_dict['entity_text']
                    })
        
        paper["figures"] = list(figures_dict.values())
        return paper

    @staticmethod
    async def get_all_papers() -> List[Dict]:
        """Retrieve all papers from the database"""
        result = db.conn.execute("""
            SELECT p.paper_id, p.title, p.abstract, p.source_type,
                   f.figure_id, f.caption, f.url,
                   e.entity_type, e.entity_text
            FROM papers p
            LEFT JOIN figures f ON p.paper_id = f.paper_id
            LEFT JOIN entities e ON f.figure_id = e.figure_id
        """)
        papers_data = result.fetchall()
        
        # Get column names from cursor description
        columns = [description[0] for description in result.description]
        
        papers_dict = {}
        for row in papers_data:
            # Convert tuple to dictionary using column names
            row_dict = dict(zip(columns, row))
            paper_id = row_dict['paper_id']
            
            if paper_id not in papers_dict:
                papers_dict[paper_id] = {
                    "paper_id": paper_id,
                    "title": row_dict['title'] or "",  # Handle None values
                    "abstract": row_dict['abstract'] or "",  # Handle None values
                    "source_type": row_dict['source_type'],
                    "figures": []
                }
            
            figure_id = row_dict['figure_id']
            if figure_id:
                # Check if this figure is already added
                figure_exists = False
                for existing_figure in papers_dict[paper_id]['figures']:
                    if existing_figure['figure_id'] == figure_id:
                        figure_exists = True
                        # Add entity if it doesn't exist
                        if row_dict['entity_type']:
                            existing_figure['entities'].append({
                                "entity_type": row_dict['entity_type'],
                                "entity_text": row_dict['entity_text']
                            })
                        break
                
                if not figure_exists:
                    figure = {
                        "figure_id": figure_id,
                        "caption": row_dict['caption'] or "",  # Handle None values
                        "url": row_dict['url'] or "",  # Handle None values
                        "entities": []
                    }
                    if row_dict['entity_type']:
                        figure['entities'].append({
                            "entity_type": row_dict['entity_type'],
                            "entity_text": row_dict['entity_text']
                        })
                    papers_dict[paper_id]['figures'].append(figure)
        
        return list(papers_dict.values())