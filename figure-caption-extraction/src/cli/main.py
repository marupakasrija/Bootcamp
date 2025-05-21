import typer
import asyncio
from typing import List
from pathlib import Path
from enum import Enum
from ..services.data_access import DataAccessService
from ..services.pubmed import PubMedService
from ..services.entity_recognition import EntityRecognitionService

app = typer.Typer()

class IDType(str, Enum):
    PMC = "pmc"
    PMID = "pmid"

@app.command()
def process_papers(
    paper_ids: List[str],
    id_type: IDType = typer.Option(
        IDType.PMC,
        help="Type of ID provided (pmc or pmid)"
    )
):
    """Process papers by their IDs (PMC or PMID)"""
    asyncio.run(async_process_papers(paper_ids, id_type))

@app.command()
def process_file(
    file_path: Path,
    id_type: IDType = typer.Option(
        IDType.PMC,
        help="Type of ID provided in file (pmc or pmid)"
    )
):
    """Process papers from a file containing IDs (PMC or PMID)"""
    if not file_path.exists():
        typer.echo(f"File {file_path} does not exist")
        raise typer.Exit(1)

    paper_ids = file_path.read_text().splitlines()
    asyncio.run(async_process_papers(paper_ids, id_type))

async def async_process_papers(paper_ids: List[str], id_type: IDType):
    data_service = DataAccessService()
    pubmed_service = PubMedService()
    entity_service = EntityRecognitionService()

    for paper_id in paper_ids:
        # Format paper ID based on type
        formatted_id = f"PMC{paper_id}" if id_type == IDType.PMC and not paper_id.startswith("PMC") else paper_id
        typer.echo(f"Processing paper {formatted_id}...")
        
        # Check if paper exists in database
        if await data_service.get_paper(formatted_id):
            typer.echo(f"Paper {formatted_id} already exists in database")
            continue

        try:
            paper_data = await pubmed_service.get_paper_data(formatted_id)
            figures = pubmed_service.extract_figures(paper_data)
            
            for figure in figures:
                entities = await entity_service.process_caption(figure["caption"])
                figure["entities"] = entities

            await data_service.save_paper(paper_data)
            for figure in figures:
                figure_id = await data_service.save_figure(formatted_id, figure)
                await data_service.save_entities(figure_id, figure["entities"])

            typer.echo(f"Successfully processed paper {formatted_id}")
        except Exception as e:
            typer.echo(f"Error processing paper {formatted_id}: {str(e)}")

if __name__ == "__main__":
    app()