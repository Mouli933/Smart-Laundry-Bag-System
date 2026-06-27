# Smart-Laundry-Bag-System
# 👕 Smart Laundry Management System using RFID and MediaPipe

A Smart Laundry Management System developed using **ESP8266**, **RC522 RFID Reader**, **Python**, **MediaPipe Pose Detection**, **OpenCV**, and **Google Drive Cloud Storage**.

The system authenticates users using RFID cards, detects the rack level and storage box using computer vision, records the complete placement process, and automatically uploads the recorded video along with metadata to Google Drive.

This project combines **Embedded Systems**, **Computer Vision**, **IoT**, and **Cloud Storage** to automate laundry rack management.

---

# 🚀 Features

- RFID-based User Authentication
- ESP8266 + RC522 Integration
- Automatic Webcam Recording
- MediaPipe Pose Detection
- Right Wrist Tracking
- Rack Level Detection
- Storage Box Detection
- Wrist Coordinate Smoothing
- Stable Detection using Frame Confirmation
- Automatic Video Recording
- Metadata Generation
- Automatic Google Drive Upload
- Unauthorized RFID Detection
- Real-Time Processing

---

# 🛠 Technologies Used

## Hardware

- ESP8266 NodeMCU
- RC522 RFID Reader
- RFID Cards
- USB Webcam

## Software

- Python
- OpenCV
- MediaPipe
- PySerial
- PyDrive2
- Google Drive API

---


---

# 🎯 Rack Detection Logic

The webcam frame is divided into:

### Horizontal Zones

- Top Rack
- Middle Rack
- Bottom Rack

### Vertical Zones

- Left Box
- Center Box
- Right Box

The detected wrist coordinates determine:

- Rack Level
- Storage Box

To improve accuracy, coordinate smoothing and multi-frame confirmation are used before finalizing the detected rack location.

---

# ☁ Cloud Storage

After successful detection:

- Recorded video is uploaded to Google Drive.
- Metadata is saved as a JSON file.
- Video and metadata are linked using a timestamp.

Example Metadata:

```json
{
    "Tag_ID":"79 FC 77 5A",
    "Rack_Level":2,
    "Box_Number":1,
    "Timestamp":"20260627_103501",
    "Video_File":"rack_record_20260627_103501.mp4"
}
