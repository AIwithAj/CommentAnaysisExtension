from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import pandas as pd
import os
import nltk
from datetime import datetime, timedelta
import mlflow
from mlflow.tracking import MlflowClient
import joblib
import dagshub
import warnings
from pandas.errors import PerformanceWarning
warnings.simplefilter("ignore", PerformanceWarning)


# Download required NLTK data
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
except Exception as e:
    print(f"NLTK download error: {e}")

app = Flask(__name__)
CORS(app)

# 🆕 Load real model and transformer
def load_model_and_vectorizer_separate_runs(model_name, vectorizer_run_id, artifact_path):
    dagshub.init(
        repo_owner="AIwithAj",
        repo_name="CommentAnalysis",
        mlflow=True,
    )

    client = MlflowClient()
    latest_prod = client.get_latest_versions(model_name, stages=["Production"])
    if not latest_prod:
        raise Exception(f"No model in 'Production' stage for: {model_name}")

    model_uri = f"models:/{model_name}/Production"
    # model = mlflow.pyfunc.load_model(model_uri)
    model = mlflow.sklearn.load_model(model_uri)

    vectorizer_path = mlflow.artifacts.download_artifacts(
        run_id=vectorizer_run_id,
        artifact_path=artifact_path
    )

    # ✅ Use pickle instead of joblib
    import pickle
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    return model, vectorizer


# Load model/vectorizer once globally
run_id = "e7456a00a6d74d1f9dfc2da425a41d24"
artifact_path = "transformer.pkl"
model, vectorizer = load_model_and_vectorizer_separate_runs("yt_chrome_plugin_model",run_id, artifact_path)

# ✅ Preprocessing remains unchanged
def preprocess_comment(comment):
    try:
        comment = comment.lower().strip()
        comment = re.sub(r'\n', ' ', comment)
        comment = re.sub(r'[^A-Za-z0-9\s!?.,]', '', comment)

        try:
            stop_words = set(stopwords.words('english')) - {'not', 'but', 'however', 'no', 'yet'}
            comment = ' '.join([word for word in comment.split() if word not in stop_words])
        except:
            common_stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            comment = ' '.join([word for word in comment.split() if word not in common_stopwords])

        try:
            lemmatizer = WordNetLemmatizer()
            comment = ' '.join([lemmatizer.lemmatize(word) for word in comment.split()])
        except:
            pass

        return comment
    except Exception as e:
        print(f"Error in preprocessing comment: {e}")
        return comment

@app.route('/')
def home():
    return jsonify({"message": "YouTube Sentiment Analysis API", "status": "running"})

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "sentiment_engine": "mlflow_model",
        "nltk_available": True
    })

# 🛠️ Updated to use real model
def analyze_comments_data(comments_data):
    comments = [item['text'] for item in comments_data]
    timestamps = [item['timestamp'] for item in comments_data]
    author_ids = [item.get('authorId', 'Unknown') for item in comments_data]

    preprocessed_comments = [preprocess_comment(comment) for comment in comments]
    
    # Use actual model and transformer
    transformed = vectorizer.transform(preprocessed_comments)
    

#     import pandas as pd

# # Get proper feature names from the vectorizer
#     feature_names = vectorizer.get_feature_names_out()


# # Convert to DataFrame with correct feature names
#     X_input = pd.DataFrame(transformed.toarray(), columns=feature_names, dtype='float32').copy()


