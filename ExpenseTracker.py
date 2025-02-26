from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt

def connect():
    conn = sqlite3.connect("loginpage.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT,username TEXT PRIMARY KEY,password TEXT)")
    conn.commit()
    conn.close()
connect()

def viewallusers():
    conn = sqlite3.connect("loginpage.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.commit()
    conn.close()   
    return rows

def adduser(name, username, password):
    try:
        conn = sqlite3.connect("loginpage.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES(?,?,?)", (name, username, password))
        conn.commit()
        messagebox.showinfo(':)', 'Registration Successful')
    except sqlite3.IntegrityError:
        messagebox.showinfo('oops something wrong', 'Username already exists')
    finally:
        conn.close()

def deleteallusers():
    conn = sqlite3.connect("loginpage.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    messagebox.showinfo('Successful', 'All users deleted')

def checkuser(username, password):
    conn = sqlite3.connect("loginpage.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    return result

def getusername(username, password):
    conn = sqlite3.connect("loginpage.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    global profilename
    if result != None:
        profilename = result[0]

def viewwindow():
    gui = Toplevel(root)
    gui.title("VIEW ALL USERS")
    gui.geometry("800x700")
    Message(gui, font=("Castellar", 22, "bold"), text=" NAME       USERNAME     PASSWORD", width=700).pack()
    for row in viewallusers():
        a = row[0]
        b = row[1]
        c = ""
        f = len(row[2])
        for i in range(f):
            c = c + "*"
        d = a + "         " + b + "           " + c
        Message(gui, fg='#6680ff', font=("adobe clean", 25, "bold"), text=d, width=700).pack()
    Button(gui, text="Exit Window", font=("candara", 15, "bold"), activebackground="#fffa66", activeforeground="red", width=10, command=gui.destroy).pack()

def register():
    a = register_name.get()
    b = register_username.get()
    c = register_password.get()
    d = register_repassword.get()
    if c == d and c != "" and len(c) > 5 and a != "" and b != "":
        try:
            adduser(a, b, c)
        except sqlite3.IntegrityError:
            messagebox.showinfo('oops something wrong', 'Username already exists')      
    else:
        if (a == "" or b == "" or c == "" or d == ""):
            messagebox.showinfo('oops something wrong', 'Field should not be empty')
        else:
            messagebox.showinfo('oops something wrong', 'Both passwords should be same! \nPassword should contain atleast 6 characters')
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)

def login():
    a = login_username.get()
    b = login_password.get()
    getusername(a, b)   
    if (checkuser(a, b)) != None:
        messagebox.showinfo('logged in sucessfully', 'login successful')
        root.destroy()
        appwindow(a) 
    else:
        e1.delete(0, END)
        e2.delete(0, END)
        messagebox.showinfo('oops something wrong', 'Invalid credentials')

profilename = ""
t = 11

def appwindow(username):
   
    user_table = f"expenses_{username}"

    def connect1():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {user_table}(id INTEGER PRIMARY KEY,itemname TEXT,date TEXT,cost TEXT, category TEXT)")
        conn.commit()
        conn.close()
    connect1()

    def insert(itemname, date, cost, category):
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {user_table} VALUES(NULL,?,?,?,?)", (itemname, date, cost, category))
        conn.commit()
        conn.close()
        clear_feilds()
    
    def clear_feilds():
        exp_itemname.set("")
        exp_date.set("")
        exp_cost.set("")
        exp_category.set("")


    def view():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {user_table}")
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    
    def search(itemname="", date="", cost="", category=""):
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {user_table} WHERE itemname=? OR date=? OR cost=? OR category=?", (itemname, date, cost, category))
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    
    def get_selected_item():
        selected = list1.curselection()  # Get index of selected item
        if selected:
            item = list1.get(selected[0])  # Get item from Listbox
            print("Selected:", item)
    
          
    def edit_item():
        selected = list1.curselection()  # Get index of selected item
        if selected:
            item = list1.get(selected[0])  # Get item from Listbox
            item_id = item.split()[0]  # Extract ID from the selected item
            new_itemname = exp_itemname.get()
            new_date = exp_date.get()
            new_cost = exp_cost.get()
            new_category = exp_category.get()
            
            if new_itemname == "" or new_date == "" or new_cost == "" or new_category == "":
                messagebox.showinfo("oops something wrong", "Field should not be empty")
            else:
                conn = sqlite3.connect("expenseapp.db")
                cur = conn.cursor()
                cur.execute(f"UPDATE {user_table} SET itemname=?, date=?, cost=?, category=? WHERE id=?", 
                            (new_itemname, new_date, new_cost, new_category, item_id))
                conn.commit()
                conn.close()
                messagebox.showinfo('Successful', 'Item updated')
                viewallitems()  # Refresh the list to show updated item
                clear_feilds()  #clear all the fields
        else:
            messagebox.showinfo("oops something wrong", "No item selected")
    
    def get_selected_item(event):
        selected = list1.curselection()  # Get index of selected item
        if selected:
            item = list1.get(selected[0])  # Get item from Listbox
            item_details = item.split()  # Split item details
            item_id = item_details[0]
            item_name = item_details[1]
            item_date = item_details[2]
            item_cost = item_details[3]
            item_category = item_details[4]

            # Set the values of the entry fields
            exp_itemname.set(item_name)
            exp_date.set(item_date)
            exp_cost.set(item_cost)
            exp_category.set(item_category)

    def delete(id):
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {user_table} WHERE id=?", (id,))
        conn.commit()
        conn.close()
    
    def deletealldata():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {user_table}")
        conn.commit()
        conn.close()
        list1.delete(0, END)
        messagebox.showinfo('Successful', 'All data deleted')

    def sumofitems():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT SUM(cost) FROM {user_table}")
        sum = cur.fetchone()
        list1.delete(0, END)
        b = str(sum[0])
        a = "YOU SPENT " + b
        messagebox.showinfo('TOTAL SPENT', a)
        conn.commit()
        conn.close()
        return sum
    
    def insertitems():
        a = exp_itemname.get()
        b = exp_date.get()
        c = exp_cost.get()
        h = exp_category.get()
        d = c.replace('.', '', 1)
        e = b.count('-')      

        if a == "" or b == "" or c == "" or h == "":
            messagebox.showinfo("oops something wrong", "Field should not be empty")
        elif len(b) != 10 or e != 2:
            messagebox.showinfo("oops something wrong", "DATE should be in format dd-mm-yyyy")
        elif (d.isdigit() == False):
            messagebox.showinfo("oops something wrong", "Cost should be a number")
        else:
            insert(a, b, c, h)
            messagebox.showinfo('Successful', 'Item added')
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
        list1.delete(0, END)

    def viewallitems():
        list1.delete(0, END)
        list1.insert(END, "ID     NAME      DATE        COST      Category")
        for row in view():
            a = str(row[0])
            b = str(row[1])
            c = str(row[2])
            d = str(row[3])
            e = str(row[4])
            f = a + "     " + b + "    " + c + "    " + d + "    " + e
            list1.insert(END, f)
            clear_feilds()
    
    def deletewithid():
        list1.delete(0, END)
        a = exp_id.get()
        delete(a)
    
    def search_item():
        list1.delete(0, END)
        list1.insert(END, "ID    NAME      DATE      COST    CATEGORY")
        for row in search(exp_itemname.get(), exp_date.get(), exp_cost.get(), exp_category.get()):
            a = str(row[0])
            b = str(row[1])
            c = str(row[2])
            d = str(row[3])
            e = str(row[4])
            f = a + "     " + b + "    " + c + "    " + d + "   " + e
            list1.insert(END, f)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)


    def fetch_data(username):
        user_table = f"expenses_{username}"
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT category, SUM(cost) FROM {user_table} GROUP BY category")
        data = cur.fetchall()
        conn.close()
        return data

    def plot_pie_chart(data):
        categories = [row[0] for row in data]
        expenses = [row[1] for row in data]

        plt.figure(figsize=(10, 7))
        plt.pie(expenses, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Expenses by Category')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
    
    def graph():
        data = fetch_data(username)
        if data:
            plot_pie_chart(data)
        else:
            print("No data found for the given username.")


#end page
    def endpage():
        Label(gui, width=100, height=100, font=("century", 35), bg="#bfbfbf", text="").place(x=-455, y=0)
        Label(gui, font=("lucida fax", 40), bg="#bfbfbf", text="EXPENSE TRACKER").place(x=190, y=10)
        Label(gui, font=("gabriola", 40), bg="#bfbfbf", text="An application developed using").place(x=70, y=170)
        Label(gui, font=("gabriola", 40), bg="#bfbfbf", text="sqlite3 and tkinter").place(x=400, y=250)
        Label(gui, font=("ink free", 22), bg="#bfbfbf", text="-Himanshu").place(x=500, y=450)
        Label(gui, font=("ink free", 22), bg="#bfbfbf", text="-Sandhya").place(x=500, y=490)
        Label(gui, font=("ink free", 22), bg="#bfbfbf", text="-Nirjala").place(x=500, y=530)
        Label(gui, font=("ink free", 22), bg="#bfbfbf", text="-Rasrim").place(x=500, y=570)
        h = Label(gui, font=("century", 25), bg="#bfbfbf", text="This window auomatically closes after")
        h.place(x=65, y=650)
        ltime = Label(gui, font=("century", 25), bg="#bfbfbf", fg="black")
        ltime.place(x=655, y=651)      
        def timer():
            global t
            a = str(t) + " seconds"
            text_input = a
            ltime.config(text=text_input)
            ltime.after(1000, timer)
            t = t - 1
        timer()
        gui.after(11000, gui.destroy)


# Dashboard window
    gui = Tk()
    gui.title("EXPENSE TRACKER")
    gui.configure(bg='white')
    gui.geometry("900x700")
    gui.iconbitmap("icon.ico")
    frame = Frame(gui, width=550, height=390, bg='#7ed4e3')
    frame.place(x=0, y=50)
    l8 = Label(gui, width=60, height=7, font=("century", 35), bg="#1ad1ff", text="").place(x=450, y=60)
    l7 = Label(gui, width=100, height=10, font=("century", 35), bg="#1affd1", text="").place(x=-455, y=410)
    l1 = Label(gui, font=("comic sans ms", 17), bg="#7ed4e3", text="Product name").place(x=10, y=150)
    exp_itemname = StringVar()
    e1 = Entry(gui, font=("adobe clean", 15), textvariable=exp_itemname)
    e1.place(x=220, y=155, height=27, width=165)
    l2 = Label(gui, font=("comic sans ms", 17), bg="#7ed4e3", text="Date(dd-mm-yyyy)").place(x=10, y=200)
    exp_date = StringVar()
    e2 = Entry(gui, font=("adobe clean", 15), textvariable=exp_date)
    e2.place(x=220, y=205, height=27, width=165)
    l3 = Label(gui, font=("comic sans ms", 17), bg="#7ed4e3", text="Cost of product").place(x=10, y=250)
    exp_cost = StringVar()
    e3 = Entry(gui, font=("adobe clean", 15), textvariable=exp_cost)
    e3.place(x=220, y=255, height=27, width=165)
    exp_category = StringVar()
    l6 = Label(gui, font=("comic sans ms", 17), bg="#7ed4e3", text="Category").place(x=10, y=300)
    e4 = ttk.Combobox(gui, textvariable=exp_category, values=["FOOD", "CLOTHES", "TRANSPORT", "HOUSING", "OTHERS"], font=("adobe clean", 15))
    e4.place(x=220, y=300, height=27, width=165)
    l4 = Label(gui, font=("comic sans ms", 17), bg="#1ad1ff", text="Select ID to delete").place(x=520, y=150)
    exp_id = StringVar()
    sb = Spinbox(gui, font=("adobe clean", 17), from_=0, to_=200, textvariable=exp_id, justify=CENTER)
    sb.place(x=745, y=153, height=30, width=50)
    scroll_bar = Scrollbar(gui)
    scroll_bar.place(x=671, y=410, height=277, width=20)  
    list1 = Listbox(gui, height=9, width=37, font=("comic sans ms", 16), yscrollcommand=scroll_bar.set)
    list1.place(x=188, y=410)
    scroll_bar.config(command=list1.yview)

    # Bind the Listbox selection event to the get_selected_item function
    list1.bind('<<ListboxSelect>>', get_selected_item)

    b1 = Button(gui, text="Add Item", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=10, command=insertitems).place(x=30, y=350)
    b2 = Button(gui, text="View all items", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=10, command=viewallitems).place(x=8, y=545)
    b3 = Button(gui, text="Delete with id", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=12, command=deletewithid).place(x=550, y=190)
    b4 = Button(gui, text="Delete all items", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=12, command=deletealldata).place(x=550, y=240)
    b5 = Button(gui, text="Search", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=10, command=search_item).place(x=220, y=350)
    b6 = Button(gui, text="Total spent", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=12, command=sumofitems).place(x=550, y=340)
    b9 = Button(gui, text="Graph", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=12, command=graph).place(x=550, y=290)
    b7 = Button(gui, text="Close app", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=10, command=endpage).place(x=710, y=620)
    b8 = Button(gui, text="Edit", font=("georgia", 17), activebackground="#fffa66", activeforeground="red", width=10, command=edit_item).place(x=8, y=490)
    l6 = Label(gui, width=60, font=("century", 35), bg="#ff9999", fg="#b32d00", text="EXPENSE  TRACKER").place(x=-450, y=0)
    # Modified welcome message to show username-specific dashboard
    name = f"Welcome to {profilename}'s Dashboard"
    l9 = Label(gui, width=60, font=("century", 24), bg="#9999ff", fg="black", text=name).place(x=-320, y=61)
    ltime = Label(gui, font=("century", 24), bg="#9999ff", fg="black")
    ltime.place(x=574, y=61)
    def digitalclock():
        text_input = time.strftime("%d-%m-%Y   %H:%M:%S")
        ltime.config(text=text_input)
        ltime.after(1000, digitalclock)
    digitalclock()
    gui.resizable(False, False)
    gui.mainloop()


# Main window
root = Tk()
root.configure(bg='#0066ff')
root.iconbitmap("icon.ico")
image1=Image.open("1.png")
image1 = image1.resize((1000, 700))
bg_image = ImageTk.PhotoImage(image1)
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
root.title("LOGIN / REGISTER")
root.geometry("1000x700")
l1 = Label(root, font=("comic sans ms", 19), bg="#94cef3", text="Username").place(x=80, y=250)
l2 = Label(root, font=("comic sans ms", 19), bg="#94cef3", text="Password").place(x=80, y=300)
b1 = Button(root, text="Login", font=("Microsoft Yahei", 16), activebackground="#fffa66", activeforeground="red", width=12, command=login).place(x=120, y=360)
l6 = Label(root, font=("comic sans ms", 19), bg="#94cef3", text="Name").place(x=653, y=195)
l3 = Label(root, font=("comic sans ms", 19), bg="#94cef3", text="Username").place(x=604, y=243)
l4 = Label(root, font=("comic sans ms", 19), bg="#94cef3", text="Password").place(x=610, y=293)
l5 = Label(root, font=("comic sans ms", 17), bg="#94cef3", text="Confirm password").place(x=532, y=342)
b2 = Button(root, text="Register", font=("Microsoft Yahei", 16), activebackground="#fffa66", activeforeground="red", width=12, command=register).place(x=670, y=400)
login_username = StringVar()
e1 = Entry(root, font=("adobe clean", 15), textvariable=login_username)
e1.place(x=205, y=257, height=25, width=165)
login_password = StringVar()
e2 = Entry(root, font=("adobe clean", 15), textvariable=login_password, show="*")
e2.place(x=205, y=307, height=25, width=165)
register_name = StringVar()
e6 = Entry(root, font=("adobe clean", 15), textvariable=register_name)
e6.place(x=740, y=200, height=25, width=165)
register_username = StringVar()
e3 = Entry(root, font=("adobe clean", 15), textvariable=register_username)
e3.place(x=740, y=250, height=25, width=165)
register_password = StringVar()
e4 = Entry(root, font=("adobe clean", 15), textvariable=register_password, show="*")
e4.place(x=740, y=300, height=25, width=165)
register_repassword = StringVar()
e5 = Entry(root, font=("adobe clean", 15), textvariable=register_repassword, show="*")
e5.place(x=740, y=350, height=25, width=165)
Label(root, font=("jokerman", 42), text="EXPENS0",bg="#fff" ).place(x=380, y=20)
b3 = Button(root, text="Exit Window", font=("candara", 15, "bold"), activebackground="#fffa66", activeforeground="red", width=10, command=root.destroy).place(x=760, y=620)
b4 = Button(root, text="Delete all users", font=("candara", 15, "bold"), activebackground="#fffa66", activeforeground="red", width=12, command=deleteallusers).place(x=430, y=620)
b5 = Button(root, text="View all users", font=("candara", 15, "bold"), activebackground="#fffa66", activeforeground="red", width=12, command=viewwindow).place(x=130, y=620)
root.resizable(False, False)
root.mainloop()