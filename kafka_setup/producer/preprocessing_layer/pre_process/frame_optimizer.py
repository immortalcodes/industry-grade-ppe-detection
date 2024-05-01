import cv2
from confluent_kafka import Producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})

class FrameRateReducer:
    def __init__(self, threshold=50):
        self.threshold = threshold

    def reduce_frame_rate(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Cannot access webcam.")
            return

        fps = 30
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter("output_video.mp4", fourcc, fps, (frame_width, frame_height))

        ret, prev_frame = cap.read()
        if not ret:
            print("Error: Cannot read webcam.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if self._is_frame_different(prev_frame, frame):
                out.write(prev_frame)

            prev_frame = frame

        cap.release()
        out.release()
    def send_to_kafka(self, frame):
        processed_frame = self.reduce_frame_rate(frame)

        # Add metadata to the frame
        frame_with_metadata = self.add_metadata(processed_frame)

        # Convert frame to bytes
        frame_bytes = cv2.imencode('.jpg', frame_with_metadata)[1].tobytes()

        producer.produce('video_frames_topic', value=frame_bytes, timestamp=int(time.time()))
        producer.flush()

    def _is_frame_different(self, frame1, frame2):
        frame_diff = cv2.absdiff(frame1, frame2)
        diff_score = cv2.sumElems(frame_diff)[0]
        return diff_score > self.threshold

    def change_threshold(self, new_threshold):
        self.threshold = new_threshold

    def change_output_path(self, new_output_path):
        self.output_video_path = new_output_path

if __name__ == "__main__":
    reducer = FrameRateReducer(threshold=50)
    reducer.reduce_frame_rate()
