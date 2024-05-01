from confluent_kafka import Consumer, KafkaError
import psycopg2
import numpy as np
import cv2

class FrameProcessor:
    def __init__(self, model):
        self.model = model
        self.db_conn = psycopg2.connect(
            database="ppe_detection",
            user="admin",
            password="admin1234",
            host="localhost",
            port="5432"
        )
        self.cursor = self.db_conn.cursor()

    def process_frame(self, frame_bytes):
        frame = cv2.imdecode(np.frombuffer(frame_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        result = self.model.predict(frame)
        
        self.store_result_in_database(result)

    def store_result_in_database(self, result):
        # Example: Insert result into a PostgreSQL table
        sql = "INSERT INTO results (column1, column2) VALUES (%s, %s)"
        data = (result['column1_value'], result['column2_value'])
        self.cursor.execute(sql, data)
        self.db_conn.commit()

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'video_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['video_frames_topic'])

# Load pre-trained ML model
# model = YourModelClass()

frame_processor = FrameProcessor(model)

while True:
    msg = consumer.poll(timeout=1.0)

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    frame_bytes = msg.value()
    frame_processor.process_frame(frame_bytes)

consumer.close()
