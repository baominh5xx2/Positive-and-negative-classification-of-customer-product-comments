import torch
from transformers import AutoTokenizer, AutoModel
from cuml.svm import SVC
from cuml.metrics import accuracy_score
from cleaning_data import clean_text_vietnamese
import pandas as pd
import numpy as np
import pickle

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

    ds = pd.read_excel('Testing_dataset.xlsx')
    print(ds.head())

    ds_clean = ds.dropna(subset=['label'])

    embeddings = [get_bert_embedding(text) for text in ds_clean['text']]
    labels = ds_clean['label'].values

    # SVM models
    svm_model_poly = SVC(kernel='poly', degree=3, C=5.0, class_weight='balanced', random_state=42)
    svm_model_rbf = SVC(kernel='rbf', C=10.0, gamma='scale', class_weight='balanced', random_state=42)
    svm_model_linear = SVC(kernel='linear', C=1.0, gamma='scale', class_weight='balanced', random_state=42)
    
    svm_models = [
        ('poly', svm_model_poly),
        ('rbf', svm_model_rbf),
        ('linear', svm_model_linear)
    ]

    accuracy_results = pd.DataFrame(columns=['Model', 'Accuracy'])

    # Train and evaluate each SVM model
    for model_name, svm_model in svm_models:
        svm_model.fit(np.array(embeddings), np.array(labels))
        with open(f'svm_model_{model_name}.pkl', 'wb') as f:
            pickle.dump(svm_model, f)

    ds_test = pd.read_excel('Testing_dataset.xlsx')
    ds_test_clean = ds_test.dropna(subset=['label'])
    test_embeddings = [get_bert_embedding(text) for text in ds_test_clean['text']]
    test_labels = ds_test_clean['label'].values

    for model_name, svm_model in svm_models:
        y_pred = svm_model.predict(np.array(test_embeddings))
        accuracy = accuracy_score(np.array(test_labels), y_pred)
        new_row = pd.DataFrame({'Model': [model_name], 'Accuracy': [accuracy]})
        accuracy_results = pd.concat([accuracy_results, new_row], ignore_index=True)

    print("\nAccuracy Results:")
    print(accuracy_results)
