import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_login_page()

    def create_login_page(self):
        self.login_frame = tk.Frame(self, bg='#fff')
        self.login_frame.pack(expand=True, fill='both')

        img = Image.open("assets/login.png")
        self.login_photo = ImageTk.PhotoImage(img)
        tk.Label(self.login_frame, image=self.login_photo, border=0, bg='white').place(x=50, y=90)

        heading = tk.Label(self.login_frame, text='Sign in', fg='#57a1f8', bg='white', font=('Helvetica', 23, 'bold'))
        heading.place(x=600, y=50)

        self.user_entry = tk.Entry(self.login_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.user_entry.place(x=500, y=110)
        self.user_entry.insert(0, 'Username')

        self.user_entry.bind("<FocusIn>", self.on_enter_username)
        self.user_entry.bind("<FocusOut>", self.on_leave_username)

        tk.Frame(self.login_frame, width=295, height=2, bg='black').place(x=500, y=137)

        self.code_entry = tk.Entry(self.login_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.code_entry.place(x=500, y=180)
        self.code_entry.insert(0, 'Password')

        self.code_entry.bind("<FocusIn>", self.on_enter_password)
        self.code_entry.bind("<FocusOut>", self.on_leave_password)

        tk.Frame(self.login_frame, width=295, height=2, bg='black').place(x=500, y=207)

        tk.Button(self.login_frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=self.signin).place(x=500, y=250)

    def signin(self):
        username = self.user_entry.get()
        password = self.code_entry.get()

        url = "https://api-dev.wortal.co/api/login"
        data = {"user_name": username, "password": password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            token = result.get('token')
            self.controller.show_business_page(token)
        else:
            messagebox.showerror("Error", f"Error {response.status_code}")

    def on_enter_username(self, event):
        if self.user_entry.get() == 'Username':
            self.user_entry.delete(0, 'end')

    def on_leave_username(self, event):
        if self.user_entry.get() == '':
            self.user_entry.insert(0, 'Username')

    def on_enter_password(self, event):
        if self.code_entry.get() == 'Password':
            self.code_entry.delete(0, 'end')
        self.code_entry.config(show="*")

    def on_leave_password(self, event):
        if self.code_entry.get() == '' or self.code_entry.get() == 'Password':
            self.code_entry.delete(0, 'end')
            self.code_entry.insert(0, 'Password')
            self.code_entry.config(show="")
        else:
            self.code_entry.config(show="*")