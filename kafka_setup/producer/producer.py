import cv2
from confluent_kafka import Producer
from kafka_setup.producer.preprocessing_layer.pre_process import FrameRateReducer

# Create an instance of FrameRateReducer
reducer = FrameRateReducer(threshold=50)

# Capture video from front camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Display frame
    cv2.imshow('Frame', frame)
    
    # Send frame to Kafka after preprocessing and adding metadata
    reducer.send_to_kafka(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close Kafka producer
cap.release()
cv2.destroyAllWindows()