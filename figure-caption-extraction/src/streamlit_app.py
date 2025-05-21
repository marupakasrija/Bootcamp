import streamlit as st
import asyncio
from src.services.data_access import DataAccessService
from src.core.init_services import initialize_services
from src.core.service_registry import ServiceRegistry
from src.services.entity_recognition import EntityRecognitionService
from src.core.config import settings

# Initialize all services
initialize_services()

st.title("Figure Caption Extraction System")

# Initialize services
data_service = DataAccessService()
source_provider = ServiceRegistry._source_providers[settings.ACTIVE_SOURCE]()
entity_service = EntityRecognitionService()
pubmed_service = source_provider  # Add this line to define pubmed_service

# Input section
st.header("Paper Processing")

# Add ID type selection
id_type = st.radio(
    "Select ID Type",
    options=["PMC ID", "PMID"],
    index=0,
    help="Choose whether you're entering a PMC ID or PubMed ID"
)

# Modify input label based on selection
paper_id = st.text_input(f"Enter {id_type}")
upload_file = st.file_uploader(f"Or upload a file with {id_type}s", type=["txt"])

if st.button("Process"):
    if paper_id:
        paper_ids = [paper_id]
    elif upload_file:
        paper_ids = upload_file.getvalue().decode().splitlines()
    else:
        st.error(f"Please provide a {id_type} or upload a file")
        st.stop()

    for pid in paper_ids:
        # Format ID based on type - only add PMC prefix for PMC IDs
        formatted_id = pid
        if id_type == "PMC ID":
            if not pid.startswith("PMC"):
                formatted_id = f"PMC{pid}"
        # For PMID, use the ID as is
            
        st.write(f"Processing {formatted_id}...")
        
        # Check cache first
        paper = asyncio.run(data_service.get_paper(formatted_id))
        if paper:
            st.success(f"Paper {formatted_id} found in database")
            st.json(paper)
            continue

        try:
            # Fetch and process paper
            paper_data = asyncio.run(pubmed_service.get_paper_data(
                formatted_id,
                id_type="pmid" if id_type == "PMID" else "pmc"
            ))
            figures = paper_data.get('figures', [])
            
            # Process figures
            for figure in figures:
                if figure.get("caption"):
                    entities = asyncio.run(entity_service.process_caption(figure["caption"]))
                    figure["entities"] = entities
                else:
                    figure["entities"] = []

            # Save to database
            asyncio.run(data_service.save_paper(paper_data))
            for figure in figures:
                figure_id = asyncio.run(data_service.save_figure(formatted_id, figure))
                asyncio.run(data_service.save_entities(figure_id, figure["entities"]))

            st.success(f"Successfully processed paper {formatted_id}")
            st.json(paper_data)
        except Exception as e:
            st.error(f"Error processing paper {formatted_id}: {str(e)}")

# Export section
st.header("Export Data")
if st.button("Export to CSV"):
    try:
        data_service.export_to_csv()
        st.success("Successfully exported data to CSV files in the 'data' directory:")
        st.markdown("- data/papers.csv")
        st.markdown("- data/figures.csv")
        st.markdown("- data/entities.csv")
    except Exception as e:
        st.error(f"Error exporting to CSV: {str(e)}")

# View existing papers
st.header("View Existing Papers")
if st.button("Show all papers"):
    papers = asyncio.run(data_service.get_all_papers())
    for paper in papers:
        st.subheader(f"Paper {paper['paper_id']}")
        st.write(f"Title: {paper['title']}")
        st.write(f"Abstract: {paper['abstract']}")
        # In the "View Existing Papers" section, modify the figure display code:
        for figure in paper['figures']:
            st.write(f"Figure: {figure['figure_id']}")
            st.write(f"Caption: {figure['caption']}")
            if figure['url']:
                # Check if URL is a remote URL or local path
                if figure['url'].startswith(('http://', 'https://', 'ftp://', 'data:')):
                    st.image(figure['url'], use_column_width=True)
                else:
                    st.write(f"Local figure path: {figure['url']}")
            st.write("Entities:")
            for entity in figure['entities']:
                st.write(f"- {entity['entity_type']}: {entity['entity_text']}")