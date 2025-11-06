---

# Real-Time News Topic Classification using Apache Kafka

## **Project Overview**

This project demonstrates a **real-time data processing pipeline** built using **Apache Kafka** and **Python** to automatically classify streaming news articles into four categories — **World, Sports, Business,** and **Sci/Tech**.
It combines **streaming, NLP preprocessing, sentiment analysis, and machine learning inference** in one end-to-end intelligent system.

---

## **Pipeline Architecture**

### **1. Data Source**

* **Dataset:** [AG News Topic Classification (Kaggle)](https://www.kaggle.com/datasets/vrindakallu/ag-news-topic-classification)
* The dataset contains news headlines and descriptions labeled into four classes:

  * 0 → *World*
  * 1 → *Sports*
  * 2 → *Business*
  * 3 → *Sci/Tech*

---

### **2. Model Training (Offline Stage)**

* Implemented in `News_Topic_Classification.ipynb`
* **Steps performed:**

  1. Data loading and cleaning
  2. Text preprocessing (lowercasing, punctuation removal, stopword removal, lemmatization)
  3. Feature extraction using `TfidfVectorizer`
  4. Addition of numeric features:

     * **Sentiment polarity** (TextBlob)
     * **Text length** (word count)
  5. Model training using **LinearSVC**
  6. Pipeline creation combining:

     * `TfidfVectorizer`
     * `StandardScaler`
     * `LinearSVC`
  7. Model evaluation on test data
  8. Saving the final pipeline as `news_topic_pipeline.pkl` using `joblib`

The resulting model achieved **~90% accuracy** on validation data.

---

### **3. Kafka Streaming Pipeline (Real-Time Stage)**

#### **Producer (`producer.py`)**

* Reads `test_data.csv` (sample news articles)
* Converts each row to JSON and publishes it to Kafka topic **`news_classifier`**
* Simulates streaming using a delay (`time.sleep(5)`)
* Handles serialization for numeric types and closes gracefully

#### **Consumer (`consumer.py`)**

* Subscribes to the `news_classifier` topic
* Receives each message, performs:

  * Text cleaning (NLTK preprocessing)
  * Sentiment computation (`TextBlob`)
  * Text length extraction
* Loads `news_topic_pipeline.pkl` for prediction
* Classifies each article into one of the four categories
* Prints both the **original text** and the **predicted topic**
* Shuts down gracefully on Ctrl+C

#### **Kafka Topic**

* Acts as a message broker between producer and consumer
* Provides fault-tolerant, scalable real-time message transfer

---

## **Project Architecture Diagram**

```
+-------------------+           +------------------------+           +-------------------------+
|   Data Source     |  --->     |    Kafka Producer      |  --->     |      Kafka Topic        |
|  (AG News Dataset)|           | (Publishes JSON news)  |           |  ('news_classifier')    |
+-------------------+           +------------------------+           +-----------+-------------+
                                                                              |
                                                                              v
                                                                 +--------------------------+
                                                                 |      Kafka Consumer      |
                                                                 | (Preprocess + Predict)   |
                                                                 +-----------+--------------+
                                                                             |
                                                                             v
                                                                +----------------------------+
                                                                | Predicted Topic Output     |
                                                                | (World, Sports, Business,  |
                                                                |  Sci/Tech)                 |
                                                                +----------------------------+
```

---

## **Technologies Used**

| Component          | Purpose                                       |
| ------------------ | --------------------------------------------- |
| **Apache Kafka**   | Message streaming and queueing                |
| **Python**         | Core programming language                     |
| **Pandas / NumPy** | Data manipulation                             |
| **NLTK**           | Tokenization, stopword removal, lemmatization |
| **TextBlob**       | Sentiment polarity calculation                |
| **scikit-learn**   | TF-IDF, scaling, model pipeline, LinearSVC    |
| **joblib**         | Saving/loading trained pipeline               |
| **Kafka-Python**   | Kafka producer/consumer implementation        |

---

## **How to Run the Project**

### **Step 1. Start Kafka and Zookeeper**

```bash
# Start Zookeeper
zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
kafka-server-start.sh config/server.properties
```

### **Step 2. Create Kafka Topic**

```bash
kafka-topics.sh --create --topic news_classifier \
--bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### **Step 3. Run the Producer**

```bash
python3 producer.py
```

### **Step 4. Run the Consumer**

```bash
python3 consumer.py
```

### **Step 5. Observe Real-Time Output**

You’ll see console output like:

```
Text: Google launches new AI model for data centers...
Predicted Topic: Sci/Tech
```

Press **Ctrl + C** to gracefully stop producer or consumer.

---

## **Results and Performance**

* **Training Accuracy:** ~90%
* **Real-time Prediction:** ~3–5 articles per second (local Kafka)
* **Latency:** <1 second per message
* **Pipeline Level:** **Level 3 – Advanced Analytics (ML Integration)**

---

## **Project Files**

| File                              | Description                                   |
| --------------------------------- | --------------------------------------------- |
| `News_Topic_Classification.ipynb` | Model training and evaluation                 |
| `news_topic_pipeline.pkl`         | Trained ML model pipeline                     |
| `producer.py`                     | Kafka producer script for streaming data      |
| `consumer.py`                     | Kafka consumer script for real-time inference |
| `test_data.csv`                   | Sample input for producer                     |
| `README.md`                       | Project documentation                         |

---

## **Conclusion**

This project showcases how **Apache Kafka** can integrate seamlessly with **machine learning pipelines** for real-time intelligent data processing. It provides a scalable framework that can be extended to other domains like sentiment analysis, anomaly detection, and recommendation systems.
---
