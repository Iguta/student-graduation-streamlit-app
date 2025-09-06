# Student Graduation Risk Prediction 🎓

[![Python](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.48.1-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Project Description
This is a **Machine Learning application** built using the **XGBoost algorithm** to identify students at higher risk of dropping out. The goal is to enable early interventions by administrators to provide support to at-risk students, helping them achieve academic success while improving the institution’s graduation rates.

---

## Tools and Libraries
- **AWS SageMaker Notebook** – for training and experimentation  
- **Streamlit** – for interactive web application deployment  
- **Pandas & NumPy** – for data manipulation  
- **Plotly & Seaborn** – for data visualization and feature selection  
- **Matplotlib** – additional plotting support  
- **Optuna** – for hyperparameter optimization  
- **Boto3 & AWS SDKs** – for interacting with SageMaker endpoints  
- **Python-dotenv** – for managing environment variables  

---

## Data & Features
- Original dataset: 34 features describing student demographics, academic performance, and socio-economic indicators.  
- Feature selection reduced the number of inputs to **11 key features** for efficient prediction.  
- Visualizations provide insight into relationships between features and dropout risk.

---

## Process

### 1. Data Visualization
- Used **Seaborn** and **Plotly** for exploratory analysis.  
- Avoided PCA to maintain interpretability in the front-end app.  
- Reduced features from 34 → 11 based on importance and correlation.

### 2. Model Training
- Trained both **Random Forest** and **XGBoost** models using AWS SageMaker.  
- **XGBoost** outperformed Random Forest, achieving better recall for the dropout class.  

**Training notebooks and scripts are available here:**  
[Student Graduation Prediction - SageMaker Training Repository](https://github.com/Iguta/student-graduation-prediction-ssagemaker-inference)

### 3. Hyperparameter Optimization
- Used **Optuna** to optimize multiple parameters simultaneously.  
- Optimized for **recall** of the dropout class and overall **accuracy**.  
- Metrics achieved:
  - **Accuracy:** 88%  
  - **Recall (Dropout class):** 79%  

> Recall was prioritized to avoid false negatives — i.e., students at risk labeled as likely graduates.

### 4. Model Saving
- Model saved in **JSON format** to reduce memory usage and improve deployment efficiency.  

### 5. Deployment
- Deployed using **SageMaker serverless inference**.  
- Model artifacts stored in **AWS S3**.  
- Streamlit app consumes the endpoint for real-time predictions.  

---

## Streamlit App
- Interactive web application for administrators to input student features and get predicted risk scores.  
- Includes additional **visualizations** to contextualize the prediction.  
- Sidebar navigation allows switching between **Prediction** and **Data Visualizations** pages.  

### Features:
- Input matching model-trained features  
- Predictions with confidence scores  
- Dynamic charts showing feature importance and correlations  

---

## Project Structure
```
student-graduation-streamlit-app/
│
├── app.py                 # Main Streamlit app
├── modules/               # Custom modules
│   ├── prediction.py      # Prediction logic (calls the model endpoint)
│   ├── visualizations.py  # Functions to create charts and graphs
│   └── helper.py          # Helper functions, e.g., AWS SDK interactions
├── requirements.txt       # List of Python dependencies
├── README.md              # Project documentation
├── .streamlit/            # Streamlit configuration files
│   └── config.toml        # Optional configuration for page settings
└── assets/ (optional)     # Images, icons, or other static assets used in app
```

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Iguta/student-graduation-streamlit-app.git
cd student-graduation-streamlit-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables for AWS
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=your_region
export SAGEMAKER_ENDPOINT=your_endpoint_name

# Run Streamlit app
streamlit run app.py
