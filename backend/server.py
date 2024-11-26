from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BertForSequenceClassification, AutoTokenizer
import os
import random
import json
import ijson
import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)
 
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    warnings.simplefilter("ignore", UserWarning)
    import torch
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sentence_transformers import SentenceTransformer
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score
    import joblib
    import sys
    import json
    import lightgbm as lgb

  
    # model_path = r"C:\Users\Anand\Desktop\cyber\back\back\src\serv\modelner\bert_model"
    # tokenizer_path = r"C:\Users\Anand\Desktop\cyber\back\back\src\serv\modelner\bert_tokenizer"

    bert_model_path = r"E:\cyber\back\back\src\serv\modelner\bert_model"
    tokenizer_path = r"E:\cyber\back\back\src\serv\modelner\bert_tokenizer"
    try:
        bert_model = BertForSequenceClassification.from_pretrained(bert_model_path)
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    except Exception as e:
        print(f"Error loading BERT model or tokenizer: {e}")

    bert_model = BertForSequenceClassification.from_pretrained(bert_model_path)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    bert_model.eval()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    tag_mapping = {
        'GENERAL_TOOL': 0,
        'IMPACT': 1,
        'ATTACK_PATTERN': 2,
        'CAMPAIGN': 3,
        'VICTIM_IDENTITY': 4,
        'ATTACK_TOOL': 5,
        'GENERAL_IDENTITY': 6,
        'MALWARE': 7,
        'COURSE_OF_ACTION': 8,
        'OBSERVED_DATA': 9,
        'INTRUSION_SET': 10,
        'THREAT_ACTOR': 11,
        'VULNERABILITY': 12,
        'INFRASTRUCTURE': 13,
        'MALWARE_ANALYSIS': 14,
        'INDICATOR': 15,
        'LOCATION': 16,
        'ATTACK_MOTIVATION': 17,
        'O': 18
    }

    reverse_tag_mapping = {v: k for k, v in tag_mapping.items()}


    file_path = r'qa.json'
    question_vectors = []
    answers = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for item in ijson.items(f, 'item'):
                question_vectors.append(item['question_vector'])
                answers.append(item['answer'])
    except Exception as e:
        print(f"Error loading JSON: {e}")

    if question_vectors:
        question_vectors = np.array(question_vectors)

    def get_best_answer(input_question):
        input_vector = model.encode(input_question, device='cpu')
        sim = cosine_similarity([input_vector], question_vectors)
        best_index = np.argmax(sim)
        return answers[best_index]



    m1 = r"random_forest_model.pkl"
    m2= r"C:\Users\Anand\Desktop\pyhton\knn_model.pkl"
    m3 = r"dt_model.pkl"
    m4 = r"lightgbm_model.pkl"
    m5 = r"svm_model.pkl"
    m6 =r"logistic_regression_model.pkl"
    d1 = joblib.load(m1)
    d2 = joblib.load(m2)
    d3 = joblib.load(m3)
    d4 = joblib.load(m4)
    d5 = joblib.load(m5)
    d6 = joblib.load(m6)
    
    

    def extract_news():
        url = "https://cybersecuritynews.com/"
        try:
            response = requests.get(url)
            response.raise_for_status()  
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        articles_list = []

        articles = soup.find_all('div', class_='td_module_10 td_module_wrap td-animation-stack')

        for article in articles:
            img_tag = article.find('img', class_='entry-thumb')
            
            if img_tag and img_tag.has_attr('src'):
                image = img_tag['src']
            else:
                image = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANoAAACWAQMAAACCSQSPAAAAA1BMVEWurq51dlI4AAAAAXRSTlMmkutdmwAAABpJREFUWMPtwQENAAAAwiD7p7bHBwwAAAAg7RD+AAGXD7BoAAAAAElFTkSuQmCC'
            
            img_tag_html = f'<img src="{image}" alt="Article Image" />'

            header_tag = article.find('h3', class_='entry-title td-module-title')
            header = header_tag.text.strip() if header_tag else None
            link = header_tag.find('a')['href'] if header_tag and header_tag.find('a') else None

            paragraph = article.find('div', class_='td-excerpt').text.strip() if article.find('div', class_='td-excerpt') else None

            articles_list.append({
                'image': img_tag_html,
                'header': header,
                'para': paragraph,
                'link': link
            })

        return articles_list

    

