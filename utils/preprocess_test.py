def preprocess_test_file(csv_path, label_column, columns_to_drop, scaler_path, preview_rows=5):
    import pandas as pd
    import numpy as np
    import joblib
    import os

    df = pd.read_csv(csv_path)

    #Loading saved scaler and feature list
    scaler = joblib.load(os.path.join(scaler_path, 'scaler.pkl'))
    feature_columns = joblib.load(os.path.join(scaler_path, 'feature_columns.pkl'))

    #Dropping extra columns
    df = df[feature_columns]

    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(df.median(numeric_only=True), inplace=True)

    X_test_scaled = scaler.transform(df)

    return X_test_scaled



