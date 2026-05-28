# 🧠 Resume Classification using Machine Learning

This project is an NLP-based machine learning system that classifies resumes into different job categories using TF-IDF and trained ML models.

---

## 🚀 Project Overview

The system extracts resume text, cleans it, converts it into numerical features using TF-IDF, and predicts the resume category using a trained model.

---

## 📂 Files Included

- `app.py` → Simple script to load model and predict
- `Resume Classification.ipynb` → Full training and analysis notebook
- `raw_resume_dataset.csv` → Extracted resume text data
- `cleaned_resume_dataset.csv` → Preprocessed dataset
- `final_model.pkl` → Trained ML model
- `tfidf.pkl` → TF-IDF vectorizer

---

## 🧠 Machine Learning Workflow

1. Load resume dataset
2. Extract and clean text
3. Apply TF-IDF vectorization
4. Train multiple ML models
5. Select best model
6. Save model using Pickle

---

## 🤖 Models Used

- Logistic Regression (Best Model)
- Naive Bayes
- SVM
- Random Forest

---

## 📊 Output

- Resume category prediction
- Model accuracy comparison
- Confusion matrix
- Classification report

---

## ⚙️ Requirements

```bash
pip install pandas numpy scikit-learn nltk matplotlib seaborn PyPDF2 python-docx
