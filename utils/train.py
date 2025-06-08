def train(X_path, y_path):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier
    from sklearn.metrics import classification_report, confusion_matrix
    import joblib
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Load data
    X = pd.read_csv(X_path)
    y = pd.read_csv(y_path).squeeze()  # Assuming y is a single column

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define models
    base_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(),
        "XGBoost": GradientBoostingClassifier()
    }

    # Hybrid: Voting Classifier
    voting_clf = VotingClassifier(estimators=[
        ('lr', base_models['Logistic Regression']),
        ('rf', base_models['Random Forest']),
        ('xgb', base_models['XGBoost'])
    ], voting='soft')

    # Hybrid: Stacking Classifier
    stacking_clf = StackingClassifier(
        estimators=[
            ('lr', base_models['Logistic Regression']),
            ('rf', base_models['Random Forest']),
            ('xgb', base_models['XGBoost'])
        ],
        final_estimator=LogisticRegression()
    )

    models = base_models.copy()
    models["Voting Ensemble"] = voting_clf
    models["Stacking Ensemble"] = stacking_clf

    results = {}
    trained_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        results[name] = report['weighted avg']

        print(f"### {name} Report")
        print(classification_report(y_test, y_pred))
        
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', ax=ax)
        plt.title(f"{name} Confusion Matrix")
        plt.show()

        trained_models[name] = model

        # Save the model
        model_save_path = f"models/{name.replace(' ', '_').lower()}.pkl"
        joblib.dump(model, model_save_path)

    return results, trained_models
