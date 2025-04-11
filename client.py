import socket
import time

HOST = '172.25.22.76'  # Replace with your Pi's IP
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to traffic light server.")

try:
    while True:
        cmd = input("Press ENTER to request pedestrian crossing, or type 'exit' to quit: ")
        if cmd.lower() == 'exit':
            break
        client_socket.sendall("pedestrian".encode())
        print("Request sent!")
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    print("Closing connection...")
    client_socket.close()