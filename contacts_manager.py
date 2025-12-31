import json   #used to save and load contacts in a JSON file
import re     #used for regular expressions (phone & email validation)  
import csv    #used to export contacts into a CSV file
from datetime import datetime, timedelta #used to store created/updated time
import os

DATA_FILE = "contacts_data.json"  #Stores all contact data permanently and Acts like a small database

# ================== VALIDATION ==================

def validate_phone(phone):  #Takes phone number as input &  Removes all non-digit characters
    digits = re.sub(r"\D", "", phone)  #Keeps only numbers (removes +, -, spaces)
    if 10 <= len(digits) <= 15: #Validates phone length & Returns cleaned number
        return True, digits #Returns invalid if length is wrong
    return False, None #Returns invalid if length is wrong

def validate_email(email): #Checks email format
    if email == "": #Allows empty email (optional field)
        return True 
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" #Regex pattern for valid email
    return re.match(pattern, email) is not None #Returns True if email matches pattern

# ================== FILE HANDLING ==================

def load_contacts(): #Loads contacts from JSON file
    if not os.path.exists(DATA_FILE): #Checks if file exists
        print("\n No existing contacts file found. Starting fresh.") #Starts with empty dictionary
        return {} 
    with open(DATA_FILE, "r") as f: 
        return json.load(f) #Loads saved contacts

def save_contacts(contacts): #Saves dictionary to JSON file
    with open(DATA_FILE, "w") as f: 
        json.dump(contacts, f, indent=4) 
    print(" Contacts saved to contacts_data.json")#Saves data in readable format

# ================== CORE FEATURES ==================

def add_contact(contacts): #Adds a new contact
    print("\n--- ADD NEW CONTACT ---")

    name = input("Enter contact name: ").strip() #Gets contact name
    if name in contacts: #Prevents duplicate contacts
        print("Contact already exists!") 
        return

    while True:
        phone = input("Enter phone number: ") #Takes phone input
        valid, phone_clean = validate_phone(phone) #Check number its valid or not
        if valid: # if incase vaild break the loop are not valid print invalid phone number
            break
        print("Invalid phone number!")

    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip() #take email input
        if validate_email(email): #check email is it corect formate or not else invaild
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip() #Stores address
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other" #store group

    now = datetime.now().isoformat()

    contacts[name] = { # defined dictionary key value pairs
        "phone": phone_clean,
        "email": email if email else None,
        "address": address if address else None,
        "group": group,
        "created_at": now,
        "updated_at": now
    }

    print(f" Contact '{name}' added successfully!")
    save_contacts(contacts)

def search_contact(contacts): #Searches by name
    term = input("Enter name to search: ").lower() #Case-insensitive search
    results = {k: v for k, v in contacts.items() if term in k.lower()} #Uses dictionary comprehension 

    if not results: #Updates modification time
        print(" No contacts found.")
        return

    print(f"\nFound {len(results)} contact(s):")
    print("-" * 50)

    for i, (name, info) in enumerate(results.items(), 1):
        print(f"{i}. {name}")
        print(f"   Phone: {info['phone']}")
        if info["email"]:
            print(f"    Email: {info['email']}")
        if info["address"]:
            print(f"   Address: {info['address']}")
        print(f"    Group: {info['group']}")
        print()

def update_contact(contacts): #delete contact info 
    name = input("Enter contact name to update: ").strip()
    if name not in contacts:
        print("Contact not found.")
        return

    contact = contacts[name]

    phone = input(f"Enter new phone ({contact['phone']}): ").strip()
    if phone:
        valid, phone_clean = validate_phone(phone)
        if valid:
            contact["phone"] = phone_clean

    email = input(f"Enter new email ({contact['email']}): ").strip()
    if email and validate_email(email):
        contact["email"] = email

    address = input("Enter new address: ").strip() #enter address as input
    if address:
        contact["address"] = address

    group = input("Enter new group: ").strip() #enter group as inpuut
    if group:
        contact["group"] = group

    contact["updated_at"] = datetime.now().isoformat() #update contact info
    print("Contact updated successfully!")
    save_contacts(contacts)

def delete_contact(contacts): #delete contact info
    name = input("Enter contact name to delete: ").strip()
    if name not in contacts:
        print(" Contact not found.")
        return

    del contacts[name]
    print(" Contact deleted successfully!")
    save_contacts(contacts)

def view_all_contacts(contacts): # define view all contacts
    if not contacts:
        print(" No contacts available.")
        return

    print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
    print("=" * 60)

    for name, info in contacts.items():
        print(f" {name}")
        print(f"    {info['phone']}")
        if info["email"]:
            print(f"   {info['email']}")
        print(f"    {info['group']}")
        print("-" * 40)

def export_to_csv(contacts):
    with open("contacts_export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])
        for name, info in contacts.items():
            writer.writerow([
                name,
                info["phone"],
                info["email"],
                info["address"],
                info["group"]
            ])
    print("Contacts exported to contacts_export.csv")

def view_statistics(contacts):
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {len(contacts)}\n")

    groups = {}
    for info in contacts.values():
        groups[info["group"]] = groups.get(info["group"], 0) + 1

    print("Contacts by Group:")
    for g, c in groups.items():
        print(f"  {g}: {c} contact(s)")

    recent = 0
    last_week = datetime.now() - timedelta(days=7)
    for info in contacts.values():
        if datetime.fromisoformat(info["updated_at"]) >= last_week:
            recent += 1

    print(f"\nRecently Updated (last 7 days): {recent}")

# ================== MAIN MENU ==================

def main(): # called functions
    print("=" * 50)
    print("      CONTACT MANAGEMENT SYSTEM")
    print("=" * 50)

    contacts = load_contacts()

    while True:
        print("\n==============================")
        print("          MAIN MENU")
        print("==============================")
        print("1. Add New Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. Export to CSV")
        print("7. View Statistics")
        print("8. Exit")
        print("==============================")

        choice = input("Enter your choice (1-8): ") #else_if statements

        if choice == "1":
            add_contact(contacts) #add contact 
        elif choice == "2":
            search_contact(contacts) #check contact in the dictionary
        elif choice == "3":
            update_contact(contacts) # if u can update the contact give choice 3
        elif choice == "4":
            delete_contact(contacts) #delete the contact in the dictionary
        elif choice == "5":
            view_all_contacts(contacts) #view all the contact dictionary
        elif choice == "6":
            export_to_csv(contacts) # export to csv file
        elif choice == "7":
            view_statistics(contacts) #view statisics dictionary
        elif choice == "8":
            save_contacts(contacts)
            print("\n" + "=" * 50)
            print("Thank you for using Contact Management System!")
            print("=" * 50)
            break
        else:
            print("Invalid choice! Try again.")

# ================== START PROGRAM ==================
main()
