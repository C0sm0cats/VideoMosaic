# Video Mosaic Script

## Overview
This Python script, `videomosaic.py`, merges multiple video streams into a single visual mosaic. It utilizes OpenCV to read video files, resize frames, and merge them into a unified display.

## Functionality
1. **Video Input:** The script accepts input from multiple video files specified in the `video_paths` list.
2. **Video Capture:** It opens video streams using OpenCV's `VideoCapture` function for each specified video file.
3. **Error Handling:** The script checks if the video captures are opened correctly and prints an error message if not.
4. **Frame Resizing:** It resizes each frame to a standard size defined by `resize_width` and `resize_height`.
5. **Mosaic Creation:** The resized frames are then merged into a mosaic layout using numpy's stacking functions.
6. **Display:** The resulting mosaic is displayed in a window titled "Result" using OpenCV's `imshow` function.
7. **User Interaction:** The script waits for the user to press the 'q' key to exit the display window.
8. **Resource Cleanup:** Finally, it releases the resources by closing all video captures and destroying the display window.

## Usage
To use the script, simply specify the paths to your video files in the `video_paths` list and run the script using Python. Ensure you have the necessary libraries installed, including numpy and OpenCV.

### Grid and Fullscreen Display

- Videos are displayed in a resizable grid.
- Clicking on a video opens it in VLC.

## Example
Here's an example of how to run the script:
```bash
python videomosaic.py
```

## Dependencies

1. numpy
2. OpenCV (cv2)
3. subprocess

## Activity

![Alt](https://repobeats.axiom.co/api/embed/3f31f2010987926295c9bb997293de01707a3d78.svg "Repobeats analytics image")