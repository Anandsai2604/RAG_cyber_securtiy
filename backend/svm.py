# import warnings

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore", FutureWarning)
#     warnings.simplefilter("ignore", UserWarning)

#     import pandas as pd
#     import numpy as np
#     from sklearn.model_selection import train_test_split
#     from sklearn.tree import DecisionTreeClassifier
#     from sentence_transformers import SentenceTransformer
#     from sklearn.neighbors import KNeighborsClassifier
#     from sklearn.metrics import accuracy_score
#     import joblib
#     import sys
#     import json
  

#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     tag_mapping = {
#         'GENERAL_TOOL': 0,
#         'IMPACT': 1,
#         'ATTACK_PATTERN': 2,
#         'CAMPAIGN': 3,
#         'VICTIM_IDENTITY': 4,
#         'ATTACK_TOOL': 5,
#         'GENERAL_IDENTITY': 6,
#         'MALWARE': 7,
#         'COURSE_OF_ACTION': 8,
#         'OBSERVED_DATA': 9,
#         'INTRUSION_SET': 10,
#         'THREAT_ACTOR': 11,
#         'VULNERABILITY': 12,
#         'INFRASTRUCTURE': 13,
#         'MALWARE_ANALYSIS': 14,
#         'INDICATOR': 15,
#         'LOCATION': 16,
#         'ATTACK_MOTIVATION': 17,
#         'O': 18
#     }

#     reverse_tag_mapping = {v: k for k, v in tag_mapping.items()}
#     model_filename = r"svm_model.pkl"
#     dt_classifier = joblib.load(model_filename)

#     def predict(input_sentence):
#         words = input_sentence.split()
#         results = []
#         for word in words:
#             word_vector = model.encode(word).reshape(1, -1)
#             tag_number = dt_classifier.predict(word_vector)[0]
#             tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
#             results.append((word, tag_name))
#         return results

#     if len(sys.argv) > 1:
#         input_sentence = " ".join(sys.argv[1:])
#         predicted_tags = predict(input_sentence)
#         qa_pairs = {word: tag for word, tag in predicted_tags}
        
#         formatted_result = [{"q": word, "a": tag} for word, tag in qa_pairs.items()]
        
#         print(json.dumps(formatted_result, indent=4))


import warnings
from flask import Flask, request, jsonify
import joblib
from sentence_transformers import SentenceTransformer
import json
import sys

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    warnings.simplefilter("ignore", UserWarning)

    app = Flask(__name__)

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
    model_filename = r"svm_model.pkl"
    dt_classifier = joblib.load(model_filename)

    def predict(input_sentence):
        words = input_sentence.split()
        results = []
        for word in words:
            word_vector = model.encode(word).reshape(1, -1)
            tag_number = dt_classifier.predict(word_vector)[0]
            tag_name = reverse_tag_mapping.get(tag_number, 'Unknown')
            results.append((word, tag_name))
        return results

    @app.route('/predict', methods=['POST'])
    def predict_api():
        data = request.get_json()
        input_sentence = data.get("sentence", "")
        predicted_tags = predict(input_sentence)
        qa_pairs = {word: tag for word, tag in predicted_tags}
        formatted_result = [{"q": word, "a": tag} for word, tag in qa_pairs.items()]
        return jsonify(formatted_result)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_sentence = " ".join(sys.argv[1:])
        with app.app_context():
            predicted_tags = predict(input_sentence)
            qa_pairs = {word: tag for word, tag in predicted_tags}
            formatted_result = [{"q": word, "a": tag} for word, tag in qa_pairs.items()]
            print(json.dumps(formatted_result, indent=4))
    app.run(debug=True)
