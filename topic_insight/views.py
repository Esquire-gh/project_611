import os
import json
import requests

from django.shortcuts import render

from .scraper import Unwrangle
from .utils import valid_amazon_url

# Create your views here.
def home(request): 
    error_message = ''
    amazon_product_url = ''
    customer_reviews_url = ''
    results = []
    result = None

    data = None

    try:
        if request.POST:
            product_url = request.POST.get('product_url')

            if valid_amazon_url(product_url):
                amazon_product_url = product_url
                scraper = Unwrangle(os.environ['UNWRANGLE_API_KEY'])
                data = scraper.get_product_data(amazon_product_url)

                with open('unwrange-result-4.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                req_body = data['detail']['top_reviews']
                
                ml_server_url = "https://772f-35-239-8-216.ngrok-free.app"

                response = requests.post(ml_server_url, json=req_body)

                if response.status_code == 200:
                    result = response.json()

                    results = result['topics']

                    with open('result-new-4.json', 'w') as json_file:
                        json.dump(result, json_file, indent=4)
                else:
                    print("Failed to submit data. Status code:", response.status_code)


                # with open('result-new-4.json', 'r') as json_file:
                #     results = json.load(json_file)
                # results = results['topics']
                
                        
            else:
                error_message = "Enter a valid amazon url."

        context = {
            "error_message": error_message,
            "product_page_link": amazon_product_url,
            "customer_reviews_page_link": customer_reviews_url,
            "results": results
        }
        return render(request, 'topic_insight/home.html', context)
    except Exception as e:
        error_message = str(e)
        context = {
            "error_message": error_message,
        }
        return render(request, 'topic_insight/home.html', context)