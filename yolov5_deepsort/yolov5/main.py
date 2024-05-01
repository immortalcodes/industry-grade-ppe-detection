import cv2

def are_frames_equal(frame1, frame2):
    


    # Compare the resized frames pixel-wise
    difference = cv2.absdiff(frame1, frame2)
    # Compute the mean pixel value of the difference image
    mean_difference = cv2.mean(difference)[0]

    # Define a threshold for mean pixel difference
    threshold = 1.0  # Adjust this threshold based on your requirements

    # Return True if the mean difference is below the threshold, indicating frames are equal
    return mean_difference < threshold

# Initialize video capture from camera or video file
cap = cv2.VideoCapture(0)  # Change 0 to the video file path if using a file

# Initialize previous frame
prev_frame = None

while True:
    # Read frame from the video capture
    ret, frame = cap.read()
    print(frame.shape)

    # If frame reading was successful
    if ret:
        # Convert frame to grayscale for comparison
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # If there is no previous frame or the current frame is different from the previous frame
        if prev_frame is None or not are_frames_equal(gray_frame, prev_frame):
            # Process the frame here (e.g., perform object detection, face tracking, etc.)
            # Your processing code goes here

            # Display the processed frame
            cv2.imshow('Processed Frame', frame)

        # Update the previous frame
        prev_frame = gray_frame.copy()

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
