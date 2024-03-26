import os
import requests
import json

new_api = os.environ.get('NEW_API_KEY')

def get_news(topic):

       url = (f'https://newsapi.org/v2/everything?q={topic}&sortBy=popularity&apiKey={new_api}')

       try:   
              response = requests.get(url)
              if response.status_code == 200:
                     new = json.dumps(response.json(), indent='\t')
                     news_json = json.loads(new)
                     status = news_json['status']
                     total_results = news_json['totalResults']
                     articles = news_json['articles']
                     final_news = []
              
                     for article in articles:
                            source_name = article['source']['name']
                            author = article['author']
                            title = article['title']
                            description = article['description']
                            url = article['url']
                            content = article['content']
                            title_description = f"""
                                   Title: {title},
                                   Author: {author},
                                   Source: {source_name},
                                   Description: {description},
                                   URL: {url}
                                   
                            """
                            final_news.append(title_description)
                     return final_news
              else:
                     return []
                     
       except requests.exceptions.RequestException as e:
              print("Error while getting API:", e)


       