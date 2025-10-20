import socket
import logging
from contextlib import closing

# ------------------------------
# Configuration
# ------------------------------
HOST = "127.0.0.1"  # Loopback interface (localhost)
PORT = 8080          # Listening port

# ------------------------------
# Setup Logging
# ------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)

# ------------------------------
# TCP Echo Server
# ------------------------------
def start_server(host: str = HOST, port: int = PORT) -> None:
    """Start a simple, robust TCP echo server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Security & stability settings
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Queue up to 5 pending connections

        logging.info(f"Server listening on {host}:{port}")

        try:
            while True:
                conn, addr = server_socket.accept()
                with closing(conn):
                    logging.info(f"Connection established from {addr}")
                    handle_client(conn, addr)

        except KeyboardInterrupt:
            logging.info("Server shutdown initiated (Ctrl+C).")
        except Exception as e:
            logging.exception(f"Unexpected server error: {e}")
        finally:
            logging.info("Server socket closed.")

# ------------------------------
# Client Handler
# ------------------------------
def handle_client(conn: socket.socket, addr: tuple) -> None:
    """Handle communication with a connected client."""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                logging.info(f"Client {addr} disconnected.")
                break

            # Echo back the received data
            conn.sendall(data)

    except ConnectionResetError:
        logging.warning(f"Connection reset by {addr}.")
    except Exception as e:
        logging.exception(f"Error handling client {addr}: {e}")

# ------------------------------
# Entry Point
# ------------------------------
if __name__ == "__main__":
    start_server()
