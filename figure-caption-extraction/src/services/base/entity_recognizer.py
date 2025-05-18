from abc import ABC, abstractmethod
from typing import List, Dict

class EntityRecognizer(ABC):
    """Base interface for entity recognition services"""
    
    @abstractmethod
    async def get_entities(self, text: str) -> List[Dict]:
        """Extract entities from text"""
        pass