import os
import cv2
import base64
import time
from gradio_client import Client
from pprint import pprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ROBOT_ID = os.environ.get("ROBOT_ID")
HF_TOKEN = os.environ.get("HF_CV_ROBOT_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found. Check your .env file.")

HF_SPACE = "OppaAI/Robot_MCP"   # HF Space name
API_NAME = "/predict"

def start_stream():
    client = Client(HF_SPACE)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not opened.")
        return

    print("Camera streaming... press Ctrl+C to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # JPEG encode
        ok, jpeg = cv2.imencode(".jpg", frame)
        if not ok:
            continue

        # Base64
        b64_img = base64.b64encode(jpeg.tobytes()).decode("utf-8")

        # JSON payload for HF Space
        payload = {
            "image_b64": b64_img,
            "robot_id": ROBOT_ID,
            "timestamp": time.time(),
            "hf_token": HF_TOKEN
        }

        # Send to HF
        try:
            resp = client.predict(
                payload,
                api_name=API_NAME
            )

            # Pretty-print key info neatly
            print("\n--- HF Response ---")
            print(f"Robot ID       : {resp.get('robot_id', 'N/A')}")
            print(f"Saved to HF Hub: {resp.get('saved_to_hf_hub', False)}")
            print(f"Repo ID        : {resp.get('repo_id', 'N/A')}")
            print(f"Image Path     : {resp.get('path_in_repo', 'N/A')}")
            print(f"Image URL      : {resp.get('image_url', 'N/A')}")
            print(f"File Size      : {resp.get('file_size_bytes', 0)} bytes")
            print("VLM Description:")
            print(resp.get("vlm_description", "N/A"))
            print("------------------\n")

        except Exception as e:
            print("Error sending to HF:", e)

        # Show locally
        #cv2.imshow("Jetson Camera", frame)
        #if cv2.waitKey(1) == ord("q"):
        #    break

        time.sleep(0.5)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_stream()
