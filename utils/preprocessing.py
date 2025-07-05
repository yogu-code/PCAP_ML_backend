def preprocess_pcap_csv(csv_path, scaler_save_path, preview_rows=5):
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import RobustScaler
    import joblib
    import os
    #Loading dataset
    df = pd.read_csv(csv_path)
    label_column = df['label']
    #Dropping specified columns
    df.drop(columns=["Flow ID", "Timestamp", "Label", "Src IP", "Dst IP", "Src Port", "Dst Port"], inplace=True, errors='ignore')
    #Replacing infinite values with NaN and filling NaN with median
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    # Filling NaN values with median of each column
    df.fillna(df.median(numeric_only=True), inplace=True)
    scaler = RobustScaler()
    X = df.drop(columns=[label_column])
    y = df[label_column]
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    if not os.path.exists(os.path.dirname(scaler_save_path)):
        os.makedirs(os.path.dirname(scaler_save_path))
    X_scaled_df.to_csv("data/X_scaled.csv", index=False)
    y.to_csv("data/y.csv", index=False)
    joblib.dump(scaler, scaler_save_path)
    joblib.dump(X_scaled_df.columns.tolist(), os.path.join(os.path.dirname(scaler_save_path), 'feature_columns.pkl'))

    return X_scaled_df, y, scaler, df.head(preview_rows)
