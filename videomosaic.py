import numpy as np
import cv2

# List of paths to the videos
# The following lines were for using .m3u8 video paths, uncomment and modify as needed
# base = ""
# video_paths = ['.m3u8', '.m3u8', '.m3u8', '.m3u8', '.m3u8', '.m3u8']
# video_files = [f'https://{base}/{path}' for path in video_paths]

# Using local .mkv video files instead
video_files = ['video1.mkv', 'video2.mkv', 'video3.mkv', 'video4.mkv', 'video5.mkv', 'video6.mkv']

captures = [cv2.VideoCapture(video) for video in video_files]

for i, cap in enumerate(captures):
    if not cap.isOpened():
        print(f"Erreur : Impossible d'ouvrir la vidéo {video_files[i]}")

resize_width, resize_height = 640, 400

fullscreen = False
fullscreen_index = -1


def enhance_frame(frame):
    frame_filtered = cv2.bilateralFilter(frame, 5, 50, 50)
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    frame_sharpened = cv2.filter2D(frame_filtered, -1, sharpen_kernel)
    return frame_sharpened


def mouse_callback(event, x, y, flags, param):
    global fullscreen, fullscreen_index
    if event == cv2.EVENT_LBUTTONDOWN:
        if fullscreen:
            fullscreen = False
            fullscreen_index = -1
        else:
            col = x // resize_width
            row = y // resize_height
            index = row * 3 + col
            if index < len(video_files):
                fullscreen = True
                fullscreen_index = index


cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Result", resize_width * 3, resize_height * 2)
cv2.setMouseCallback("Result", mouse_callback)

while True:
    frames = []
    for cap in captures:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (resize_width, resize_height))
            #frame = enhance_frame(frame)
            frames.append(frame)
        else:
            frames.append(np.zeros((resize_height, resize_width, 3), dtype=np.uint8))

    if len(frames) == len(video_files):
        if fullscreen:
            full_frame = cv2.resize(frames[fullscreen_index], (resize_width * 4, resize_height * 4))
            cv2.imshow("Result", full_frame)
        else:
            s1 = np.hstack(frames[:3])
            s2 = np.hstack(frames[3:])
            s3 = np.vstack((s1, s2))
            cv2.imshow("Result", s3)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

for cap in captures:
    cap.release()

cv2.destroyAllWindows()
