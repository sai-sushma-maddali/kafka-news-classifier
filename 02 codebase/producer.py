import pandas as pd
from kafka import KafkaProducer
import json
import time
import numpy as np

def json_serializer(obj):
    if isinstance(obj, (np.int64, np.int32, np.float32, np.float64)):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")
    
# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=json_serializer).encode('utf-8')
)

print("Kafka producer initialized successfully!")

# Load csv data into DataFrame
try:
    df = pd.read_csv("test_data.csv")
    print(f"Loaded csv file with {len(df)} rows.")
except Exception as e:
    print("Error while reading the data:", e)
    exit(1)
	
topic_name = 'news_classifier'
    
try:

	# Stream each row as a Kafka message
	for i, row in df.iterrows():
		message = row.to_dict()
		news_text = message["text"]
		try:
			producer.send(topic_name, value=message)
			print(f"Sent news article {i + 1}")
		except Exception as e:
			print(f"Error sending news article {i + 1}: {e}")
		
		time.sleep(5)  # simulate streaming delay
except KeyboardInterrupt:
    print("\nStreaming stopped manually.")
finally:
    producer.flush()
    producer.close()
    print("Kafka producer closed gracefully.")
	
