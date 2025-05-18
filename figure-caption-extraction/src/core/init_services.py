from .service_registry import ServiceRegistry
from ..services.pubmed import PubMedService
# Import future providers here
# from ..services.arxiv import ArxivProvider

def initialize_services():
    """Initialize and register all service providers"""
    # Register default PubMed provider
    ServiceRegistry.register_source("pubmed", PubMedService)
    
    # Register future providers here
    # ServiceRegistry.register_source("arxiv", ArxivProvider)