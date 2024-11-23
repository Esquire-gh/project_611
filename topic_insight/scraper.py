import json
import re
import os
import requests
from bs4 import BeautifulSoup
from .constants import header
from urllib.parse import urlparse, urlparse, quote


class OxylabScraperAPI:
    def __init__(self, product_asin):
        self.payload = {
            'source': 'amazon_reviews',
            'query': product_asin,
            'pages': 1, 
            'parse': True
        }
        self.username = os.environ['OXYLAB_USERNAME']
        self.password = os.environ['OXYLAB_PASSWORD']

    def get_product_reviews(self):
        response = requests.request(
            'POST',
            'https://realtime.oxylabs.io/v1/queries',
            auth=(self.username, self.password),
            json=self.payload,
        )
        response.raise_for_status()
        return response.json()

    def list_reviews(self):
        reviews = []
        data = self.get_product_reviews()
        if data:
            results = data['results']
            for result in results:
                reviews.extend(result['content']['reviews'])

            return [
                {
                    **review, 
                    "title": re.sub(r"^\d+(\.\d+)? out of 5 stars", "", review["title"]).strip(),
                    "timestamp": re.sub(r"Reviewed in the United States", "", review["timestamp"]).strip()
                }
                for review in reviews
            ]
        
class AmazonScraper:
    """
        1. scape product page and find link to customer reviews page.
        2. Go to customer reviews page and scrape.
        3. Send the scraped data to the ml model for out
    """
    def __init__(self, url):
        self.url = url
        self.header = header

    def scrape_page_content(self, url):
        request = requests.get(url, headers=self.header)
        return BeautifulSoup(request.content, 'html.parser')

    def get_customer_reviews_link(self):
        soup = self.scrape_page_content(self.url)
        review_link = [a.get('href') for a in soup.find_all('a') if a.text.strip() == 'See more reviews' and a.get('href')][0]
        customer_reviews_path = f'https://{urlparse(self.url).netloc}/{review_link}'

        return customer_reviews_path
    
    def generate_customer_reviews(self, reviews_url):
        soup = self.scrape_page_content(reviews_url)
        # TODO: delete just for testing.
        with open('reviews-content.txt', mode='w') as f:
            f.write(str(soup))
        reviews = self.parse_customer_review_content(soup)
        return reviews
    
    def parse_customer_review_content(self, soup):
        all_reviews = []
        reviews = soup.find_all("div", {"id": lambda x: x and x.startswith("customer_review")})

        for index, review in enumerate(reviews, start=1):
            reviewer = review.find("span", class_="a-profile-name")
            reviewer_name = reviewer.get_text(strip=True) if reviewer else "No name available"
            
            title = review.find("span", {"data-hook": "review-title"})
            review_title = title.get_text(strip=True) if title else "No title available"
            
            content = review.find("div", class_="cr-full-content")
            review_content = content.get_text(strip=True) if content else "No content available"
            
            date = review.find("span", {"data-hook": "review-date"})
            review_date = date.get_text(strip=True) if date else "No date available"
            
            review_data = {
                "id": index,
                "reviewer": reviewer_name,
                "title": review_title,
                "date": review_date,
                "content": review_content
            }
            
            all_reviews.append(review_data) 

        return all_reviews
    
    def get_reviews_on_main_page(self):
        request = requests.get(self.url, headers=self.header)
        soup = BeautifulSoup(request.content, 'html.parser')
        reviews = soup.find_all(attrs={"data-hook": "review-body"})
        return reviews
class Unwrangle:
    BASE_URL = "https://data.unwrangle.com/api/getter/"
    PLATFORM = "amazon_detail"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # self.headers = {
        #     "Authorization": api_key,
        #     "Accept": "application/json"
        # }
    
    def _extract_product_url(self, url: str) -> str:
        """
        Extracts the product URL from an Amazon URL by removing query parameters
        but keeping the product title and ID.
        """
        parsed = urlparse(url)
        
        # Verify it's an Amazon URL
        if "amazon.com" not in parsed.netloc:
            raise ValueError("Not a valid Amazon URL")
            
        # Find the /dp/ or /gp/product/ section
        path_parts = parsed.path.split('/')
        dp_index = -1
        
        for i, part in enumerate(path_parts):
            if part in ['dp', 'gp']:
                dp_index = i
                break
                
        if dp_index == -1:
            raise ValueError("Could not find product ID in URL")
            
        # Keep everything up to and including the product ID
        # This includes the product title and ID
        relevant_path = '/'.join(path_parts[:dp_index + 2])
        
        # Reconstruct the URL without query parameters
        clean_url = f"https://www.amazon.com{relevant_path}/"
        return clean_url
    
    def _build_api_url(self, product_url: str) -> str:
        """
        Builds the Unwrangle API URL with the encoded product URL.
        """
        encoded_url = quote(product_url, safe='')
        return f"{self.BASE_URL}?platform={self.PLATFORM}&url={encoded_url}&api_key={self.api_key}"
    
    def get_product_data(self, url: str):
        """
        Fetches product data from Unwrangle API for a given Amazon URL.
        
        Args:
            url (str): The full Amazon product URL
            
        Returns:
            UnwrangleResponse: The parsed API response
            
        Raises:
            ValueError: If the URL is invalid
            requests.RequestException: If the API request fails
        """
        try:
            # Clean the Amazon URL
            clean_url = self._extract_product_url(url)
            print(f"Cleaned URL: {clean_url}")  # For debugging
            
            # Build the API URL
            api_url = self._build_api_url(clean_url)
            print(f"API URL: {api_url}")  # For debugging

            
            # Make the request
            response = requests.get(api_url)
            response.raise_for_status()
            
            # Parse and return the response
            return response.json()
            
        except requests.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")