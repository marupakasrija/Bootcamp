from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...core.auth import verify_api_key
from ...services.data_access import DataAccessService
from ...services.pubmed import PubMedService
from ...services.entity_recognition import EntityRecognitionService
from ..models import Paper, PaperRequest

router = APIRouter()

@router.post("/papers/process", response_model=List[Paper])
async def process_papers(request: PaperRequest, api_key: str = Depends(verify_api_key)):
    papers = []
    data_service = DataAccessService()
    pubmed_service = PubMedService()
    entity_service = EntityRecognitionService()

    for paper_id in request.paper_ids:
        # Check if paper exists in database
        paper = await data_service.get_paper(paper_id)
        if paper:
            papers.append(paper)
            continue

        # Fetch from PubMed if not in database
        try:
            paper_data = await pubmed_service.get_paper_data(paper_id)
            figures = pubmed_service.extract_figures(paper_data)
            
            # Process entities for each figure
            for figure in figures:
                entities = await entity_service.process_caption(figure["caption"])
                figure["entities"] = entities

            # Save to database
            await data_service.save_paper(paper_data)
            for figure in figures:
                figure_id = await data_service.save_figure(paper_id, figure)
                await data_service.save_entities(figure_id, figure["entities"])

            papers.append(paper_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return papers

@router.get("/papers/{paper_id}", response_model=Paper)
async def get_paper(paper_id: str, api_key: str = Depends(verify_api_key)):
    data_service = DataAccessService()
    paper = await data_service.get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper