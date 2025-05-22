from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import pymysql
import csv
from datetime import datetime
import numpy as np
import uuid

window = tkinter.Tk()
window.title("Airport Management System")
my_tree = ttk.Treeview(window, show='headings', height=20)
window.geometry("720x640")
style = ttk.Style()

placeholderArray = ['' for _ in range(5)]

def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='snxhx*472',
        db='sneha'
    )
    return conn

def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.connection.ping()
    sql = "SELECT * FROM Crew"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    fetched_data = read()
    for array in fetched_data:
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.pack()


def updateRow():
    selected_item = my_tree.focus()
    item_data = my_tree.item(selected_item)['values']
    if item_data:
        pilot_name = idEntry.get()
        flight_attn_name = fnameEntry.get()
        flight_num = lnameEntry.get()
        airlines = flightEntry.get()

        conn = connection()
        cursor = conn.cursor()
        cursor.connection.ping()
        sql = "UPDATE Crew SET pilotName=%s, flightAttnName=%s, flightNum=%s, airlines=%s WHERE flightNum=%s"
        cursor.execute(sql, (pilot_name, flight_attn_name, flight_num, airlines, item_data[2]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Update", "Row updated successfully!")
        refreshTable()
    else:
        messagebox.showerror("Error", "Please select a row to update.")


def deleteRow():
    selected_item = my_tree.focus()
    item_data = my_tree.item(selected_item)['values']
    if item_data:
        flight_num = item_data[2]  # Retrieve flight number from item_data
        conn = connection()
        cursor = conn.cursor()
        cursor.connection.ping()
        sql_crew = "DELETE FROM Crew WHERE flightNum = %s"
        cursor.execute(sql_crew, (flight_num,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Delete", "Row deleted successfully!")
        refreshTable()
    else:
        messagebox.showerror("Error", "Please select a row to delete.")


def addRow():   
    pilotName = idEntry.get()
    flightAttnName = fnameEntry.get()
    flightNum = lnameEntry.get()
    airlines = flightEntry.get()
   
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Flight WHERE flightNum = %s", (flightNum,))
    flight_exists = cursor.fetchone() is not None
    conn.close()

    if flight_exists:
        conn = connection()
        cursor = conn.cursor()
        cursor.connection.ping()
        sql = "INSERT INTO Crew (pilotName, flightAttnName, flightNum, airlines) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (pilotName, flightAttnName, flightNum, airlines))
        conn.commit()
        conn.close()
        messagebox.showinfo("Add", "Row added successfully!")
        refreshTable()
    else:
        
        conn = connection()
        cursor = conn.cursor()
        cursor.connection.ping()
        sql_flight = "INSERT INTO Flight (flightNum, airlines) VALUES (%s, %s)"
        cursor.execute(sql_flight, (flightNum, airlines))
        conn.commit()
        conn.close()

    
        conn = connection()
        cursor = conn.cursor()
        cursor.connection.ping()
        sql = "INSERT INTO Crew (pilotName, flightAttnName, flightNum, airlines) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (pilotName, flightAttnName, flightNum, airlines))
        conn.commit()
        conn.close()
        messagebox.showinfo("Add", "Row added successfully!")
        refreshTable()

def orderTable():
    conn = connection()
    cursor = conn.cursor()
    cursor.connection.ping()
    sql = "SELECT * FROM Crew ORDER BY pilotName"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in results:
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.pack()
    messagebox.showinfo ("Order", "Table has been ordered!")

frame = tkinter.Frame(window, bg="#02577A")
frame.pack()

btnColor = "#4C7EA9"

manageFrame = tkinter.LabelFrame(frame, text='Manage', borderwidth=5, bg="#02577A")
manageFrame.grid(row=0, column=0, sticky="w", padx=[175, 200], pady=20, ipadx=[6])

addBtn = tkinter.Button(manageFrame, text="Add", width=10, borderwidth=3, bg=btnColor, fg='white', command=addRow)
UpdateBtn = tkinter.Button(manageFrame, text="Update", width=10, borderwidth=3, bg=btnColor, fg='white', command=updateRow)
DeleteBtn = tkinter.Button(manageFrame, text="Delete", width=10, borderwidth=3, bg=btnColor, fg='white', command=deleteRow)
OrderBtn = tkinter.Button(manageFrame, text="Order", width=10, borderwidth=3, bg=btnColor, fg='white', command=orderTable)

addBtn.grid(row=0, column=0, padx=5, pady=5)
UpdateBtn.grid(row=0, column=1, padx=5, pady=5)
DeleteBtn.grid(row=0, column=2, padx=5, pady=5)
OrderBtn.grid(row=0, column=3, padx=5, pady=5)

entriesFrame = tkinter.LabelFrame(frame, text="Form", borderwidth=5, bg="#02577A")
entriesFrame.grid(row=1, column=0, sticky='w', padx=[125, 200], pady=20, ipadx=[6])

idLabel = tkinter.Label(entriesFrame, text="Pilot Name", anchor="e", width=10, bg="#02577A", fg="white")
fnameLabel = tkinter.Label(entriesFrame, text="Flight Attendant", anchor="e", width=15, bg="#02577A", fg="white")
lnameLabel = tkinter.Label(entriesFrame, text="Flight Number", anchor="e", width=15, bg="#02577A", fg="white")
flightLabel = tkinter.Label(entriesFrame, text="Airline", anchor="e", width=10, bg="#02577A", fg="white")

idLabel.grid(row=0, column=0, padx=10)
fnameLabel.grid(row=1, column=0, padx=10)
lnameLabel.grid(row=2, column=0, padx=10)
flightLabel.grid(row=3, column=0, padx=10)

idEntry = tkinter.Entry(entriesFrame, width=50)
fnameEntry = tkinter.Entry(entriesFrame, width=50)
lnameEntry = tkinter.Entry(entriesFrame, width=50)
flightEntry = tkinter.Entry(entriesFrame, width=50)

idEntry.grid(row=0, column=2, padx=5, pady=5)
fnameEntry.grid(row=1, column=2, padx=5, pady=5)
lnameEntry.grid(row=2, column=2, padx=5, pady=5)
flightEntry.grid(row=3, column=2, padx=5, pady=5)

my_tree['columns'] = ("Passenger ID", "First Name", "Last Name", "Flight Number")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Passenger ID", anchor=W, width=70)
my_tree.column("First Name", anchor=W, width=125)
my_tree.column("Last Name", anchor=W, width=125)
my_tree.column("Flight Number", anchor=W, width=100)

my_tree.heading("Passenger ID", text="Pilot Name", anchor=W)
my_tree.heading("First Name", text="Flight Attendant Name", anchor=W)
my_tree.heading("Last Name", text="Flight Number", anchor=W)
my_tree.heading("Flight Number", text="Airlines", anchor=W)
my_tree.tag_configure('orow', background="#EEEEEE")

refreshTable()

window.resizable(False, False)
window.mainloop()