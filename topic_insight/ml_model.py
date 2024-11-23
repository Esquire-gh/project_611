import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

class Review(BaseModel):
    phrase: str

class Cluster(BaseModel):
    cluster_name: str
    sentiment: Literal["positive", "negative"]
    cluster_reviews: list[Review]

class TopicCluster(BaseModel):
    clusters: list[Cluster]

class OpenAIModel:
    def __init__(self, reviews):
        self.client = OpenAI(api_key=os.environ['OPENAIAPI_SECRET_KEY'])
        self.reviews = reviews
        
    def categorize_reviews(self):
        completion = self.client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a trained clustering model that groups a list of review objects into topic clusters."
                        "By using the values of the objects' content key,"
                        "summarize it and group into topic clusters. Produce a list "
                        "of topic clusters where we want to show for each topic, whether the sentiment on that topic if positive or negative"
                        "and then a list of phrases from the reviews contents belonging to the topic cluster that were used to describe it "
                    )
                },
                {
                    "role": "user",
                    "content": str(self.reviews)
                }
            ],
            response_format=TopicCluster,
        )
        return completion.choices[0].message.parsed
