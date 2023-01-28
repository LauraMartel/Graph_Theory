# This code creates a database from the input dictionary in the file
# network_data. Add or delete users and create connections between them

from network_data import network
import sqlite3
import tkinter as tk
from tkinter import ttk

# Create a new window
root = tk.Tk()
root.title("Contacts")

def create_db(contacts_dict):
    # Connect to the database file
    conn = sqlite3.connect('network.db')
    c = conn.cursor()

    # Create a table called 'contacts' with the appropriate columns
    c.execute('''CREATE TABLE contacts
                 (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, liked_activities TEXT, disliked_activities TEXT, location TEXT)''')

    # Iterate through the dictionary and insert the data into the table
    for key, value in contacts_dict.items():
        c.execute("INSERT INTO contacts VALUES (?,?,?,?,?,?,?)", (key, value[0], value[1], value[2], ','.join(value[3]), ','.join(value[4]), value[5]))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return contacts_dict


def add_to_db():
    # Create a new window
    add_window = tk.Tk()
    add_window.title("Add Contact")
    # Create labels and entry widgets for the contact information
    labels_text = ["ID:", "First Name:", "Last Name:", "Age:", "Liked activities:", "Disliked activities:", "Location:"]
    entries = [tk.Entry(add_window) for i in range(len(labels_text))]

    for i, label_text in enumerate(labels_text):
        label = tk.Label(add_window, text=label_text)
        label.grid(row=i, column=0)
        entries[i].grid(row=i, column=1)

    #create a button to add the contact to the database
    add_button = tk.Button(add_window, text="Add",
                           command=lambda: add_to_db_helper(add_window, entries[0].get(), entries[1].get(),
                                                            entries[2].get(), entries[3].get(), entries[4].get(),
                                                            entries[5].get(), entries[6].get()))
    add_button.grid(row=7, column=1)

    #start the mainloop
    add_window.mainloop()


def add_to_db_helper(add_window, id, first_name, last_name, age, liked_activities, disliked_activities, location):
    # Connect to the database
    conn = sqlite3.connect('network.db')
    c = conn.cursor()
    # Insert the new contact into the database
    c.execute("INSERT INTO contacts VALUES (?,?,?,?,?,?,?)", (id, first_name, last_name, age, liked_activities, disliked_activities, location))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    show_contacts()
    add_window.destroy()


def delete_from_db():
    # Create a new window
    delete_window = tk.Tk()
    delete_window.title("Delete Contact")

    # Create a label and entry widget for the primary key
    id_label = tk.Label(delete_window, text="ID:")
    id_label.grid(row=0, column=0)
    id_entry = tk.Entry(delete_window)
    id_entry.grid(row=0, column=1)

    # Create a button to delete the contact from the database
    delete_button = tk.Button(delete_window, text="Delete", command=lambda: delete_from_db_helper(delete_window, id_entry.get()))
    delete_button.grid(row=1, column=1)

    # Start the mainloop
    delete_window.mainloop()

def delete_from_db_helper(delete_window, id_entry):
    # Connect to the database file
    conn = sqlite3.connect('network.db')
    c = conn.cursor()

    # Delete the data from the table
    try:
        c.execute("DELETE FROM contacts WHERE id = ?", (id_entry,))
    except sqlite3.Error as e:
        print(f"Error Occured: {e}")
        print("This key is not present in the database and can't be deleted")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    show_contacts()
    delete_window.destroy()



def show_contacts():
    # Connect to the database
    conn = sqlite3.connect('network.db')
    c = conn.cursor()

    # Fetch all the contacts from the database
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()

    # Create a treeview to display the contacts
    tree = ttk.Treeview(root, columns=("id", "first_name", "last_name", "age", "liked activities", "disliked activities", "location"))
    headings = ["id", "first_name", "last_name", "age", "liked activities", "disliked activities", "location"]

    # Assign headings and columns to the treeview
    for i, heading in enumerate(headings, 1):
        tree.heading("#{}".format(i), text=heading)
        tree.column("#{}".format(i), stretch=tk.YES)

    # Insert the contacts into the treeview
    for contact in contacts:
        tree.insert("", "end", values=(contact[0], contact[1], contact[2], contact[3], contact[4], contact[5], contact[6]))

    # Create a button to add a new contact
    add_button = tk.Button(root, text="Add Contact", command=add_to_db)
    add_button.pack()

    # Create a button to delete a contact
    delete_button = tk.Button(root, text="Delete Contact", command=delete_from_db)
    delete_button.pack()

    # Pack the treeview and start the main loop
    tree.pack(expand=True, fill='both')



def create_connections():
    # Connect to the database file
    conn = sqlite3.connect('network.db')
    c = conn.cursor()

    # Create a table called 'connections'
    c.execute('''CREATE TABLE connections
                 (id_1 INTEGER, id_2 INTEGER)''')


    # Get all the contacts from the database
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()

    # Iterate through the contacts and check for connections
    for contact in contacts:
        # Get all contacts with the same location and activities
        query = "SELECT * FROM contacts WHERE location = ? AND liked_activities LIKE ?"
        c.execute(query, (contact[6], '%' + contact[4] + '%'))
        connections = c.fetchall()


        # Iterate through the connections and create the connections
        for connection in connections:
            if contact[0] != connection[0]:
                c.execute("INSERT INTO connections VALUES (?,?)", (contact[0], connection[0]))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

root.mainloop()

# -----------------Create the database and connections
# contacts_dict = network
# contacts_dict = create_db(contacts_dict)
# create_connections()

# ----------------Add New data to the database
# new_data = {220: ('Jack', 'Sparrow', 35, ['sailing', 'treasure hunting'], ['working'], 'Los Angeles')}
# contacts_dict = add_to_db(network, new_data)

# ---------------create a list of keys to be deleted
# delete_keys = [217, 220]
# #delete the keys from the database
# contacts_dict = delete_from_db(delete_keys)


# Display your database
show_contacts()
