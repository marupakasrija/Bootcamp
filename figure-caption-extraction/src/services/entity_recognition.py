from typing import List, Dict
import httpx
import uuid  # Add this import
from ..core.config import settings

class EntityRecognitionService:
    def __init__(self):
        self.base_url = settings.PUBTATOR_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_entities(self, text: str) -> List[Dict]:
        """Extract entities from text using PubTator API"""
        if not text or not text.strip():
            return []
            
        try:
            response = await self.client.post(
                f"{self.base_url}/annotations/annotate",
                json={
                    "text": text,
                    "concepts": ["gene", "disease", "chemical", "species", "mutation"]
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Add better error logging
            if not data:
                print(f"No entities found for text: {text[:100]}...")
            else:
                print(f"Found {len(data)} entities in text")
                print(f"Response data: {data[:2]}")  # Print first two entities for debugging
            return data
        except httpx.HTTPError as e:
            print(f"PubTator API error: {str(e)}\nURL: {e.request.url}")
            return []
        except Exception as e:
            print(f"Unexpected error in entity extraction: {str(e)}")
            return []

    async def process_caption(self, caption: str) -> List[Dict]:
        """Process a figure caption to extract relevant entities"""
        if not caption:
            return []
            
        try:
            # Split caption into smaller chunks if too long
            max_chunk_size = 1000
            chunks = [caption[i:i + max_chunk_size] for i in range(0, len(caption), max_chunk_size)]
            
            all_entities = []
            for chunk in chunks:
                entities = await self.get_entities(chunk)
                all_entities.extend(entities)
                
            # Remove duplicates and format entities
            seen_entities = set()
            unique_entities = []
            for entity in all_entities:
                key = (entity.get("type"), entity.get("text"))
                if key not in seen_entities:
                    seen_entities.add(key)
                    unique_entities.append({
                        "entity_type": entity.get("type", "unknown"),
                        "entity_text": entity.get("text", ""),
                        "entity_id": entity.get("id") or str(uuid.uuid4())
                    })
                    
            return unique_entities
        except Exception as e:
            print(f"Error processing caption: {str(e)}")
            return []

    async def close(self):
        await self.client.aclose()