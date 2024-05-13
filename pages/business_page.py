import tkinter as tk
from tkinter import messagebox,font
import requests

class BusinessPage(tk.Frame):
    def __init__(self, parent, controller, token):
        super().__init__(parent)
        self.controller = controller
        self.token = token

        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Verdana", size=12)

        self.create_business_page()

    def create_business_page(self):
        self.business_frame = tk.Frame(self, bg="#F5F5F5")
        self.business_frame.pack(expand=True, fill='both')

        self.header_frame = tk.Frame(self.business_frame, bg='#57a1f8')
        self.header_frame.pack(pady=20, padx=20,fill='x')

        title_label = tk.Label(self.header_frame, text="Select Your Business", fg="white", bg="#57a1f8",font=self.title_font)
        title_label.pack(pady=10)

        self.radio_frame = tk.Frame(self.business_frame, bg='#F5F5F5')
        self.radio_frame.pack(pady=15, padx=100)

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

        for i, business in enumerate(businesses):
            radio_button = tk.Radiobutton(self.radio_frame, text=business["name"], variable=self.selected_business, value=business["id"],font=self.label_font,bg="#F5F5F5",fg="#333333", padx=20,pady=4, anchor='w')
            radio_button.grid(row=i, column=0, sticky='w')

        submit_button = tk.Button(self.business_frame, width=10, pady=10, text='Submit', bg='#4CAF50', fg='white', font=self.button_font, border=0, relief="raised", command=lambda: self.show_branch_page())
        submit_button.place(relx=0.4,rely=0.8,anchor="center")

        back_button = tk.Button(self.business_frame, width=10, pady=10, text='Back', bg='#F44336', fg='white',font=self.button_font, border=0,relief="raised", command=back_to_login)
        back_button.place(relx=0.6,rely=0.8,anchor="center")

    def show_branch_page(self):
        selected_business = self.selected_business.get()
        print("selected business------->", selected_business)
        if not selected_business:
            messagebox.showerror("Error", "Please select a business")
            return

        self.controller.show_branch_page(self.token, selected_business)