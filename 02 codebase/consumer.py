from kafka import KafkaConsumer
import json
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import joblib

# ---- Download required NLTK resources ----
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# ---- Load saved model ----
model = joblib.load("news_topic_pipeline.pkl")

# ---- Initialize Kafka consumer ----
consumer = KafkaConsumer(
    "news_classifier",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,   # ensures offsets are auto-committed
    group_id='news_consumer_group'  # good practice to assign a group
)

# ---- Function to clean text ----
def preprocess_text(text):
  # converting to lowercase
  text = text.lower()

  # removing punctuations, digits and special characters
  text = re.sub(r'[^a-zA-Z\s]', '', text)

  # removing stop words
  stop_words = set(stopwords.words('english'))
  text = ' '.join([w for w in text.split() if w not in stop_words])

  # tokenization
  tokens = word_tokenize(text)

  # lemmatization
  lemmatizer = WordNetLemmatizer()
  tokens = [lemmatizer.lemmatize(w) for w in tokens]

  # remove short tokens
  tokens = [w for w in tokens if len(w) > 2]

  # Joining the text back to cleaned sentence
  clean_text = ' '.join(tokens)

  return clean_text

# ---- Label mapping ----
label_map = {
    0: "World",
    1: "Sports",
    2: "Business",
    3: "Sci/Tech"
}

print("Kafka consumer started. Waiting for messages...")

try:
    for message in consumer:
        data = message.value
        raw_text = data.get("text", "")
        if not raw_text:
            continue

        # Clean and prepare features
        clean_text = preprocess_text(raw_text)
        sentiment = TextBlob(raw_text).sentiment.polarity
        text_len = len(raw_text.split())

        input_df = pd.DataFrame([{
            'processed_text': clean_text,
            'sentiment': sentiment,
            'text_len': text_len
        }])

        # Predict
        prediction = model.predict(input_df)[0]
        topic_name = label_map.get(prediction, "Unknown")

        print(f"\nText: {raw_text[:80]}...")
        print(f"Predicted Topic: {topic_name}")

except KeyboardInterrupt:
    print("\nConsumer stopped manually (Ctrl+C).")

finally:
    print("Closing Kafka consumer gracefully...")
    consumer.close()
    print("Kafka consumer closed successfully.")

