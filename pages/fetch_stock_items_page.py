import tkinter as tk
from tkinter import messagebox,ttk,font
import requests
import xml.etree.ElementTree as ET
import json

class FetchStockItemsPage(tk.Frame):
    def __init__(self, parent, controller, branch_id,token,selected_business):
        super().__init__(parent)
        self.controller = controller
        self.branch_id = branch_id
        self.token = token
        self.selected_business = selected_business

        self.create_fetch_stock_items_page()

    def create_fetch_stock_items_page(self):
        def back_to_branch_page():
            self.controller.show_business_page(self.token)

        self.fetch_stock_items_frame = tk.Frame(self, bg='#f5f5f5')
        self.fetch_stock_items_frame.pack(expand=True, fill='both')

        custom_font = font.Font(family="Helvetica", size=12)

        t1 = self.token['token']
        headers = {"Authorization": f"Bearer {t1}", "X-Business-Id": self.selected_business}
        response = requests.get("https://api-dev.wortal.co/api/my_branches", headers=headers)

        if response.status_code == 200:
            branches = response.json()
        else:
            messagebox.showerror("Error", f"Request failed with status code {response.status_code}")
            branches = []

        branch_names = [branch["name"] for branch in branches]

        header_label = tk.Label(self.fetch_stock_items_frame, text="Fetch Stock Items", font=("Helvetica", 18, "bold"),fg="#333333", bg="#f5f5f5")
        header_label.pack(pady=20)

        branch_frame = tk.Frame(self.fetch_stock_items_frame, bg="#f5f5f5")
        branch_frame.pack(pady=10)

        self.droupdown_menu = ttk.Combobox(branch_frame,state="readonly", values=branch_names, font=custom_font)
        self.droupdown_menu.pack(side="left", padx=10)

        url_frame = tk.Frame(self.fetch_stock_items_frame, bg="#f5f5f5")
        url_frame.pack(pady=10)

        self.url_label = tk.Label(url_frame, text="Enter Tally URL:", font=custom_font, fg="#333333", bg="#f5f5f5")
        self.url_label.pack(side="left", padx=10)

        self.url_entry = tk.Entry(url_frame, font=custom_font)
        self.url_entry.pack(side="left", padx=10, fill="x", expand=True)

        button_frame = tk.Frame(self.fetch_stock_items_frame, bg="#f5f5f5")
        button_frame.pack(pady=20)

        self.submit_button = tk.Button(button_frame, text="Fetch Data", font=custom_font, bg="#4CAF50", fg="#ffffff", command=self.fetch_data, relief="raised")
        self.submit_button.pack(side="left", padx=10)

        self.back_button = tk.Button(button_frame, text='Back', font=custom_font, bg="#f44336", fg="#ffffff", command=back_to_branch_page, relief="raised")
        self.back_button.pack(side="left", padx=10)

    def fetch_data(self):
        tally_url = self.url_entry.get()

        if not tally_url:
            messagebox.showerror("Error", "Please enter the Tally URL.")
            return

        xml_string = """
        <ENVELOPE>
            <HEADER>
                <VERSION>1</VERSION>
                <TALLYREQUEST>EXPORT</TALLYREQUEST>
                <TYPE>COLLECTION</TYPE>
                <ID>List of Stock Items</ID>
            </HEADER>
            <BODY>
                <DESC>
                    <STATICVARIABLES>
                        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    </STATICVARIABLES>
                    <TDL>
                        <TDLMESSAGE>
                            <COLLECTION NAME="List of Stock Items" ISINITIALIZE="Yes">
                                <TYPE>Stock item</TYPE>
                                <ADD>CHILD OF : Electronics</ADD>
                                <NATIVEMETHOD>Name</NATIVEMETHOD>
                                <NATIVEMETHOD>Parent</NATIVEMETHOD>
                                <NATIVEMETHOD>OpeningBalance</NATIVEMETHOD>
                                <NATIVEMETHOD>OpeningValue</NATIVEMETHOD>
                                <NATIVEMETHOD>GSTDetails</NATIVEMETHOD>
                                <NATIVEMETHOD>HSNDetails</NATIVEMETHOD>
                                <NATIVEMETHOD>BaseUnits</NATIVEMETHOD>
                                <NATIVEMETHOD>GSTTypeOfSupply</NATIVEMETHOD>
                                <NATIVEMETHOD>BatchalLocations</NATIVEMETHOD>
                            </COLLECTION>
                        </TDLMESSAGE>
                    </TDL>
                </DESC>
            </BODY>
        </ENVELOPE>
        """
        response = requests.post(tally_url, data=xml_string)
        response.raise_for_status()
        cleaned_response = response.text.replace('&', '&amp;')
        root = ET.fromstring(cleaned_response)

        stock_items = []
        for item in root.findall('.//COLLECTION/STOCKITEM'):
            name = item.attrib['NAME']
            parent = item.find('PARENT').text.strip().replace("&#4; ", "") if item.find('PARENT') is not None else ''
            opening_balance = item.find('OPENINGBALANCE').text
            sell_price = item.find('OPENINGVALUE').text
            uom= item.find('BASEUNITS').text
            type_of_supply = item.find('GSTTYPEOFSUPPLY').text
            gst_rate = None
            hsn_code = None
            desc = None
            items = []
            opening_stock = []

            gst_details = item.find('GSTDETAILS.LIST')
            if gst_details is not None:
                for rate_detail in gst_details.findall('.//RATEDETAILS.LIST'):
                    gst_rate_head = rate_detail.find('GSTRATEDUTYHEAD').text.strip()
                    if gst_rate_head == 'IGST':
                        gst_rate = rate_detail.find('GSTRATE').text.strip()
                        break

            hsn_details = item.find('HSNDETAILS.LIST')
            if hsn_details is not None:
                hsn_code = hsn_details.find('HSNCODE').text.strip()
                desc = hsn_details.find('HSN').text.strip()

            batch_locations = item.find('BATCHALLOCATIONS.LIST')
            if batch_locations is not None:
                for loc in item.findall('BATCHALLOCATIONS.LIST'):
                    sub_location = loc.find('GODOWNNAME').text.strip()
                    stock = loc.find('OPENINGBALANCE').text.strip()
                    opening_stock.append({"sub_location_name": sub_location, "stock": stock})

            items.append({
                "item_id": "null",
                "name": name,
                "sell_price": sell_price,
                "quantity": opening_balance,
                "hsn_code": hsn_code,
                "desc": desc,
                "remarks": "null",
                "opening_stock": opening_stock
            })
            stock_items.append(
                {
                    "item_group_name": parent,
                    "item_type": type_of_supply,
                    "uom": uom,
                    "gst_rate": gst_rate,
                    "items": items
                }
            )

        output_json = json.dumps(stock_items, indent=4)
        print(output_json)