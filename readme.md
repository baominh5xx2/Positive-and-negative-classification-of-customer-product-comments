# Positive and Negative Classification of Customer Product Comments

This project applies **PhoBERT embeddings** for feature extraction and then classifies customer comments using **SVM with different kernels** and **Logistic Regression**. The goal is to compare the classification performance across different SVM kernels and Logistic Regression.

---

## 📖 Overview
Customer sentiment analysis is crucial for businesses to understand feedback. This project classifies **Vietnamese product reviews** into **positive** or **negative** comments using **PhoBERT embeddings** and **SVM/Logistic Regression**.

**Steps:**
1. Extract feature vectors using **PhoBERT embeddings**.
2. Train and evaluate **SVM with different kernels** (`linear`, `RBF`, `poly`) and **Logistic Regression**.
3. Using two treatments to train the model: scikit-learn library (training on CPU) and cuML to call the API of scikit-learn for training on GPU.
4. Compare accuracy and other metrics.

---

### **Model Comparison Table**

| Model Name            | Model Type            | Accuracy (%) |
|-----------------------|----------------------|--------------|
| Linear SVM            | SVM                  | 98.049       |
| Polynomial SVM        | SVM                  | 98.2991      |
| RBF SVM               | SVM                  | 98.3492      |
| Logistic Regression   | Logistic Regression  | 98.1491      |

---

## 📩 Contact
For any questions, suggestions, or feedback, feel free to reach out!

- **Author**: Nguyễn Minh Bảo
- **GitHub**: [baominh5xx2](https://github.com/baominh5xx2)
- **Email**: [baominh5xx2@gmail.com](mailto:baominh5xx2@gmail.com)
