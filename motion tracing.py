import cv2
import numpy as np

# Initialize a list to store points selected by the user
points = []

# Mouse callback function to select points for ROI
def select_points(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Draw a small circle on the selected point
        cv2.imshow("Select Points", image)

# Function to select ROI and perform motion tracking
def motion_tracking(video_path):
    global points
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    ret, first_frame = cap.read()

    if not ret:
        print("Error: Couldn't read the video.")
        return

    # Convert the first frame to grayscale
    first_frame_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    # Show the first frame and let the user select points for the ROI
    global image
    image = first_frame.copy()
    cv2.imshow("Select Points", image)
    cv2.setMouseCallback("Select Points", select_points)

    print("Click to select points around the object. Press 'Enter' when done.")
    cv2.waitKey(0)
    cv2.destroyWindow("Select Points")

    # Check if enough points are selected to create a polygon
    if len(points) < 3:
        print("Error: Need at least 3 points to create a polygon.")
        return

    # Convert points to a numpy array and create a mask
    points_np = np.array(points, dtype=np.int32)
    mask = np.zeros_like(first_frame_gray)  # Create a mask the same size as the frame
    cv2.fillPoly(mask, [points_np], 255)  # Fill the polygon defined by the points

    # Detect features to track inside the mask (within the polygon)
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    p0 = cv2.goodFeaturesToTrack(first_frame_gray, mask=mask, **feature_params)

    if p0 is None:
        print("Error: No features found in the selected region.")
        return

    # Parameters for Lucas-Kanade optical flow
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Create a mask for drawing motion paths
    draw_mask = np.zeros_like(first_frame)

    # Loop through the video frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the current frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow to track the features across frames
        p1, st, err = cv2.calcOpticalFlowPyrLK(first_frame_gray, frame_gray, p0, None, **lk_params)

        # Select good points (those that are successfully tracked)
        if p1 is not None and st is not None:
            good_new = p1[st == 1]
            good_old = p0[st == 1]

            # Draw the motion paths and the current feature points
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                draw_mask = cv2.line(draw_mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
                frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)

            # Overlay the mask on the current frame
            output_frame = cv2.add(frame, draw_mask)

            # Display the frame with tracking paths
            cv2.imshow('Motion Tracking', output_frame)

            # Update the previous frame and points
            first_frame_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break

    # Release the video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

# Path to the video file
video_path = "C:/Users/shyam/Videos/Screen Recordings/Screen Recording 2024-06-21 010606.mp4"  # Replace with your video file path

# Run the motion tracking function
motion_tracking(video_path)
