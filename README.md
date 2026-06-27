🕶️ NavAssist

<p align="center"> <b>AI-powered assistive navigation for visually impaired individuals.</b><br> Helping users navigate safely through real-time computer vision and contextual audio guidance. </p>

🚀 Overview

NavAssist is an AI-powered assistive navigation system designed to improve independent mobility for visually impaired individuals.

Using computer vision, the system analyses a user's surroundings in real time, detects nearby obstacles, identifies the safest walking direction, and delivers intuitive voice guidance.

Unlike traditional obstacle detection systems, NavAssist interprets the environment to recommend safe navigation decisions rather than simply announcing detected objects.

🎯 Key Features

✅ Real-time obstacle detection using YOLOv8

✅ Spatial scene understanding (Left • Ahead • Right)

✅ Risk assessment based on object position and proximity

✅ Intelligent safe-path recommendation

✅ Context-aware voice guidance

✅ Works with webcam and recorded video

🖥️ Example Navigation Instructions
✓ Path clear ahead

⚠ Chair ahead. Move left.

⚠ Person ahead. Move right.

⛔ Stop. Obstacle directly ahead.
🏗️ System Architecture
Camera Input
      │
      ▼
YOLOv8 Object Detection
      │
      ▼
Spatial Zone Classification
      │
      ▼
Risk Assessment Engine
      │
      ▼
Navigation Decision Logic
      │
      ▼
Voice Guidance
⚙️ Technology Stack
Component	Technology
Programming Language	Python
Computer Vision	OpenCV
Object Detection	YOLOv8 (Ultralytics)
AI	Deep Learning
Speech	pyttsx3
Video Processing	OpenCV
📈 Current Progress
✅ Functional computer vision prototype
✅ Real-time navigation guidance
✅ Context-aware audio feedback
✅ Pilot testing with visually impaired participants
🚧 Mobile application integration
🚧 Smart glasses deployment
🔬 Future Development
GPS-assisted navigation
Indoor localisation
Custom object detection model for accessibility
Haptic feedback
Dedicated smart glasses hardware
Cloud-based route planning
📂 Repository Structure
NavAssist
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── assets/
│     ├── logo.png
│     ├── architecture.png
│     ├── demo.gif
│     └── screenshot.png
│
├── demo/
│     └── prototype.mp4
📹 Demonstration

A demonstration video showcasing obstacle detection and real-time navigation guidance will be added here.

📜 Disclaimer

NavAssist is currently an early-stage research prototype developed for pilot testing and user validation. It is not intended to replace certified mobility aids or professional mobility training.
