import cv2
import numpy as np
import threading

class ArucoDetector:
    def __init__(self):
        # Set the dictionary and parameters for detecting ArUco markers
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_100)
        self.parameters = cv2.aruco.DetectorParameters()

        # Variable to store the current frame
        self.frame = None

        # Thread for detection
        self.detection_thread = threading.Thread(target=self.detect_markers_in_thread)
        self.detection_thread.daemon = True
        self.detection_thread.start()

    def update_frame(self, frame):
        """
        Updates the frame for detection.
        
        Args:
            frame: The frame to process for ArUco marker detection.
        """
        self.frame = frame

    def detect_markers_in_thread(self):
        """
        Thread function to detect ArUco markers in the current frame.
        This function continuously checks for new frames and processes them.
        """
        while True:
            if self.frame is not None:
                # Process the frame to detect ArUco markers
                processed_frame = self.detect_aruco_markers(self.frame.copy())

                # Show the processed frame with detection
                cv2.imshow("ArUco Detection", processed_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def detect_aruco_markers(self, frame):
        """
        Detects ArUco markers and draws them on the frame.

        Args:
            frame: The frame to detect markers in.

        Returns:
            The frame with detected markers and additional information.
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers in the frame
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

        # Get the center of the camera frame
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2

        # Draw a circle and a point at the center of the frame
        cv2.circle(frame, (frame_center_x, frame_center_y), 30, (255, 0, 0), 2)  # Circle
        cv2.circle(frame, (frame_center_x, frame_center_y), 5, (0, 255, 255), -1)  # Center point

        # If markers are detected
        if np.all(ids is not None):
            # Draw detected markers
            frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Calculate the center of the first detected marker
            for corner in corners:
                # Get the marker's corner points
                top_left, top_right, bottom_right, bottom_left = corner[0]

                # Calculate the center of the marker
                marker_center_x = int((top_left[0] + bottom_right[0]) / 2)
                marker_center_y = int((top_left[1] + bottom_right[1]) / 2)

                # Draw the center point of the marker
                cv2.circle(frame, (marker_center_x, marker_center_y), 5, (0, 255, 0), -1)

                # Move the camera to align the marker's center with the frame's center
                self.move_camera(frame_center_x - marker_center_x, frame_center_y - marker_center_y)

        return frame

    def move_camera(self, x_diff, y_diff):
        """
        Controls camera movement based on marker position.

        Args:
            x_diff: Difference between the center of the frame and the marker on the x-axis.
            y_diff: Difference between the center of the frame and the marker on the y-axis.
        """
        if abs(x_diff) > 10:
            if x_diff > 0:
                print("Move camera left")
            else:
                print("Move camera right")

        if abs(y_diff) > 10:
            if y_diff > 0:
                print("Move camera up")
            else:
                print("Move camera down")
