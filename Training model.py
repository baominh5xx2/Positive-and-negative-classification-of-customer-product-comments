import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from cleaning_data import clean_text_vietnamese
import pandas as pd
import numpy as np
import joblib

if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Đang sử dụng thiết bị: {device}")

    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
    model = AutoModel.from_pretrained("vinai/phobert-base").to(device)

    def get_bert_embedding(sentence):
        cleaned_sentence = clean_text_vietnamese(sentence, keep_punct=True)
        inputs = tokenizer(cleaned_sentence, return_tensors='pt', truncation=True, padding=True, max_length=128)
        inputs = {key: value.to(device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state
        sentence_embedding = embeddings.mean(dim=1).squeeze().cpu().numpy()
        return sentence_embedding

    ds = pd.read_excel('Training_dataset.xlsx')
    print(ds.head())

    print(f"Số lượng NaN trong nhãn: {ds['label'].isna().sum()}")
    ds_clean = ds.dropna(subset=['label'])
    print(f"Số lượng NaN trong nhãn sau khi loại bỏ: {ds_clean['label'].isna().sum()}")

    embeddings = [get_bert_embedding(text) for text in ds_clean['text']]
    labels = ds_clean['label'].values

    svm_model_poly= SVC(
        kernel='poly',
        degree=3,  # polynomial degree
        C=5.0,
        probability=True,
        class_weight='balanced',
        random_state=42
    )
    svm_model_rbf = SVC(
        kernel='rbf',
        C=10.0,
        gamma='scale',
        probability=True,
        class_weight='balanced',
        random_state=42
    )
    svm_model_linear = SVC(
        kernel='linear',
        C=1.0,
        gamma='scale',
        probability=True,
        class_weight='balanced',
        random_state=42
    )

    # Create a list of SVM models with their names
    svm_models = [
        ('poly', svm_model_poly),
        ('rbf', svm_model_rbf),
        ('linear', svm_model_linear)
    ]

    # Train and evaluate each model
    for model_name, svm_model in svm_models:
        print(f"\nTraining {model_name} SVM model...")
        svm_model.fit(embeddings, labels)
        
        print(f"\nModel {model_name} SVM trained successfully!")
        # Save the model
        joblib.dump(svm_model, f'svm_model_{model_name}.pkl')

    def predict_sentiment(text, model_name='rbf'):
        embedding = get_bert_embedding(text)
        model = joblib.load(f'svm_model_{model_name}.pkl')
        prediction = model.predict([embedding])
        return prediction[0]
