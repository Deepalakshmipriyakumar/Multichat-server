import csv
from db_confi import get_connection 

def export_to_csv():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()

    with open("chat_history.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["message_id", "sender", "message", "timestamp"])
        writer.writerows(rows)

    conn.close()
    print("✅ Exported to chat_history.csv")

def show_messages():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]} | Sender: {row[1]} | Message: {row[2]} | Time: {row[3]}")

    conn.close()

def add_message(sender, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, message) VALUES (%s, %s)", (sender, message))
    conn.commit()
    conn.close()
    print("✅ Message added.")

def update_message(msg_id, new_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE messages SET message = %s WHERE message_id = %s", (new_text, msg_id))
    conn.commit()
    conn.close()
    print(f"✅ Message ID {msg_id} updated.")

def delete_message(msg_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE message_id = %s", (msg_id,))
    conn.commit()
    conn.close()
    print(f"🗑️ Message ID {msg_id} deleted.")