@app.route('/knn', methods=['POST'])
def knn():
    data = request.json
    input_sentence = data.get('input_sentence')
    words = input_sentence.split()
    results = []
    for word in words:
        word_vector = model.encode(word).reshape(1, -1)
        tag_number = d2.predict(word_vector)[0]
        tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
        results.append((word, tag_name))
    formatted_result = [{"q": word, "a": tag} for word, tag in results]
        
    try:
        # json_data = json.loads(results)
        return jsonify(formatted_result), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Internal Server Error: Error parsing JSON'}), 500

@app.route('/dt', methods=['POST'])
def dt():
    data = request.json
    input_sentence = data.get('input_sentence')
    words = input_sentence.split()
    results = []
    for word in words:
        word_vector = model.encode(word).reshape(1, -1)
        tag_number = d3.predict(word_vector)[0]
        tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
        results.append((word, tag_name))
    formatted_result = [{"q": word, "a": tag} for word, tag in results]
        
    try:
        # json_data = json.loads(results)
        return jsonify(formatted_result), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Internal Server Error: Error parsing JSON'}), 500


@app.route('/lr', methods=['POST'])
def lr():
    data = request.json
    input_sentence = data.get('input_sentence')
    words = input_sentence.split()
    results = []
    for word in words:
        word_vector = model.encode(word).reshape(1, -1)
        tag_number = d6.predict(word_vector)[0]
        tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
        results.append((word, tag_name))
    formatted_result = [{"q": word, "a": tag} for word, tag in results]
        
    try:
        # json_data = json.loads(results)
        return jsonify(formatted_result), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Internal Server Error: Error parsing JSON'}), 500

        

@app.route('/gb', methods=['POST'])
def gb():
    data = request.json
    input_sentence = data.get('input_sentence')
    words = input_sentence.split()
    results = []
    for word in words:
        word_vector = model.encode(word).reshape(1, -1)
        tag_number = d4.predict(word_vector)[0]
        tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
        results.append((word, tag_name))
    formatted_result = [{"q": word, "a": tag} for word, tag in results]
        
    try:
        # json_data = json.loads(results)
        return jsonify(formatted_result), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Internal Server Error: Error parsing JSON'}), 500

        

@app.route('/rf', methods=['POST'])
def rf():
    data = request.json
    input_sentence = data.get('input_sentence')
    words = input_sentence.split()
    results = []
    for word in words:
        word_vector = model.encode(word).reshape(1, -1)
        tag_number = d1.predict(word_vector)[0]
        tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
        results.append((word, tag_name))
    formatted_result = [{"q": word, "a": tag} for word, tag in results]
        
    try:
        # json_data = json.loads(results)
        return jsonify(formatted_result), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Internal Server Error: Error parsing JSON'}), 500

    
@app.route('/svm', methods=['POST'])
def svm():
    data = request.json
    input_sentence = data.get('input_sentence')
    words = input_sentence.split()
    results = []
    for word in words:
        word_vector = model.encode(word).reshape(1, -1)
        tag_number = d5.predict(word_vector)[0]
        tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
        results.append((word, tag_name))
    formatted_result = [{"q": word, "a": tag} for word, tag in results]
        
    try:
        # json_data = json.loads(results)
        return jsonify(formatted_result), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Internal Server Error: Error parsing JSON'}), 500


@app.route('/news', methods=['POST'])
def news():
    print('Fetching news')
    extracted_articles = extract_news()
    if extracted_articles:
        try:
            return jsonify(extracted_articles), 200
        except Exception as e:
            return jsonify({'error': 'Internal Server Error: Error creating JSON'}), 500
    else:
        return jsonify({'error': 'No articles extracted.'}), 404
    



@app.route('/bert', methods=['POST'])
def bert_predict():
    try:
        data = request.json
        input_sentence = data.get('input_sentence')

        inputs = tokenizer(input_sentence, padding=True, truncation=True, return_tensors='pt')

        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        with torch.no_grad():
            outputs = bert_model(input_ids=input_ids, attention_mask=attention_mask)

        logits = outputs.logits
        predicted_labels = torch.argmax(logits, dim=1)

        predicted_tags = [reverse_tag_mapping[label.item()] for label in predicted_labels]

        return jsonify(predicted_tags), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    

@app.route('/rag', methods=['POST'])
def rag():
    try:
        data = request.json
        input_sentence = data.get('input_sentence')

        if not input_sentence:
            return jsonify({'error': 'Input question is required.'}), 400

        best_answer = get_best_answer(input_sentence)
        return jsonify([{"q": input_sentence, "a": best_answer}]), 200

    except Exception as e:
        print(f"Error in RAG processing: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000)
