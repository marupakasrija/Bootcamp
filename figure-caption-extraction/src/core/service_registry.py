from typing import Dict, Type
from ..services.base.source_provider import SourceProvider
from ..services.base.entity_recognizer import EntityRecognizer

class ServiceRegistry:
    """Central registry for service providers"""
    
    _source_providers: Dict[str, Type[SourceProvider]] = {}
    _entity_recognizers: Dict[str, Type[EntityRecognizer]] = {}
    
    @classmethod
    def register_source(cls, name: str, provider: Type[SourceProvider]):
        cls._source_providers[name] = provider
    
    @classmethod
    def register_recognizer(cls, name: str, recognizer: Type[EntityRecognizer]):
        cls._entity_recognizers[name] = recognizer