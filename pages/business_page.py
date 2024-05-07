import tkinter as tk
from tkinter import messagebox
import requests

class BusinessPage(tk.Frame):
    def __init__(self, parent, controller, token):
        super().__init__(parent)
        self.controller = controller
        self.token = token

        self.create_business_page()

    def create_business_page(self):
        self.business_frame = tk.Frame(self, bg='#fff')
        self.business_frame.pack(expand=True, fill='both')

        self.radio_frame = tk.Frame(self.business_frame, bg='#FFF8DC')
        self.radio_frame.pack(pady=100, padx=100)

        def back_to_login():
            self.controller.show_login_page()

        t1 = self.token['token']
        headers = {"Authorization": f"Bearer {t1}"}
        response = requests.get("https://api-dev.wortal.co/api/businesses", headers=headers)

        if response.status_code == 200:
            businesses = response.json()
        else:
            messagebox.showerror("Error", f"Request failed with status code {response.status_code}")
            businesses = []

        self.selected_business = tk.StringVar()
        self.selected_business.set(None)

        tk.Label(self.radio_frame, text='', fg='#FFF8DC', bg='white', pady=20).grid(row=1, column=0, sticky='w')

        for i, business in enumerate(businesses):
            tk.Radiobutton(self.radio_frame, text=business["name"], variable=self.selected_business, value=business["id"], bg='#FFF8DC', padx=100, anchor='w').grid(row=i+2, column=0, sticky='w')

        tk.Label(self.radio_frame, text='', fg='#FFF8DC', bg='white', height=3).grid(column=0, sticky='w')

        tk.Button(self.business_frame, width=20, pady=7, text='Submit', bg='#57a1f8', fg='white', border=0, command=lambda: self.show_branch_page()).place(x=300, y=400)
        back_button = tk.Button(self.business_frame, width=20, pady=7, text='Back', bg='#57a1f8', fg='white', border=0, command=back_to_login)
        back_button.place(x=450, y=400)

    def show_branch_page(self):
        selected_business = self.selected_business.get()
        print("selected business------->", selected_business)
        if not selected_business:
            messagebox.showerror("Error", "Please select a business")
            return

        self.controller.show_branch_page(self.token, selected_business)