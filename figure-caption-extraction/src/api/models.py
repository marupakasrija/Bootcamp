from pydantic import BaseModel
from typing import List, Optional

class FigureEntity(BaseModel):
    entity_type: str
    entity_text: str
    entity_id: str

class Figure(BaseModel):
    figure_id: str
    caption: str
    url: Optional[str] = None
    entities: List[FigureEntity] = []

class Paper(BaseModel):
    paper_id: str
    title: str
    abstract: str
    figures: List[Figure] = []

class PaperRequest(BaseModel):
    paper_ids: List[str]