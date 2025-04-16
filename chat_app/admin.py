import crud

def admin_menu():
    while True:
        print("\n📋 Admin Menu")
        print("1. View Messages")
        print("2. Add Message")
        print("3. Update Message")
        print("4. Delete Message")
        print("5. Export as CSV")
        print("0. Exit")

        choice = input("Enter option: ")

        if choice == "1":
            crud.show_messages()

        elif choice == "2":
            sender = input("Sender: ")
            message = input("Message: ")
            crud.add_message(sender, message)  # ✅ Added back the function call

        elif choice == "3":
            msg_id = int(input("Message ID: "))
            new_text = input("New message: ")
            crud.update_message(msg_id, new_text)

        elif choice == "4":
            msg_id = int(input("Message ID to delete: "))
            crud.delete_message(msg_id)

        elif choice == "5":
            crud.export_to_csv()

        elif choice == "0":
            break

        else:
            print("Invalid option.")

def login():
    admin_user = "admin"
    admin_pass = "admin123"

    username = input("Username: ")
    password = input("Password: ")

    if username == admin_user and password == admin_pass:
        print("✅ Login successful.")
        admin_menu()
    else:
        print("❌ Invalid credentials.")

if __name__ == "__main__":
    login()