# Pass this named DataFrame to your model
    predictions = model.predict(transformed)
    
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    sentiment_data = []

    for i, (comment, sentiment, timestamp, author_id) in enumerate(zip(comments, predictions, timestamps, author_ids)):
        if sentiment == 1:
            sentiment_label = "positive"
        elif sentiment == 0:
            sentiment_label = "neutral"
        else:
            sentiment_label = "negative"

        sentiment_counts[sentiment_label] += 1
        sentiment_data.append({
            "id": i,
            "comment": comment,
            "sentiment": int(sentiment),
            "sentiment_label": sentiment_label,
            "timestamp": timestamp,
            "author_id": author_id,
            "word_count": len(comment.split())
        })
    
    total_comments = len(comments)
    unique_commenters = len(set(author_ids))
    total_words = sum(len(comment.split()) for comment in comments)
    avg_words_per_comment = round(total_words / total_comments, 2) if total_comments > 0 else 0

    total_sentiment_score = sum(predictions)
    avg_sentiment_raw = total_sentiment_score / total_comments if total_comments > 0 else 0
    avg_sentiment_normalized = round(((avg_sentiment_raw + 1) / 2) * 10, 2)

    engagement_score = min(avg_words_per_comment * 10, 100)

    from collections import defaultdict
    hourly_sentiment = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})

    for item in sentiment_data:
        try:
            timestamp_dt = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
            hour_key = timestamp_dt.strftime('%Y-%m-%d %H:00:00')
            sentiment_label = item['sentiment_label']
            hourly_sentiment[hour_key][sentiment_label] += 1
        except:
            continue

    trend_data = [{
        "hour": hour,
        "positive": sentiments["positive"],
        "neutral": sentiments["neutral"],
        "negative": sentiments["negative"]
    } for hour, sentiments in sorted(hourly_sentiment.items())]

    all_words = []
    for comment in preprocessed_comments:
        all_words.extend(comment.split())

    from collections import Counter
    word_counts = Counter(all_words)
    word_cloud_data = [[word, count] for word, count in word_counts.most_common(20)]

    positive_comments = [item for item in sentiment_data if item['sentiment_label'] == 'positive']
    negative_comments = [item for item in sentiment_data if item['sentiment_label'] == 'negative']
    most_engaged = sorted(sentiment_data, key=lambda x: x['word_count'], reverse=True)[:10]

    return {
        "success": True,
        "metrics": {
            "total_comments": total_comments,
            "unique_commenters": unique_commenters,
            "avg_words_per_comment": avg_words_per_comment,
            "sentiment_score": avg_sentiment_normalized,
            "engagement_score": engagement_score
        },
        "sentiment_distribution": sentiment_counts,
        "sentiment_data": sentiment_data,
        "trend_data": trend_data,
        "word_cloud_data": word_cloud_data,
        "top_comments": {
            "positive": positive_comments[:5],
            "negative": negative_comments[:5],
            "most_engaged": most_engaged
        }
    }

@app.route('/demo')
def demo_analysis():
    demo_comments = [
        {"text": "This video is absolutely amazing!", "timestamp": "2025-01-15T10:00:00Z", "authorId": "user1"},
        {"text": "This is terrible. Waste of my time.", "timestamp": "2025-01-15T10:45:00Z", "authorId": "user2"},
        {"text": "Perfect explanation! Thank you", "timestamp": "2025-01-15T11:00:00Z", "authorId": "user3"},
    ]
    return jsonify(analyze_comments_data(demo_comments))

@app.route('/analyze_comments', methods=['POST'])
def analyze_comments():
    data = request.json
    comments_data = data.get('comments')
    
    if not comments_data:
        return jsonify({"error": "No comments provided"}), 400

    try:
        return jsonify(analyze_comments_data(comments_data))
    except Exception as e:
        app.logger.error(f"Error in analyze_comments: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/predict_with_timestamps', methods=['POST'])
def predict_with_timestamps():
    data = request.json
    comments_data = data.get('comments')
    
    if not comments_data:
        return jsonify({"error": "No comments provided"}), 400

    try:
        comments = [item['text'] for item in comments_data]
        timestamps = [item['timestamp'] for item in comments_data]

        preprocessed_comments = [preprocess_comment(comment) for comment in comments]
        transformed = vectorizer.transform(preprocessed_comments)
#         import pandas as pd

# # Get proper feature names from the vectorizer
#         feature_names = vectorizer.get_feature_names_out()

# # Convert to DataFrame with correct feature names
#         X_input = pd.DataFrame(transformed.toarray(), columns=feature_names, dtype='float32').copy()





# Pass this named DataFrame to your model
        predictions = model.predict(transformed)
        predictions = [int(p) for p in predictions]
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    response = [{"comment": comment, "sentiment": sentiment, "timestamp": timestamp}
                for comment, sentiment, timestamp in zip(comments, predictions, timestamps)]
    return jsonify(response)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
