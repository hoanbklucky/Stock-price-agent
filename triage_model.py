import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import StandardScaler
import joblib

class TriageModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def create_model(self, input_shape):
        """Create a neural network model for triage prediction"""
        model = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=input_shape),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(3, activation='softmax')  # 3 classes: Low, Medium, High priority
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def preprocess_data(self, data):
        """Preprocess the input data"""
        return self.scaler.transform(data)
    
    def train(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
        """Train the model"""
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Train the model
        history = self.model.fit(
            X_train_scaled, y_train,
            validation_data=(X_val_scaled, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        return history
    
    def predict(self, X):
        """Make predictions on new data"""
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        return predictions
    
    def save_model(self, model_path='triage_model.h5', scaler_path='scaler.save'):
        """Save the model and scaler"""
        self.model.save(model_path)
        joblib.dump(self.scaler, scaler_path)
    
    def load_model(self, model_path='triage_model.h5', scaler_path='scaler.save'):
        """Load the model and scaler"""
        self.model = models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)

# Example feature names for reference
FEATURE_NAMES = [
    'age',
    'temperature',
    'heart_rate',
    'respiratory_rate',
    'blood_pressure_systolic',
    'blood_pressure_diastolic',
    'oxygen_saturation',
    'pain_level',
    'consciousness_level',
    'bleeding_severity'
]

# Example of how to use the model:
"""
# Create and train the model
model = TriageModel()
model.create_model(input_shape=(len(FEATURE_NAMES),))

# Train the model with your data
history = model.train(X_train, y_train, X_val, y_val)

# Make predictions
predictions = model.predict(X_test)

# Save the model
model.save_model()
""" 