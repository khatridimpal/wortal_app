import tkinter as tk
from tkinter import messagebox
from pages.login_page import LoginPage
from pages.business_page import BusinessPage
from pages.branch_page import BranchPage
from pages.fetch_stock_items_page import FetchStockItemsPage

class WortalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wortal")
        self.geometry("925x500")
        self.configure(bg='#fff')
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file="assets/favicon.png"))

        self.container=None

        self.show_login_page()

    def show_login_page(self):
        if self.container is not None:
            self.container.destroy()
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both")
        page = LoginPage(self.container, self)
        page.pack(expand=True, fill="both")

    def show_business_page(self, token):
        if isinstance(token, dict) and 'token' in token:
            self.container.destroy()
            self.container = tk.Frame(self)
            self.container.pack(expand=True, fill="both")
            page = BusinessPage(self.container, self, token)
            page.pack(expand=True, fill="both")
        else:
            print("token----------->",token)
            messagebox.showerror("Error", "Invalid token")

    def show_branch_page(self, token, selected_business):
        self.container.destroy()
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both")
        page = BranchPage(self.container, self, token, selected_business)
        page.pack(expand=True, fill="both")

    def show_fetch_stock_items_page(self,token, branch_id):
        self.container.destroy()
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both")
        page = FetchStockItemsPage(self.container, self, branch_id,token)
        page.pack(expand=True, fill="both")