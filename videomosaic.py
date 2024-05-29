import numpy as np
import cv2

# List of paths to the videos
# The following lines were for using .m3u8 video paths, uncomment and modify as needed
# base = ""
# video_paths = ['.m3u8', '.m3u8', '.m3u8', '.m3u8', '.m3u8', '.m3u8']
# video_files = [f'https://{base}/{path}' for path in video_paths]

# Using local .mkv video files instead
video_paths = ['video1.mkv', 'video2.mkv', 'video3.mkv', 'video4.mkv', 'video5.mkv', 'video6.mkv']

# Open video streams
captures = [cv2.VideoCapture(path) for path in video_paths]

# Check if captures are opened correctly
for i, cap in enumerate(captures):
    if not cap.isOpened():
        print(f"Error: Unable to open video {video_paths[i]}")

# Resizing dimensions
resize_width, resize_height = 640, 480

while True:
    frames = []
    for cap in captures:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (resize_width, resize_height))
            frames.append(frame)
        else:
            frames.append(np.zeros((resize_height, resize_width, 3), dtype=np.uint8))

    # Check if all videos have been read correctly
    if len(frames) == len(video_paths):
        # Merge the images
        s1 = np.hstack(frames[:3])
        s2 = np.hstack(frames[3:])
        s3 = np.vstack((s1, s2))

        cv2.imshow("Result", s3)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Release resources
for cap in captures:
    cap.release()

cv2.destroyAllWindows()
