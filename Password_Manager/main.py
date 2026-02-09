from tkinter import *
from tkinter import messagebox
from random import *
import json
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for let in range(randint(8, 10))]
    password_symbols = [choice(symbols) for sym in range(randint(2, 4))]
    password_numbers = [choice(numbers) for num in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(END, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD (to txt) ------------------------------- #

def save_to_file():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "":
        messagebox.showerror(message=f"Website field left blank :(")

    elif email == "":
        messagebox.showerror(message=f"Email field left blank :(")
    elif password == "":
        messagebox.showerror(message=f"Password field left blank :(")

    else:
        # is_ok = messagebox.askokcancel(title=website,
        #                                message=f"Password: {password}\nemail: {email}\nOK to save?")
        # if is_ok:
        try:
            with open("data.json", "r") as data_file:
                # reads the old data
                data = json.load(data_file)
                # updates the data with new data
                data.update(new_data)
        except FileNotFoundError:
            data = new_data
            # with open("data.json", "w") as data_file:
            #     json.dump({}, data_file)
            # with open("data.json", "r") as data_file:
            #     data = json.load(data_file) # reads the old data
            #     data.update(new_data) # updates the data with new data
        finally:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)  # Saves the updated file
            website_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            password_entry.delete(0, 'end')


# ---------------------------- SEARCH ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            email = data[website]["email"]
            password = data[website]["password"]
            text = f"Email: {email}\nPassword: {password}"
        messagebox.showinfo(message=text)
    except KeyError:
        messagebox.showinfo(message="website name not found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=45, pady=40, bg="white")
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock)
canvas.grid(column=1, row=0)

# ---Labels---
# website label
website_label = Label(text="Website's Name:", fg="black", bg="white", font=20)
website_label.grid(column=0, row=2)
# email-username label
email_label = Label(text="Email/Username:", fg="black", bg="white", font=20)
email_label.grid(column=0, row=3)
# Password label
password_label = Label(text="Password:", fg="black", bg="white", font=20)
password_label.grid(column=0, row=4)

# ---Entries---
# website entry
website_entry = Entry(width=22)
website_entry.grid(row=2, column=1)
website_entry.focus()
# Email entry
email_entry = Entry(width=40)
email_entry.insert(END, string="github.com/mattbobea")
email_entry.grid(row=3, column=1, columnspan=2)
# Password entry
password_entry = Entry(width=22)
password_entry.grid(row=4, column=1)

# ---Buttons---
# --Generate search button--
search_button = Button(text="Search", command=search)
search_button.grid(row=2, column=2)
# --Generate password button--
password_button = Button(text="Generate Password", command=gen_password)
password_button.grid(row=4, column=2)

# --Add button--
# calls action() when pressed
add_button = Button(text="Add to file", command=save_to_file, width=34)
add_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
