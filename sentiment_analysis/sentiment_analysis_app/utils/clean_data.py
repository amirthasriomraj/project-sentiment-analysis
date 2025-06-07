import re

def clean_tweet(text):
    text = re.sub(r"http\S+", "", text)               # Remove URLs
    text = re.sub(r"@\w+", "", text)                  # Remove mentions
    text = re.sub(r"#\w+", "", text)                  # Remove hashtags
    text = re.sub(r"[^\w\s]", "", text)               # Remove punctuation/emojis
    text = re.sub(r"\s+", " ", text).strip()          # Normalize spaces
    return text
