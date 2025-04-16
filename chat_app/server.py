import socket
import threading
from db_confi import get_connection  # Your DB connection file

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

clients = []
names = []

# ✅ Save each message to MySQL
def save_message(sender, message):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO messages (sender, message) VALUES (%s, %s)"
        cursor.execute(query, (sender, message))
        conn.commit()
        print(f"💾 Saved to DB: {sender} -> {message}")
    except Exception as e:
        print("❌ DB Error:", e)
    finally:
        conn.close()

# ✅ Send a message to all clients
def broadcast(msg):
    for client in clients:
        try:
            client.send(msg)
        except:
            pass  # Ignore broken clients

# ✅ Handle one client connection
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break

            sender_index = clients.index(client)
            sender_name = names[sender_index]
            decoded = message.decode('utf-8').strip()

            # Remove redundant "name: " prefix
            if decoded.startswith(f"{sender_name}: "):
                actual_msg = decoded[len(sender_name) + 2:]
            else:
                actual_msg = decoded

            save_message(sender_name, actual_msg)
            broadcast(f"{sender_name}: {actual_msg}".encode('utf-8'))

        except Exception as e:
            print("⚠️ Client error:", e)
            break

    # Clean up on disconnect
    index = clients.index(client)
    name = names[index]
    clients.remove(client)
    names.remove(name)
    client.close()
    broadcast(f"❌ {name} left the chat.".encode('utf-8'))
    print(f"👋 {name} disconnected")

# ✅ Accept incoming connections
def receive():
    print(f"🚀 Server is running on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        print(f"✅ Connected with {addr}")

        client.send("NAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        print(f"🎉 Name: {name}")
        broadcast(f"👤 {name} joined the chat!".encode('utf-8'))
        client.send("✅ You are connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()

