import cv2

def list_camera_ports():
    num_ports = 5  # Adjust this based on the number of ports to check.
    for i in range(num_ports):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            print(f"Port {i}: Closed")
        else:
            print(f"Port {i}: Opened")
            cap.release()

if __name__ == "__main__":
    list_camera_ports()
