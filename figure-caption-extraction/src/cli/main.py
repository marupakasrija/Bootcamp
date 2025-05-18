import typer
import asyncio
from typing import List
from pathlib import Path
from ..services.data_access import DataAccessService
from ..services.pubmed import PubMedService
from ..services.entity_recognition import EntityRecognitionService

app = typer.Typer()

@app.command()
def process_papers(paper_ids: List[str]):
    """Process papers by their PMC IDs"""
    asyncio.run(async_process_papers(paper_ids))

@app.command()
def process_file(file_path: Path):
    """Process papers from a file containing PMC IDs"""
    if not file_path.exists():
        typer.echo(f"File {file_path} does not exist")
        raise typer.Exit(1)

    paper_ids = file_path.read_text().splitlines()
    asyncio.run(async_process_papers(paper_ids))

async def async_process_papers(paper_ids: List[str]):
    data_service = DataAccessService()
    pubmed_service = PubMedService()
    entity_service = EntityRecognitionService()

    for paper_id in paper_ids:
        typer.echo(f"Processing paper {paper_id}...")
        
        # Check if paper exists in database
        if await data_service.get_paper(paper_id):
            typer.echo(f"Paper {paper_id} already exists in database")
            continue

        try:
            paper_data = await pubmed_service.get_paper_data(paper_id)
            figures = pubmed_service.extract_figures(paper_data)
            
            for figure in figures:
                entities = await entity_service.process_caption(figure["caption"])
                figure["entities"] = entities

            await data_service.save_paper(paper_data)
            for figure in figures:
                figure_id = await data_service.save_figure(paper_id, figure)
                await data_service.save_entities(figure_id, figure["entities"])

            typer.echo(f"Successfully processed paper {paper_id}")
        except Exception as e:
            typer.echo(f"Error processing paper {paper_id}: {str(e)}")

if __name__ == "__main__":
    app()