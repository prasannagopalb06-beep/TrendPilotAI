import cv2
import os

def extract_frame(video_path, output_dir="uploads", frame_second=1):
    """
    Extract a frame from a video file.
    Returns path to the extracted image.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"VIDEO ERROR: Cannot open {video_path}")
            return None

        fps        = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_no   = int(fps * frame_second)
        total      = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # clamp to valid range
        frame_no = min(frame_no, max(0, total - 1))

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            print("VIDEO ERROR: Could not read frame")
            return None

        # save frame as jpg next to the video
        base       = os.path.splitext(os.path.basename(video_path))[0]
        frame_path = os.path.join(output_dir, f"{base}_frame.jpg")
        cv2.imwrite(frame_path, frame)
        print(f"VIDEO FRAME EXTRACTED: {frame_path}")
        return frame_path

    except Exception as e:
        print(f"VIDEO FRAME EXTRACT ERROR: {e}")
        return None


def is_video(path):
    ext = os.path.splitext(path)[1].lower()
    return ext in [".mp4", ".mov", ".avi", ".mkv", ".webm", ".3gp", ".flv"]


def get_analysis_image(file_path):
    """
    If file is a video, extract a frame and return frame path.
    If file is an image, return as-is.
    """
    if is_video(file_path):
        output_dir = os.path.dirname(file_path)
        frame_path = extract_frame(file_path, output_dir=output_dir)
        if frame_path:
            return frame_path
        print("VIDEO: Frame extraction failed — analysis will use defaults")
        return None
    return file_path
