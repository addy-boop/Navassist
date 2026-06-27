from ultralytics import YOLO
import cv2
import pyttsx3
import time

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

last_speech_time = 0
speech_cooldown = 3

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_height, frame_width = frame.shape[:2]

    results = model(frame, conf=0.65)
    annotated_frame = results[0].plot()

    cv2.line(annotated_frame, (frame_width // 3, 0), (frame_width // 3, frame_height), (255, 255, 255), 2)
    cv2.line(annotated_frame, (2 * frame_width // 3, 0), (2 * frame_width // 3, frame_height), (255, 255, 255), 2)

    zone_risk = {"left": 0, "ahead": 0, "right": 0}

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            center_x = (x1 + x2) / 2

            if center_x < frame_width / 3:
                position = "left"
            elif center_x > 2 * frame_width / 3:
                position = "right"
            else:
                position = "ahead"

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

            risk = 0

            if position == "ahead":
                risk += 5
            else:
                risk += 2

            if distance == "very close":
                risk += 6
            elif distance == "close":
                risk += 4
            elif distance == "medium":
                risk += 2
            else:
                risk += 1

            if label in ["person", "car", "bus", "truck", "motorcycle", "bicycle"]:
                risk += 5
            elif label in ["chair", "bench", "suitcase", "backpack"]:
                risk += 3
            else:
                risk += 1

            zone_risk[position] += risk

            text = f"{label}: {position}, {distance}, risk {risk}"

            cv2.putText(
                annotated_frame,
                text,
                (x1, y1 + 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    safe_zone = min(zone_risk, key=zone_risk.get)

    if zone_risk["ahead"] < 5:
        instruction = "Path clear ahead"
    elif safe_zone == "left":
        instruction = "Obstacle ahead. Move slightly left"
    elif safe_zone == "right":
        instruction = "Obstacle ahead. Move slightly right"
    else:
        instruction = "Stop. Obstacle ahead"

    current_time = time.time()

    if current_time - last_speech_time > speech_cooldown:
        engine.say(instruction)
        engine.runAndWait()
        last_speech_time = current_time

    cv2.putText(
        annotated_frame,
        instruction,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    print("Zone Risk:", zone_risk)
    print("Instruction:", instruction)

    cv2.imshow("YOLOv8 Detection", annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
