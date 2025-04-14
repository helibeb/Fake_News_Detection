from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import os

# Initialize FastAPI app
app = FastAPI(title="Fake News Detector API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class NewsRequest(BaseModel):
    text: str

# Define response model
class FeatureContribution(BaseModel):
    name: str
    contribution: float
    description: str

class AnalysisResult(BaseModel):
    prediction: str
    probability: float
    features: List[FeatureContribution]

# Load model (in a real app, you would train and save this model)
# For demonstration, we'll create a simple model on startup
model_path = "models/news_classifier.pkl"
vectorizer_path = "models/tfidf_vectorizer.pkl"

# Feature descriptions for explanation
feature_descriptions = {
    "emotional_language": "High emotional content often indicates potential bias",
    "source_credibility": "Analysis of cited sources and their reliability",
    "statistical_consistency": "Evaluation of numerical claims and statistics",
    "writing_style": "Linguistic patterns common in misleading content"
}

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Initialize or load model
try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("Model loaded successfully")
except:
    print("Creating new model")
    # In a real application, you would train this on a dataset
    # This is just a placeholder implementation
    vectorizer = TfidfVectorizer(max_features=5000)
    model = MultinomialNB()
    
    # Dummy training data
    X_train = [
        "This is a real news article about politics",
        "Scientists discover new species in the Amazon",
        "Breaking news: Stock market reaches record high",
        "SHOCKING: You won't believe what this celebrity did!",
        "This SECRET the government doesn't want you to know!!!",
        "Doctors HATE this one weird trick to lose weight fast"
    ]
    y_train = [0, 0, 0, 1, 1, 1]  # 0 = real, 1 = fake
    
    # Fit the model
    X_train_vec = vectorizer.fit_transform(X_train)
    model.fit(X_train_vec, y_train)
    
    # Save the model
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

# Helper function to extract features from text
def extract_features(text):
    # In a real application, you would implement sophisticated feature extraction
    # This is a simplified version for demonstration
    features = {
        "emotional_language": 0.0,
        "source_credibility": 0.0,
        "statistical_consistency": 0.0,
        "writing_style": 0.0
    }
    
    # Simple heuristics for feature extraction
    text_lower = text.lower()
    
    # Emotional language detection
    emotional_words = ["shocking", "unbelievable", "incredible", "amazing", "outrageous"]
    features["emotional_language"] = sum(word in text_lower for word in emotional_words) / max(1, len(text.split()))
    
    # Source credibility (simplified)
    credible_sources = ["according to research", "studies show", "experts say", "evidence suggests"]
    features["source_credibility"] = sum(phrase in text_lower for phrase in credible_sources) / max(1, len(text.split()) / 10)
    
    # Statistical consistency (simplified)
    statistical_terms = ["percent", "study", "survey", "research", "data"]
    features["statistical_consistency"] = sum(term in text_lower for term in statistical_terms) / max(1, len(text.split()) / 10)
    
    # Writing style (simplified)
    clickbait_patterns = ["you won't believe", "this will shock you", "secret", "revealed", "!!!"]
    features["writing_style"] = sum(pattern in text_lower for pattern in clickbait_patterns) / max(1, len(text.split()) / 10)
    
    return features

# Endpoint to analyze news
@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_news(request: NewsRequest):
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text is too short for analysis")
    
    try:
        # Vectorize the text
        text_vectorized = vectorizer.transform([request.text])
        
        # Get prediction and probability
        prediction = model.predict(text_vectorized)[0]
        probabilities = model.predict_proba(text_vectorized)[0]
        
        # Get the probability of the predicted class
        probability = probabilities[prediction]
        
        # Extract features for explanation
        features_dict = extract_features(request.text)
        
        # Normalize feature contributions to sum to 1
        total = sum(features_dict.values())
        if total > 0:
            features_dict = {k: v/total for k, v in features_dict.items()}
        
        # Create feature contributions list
        feature_contributions = [
            FeatureContribution(
                name=k.replace("_", " ").title(),
                contribution=v,
                description=feature_descriptions.get(k, "")
            )
            for k, v in features_dict.items()
        ]
        
        # Sort by contribution (highest first)
        feature_contributions.sort(key=lambda x: x.contribution, reverse=True)
        
        return AnalysisResult(
            prediction="FAKE" if prediction == 1 else "REAL",
            probability=float(probability),
            features=feature_contributions
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Fake News Detection API is running"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)