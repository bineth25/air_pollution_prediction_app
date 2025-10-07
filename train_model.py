import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocess import load_and_preprocess_data

def train_regression_model():
    df, le = load_and_preprocess_data(
        "data/US_air_pollution_dataset_2000_2023.csv",
        start_year=2020
    )

    
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day

    
    X_reg = df[["Year", "Month", "Day", "State", "County", "City"]]
    y_reg = df[[
        "O3 Mean", "O3 1st Max Value", "O3 AQI",
        "CO Mean", "CO 1st Max Value", "CO AQI",
        "SO2 Mean", "SO2 1st Max Value", "SO2 AQI",
        "NO2 Mean", "NO2 1st Max Value", "NO2 AQI"
    ]]

    
    X_train, X_test, y_train, y_test = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )

    
    categorical_features = ["State", "County", "City"]
    numeric_features = ["Year", "Month", "Day"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features),
        ]
    )

    
    regressor = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    reg_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", regressor)
    ])

    
    print("🔄 Training Random Forest Regressor...")
    reg_pipeline.fit(X_train, y_train)

   
    y_pred = reg_pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n📊 Model Evaluation Results:")
    print(f"Mean Absolute Error (MAE): {mae:.3f}")
    print(f"Mean Squared Error (MSE): {mse:.3f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.3f}")
    print(f"R² Score (Accuracy): {r2:.3f}")

    print("\n✅ Model trained successfully (no external file saved).")
    print("💾 Model will be re-trained each time the app starts.")

    return reg_pipeline
