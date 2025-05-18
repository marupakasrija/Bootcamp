from abc import ABC, abstractmethod
from typing import Dict, List

class SourceProvider(ABC):
    """Base interface for paper source providers"""
    
    @abstractmethod
    async def get_paper_data(self, paper_id: str) -> Dict:
        """Fetch paper data from source"""
        pass
    
    @abstractmethod
    async def extract_figures(self, content: str) -> List[Dict]:
        """Extract figures from paper content"""
        pass