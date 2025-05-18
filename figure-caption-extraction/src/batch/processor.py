import sys
import logging
from pathlib import Path
from typing import List, Union
from ..core.config import settings
from ..core.service_registry import ServiceRegistry
from ..services.data_access import DataAccessService

class BatchProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_service = DataAccessService()
        self.source = ServiceRegistry._source_providers[settings.ACTIVE_SOURCE]()
        
    async def process_file(self, file_path: Union[str, Path]) -> bool:
        """Process a file containing paper IDs"""
        try:
            with open(file_path, 'r') as f:
                paper_ids = [line.strip() for line in f if line.strip()]
            
            success = await self.process_ids(paper_ids)
            return success
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return False
    
    async def process_ids(self, paper_ids: List[str]) -> bool:
        """Process a list of paper IDs"""
        success_count = 0
        total = len(paper_ids)
        
        for i in range(0, total, settings.BATCH_SIZE):
            batch = paper_ids[i:i + settings.BATCH_SIZE]
            try:
                for paper_id in batch:
                    paper_data = await self.source.get_paper_data(paper_id)
                    if paper_data:
                        await self.data_service.save_paper(paper_data)
                        success_count += 1
            except Exception as e:
                self.logger.error(f"Batch processing error: {str(e)}")
        
        success_rate = success_count / total
        self.logger.info(f"Processed {success_count}/{total} papers successfully")
        return success_rate >= 0.9  # Consider successful if 90% processed

    def watch_folder(self):
        """Watch folder for new files"""
        watch_path = Path(settings.WATCH_FOLDER)
        watch_path.mkdir(parents=True, exist_ok=True)
        
        try:
            import watchdog.observers
            import watchdog.events
            # Implement watchdog observer here
            self.logger.info(f"Watching folder: {watch_path}")
        except Exception as e:
            self.logger.error(f"Error watching folder: {str(e)}")
            sys.exit(settings.EXIT_FAILURE)

if __name__ == "__main__":
    processor = BatchProcessor()
    success = processor.watch_folder()
    sys.exit(settings.EXIT_SUCCESS if success else settings.EXIT_FAILURE)