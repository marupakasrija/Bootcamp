import httpx
import json
import uuid
import xml.etree.ElementTree as ET
from typing import Dict, List
from ..core.config import settings

class PubMedService:
    async def get_paper_data(self, paper_id: str) -> Dict:
        """Fetch paper data from PubMed API"""
        # Clean up the paper_id format
        if paper_id.startswith("PMC"):
            pmcid = paper_id
        else:
            pmcid = f"PMC{paper_id}"
            
        # Use E-utilities API
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            "db": "pmc",
            "id": pmcid.replace("PMC", ""),
            "retmode": "xml"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                # Parse XML response
                xml_content = response.text
                if not xml_content.strip():
                    raise Exception("Empty response from API")
                    
                root = ET.fromstring(xml_content)
                if root is None:
                    raise Exception("Failed to parse XML response")
                    
                # Process the XML data
                # Update this line in the return statement
                return {
                    "paper_id": pmcid,
                    "title": self._extract_title_from_xml(root),
                    "abstract": self._extract_abstract_from_xml(root),
                    "source_type": "pubmed",
                    "figures": self.extract_figures_from_xml(root, pmcid)  # Pass pmcid here
                }
            except httpx.HTTPStatusError as e:
                raise Exception(f"Failed to fetch paper data: {e}")
            except ET.ParseError as e:
                raise Exception(f"Failed to parse XML response: {e}")
            except Exception as e:
                raise Exception(f"Error processing paper data: {str(e)}")

    def _extract_title_from_xml(self, root: ET.Element) -> str:
        """Extract title from XML response"""
        try:
            title_elem = root.find(".//article-title")
            return title_elem.text if title_elem is not None else ""
        except AttributeError:
            return ""
    
    def _extract_abstract_from_xml(self, root: ET.Element) -> str:
        """Extract abstract from XML response"""
        try:
            abstract_texts = []
            # Find all text content in abstract, including nested elements
            abstract = root.find(".//abstract")
            if abstract is not None:
                for elem in abstract.iter():
                    if elem.text and elem.text.strip():
                        abstract_texts.append(elem.text.strip())
                    if elem.tail and elem.tail.strip():
                        abstract_texts.append(elem.tail.strip())
            return " ".join(abstract_texts)
        except AttributeError:
            return ""
    
    def extract_figures_from_xml(self, root: ET.Element, paper_id: str) -> List[Dict]:
        figures = []
        seen_urls = set()
        try:
            # Find all figure elements including supplementary materials
            figure_elements = (
                root.findall(".//fig") +
                root.findall(".//graphic") +
                root.findall(".//supplementary-material") +
                root.findall(".//inline-graphic") +
                root.findall(".//fig-group/*")
            )
    
            print(f"Found {len(figure_elements)} figure elements")
            
            for fig in figure_elements:
                url = self._get_figure_url(fig, paper_id)
                
                # Skip duplicates based on URL
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                
                caption_texts = []
                caption = fig.find(".//caption") or fig.find(".//label")
                if caption is not None:
                    for elem in caption.iter():
                        if elem.text and elem.text.strip():
                            caption_texts.append(elem.text.strip())
                        if elem.tail and elem.tail.strip():
                            caption_texts.append(elem.tail.strip())
                
                label = fig.find(".//label") or fig.find(".//title")
                label_text = label.text if label is not None and label.text else ""
                
                fig_id = (
                    fig.get("id") or
                    fig.get("xlink:href") or
                    (fig.find(".//object-id[@pub-id-type='doi']").text if fig.find(".//object-id[@pub-id-type='doi']") else None) or
                    label_text or
                    str(uuid.uuid4())
                )
                
                # Only add figures with either a caption or URL
                if caption_texts or url:
                    figure = {
                        "figure_id": f"{paper_id}_{fig_id}",
                        "caption": " ".join(caption_texts),
                        "label": label_text,
                        "url": url
                    }
                    figures.append(figure)
    
            return figures
        except Exception as e:
            print(f"Error extracting figures: {str(e)}")
            return []
    
    def _get_figure_url(self, fig_elem: ET.Element, paper_id: str) -> str:
        try:
            url = None
            # Try all possible URL sources with proper namespace handling
            sources = [
                (".//graphic", "{http://www.w3.org/1999/xlink}href"),
                (".//graphic", "xlink:href"),
                (".//media", "{http://www.w3.org/1999/xlink}href"),
                (".//media", "xlink:href"),
                (".//supplementary-material", "{http://www.w3.org/1999/xlink}href"),
                (".//supplementary-material", "xlink:href"),
                # Direct attribute on the element itself
                (".", "{http://www.w3.org/1999/xlink}href"),
                (".", "xlink:href")
            ]
            
            for xpath, attr in sources:
                elem = fig_elem.find(xpath) if xpath != "." else fig_elem
                if elem is not None:
                    url = elem.get(attr)
                    if url:
                        break
        
            # Check for DOI
            if not url:
                doi = fig_elem.find(".//object-id[@pub-id-type='doi']")
                if doi is not None and doi.text:
                    url = f"https://doi.org/{doi.text}"
        
            # Convert relative URLs to absolute URLs using the correct base URL format
            if url and not url.startswith(('http://', 'https://', 'ftp://', 'data:')):
                pmc_id = paper_id.replace('PMC', '')
                url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/bin/{url}"
                print(f"Constructed URL: {url}")  # Debug logging
        
            return url if url else ""
        except Exception as e:
            print(f"Error getting figure URL: {str(e)}")
            return ""