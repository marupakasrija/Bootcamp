import httpx
import json
import uuid
import xml.etree.ElementTree as ET
from typing import Dict, List
from ..core.config import settings

class PubMedService:
    async def get_paper_data(self, paper_id: str, id_type: str = "pmc") -> Dict:
        """Fetch paper data from PubMed API
        Args:
            paper_id: The ID of the paper
            id_type: Either 'pmc' or 'pmid'
        """
        try:
            # First, get detailed metadata using esummary
            summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            summary_params = {
                "db": "pubmed" if id_type.lower() == "pmid" else "pmc",
                "id": paper_id,
                "retmode": "json"
            }
            
            async with httpx.AsyncClient() as client:
                print(f"[DEBUG] Fetching metadata for {paper_id} from {summary_params['db']} database")
                summary_response = await client.get(summary_url, params=summary_params)
                summary_response.raise_for_status()
                summary_data = summary_response.json()
                
                # Then get full article data using efetch
                url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
                params = {
                    "db": summary_params['db'],
                    "id": paper_id,
                    "retmode": "xml"
                }
                
                print(f"[DEBUG] Fetching full article data")
                print(f"[DEBUG] URL: {url}")
                print(f"[DEBUG] Params: {params}")
                
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
                return {
                    "paper_id": paper_id,
                    "title": self._extract_title_from_xml(root),
                    "abstract": self._extract_abstract_from_xml(root),
                    "source_type": "pubmed",
                    "figures": self.extract_figures_from_xml(root, paper_id)
                }
        except Exception as e:
            print(f"[DEBUG] Error: {str(e)}")
            raise

    def _print_xml_structure(self, element: ET.Element, depth: int = 0):
        """Helper method to print XML structure"""
        indent = "  " * depth
        print(f"{indent}[DEBUG] Element: {element.tag}")
        # Print attributes if they exist
        if element.attrib:
            print(f"{indent}[DEBUG] Attributes: {element.attrib}")
        # Print text content if it exists and isn't just whitespace
        if element.text and element.text.strip():
            print(f"{indent}[DEBUG] Text: {element.text.strip()[:100]}")
        for child in element:
            self._print_xml_structure(child, depth + 1)

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
                if paper_id.startswith('PMC'):
                    pmc_id = paper_id.replace('PMC', '')
                    url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/bin/{url}"
                else:
                    # For PubMed articles, use a different base URL
                    url = f"https://www.ncbi.nlm.nih.gov/pubmed/{paper_id}/bin/{url}"
                print(f"Constructed URL: {url}")  # Debug logging
        
            return url if url else ""
        except Exception as e:
            print(f"Error getting figure URL: {str(e)}")
            return ""

    def extract_figures_from_xml(self, root: ET.Element, paper_id: str) -> List[Dict]:
        figures = []
        seen_urls = set()
        try:
            print(f"[DEBUG] Starting figure extraction for paper {paper_id}")
            print(f"[DEBUG] XML root tag: {root.tag}")
            
            # Handle both PubMed and PMC XML structures
            if root.tag == 'PubmedArticleSet':
                article = root.find('.//Article')
            else:
                article = root.find('.//article')
                
            if article is None:
                print("[DEBUG] No article element found")
                return []
            
            print("[DEBUG] Found article element, checking its structure:")
            self._print_xml_structure(article)
            
            # Rest of the method remains the same
            figure_elements = []
            
            # For PubMed XML
            if root.tag == 'PubmedArticleSet':
                figures_section = article.find('.//Figures')
                if figures_section is not None:
                    figure_elements.extend(figures_section.findall('.//Figure'))
            else:
                # For PMC XML - existing code
                body = article.find('.//body')
                if body is not None:
                    figure_elements.extend(body.findall('.//fig'))
                    figure_elements.extend(body.findall('.//graphic'))
                    figure_elements.extend(body.findall('.//supplementary-material'))
                
                back = article.find('.//back')
                if back is not None:
                    figure_elements.extend(back.findall('.//fig'))
                    figure_elements.extend(back.findall('.//graphic'))
                    figure_elements.extend(back.findall('.//supplementary-material'))
                
                floats = article.find('.//floats-group')
                if floats is not None:
                    figure_elements.extend(floats.findall('.//fig'))
                    figure_elements.extend(floats.findall('.//graphic'))
                    figure_elements.extend(floats.findall('.//supplementary-material'))
            
            # Process figures
            for i, fig in enumerate(figure_elements, 1):
                print(f"\n[DEBUG] Processing figure {i}/{len(figure_elements)}")
                print(f"[DEBUG] Figure element tag: {fig.tag}")
                print(f"[DEBUG] Figure attributes: {fig.attrib}")
                print(f"[DEBUG] Figure parent: {fig.getparent().tag if hasattr(fig, 'getparent') else 'unknown'}")
                
                # Try to get figure ID first
                fig_id = None
                id_candidates = ['id', 'ID', '{http://www.w3.org/1999/xlink}href']
                for id_attr in id_candidates:
                    fig_id = fig.get(id_attr)
                    if fig_id:
                        print(f"[DEBUG] Found figure ID using attribute {id_attr}: {fig_id}")
                        break
                        
                if not fig_id:
                    fig_id = str(uuid.uuid4())
                    print(f"[DEBUG] Generated UUID for figure: {fig_id}")
                
                # Extract caption
                caption_texts = []
                caption = fig.find('caption')
                if caption is not None:
                    print("[DEBUG] Found caption element")
                    for elem in caption.iter():
                        if elem.text and elem.text.strip():
                            caption_texts.append(elem.text.strip())
                            print(f"[DEBUG] Added caption text: {elem.text.strip()}")
                        if elem.tail and elem.tail.strip():
                            caption_texts.append(elem.tail.strip())
                            print(f"[DEBUG] Added caption tail: {elem.tail.strip()}")
                
                # Get URL
                url = self._get_figure_url(fig, paper_id)
                print(f"[DEBUG] Extracted URL: {url}")
                
                if url in seen_urls:
                    print(f"[DEBUG] Skipping duplicate URL: {url}")
                    continue
                seen_urls.add(url)
                
                # Create figure object
                if caption_texts or url:
                    figure = {
                        "figure_id": f"{paper_id}_{fig_id}",
                        "caption": " ".join(caption_texts),
                        "url": url
                    }
                    figures.append(figure)
                    print(f"[DEBUG] Added figure: {figure}")
                else:
                    print("[DEBUG] Skipping figure due to missing caption and URL")
            
            print(f"\n[DEBUG] Total figures extracted: {len(figures)}")
            return figures
        except Exception as e:
            print(f"[DEBUG] Error in figure extraction: {str(e)}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return []
    
    def _extract_title_from_xml(self, root: ET.Element) -> str:
        """Extract paper title from XML"""
        try:
            # Try different possible locations for title
            title_elem = root.find('.//ArticleTitle')  # PubMed XML uses ArticleTitle
            if title_elem is None:
                title_elem = root.find('.//article-title')  # PMC XML uses article-title
            if title_elem is None:
                title_elem = root.find('.//title')
            
            if title_elem is not None and title_elem.text:
                return title_elem.text.strip()
            else:
                print("[DEBUG] No title found in XML")
                return ""
        except Exception as e:
            print(f"[DEBUG] Error extracting title: {e}")
            return ""

    def _extract_abstract_from_xml(self, root: ET.Element) -> str:
        """Extract paper abstract from XML"""
        try:
            # Try PubMed XML structure first
            abstract_elem = root.find('.//Abstract')
            if abstract_elem is not None:
                abstract_text = ' '.join(
                    text.strip() for text in abstract_elem.itertext()
                    if text and text.strip()
                )
                return abstract_text

            # Try PMC XML structure
            abstract_elem = root.find('.//abstract')
            if abstract_elem is not None:
                abstract_text = ' '.join(
                    p.text.strip() for p in abstract_elem.findall('.//p') 
                    if p.text and p.text.strip()
                )
                return abstract_text

            print("[DEBUG] No abstract found in XML")
            return ""
        except Exception as e:
            print(f"[DEBUG] Error extracting abstract: {e}")
            return ""