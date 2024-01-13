import socket
import cv2
import pickle
import struct

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('IP', 12345)#Put the actual address of the serve in 'IP'
    client_socket.connect(server_address)
    print(f"Connected to {server_address}")

    # Open a window to display the received video
    cv2.namedWindow("Client Video")

    try:
        while True:
            # Receive the frame size from the server
            message_size = client_socket.recv(struct.calcsize("L"))
            if not message_size:
                break

            message_size = struct.unpack("L", message_size)[0]

            # Receive the frame data from the server
            data = b""
            while len(data) < message_size:
                packet = client_socket.recv(message_size - len(data))
                if not packet:
                    break
                data += packet

            # Deserialize the frame
            frame = pickle.loads(data)

            # Display the received frame
            cv2.imshow("Client Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Clean up the connection and close the window
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_client()
