import time
import cv2
import numpy as np
from ultralytics import YOLO
from flask import Flask, Response, request, jsonify, render_template
import threading

app = Flask(__name__)

latest_frame_bytes = None
processed_frame = None  
current_person_count = 0
last_boxes = []

model = YOLO("yolov8n.pt")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    global latest_frame_bytes
    if request.data:
        latest_frame_bytes = request.data
        return "OK", 200
    return "No Data", 400

@app.route("/person_count")
def person_count():
    return jsonify(count=int(current_person_count))

def yolo_worker():
    global latest_frame_bytes, current_person_count, last_boxes, processed_frame
    
    CONF = 0.25
    IMG_SIZE = 160 

    while True:
        if latest_frame_bytes is not None:
            nparr = np.frombuffer(latest_frame_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is not None:
                results = model(frame, verbose=False, imgsz=IMG_SIZE)[0]
                
                temp_boxes = []
                count = 0
                for box in results.boxes:
                    if int(box.cls[0]) == 0 and float(box.conf[0]) >= CONF:
                        count += 1
                        temp_boxes.append(box.xyxy[0].cpu().numpy().astype(int))
                
                current_person_count = count
                last_boxes = temp_boxes

                for (x1, y1, x2, y2) in last_boxes:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                cv2.putText(frame, f"Kisi: {current_person_count}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                processed_frame = buffer.tobytes()

        time.sleep(0.01) 

def generate_frames():
    global processed_frame
    while True:
        if processed_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + processed_frame + b'\r\n')
        else:
            time.sleep(0.1)

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")   

if __name__ == "__main__":
    t = threading.Thread(target=yolo_worker, daemon=True)
    t.start()
    
    app.run(host="0.0.0.0", port=8000, debug=False, threaded=True)