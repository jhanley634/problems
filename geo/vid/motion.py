#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path

import cv2


def detect_motion(video_path):
    cap = cv2.VideoCapture(video_path)
    assert cap

    fgbg = cv2.createBackgroundSubtractorMOG2(
        history=500, varThreshold=50, detectShadows=True
    )

    motion_segments = []
    start_frame = None
    end_frame = None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply background subtraction
        fgmask = fgbg.apply(frame)

        # Threshold the mask to get a binary image
        _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                motion_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                # Draw bounding box around moving object
                cv2.rectangle(
                    frame, (x, y), (x + w, y + h), (0, 255, 0), 2
                )

        if motion_detected:
            if start_frame is None:
                start_frame = frame_count
            end_frame = frame_count

        # If motion was detected previously but is no longer detected, finalize the segment
        elif start_frame is not None:
            motion_segments.append((start_frame / fps, end_frame / fps))  # In seconds
            start_frame = None

        frame_count += 1
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return motion_segments


if __name__ == "__main__":
    desktop = Path("~/Desktop").expanduser()
    video_path = desktop / "video.mp4"
    segments = detect_motion(video_path)

    for start, end in segments:
        print(f"Motion detected from {start:.2f} to {end:.2f} seconds.")
