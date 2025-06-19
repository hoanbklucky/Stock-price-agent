import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def load_and_prepare_data(file_path):
    """
    Load and prepare the tonsillectomy patient data for training
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing patient data
        
    Returns:
    --------
    tuple
        (X_train, X_test, y_train, y_test, feature_names, class_names)
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Clean column names by stripping whitespace and special characters
    df.columns = df.columns.str.strip()
    print('COLUMNS:', list(df.columns))
    
    # Drop rows where Triage Deposition is blank
    df = df.dropna(subset=['Triage Deposition'])
    
    # Convert Triage Deposition to lowercase
    df['Triage Deposition'] = df['Triage Deposition'].str.lower()
    
    # Drop the first 4 columns and the target column
    X = df.drop(columns=['Triage Deposition'])
    print('X:', X.columns)
    # Handle categorical features
    categorical_features = X.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for feature in categorical_features:
        X[feature] = X[feature].fillna('Unknown')
        X[feature] = le.fit_transform(X[feature])
    
    # Handle numerical features
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
    for feature in numerical_features:
        X[feature] = X[feature].fillna(X[feature].mean())
    
    # Create target variable using Triage Deposition
    le = LabelEncoder()
    y = le.fit_transform(df['Triage Deposition'])
    class_names = le.classes_
    print("Class names and their corresponding numbers:")
    for i, name in enumerate(class_names):
        print(f"{name}: {i}")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, X.columns, class_names

if __name__ == "__main__":
    # Example usage
    file_path = "Review sheet for Tonsillectomy App_04_22 EO.xlsx - Breakdown by question.csv"
    X_train, X_test, y_train, y_test, features, class_names = load_and_prepare_data(file_path)
    
    print("Training data shape:", X_train.shape)
    print("Test data shape:", X_test.shape)
    print("\nFeature names:", features)
    print("\nClass distribution in training set:")
    print(pd.Series(y_train).value_counts(normalize=True)) 
    print(pd.Series(y_train).value_counts(normalize=False)) 
    print("\nClass distribution in Test set:")
    print(pd.Series(y_test).value_counts(normalize=True)) 
    print(pd.Series(y_test).value_counts(normalize=False))