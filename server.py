import RPi.GPIO as GPIO
import socket
import time

# GPIO Setup
RED = 17
YELLOW = 27
GREEN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

# Network Setup
HOST = ''
PORT = 5001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Waiting for client...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

def traffic_cycle():
    print("Normal traffic cycle...")
    GPIO.output(RED, True)
    GPIO.output(YELLOW, False)
    GPIO.output(GREEN, False)
    time.sleep(3)
    
    GPIO.output(RED, False)
    GPIO.output(YELLOW, True)
    time.sleep(1)

    GPIO.output(YELLOW, False)
    GPIO.output(GREEN, True)
    time.sleep(3)

    GPIO.output(GREEN, False)

try:
    while True:
        conn.settimeout(0.1)
        try:
            data = conn.recv(1024).decode()
            if data.lower() == 'pedestrian':
                print("Pedestrian request received!")
                # Activate Pedestrian Crossing Phase
                GPIO.output(RED, True)
                GPIO.output(YELLOW, False)
                GPIO.output(GREEN, False)
                time.sleep(5)  # Crossing time
                continue
        except socket.timeout:
            pass

        traffic_cycle()
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    GPIO.cleanup()
    conn.close()
    server_socket.close()