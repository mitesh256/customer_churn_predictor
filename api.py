from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="Customer Churn Predictor API")

# Model aur feature names load karo
model = joblib.load("best_model.pkl")
feature_names = joblib.load("feature_names.pkl")

class CustomerData(BaseModel):
    gender: int              # 0 = Female, 1 = Male
    SeniorCitizen: int       # 0 = No, 1 = Yes
    Partner: int             # 0 = No, 1 = Yes
    Dependents: int          # 0 = No, 1 = Yes
    tenure: int              # months
    PhoneService: int        # 0 = No, 1 = Yes
    PaperlessBilling: int    # 0 = No, 1 = Yes
    MonthlyCharges: float
    TotalCharges: float
    MultipleLines_No_phone_service: int
    MultipleLines_Yes: int
    InternetService_Fiber_optic: int
    InternetService_No: int
    OnlineSecurity_No_internet_service: int
    OnlineSecurity_Yes: int
    OnlineBackup_No_internet_service: int
    OnlineBackup_Yes: int
    DeviceProtection_No_internet_service: int
    DeviceProtection_Yes: int
    TechSupport_No_internet_service: int
    TechSupport_Yes: int
    StreamingTV_No_internet_service: int
    StreamingTV_Yes: int
    StreamingMovies_No_internet_service: int
    StreamingMovies_Yes: int
    Contract_One_year: int
    Contract_Two_year: int
    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int

@app.get("/")
def home():
    return {"message": "Customer Churn Predictor API is running!"}

@app.post("/predict")
def predict(data: CustomerData):
    try:
        # Input ko dictionary mein convert karo
        input_dict = data.dict()

        # Spaces wale column names fix karo
        # Pydantic mein underscore use kiya tha, model mein spaces/parentheses hain
        column_mapping = {
            "MultipleLines_No_phone_service": "MultipleLines_No phone service",
            "InternetService_Fiber_optic": "InternetService_Fiber optic",
            "OnlineSecurity_No_internet_service": "OnlineSecurity_No internet service",
            "OnlineBackup_No_internet_service": "OnlineBackup_No internet service",
            "DeviceProtection_No_internet_service": "DeviceProtection_No internet service",
            "TechSupport_No_internet_service": "TechSupport_No internet service",
            "StreamingTV_No_internet_service": "StreamingTV_No internet service",
            "StreamingMovies_No_internet_service": "StreamingMovies_No internet service",
            "Contract_One_year": "Contract_One year",
            "Contract_Two_year": "Contract_Two year",
            "PaymentMethod_Credit_card_automatic": "PaymentMethod_Credit card (automatic)",
            "PaymentMethod_Electronic_check": "PaymentMethod_Electronic check",
            "PaymentMethod_Mailed_check": "PaymentMethod_Mailed check",
        }

        # Rename keys
        for old_key, new_key in column_mapping.items():
            if old_key in input_dict:
                input_dict[new_key] = input_dict.pop(old_key)

        # DataFrame banao — same order mein jo model ne dekha tha
        input_df = pd.DataFrame([input_dict], columns=feature_names)

        # Prediction karo
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        return {
            "churn_prediction": int(prediction),
            "churn_label": "Yes - Will Churn" if prediction == 1 else "No - Will Stay",
            "churn_probability": round(float(probability), 3),
            "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))