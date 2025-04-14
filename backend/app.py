from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock training data for demonstration
# In a real application, you would use a much larger dataset
fake_news = [
    "BREAKING: Shocking scandal revealed! Government officials CAUGHT in massive conspiracy!",
    "You won't BELIEVE what this celebrity did! The truth will SHOCK you!",
    "URGENT: Scientists discover MIRACLE cure that Big Pharma doesn't want you to know about!",
    "WARNING: The media is LYING to you about this important issue!",
    "EXCLUSIVE: Secret document reveals what they've been hiding from the public!",
    "This ONE WEIRD TRICK will make you rich overnight! Banks HATE this!",
    "ALERT: Dangerous new threat that NO ONE is talking about! Are you at risk?",
    "The TRUTH about vaccines that doctors won't tell you! SHARE before they delete this!",
    "BOMBSHELL report exposes massive election fraud! Thousands of fake votes found!",
    "They're putting CHEMICALS in the water that are making people sick! Government cover-up EXPOSED!"
]

real_news = [
    "Study finds correlation between exercise and improved mental health, researchers say more data needed",
    "Local council approves new infrastructure project, construction to begin next month",
    "Company reports 2% increase in quarterly earnings, slightly below market expectations",
    "Scientists publish findings of 3-year climate study in peer-reviewed journal",
    "New legislation aims to address housing shortage through zoning changes",
    "Survey indicates slight shift in consumer preferences for electric vehicles",
    "Health officials recommend seasonal vaccination as flu season approaches",
    "Stock market shows modest gains following central bank interest rate decision",
    "Research team identifies potential new treatment for common illness, clinical trials planned",
    "International diplomatic talks continue, representatives report progress on key issues"
]

# Create labels for our training data
labels = np.array([1] * len(fake_news) + [0] * len(real_news))  # 1 for fake, 0 for real

# Function to extract features from text
def extract_features(text):
    # Count exclamation marks
    exclamation_count = len(re.findall(r'!', text))
    
    # Count question marks
    question_count = len(re.findall(r'\?', text))
    
    # Count all caps words (as a measure of sensationalism)
    all_caps_count = len(re.findall(r'\b[A-Z]{2,}\b', text))
    
    # Count words like "shocking", "breaking", "urgent", etc.
    sensational_words = ['shocking', 'breaking', 'urgent', 'exclusive', 'bombshell', 
                         'miracle', 'secret', 'conspiracy', 'exposed', 'warning']
    sensational_count = sum(1 for word in sensational_words if word.lower() in text.lower())
    
    # Word count
    word_count = len(text.split())
    
    # Normalize by word count
    features = {
        'exclamation_ratio': exclamation_count / max(word_count, 1),
        'question_ratio': question_count / max(word_count, 1),
        'all_caps_ratio': all_caps_count / max(word_count, 1),
        'sensational_ratio': sensational_count / max(word_count, 1)
    }
    
    return features

# Initialize and train the model
def train_model():
    # Combine all training data
    all_texts = fake_news + real_news
    
    # Extract features for each text
    X = []
    for text in all_texts:
        features = extract_features(text)
        X.append([
            features['exclamation_ratio'],
            features['question_ratio'],
            features['all_caps_ratio'],
            features['sensational_ratio']
        ])
    
    X = np.array(X)
    
    # Train a Naive Bayes classifier (which implements Bayesian decision theory)
    model = MultinomialNB()
    model.fit(X, labels)
    
    return model

# Train the model
model = train_model()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    
    # Extract features  'No text provided'}), 400
    
    text = data['text']
    
    # Extract features
    features = extract_features(text)
    
    # Convert features to array for prediction
    X = np.array([[
        features['exclamation_ratio'],
        features['question_ratio'],
        features['all_caps_ratio'],
        features['sensational_ratio']
    ]])
    
    # Get prediction and probability
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    # Format the response
    result = {
        'prediction': 'FAKE' if prediction == 1 else 'REAL',
        'probability': float(probabilities[1] if prediction == 1 else probabilities[0]),
        'features': {
            'Exclamation ratio': features['exclamation_ratio'],
            'Question ratio': features['question_ratio'],
            'ALL CAPS ratio': features['all_caps_ratio'],
            'Sensational words ratio': features['sensational_ratio']
        }
    }
    
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# Print a message to show the app is running
print("Fake News Detection API is running!")
print("Training data: {} fake news articles, {} real news articles".format(len(fake_news), len(real_news)))
print("Model trained with Naive Bayes classifier (Bayesian decision theory)")
print("API endpoint: POST /analyze with JSON body containing 'text' field")