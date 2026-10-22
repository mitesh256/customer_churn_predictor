
ChurnSight — Customer Churn Prediction
A machine-learning project for predicting whether a telecom customer is likely to churn. The project includes an exploratory data analysis and model-training notebook, a FastAPI prediction endpoint, and a Streamlit interface for entering customer details and viewing a prediction.

Important: Predictions are estimates from a trained model, not guarantees that a customer will leave or stay. Confirm model quality on suitable validation data before using predictions for business decisions.

Project Objective
Customer churn occurs when a customer stops using a service. The goal of this project is to use customer account, service, contract, and billing information to estimate churn risk and demonstrate how a trained classification model can be served through an API and a user interface.

Features
Exploratory data analysis (EDA) and model training in Jupyter Notebook.
Data preparation, including numeric conversion of TotalCharges, target encoding, and one-hot encoding of categorical features.
Comparison of Random Forest and XGBoost classifiers using a stratified train/test split.
Selection of a model based on ROC-AUC in the notebook.
FastAPI endpoint for churn predictions and predicted churn probability.
Streamlit interface for entering a customer profile and displaying the prediction.
Tech Stack
Python
pandas and NumPy
scikit-learn
XGBoost
Matplotlib and Seaborn
Jupyter Notebook
FastAPI and Pydantic
Streamlit and Requests
joblib
Repository Structure
CUSTOMER_CHURN_PROJECT/
├── api.py
├── app.py
├── best_model.pkl
├── feature_names.pkl
├── requirements.txt
├── start.sh
├── README.md
├── .gitignore
├── notebooks/
│   └── eda_and_training.ipynb
└── images/
    ├── churn_distribution.png
    ├── tenure_vs_churn.png
    └── model_evaluation.png
The images/ examples are suggested filenames. Add the actual charts exported from your notebook, and update the filenames below to match. Keep the model files in their current location unless you also update the file paths in api.py and the training notebook.

Dataset
The notebook uses a telecom churn CSV dataset with customer, service, contract, billing, and churn fields. The current notebook contains a local machine-specific input path, so update it before rerunning training:

filepath = "data/telco_churn.csv"
df = pd.read_csv(filepath)
Place the dataset at that path, or change the path to match your own setup. Do not publish personal, confidential, or otherwise restricted customer data. If you cannot redistribute the dataset, document where it can be obtained instead of committing it.

The notebook removes customerID, converts TotalCharges to numeric values, drops rows with missing values, encodes Churn as 0/1, encodes selected binary fields, and one-hot encodes the specified categorical columns.

Setup
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/customer_churn_predictor.git
cd customer_churn_predictor
Replace YOUR-USERNAME with the GitHub account that owns the repository.

2. Create and activate a virtual environment (recommended)
Windows PowerShell

python -m venv .venv
.\.venv\Scripts\Activate.ps1
macOS / Linux

python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
Run the Application
The Streamlit interface in app.py sends requests to the FastAPI service at http://127.0.0.1:8000. Start the API first, then start the interface in a separate terminal.

Terminal 1 — start the API

uvicorn api:app --reload
The API root is available at http://127.0.0.1:8000/. Interactive API documentation is normally available at http://127.0.0.1:8000/docs.

Terminal 2 — start the Streamlit UI

streamlit run app.py
Open the local URL printed by Streamlit in your browser.

API endpoint
GET / — returns a message indicating that the API is running.
POST /predict — accepts the customer fields defined by the CustomerData Pydantic model and returns the predicted class, churn probability, and a probability-based risk label.
The API expects the input fields and encoded category values described in api.py. Use the exact schema when testing /predict.

Model Training and Evaluation
Open notebooks/eda_and_training.ipynb and run its cells in order to inspect the data, train the models, and view the evaluation output.

The notebook currently:

Creates a stratified 80/20 train/test split with random_state=42.
Trains a Random Forest classifier with class_weight="balanced".
Trains an XGBoost classifier with a configured scale_pos_weight.
Calculates classification reports and ROC-AUC scores.
Selects the model with the higher ROC-AUC and saves it as best_model.pkl.
Saves the training feature names to feature_names.pkl.
Reporting results: Add your actual ROC-AUC, precision, recall, F1-score, and confusion-matrix results here after running the notebook. Do not report example or assumed metrics as project results.

Analysis Visuals and Insights
Export 2–3 charts from the notebook into images/, then replace the placeholders below with the real images and evidence-based findings.

1. Tenure and Monthly Charges by Churn


Insight: Write 1–2 sentences describing the pattern visible in your actual plot. Avoid claiming a relationship that the chart does not show.

2. Churn Distribution


Insight: State the number or proportion of churned and non-churned customers from the dataset output.

3. Model Evaluation or Feature Importance


Insight: Summarize the actual confusion matrix, evaluation metric, or top features produced by your notebook. Ensure the chart matches the text.

Example Prediction Response
The API response contains these fields:

{
  "churn_prediction": 0,
  "churn_label": "No - Will Stay",
  "churn_probability": 0.123,
  "risk_level": "Low"
}
This is an illustrative response format only; the numbers are examples, not measured model results.

Conclusion
This project demonstrates an end-to-end machine-learning workflow for customer churn prediction: preparing customer data, exploring patterns, comparing classifiers, saving a trained model, exposing predictions through an API, and presenting results through a Streamlit interface.

Future Scope
Add reproducible dataset paths and a documented data-download process.
Evaluate model performance with appropriate metrics and cross-validation.
Review recall and precision for the churn class, not ROC-AUC alone.
Add input validation and clearer API error handling.
Add automated tests for the API and feature mapping.
Add model versioning and a documented retraining workflow.
Monitor model performance and data drift if the project is deployed.
Add explainability, such as feature importance or SHAP, if suitable for the selected model.
Known Setup Notes
The notebook's original CSV path is machine-specific; change it to a project-relative path before rerunning.
api.py loads best_model.pkl and feature_names.pkl from the current working directory. Start Uvicorn from the repository root, or update the code to use paths relative to api.py.
The notebook saves the selected model and feature names using paths beginning with ../; verify the working directory and output location when running it.
The API schema and the model's training feature columns must stay aligned. Test a sample request after training or replacing the model.
The notebook's final confusion matrix and feature-importance plot currently use the Random Forest model variables even when XGBoost may have been selected as the best model. Label these plots accurately or update the notebook to evaluate the selected model.
Author
Mitesh
GitHub: @mitesh256

⋮⋮⋮⋮
