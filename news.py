import requests
from bs4 import BeautifulSoup
import json

#  Function to get detailed news from a news page
def get_news_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    details = {}
    
    # Extracting additional details (will be change as per page structure)
    paragraphs = soup.find_all('p')
    details['content'] = ' '.join(p.text.strip() for p in paragraphs)
    print(details['content'])
    return details

# main func
def scrape_efy_news():
    url = "https://www.electronicsforu.com/category/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_data = []
    news_cards = soup.find_all('div', class_='td-image-container')
    
    for card in news_cards:
        news_item = {}
        link_tag = card.find('a', class_='td-image-wrap')
        if link_tag:
            news_item['title'] = link_tag.get('title')
            news_item['link'] = link_tag.get('href')
            img_tag = link_tag.find('span', class_='entry-thumb td-thumb-css')
            if img_tag and 'data-img-url' in img_tag.attrs:
                news_item['image_url'] = img_tag['data-img-url']
            else:
                news_item['image_url'] = None


            # Get details from the linked page
            news_item['details'] = get_news_details(news_item['link'])
            news_data.append(news_item)
    
    return news_data

# Scrape the news and store it in a JSON file
news_data = scrape_efy_news()

# print(news_data)
with open('news_data.json', 'w') as json_file:
    json.dump(news_data, json_file, indent=4)

print("News data has been saved to news_data.json")