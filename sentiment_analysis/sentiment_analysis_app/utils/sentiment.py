# from transformers import pipeline

# # Load the model once globally
# sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# def analyze_sentiment(text):
#     result = sentiment_model(text[:512])[0]  # truncate long input
#     label = result['label']
#     score = float(result['score'])

#     # Define neutral range (adjust as needed)
#     if 0.45 <= score <= 0.55:
#         sentiment = 'Neutral'
#     else:
#         sentiment = label.capitalize()  # 'positive' or 'negative'

#     return sentiment, score


from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # range: [-1.0, 1.0]

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, polarity
