import tkinter as tk
from tkinter import messagebox
import requests

class BranchPage(tk.Frame):
    def __init__(self, parent, controller, token, selected_business):
        super().__init__(parent)
        self.controller = controller
        self.token = token
        self.selected_business = selected_business

        self.create_branch_page()

    def create_branch_page(self):
        self.branch_frame = tk.Frame(self, bg='#fff')
        self.branch_frame.pack(expand=True, fill='both')

        def back_to_business_page():
            self.controller.show_business_page(self.token)

        t1 = self.token['token']
        headers = {"Authorization": f"Bearer {t1}", "X-Business-Id": self.selected_business}
        response = requests.get("https://api-dev.wortal.co/api/my_branches", headers=headers)

        if response.status_code == 200:
            branches = response.json()
        else:
            messagebox.showerror("Error", f"Request failed with status code {response.status_code}")
            branches = []

        self.selected_branch = tk.StringVar()
        self.selected_branch.set(None)

        for branch in branches:
            tk.Radiobutton(self.branch_frame, bg='white', text=branch["name"], variable=self.selected_branch, value=branch["id"]).pack(anchor='w')

        tk.Button(self.branch_frame, width=20, pady=7, text='Submit', bg='#57a1f8', fg='white', border=0, command=self.select_branch).pack()
        back_button = tk.Button(self.branch_frame, width=20, pady=7, text='Back', bg='#57a1f8', fg='white', border=0, command=back_to_business_page)
        back_button.pack()

    def select_branch(self):
        selected_branch = self.selected_branch.get()
        if not selected_branch:
            messagebox.showerror("Error", "Please select a branch")
            return

        self.controller.show_fetch_stock_items_page(self.token,selected_branch)