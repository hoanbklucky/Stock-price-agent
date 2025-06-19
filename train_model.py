import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from prepare_data import load_and_prepare_data
import xgboost as xgb
from sklearn.neighbors import KNeighborsClassifier

def train_random_forest(X_train, y_train, max_depth=5):
    """
    Train a random forest model for triage prediction
    
    Parameters:
    -----------
    X_train : pandas.DataFrame
        Training features
    y_train : numpy.ndarray
        Training labels
    max_depth : int, optional
        Maximum depth of the trees in the forest
        
    Returns:
    --------
    sklearn.ensemble.RandomForestClassifier
        Trained random forest model
    """
    # Initialize and train the model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=max_depth,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    return model

def train_svm(X_train, y_train):
    model = SVC(kernel='rbf', probability=True, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_xgboost(X_train, y_train, max_depth=5):
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=max_depth,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def train_neural_network(X_train, y_train):
    model = MLPClassifier(
        hidden_layer_sizes=(100, 50),
        max_iter=1000,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def train_knn(X_train, y_train, n_neighbors=5):
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    return model

def rule_based_prediction(X):
    """
    Predict triage decision based on predefined rules.
    
    Parameters:
    -----------
    X : pandas.DataFrame
        Features
        
    Returns:
    --------
    numpy.ndarray
        Predicted labels
    """
    predictions = []
    for _, row in X.iterrows():
        # Example rule: If bleeding is present, predict 'Call Emergency Medical Services Now'
        if row['Is there any bleeding?'] == 1:
            predictions.append(0)  # 'Call Emergency Medical Services Now'
        # Example rule: If fever is present, predict 'Go to the ED Now (by car)'
        elif row['Are they having any fevers, pain, bloody sputum, healing issues, or trouble breathing?'] == 1:
            predictions.append(1)  # 'Go to the ED Now (by car)'
        # Example rule: If eating well, predict 'See within 6-8 weeks in office'
        elif row['Is pain preventing them from eating/ drinking?'] == 1:
            predictions.append(4)  # 'See within 6-8 weeks in office'
        # Default rule: Predict 'Unknown'
        else:
            predictions.append(5)  # 'Unknown'
    return np.array(predictions)

def evaluate_model(model, X_test, y_test, class_names, model_name):
    """
    Evaluate the trained model on test data
    
    Parameters:
    -----------
    model : sklearn.tree.DecisionTreeClassifier
        Trained decision tree model
    X_test : pandas.DataFrame
        Test features
    y_test : numpy.ndarray
        Test labels
    class_names : list or array
        List of class names for the target variable
    model_name : str
        Name of the model
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Print classification report
    print(f"\nClassification Report for {model_name}:")
    print(classification_report(
        y_test, y_pred,
        target_names=class_names,
        labels=range(len(class_names))
    ))
    
    # Print confusion matrix
    print(f"\nConfusion Matrix for {model_name}:")
    print(confusion_matrix(y_test, y_pred))
    
    # Print feature importance only for models that support it
    if hasattr(model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': X_test.columns,
            'importance': model.feature_importances_
        })
        print(f"\nFeature Importance for {model_name}:")
        print(feature_importance.sort_values('importance', ascending=False))
    
    return classification_report(y_test, y_pred, output_dict=True)

def main():
    # Load and prepare data
    file_path = "Review sheet for Tonsillectomy App_04_22 EO.xlsx - Breakdown by question.csv"
    X_train, X_test, y_train, y_test, features, class_names = load_and_prepare_data(file_path)
    
    # Train and evaluate multiple models
    models = {
        'Random Forest': train_random_forest(X_train, y_train),
        'SVM': train_svm(X_train, y_train),
        'XGBoost': train_xgboost(X_train, y_train),
        'Neural Network': train_neural_network(X_train, y_train),
        'KNN': train_knn(X_train, y_train)
    }
    
    results = {}
    for name, model in models.items():
        results[name] = evaluate_model(model, X_test, y_test, class_names, name)
    
    # Evaluate rule-based prediction
    rule_predictions = rule_based_prediction(X_test)
    results['Rule-Based'] = evaluate_model(
        type('obj', (object,), {'predict': lambda x: rule_predictions}),
        X_test, y_test, class_names, 'Rule-Based'
    )
    
    # Compare models
    print("\nModel Comparison:")
    for name, report in results.items():
        print(f"\n{name} - Weighted Avg F1-score: {report['weighted avg']['f1-score']:.3f}")
    
    # Save the best model (Random Forest for now)
    joblib.dump(models['Random Forest'], 'triage_decision_tree.joblib')
    print("\nBest model (Random Forest) saved as 'triage_decision_tree.joblib'")

if __name__ == "__main__":
    main() 