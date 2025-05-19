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
paper_id = st.text_input("Enter PMC ID")
upload_file = st.file_uploader("Or upload a file with PMC IDs", type=["txt"])

if st.button("Process"):
    if paper_id:
        paper_ids = [paper_id]
    elif upload_file:
        paper_ids = upload_file.getvalue().decode().splitlines()
    else:
        st.error("Please provide a PMC ID or upload a file")
        st.stop()

    for pid in paper_ids:
        st.write(f"Processing {pid}...")
        
        # Check cache first
        paper = asyncio.run(data_service.get_paper(pid))
        if paper:
            st.success(f"Paper {pid} found in database")
            st.json(paper)
            continue

        try:
            # Fetch and process paper
            # Current incorrect code
            # Remove this incorrect line:
            # figures = pubmed_service.extract_figures_from_xml(paper_data)  # This is wrong
            
            # Replace with:
            paper_data = asyncio.run(pubmed_service.get_paper_data(pid))
            figures = paper_data.get('figures', [])  # The figures are already in paper_data
            
            # Inside the try block where figures are processed
            for figure in figures:
                if figure.get("caption"):  # Only process if caption exists
                    print(f"Processing caption: {figure['caption'][:100]}...")
                    entities = asyncio.run(entity_service.process_caption(figure["caption"]))
                    print(f"Found {len(entities)} entities")
                    figure["entities"] = entities
                else:
                    figure["entities"] = []

            # Save to database
            asyncio.run(data_service.save_paper(paper_data))
            for figure in figures:
                figure_id = asyncio.run(data_service.save_figure(pid, figure))
                asyncio.run(data_service.save_entities(figure_id, figure["entities"]))

            st.success(f"Successfully processed paper {pid}")
            st.json(paper_data)
        except Exception as e:
            st.error(f"Error processing paper {pid}: {str(e)}")

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