from ultralytics import YOLO
import cv2
import time
import os
import threading

def speak(text):
    os.system("killall say 2>/dev/null")
    os.system(f'say "{text}"')

# Load YOLO model
model = YOLO("yolov8n.pt")

# Webcam input
cap = cv2.VideoCapture("nav13.mp4")

frame_count = 0
last_results = None
last_speech_time = 0
speech_interval = 2


# Speech settings
last_speech_time = 0
speech_cooldown = 5  # seconds
last_instruction = ""

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    if not ret:
        break
    
    frame_count += 1

    frame_height, frame_width = frame.shape[:2]

    # Run YOLO detection
    if frame_count % 8 == 0:
     last_results = model(frame, conf=0.5,classes = [0,56, 57,24,39, 28] )

    if last_results is None:
     continue

    results = last_results

    # Draw YOLO annotations
    annotated_frame = results[0].plot()

    # Draw navigation zones
    cv2.line(
        annotated_frame,
        (frame_width // 3, 0),
        (frame_width // 3, frame_height),
        (255, 255, 255),
        2
    )

    cv2.line(
        annotated_frame,
        (2 * frame_width // 3, 0),
        (2 * frame_width // 3, frame_height),
        (255, 255, 255),
        2
    )

    # Risk score for each zone
    zone_risk = {
        "left": 0,
        "ahead": 0,
        "right": 0
    }

    # Main object directly ahead
    main_obstacle = None
    main_distance = None
    highest_ahead_risk = 0

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            center_x = (x1 + x2) / 2

            # Decide object position
            if center_x < frame_width / 3:
                position = "left"
            elif center_x > 2 * frame_width / 3:
                position = "right"
            else:
                position = "ahead"

            # Approximate distance using bounding box size
            box_height = y2 - y1
            relative_size = box_height / frame_height

            if relative_size > 0.6:
                distance = "very close"
            elif relative_size > 0.35:
                distance = "close"
            elif relative_size > 0.18:
                distance = "medium"
            else:
                distance = "far"

            # Risk scoring
            risk = 0

            # Position weighting
            if position == "ahead":
                risk += 5
            else:
                risk += 2

            # Distance weighting
            if distance == "very close":
                risk += 6
            elif distance == "close":
                risk += 4
            elif distance == "medium":
                risk += 2
            else:
                risk += 1

            # Object weighting
            if label in ["person", "car", "bus", "truck", "motorcycle", "bicycle"]:
                risk += 5
            elif label in ["chair", "bench", "suitcase", "backpack"]:
                risk += 3
            else:
                risk += 1

            zone_risk[position] += risk

            # Only store the most risky object directly ahead
            if position == "ahead" and risk > highest_ahead_risk:
                highest_ahead_risk = risk
                main_obstacle = label
                main_distance = distance

            # Display detection text
            text = f"{label}: {position}, {distance}, risk {risk}"

            cv2.putText(
                annotated_frame,
                text,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # Choose safest zone
    safe_zone = min(zone_risk, key=zone_risk.get)

    # Generate spoken instruction
    if zone_risk["ahead"] < 5:
        instruction = "Continue Straight"

    elif main_obstacle is not None:
        if safe_zone == "left":
            instruction = f"{main_obstacle} ahead. Move left"
        elif safe_zone == "right":
            instruction = f"{main_obstacle} ahead. Move right"
        else:
            instruction = f"Stop. {main_obstacle} ahead"

    else:
        instruction = "Obstacle ahead"

    # Speak instruction using macOS say
    current_time = time.time()

    if current_time - last_speech_time >= speech_interval:

      threading.Thread(
        target=speak,
        args=(instruction,),
        daemon=True
     ).start()
      last_speech_time = current_time

    # Display instruction on screen
    cv2.putText(
        annotated_frame,
        instruction,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    # Debug output
    print("Zone Risk:", zone_risk)
    print("Main Obstacle:", main_obstacle)
    print("Instruction:", instruction)

    cv2.imshow("NavAssist Prototype", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
