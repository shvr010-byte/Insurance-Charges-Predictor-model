import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os

# Set page config
st.set_page_config(page_title="Insurance Charges Predictor", layout="wide")

st.title("🏥 Insurance Charges Predictor")
st.write("Predict health insurance charges based on personal information")

# Create a function to train and save the model
@st.cache_resource
def load_or_train_model():
    model_path = "insurance_model.pkl"
    scaler_path = "scaler.pkl"
    
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler
    else:
        # Train model if not exists
        try:
            df = pd.read_csv('insurance.csv')
            
            # Data preprocessing
            df_cleaned = df.copy()
            df_cleaned.drop_duplicates(inplace=True)
            df_cleaned['sex'] = df_cleaned['sex'].map({'male': 0, 'female': 1})
            df_cleaned['smoker'] = df_cleaned['smoker'].map({'no': 0, 'yes': 1})
            df_cleaned.rename(columns={'sex': 'is_female', 'smoker': 'is_smoker'}, inplace=True)
            df_cleaned = pd.get_dummies(df_cleaned, columns=['region'], drop_first=True)
            df_cleaned = df_cleaned.astype(int)
            
            # Feature engineering
            df_cleaned['bmi_category'] = pd.cut(
                df_cleaned['bmi'],
                bins=[0, 18.5, 24.9, 29.9, float('inf')],
                labels=['Underweight', 'Normal', 'Overweight', 'Obese']
            )
            df_cleaned = pd.get_dummies(df_cleaned, columns=['bmi_category'], drop_first=True)
            
            # Scale numeric features
            scaler = StandardScaler()
            cols = ['age', 'bmi', 'children']
            df_cleaned[cols] = scaler.fit_transform(df_cleaned[cols])
            
            # Select final features
            final_df = df_cleaned[['age', 'is_female', 'bmi', 'children', 'is_smoker', 'charges', 
                                    'region_southeast', 'bmi_category_Obese']]
            
            X = final_df.drop('charges', axis=1)
            y = final_df['charges']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
            
            # Train Ridge model with CV
            ridge_cv = RidgeCV(alphas=[0.1, 1.0, 10.0, 100.0], cv=5)
            ridge_cv.fit(X_train, y_train)
            
            # Save model and scaler
            with open(model_path, 'wb') as f:
                pickle.dump(ridge_cv, f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)
            
            return ridge_cv, scaler
        except Exception as e:
            st.error(f"Error training model: {e}")
            return None, None

# Load model
model, scaler = load_or_train_model()

if model is None:
    st.warning("Please ensure 'insurance.csv' is in the same directory as this app.")
else:
    st.success("✅ Model loaded successfully!")
    
    # Create input form
    st.sidebar.header("📋 Enter Patient Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.sidebar.slider("Age", min_value=18, max_value=100, value=30, step=1)
        bmi = st.sidebar.slider("BMI", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
        children = st.sidebar.slider("Number of Children", min_value=0, max_value=5, value=0, step=1)
    
    with col2:
        gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
        smoker = st.sidebar.selectbox("Smoker", ["No", "Yes"])
        region = st.sidebar.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])
    
    # Prepare input data
    is_female = 1 if gender == "Female" else 0
    is_smoker = 1 if smoker == "Yes" else 0
    
    # Region encoding
    region_southeast = 1 if region == "Southeast" else 0
    
    # BMI category encoding
    if bmi < 18.5:
        bmi_category_obese = 0
    elif bmi < 25:
        bmi_category_obese = 0
    elif bmi < 30:
        bmi_category_obese = 0
    else:
        bmi_category_obese = 1
    
    # Scale numeric features
    scaled_age = (age - 39.21) / 14.45  # Mean and std from training data (approximate)
    scaled_bmi = (bmi - 30.66) / 6.10
    scaled_children = (children - 1.09) / 1.21
    
    # Create feature vector
    input_data = np.array([[scaled_age, is_female, scaled_bmi, scaled_children, is_smoker, 
                            region_southeast, bmi_category_obese]])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Prediction Result")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Predicted Annual Charges", f"${prediction:,.2f}")
    
    with col2:
        st.info(f"**Monthly Cost:** ${prediction/12:,.2f}")
    
    # Display input summary
    st.subheader("📝 Input Summary")
    summary_data = {
        "Feature": ["Age", "Gender", "BMI", "Children", "Smoker", "Region"],
        "Value": [f"{age} years", gender, f"{bmi:.1f}", children, smoker, region]
    }
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)
    
    # Risk assessment
    st.subheader("⚠️ Risk Assessment")
    if prediction < 5000:
        st.success("Low Risk - Affordable insurance rates")
    elif prediction < 15000:
        st.warning("Medium Risk - Moderate insurance rates")
    else:
        st.error("High Risk - Higher insurance rates")

st.markdown("---")
st.caption("Insurance Charges Prediction Model | Based on Ridge Regression with Cross-Validation")
