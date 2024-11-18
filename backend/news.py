import requests
from bs4 import BeautifulSoup
import json

def extract_news():
    url = "https://cybersecuritynews.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles_list = []

    articles = soup.find_all('div', class_='td_module_10 td_module_wrap td-animation-stack')

    for article in articles:
        img_tag = article.find('img', class_='entry-thumb')
        
        image = img_tag['data-img-url'] #if img_tag and img_tag.has_attr('src') else 'https://via.placeholder.com/150'  # Placeholder image

        header_tag = article.find('h3', class_='entry-title td-module-title')
        header = header_tag.text.strip() if header_tag else None
        link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else None
        
        paragraph = article.find('div', class_='td-excerpt').text.strip() if article.find('div', class_='td-excerpt') else None
        
        articles_list.append({
            'image': image,
            'header': header,
            'para': paragraph,
            'link': link
        })

    return articles_list

if __name__ == "__main__":
    extracted_articles = extract_news()
    if extracted_articles:
        try:
            print(json.dumps(extracted_articles, ensure_ascii=False, indent=2))
        except Exception as e:
            print("Error creating JSON:", str(e))
    else:
        print("No articles extracted.")


# from flask import Flask, jsonify
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)

# def extract_news():
#     url = "https://cybersecuritynews.com/"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print(f"Error fetching URL {url}: {e}")
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')
#     articles_list = []

#     # Find articles in the webpage
#     articles = soup.find_all('div', class_='td_module_10 td_module_wrap td-animation-stack')

#     for article in articles:
#         img_tag = article.find('img', class_='entry-thumb')
#         image = img_tag['src'] if img_tag and img_tag.has_attr('src') else 'https://via.placeholder.com/150'
#         header_tag = article.find('h3', class_='entry-title td-module-title')
#         header = header_tag.text.strip() if header_tag else None
#         link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else None
#         paragraph = article.find('div', class_='td-excerpt').text.strip() if article.find('div', class_='td-excerpt') else None
        
#         article_data = {
#             'image': image,
#             'header': header,
#             'para': paragraph,
#             'link': link
#         }
        
#         # Print each article data to the console
#         print(article_data)
        
#         articles_list.append(article_data)

#     return articles_list

# @app.route('/news', methods=['POST'])
# def get_news():
#     extracted_articles = extract_news()
    
#     if extracted_articles:
#         # Print the entire list of articles to the console
#         print("Extracted Articles JSON:")
#         print(extracted_articles)

#         # Return the extracted articles as JSON response
#         return jsonify(extracted_articles)
#     return jsonify({"message": "No articles extracted"}), 404

# if __name__ == "__main__":
#     app.run(debug=True)
