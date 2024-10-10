import numpy as np
import cv2
import subprocess

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

audio_process = None

def enhance_frame(frame):
    frame_filtered = cv2.bilateralFilter(frame, 5, 50, 50)
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    frame_sharpened = cv2.filter2D(frame_filtered, -1, sharpen_kernel)
    return frame_sharpened

def mouse_callback(event, x, y, flags, param):
    global fullscreen, fullscreen_index, audio_process
    if event == cv2.EVENT_LBUTTONDOWN:
        cols = min(3, len(valid_video_paths))
        col = x // resize_width
        row = y // resize_height
        index = row * cols + col
        if index < len(video_files):
            if audio_process:
                audio_process.terminate()
                audio_process.wait()

            audio_process = subprocess.Popen([
                'vlc',
                '--play-and-exit',
                '--no-fullscreen',
                '--video-x=100',
                '--video-y=100',
                '--width=800',
                '--height=600',
                video_files[index]
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

cv2.namedWindow("Result", cv2.WINDOW_NORMAL)

cols = min(3, len(valid_video_paths))
rows = (len(valid_video_paths) + 2) // 3
cv2.resizeWindow("Result", resize_width * cols, resize_height * rows)

cv2.setMouseCallback("Result", mouse_callback)

while True:
    frames = []
    for cap in captures:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (resize_width, resize_height))
            # frame = enhance_frame(frame)
            frames.append(frame)
        else:
            frames.append(np.zeros((resize_height, resize_width, 3), dtype=np.uint8))

    if len(frames) == len(video_files):
        rows = (len(frames) + 2) // 3
        stacked_frames = []

        for r in range(rows):
            row_frames = frames[r * 3:(r + 1) * 3]

            while len(row_frames) < 3:
                row_frames.append(np.zeros((resize_height, resize_width, 3), dtype=np.uint8))

            stacked_frames.append(np.hstack(row_frames))

        s3 = np.vstack(stacked_frames)
        cv2.imshow("Result", s3)

    key = cv2.waitKey(20)
    if key & 0xFF == ord('q'):
        break

    if cv2.getWindowProperty('Result', cv2.WND_PROP_VISIBLE) < 1:
        break

for cap in captures:
    cap.release()
if audio_process:
    audio_process.terminate()
    audio_process.wait()
cv2.destroyAllWindows()
