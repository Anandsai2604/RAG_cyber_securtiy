# # # import pandas as pd
# # # import numpy as np
# # # import ast
# # # import re
# # # from sklearn.tree import DecisionTreeClassifier
# # # from sklearn.metrics import accuracy_score, classification_report
# # # from sklearn.linear_model import LogisticRegression
# # # from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# # # from sklearn.svm import SVC
# # # import joblib
# # # from sentence_transformers import SentenceTransformer

# # # model = SentenceTransformer('all-MiniLM-L6-v2')

# # # df = pd.read_csv('E:\\cybersec\\word_vectors.csv')

# # # def clean_vector_string(vector_str):
# # #     cleaned_str = re.sub(r'(?<=\d)\s+(?=-?\d)', ',', vector_str)
# # #     return cleaned_str

# # # models = {
# # #     "Logistic Regression": LogisticRegression(max_iter=1000),
# # #     "Random Forest": RandomForestClassifier(n_estimators=100),
# # #     "SVM": SVC(),
# # #     "Gradient Boosting": GradientBoostingClassifier()
# # # }

# # # df['Vector'] = df['Vector'].apply(lambda x: np.array(ast.literal_eval(clean_vector_string(x))))

# # # X = np.vstack(df['Vector'].values)
# # # y = df['Tag Number'].values 

# # # # models = {
# # # #     "Logistic Regression": LogisticRegression(max_iter=1000),
# # # #     "Random Forest": RandomForestClassifier(n_estimators=100),
# # # #     "SVM": SVC(),
# # # #     "Gradient Boosting": GradientBoostingClassifier()
# # # # }

# # # # for i,j in models.items():
# # # #     j.fit(X,y)


# # # model_filename = f'{i.replace(" ", "_").lower()}_model.pkl'  
# # # joblib.dump(j, model_filename)

# # # print(f"Model saved as {model_filename}")


# # import pandas as pd
# # import numpy as np
# # import ast
# # import re
# # import lightgbm as lgb
# # import joblib
# # from sklearn.metrics import accuracy_score, classification_report
# # from imblearn.over_sampling import SMOTE

# # df = pd.read_csv('E:\\cybersec\\word_vectors.csv')

# # def clean_vector_string(vector_str):
# #     cleaned_str = re.sub(r'(?<=\d)\s+(?=-?\d)', ',', vector_str)
# #     return cleaned_str

# # df['Vector'] = df['Vector'].apply(lambda x: np.array(ast.literal_eval(clean_vector_string(x))))

# # X = np.vstack(df['Vector'].values)
# # y = df['Tag Number'].values 

# # smote = SMOTE(random_state=42)
# # X_resampled, y_resampled = smote.fit_resample(X, y)

# # lgbm_params = {
# #     'boosting_type': 'gbdt',
# #     'objective': 'multiclass',
# #     'num_class': len(np.unique(y)),
# #     'learning_rate': 0.01,
# #     'n_estimators': 1000,
# #     'max_depth': -1,
# #     'num_leaves': 255,
# #     'min_child_samples': 20,
# #     'subsample': 0.8,
# #     'colsample_bytree': 0.8,
# #     'class_weight': 'balanced',
# #     'n_jobs': -1,
# #     'verbose': -1
# # }

# # lgbm_classifier = lgb.LGBMClassifier(**lgbm_params)
# # lgbm_classifier.fit(X_resampled, y_resampled)

# # model_filename = 'lightgbm_model.pkl'
# # joblib.dump(lgbm_classifier, model_filename)

# # y_pred = lgbm_classifier.predict(X_resampled)
# # accuracy = accuracy_score(y_resampled, y_pred)
# # print(f"Accuracy: {accuracy:.4f}")
# # print(classification_report(y_resampled, y_pred))

# import json
# from sentence_transformers import SentenceTransformer
# import csv

# model = SentenceTransformer('all-MiniLM-L6-v2')
# s = r'E:\cybersec\RAG-based-QA-main\RAG-based-QA-main\QA pairs for KB.csv'
# r = r'qa.json'
# json_data = []

# with open(s, mode='r', encoding='utf-8-sig') as file: 
#     reader = csv.DictReader(file)
#     headers = reader.fieldnames
#     print("CSV Headers:", headers)  
#     for i in reader:
#         q = i['Question'].strip()
#         a = i['Ground Truth'].strip()
#         q_vector = model.encode(q).tolist()
#         a_vector = model.encode(a).tolist()
#         json_data.append({
#             "question": q,
#             "question_vector": q_vector,
#             "answer": a,
#             "answer_vector": a_vector
#         })

# with open(r, mode='w', encoding='utf-8') as jfile:
#     json.dump(json_data, jfile, ensure_ascii=False, indent=4)

# print("Done")


import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle
from tqdm import tqdm

with open(r"E:\json\a_squad.json", 'r', encoding='utf-8') as file:
    json_data = json.load(file)

answers = [item['answer'] for item in json_data]
answer_vectors = np.array([item['answer_vector'] for item in json_data])

# knn_model = KNeighborsClassifier(n_neighbors=3, metric='cosine') 
# decision_tree_model = DecisionTreeClassifier(random_state=42)  
random_forest_model = RandomForestClassifier(n_estimators=100, random_state=42) 

# knn_model.fit(answer_vectors, answers)
# decision_tree_model.fit(answer_vectors, answers)
random_forest_model.fit(answer_vectors, answers)


for _ in tqdm(range(1), desc="Training Random Forest Model"):  
    random_forest_model.fit(answer_vectors, answers)


# with open('knn_qna.pkl', 'wb') as knn_file:
#     pickle.dump(knn_model, knn_file)

# with open('decisiontree_qna.pkl', 'wb') as dt_file:
#     pickle.dump(decision_tree_model, dt_file)

with open('randomforest_qna.pkl', 'wb') as rf_file:
    pickle.dump(random_forest_model, rf_file)

print("Models trained on the entire dataset and saved.")
