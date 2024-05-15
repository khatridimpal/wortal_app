import tkinter as tk
from tkinter import messagebox,ttk
import requests
import xml.etree.ElementTree as ET
import json

class FetchStockItemsPage(tk.Frame):
    def __init__(self, parent, controller, branch_id,token):
        super().__init__(parent)
        self.controller = controller
        self.branch_id = branch_id
        self.token = token

        self.create_fetch_stock_items_page()

    def create_fetch_stock_items_page(self):
        def back_to_branch_page():
            self.controller.show_business_page(self.token)

        self.fetch_stock_items_frame = tk.Frame(self, bg='#fff')
        self.fetch_stock_items_frame.pack(expand=True, fill='both')

        self.combo = ttk.Combobox(
            self.fetch_stock_items_frame,
            state="readonly",
            values=["Python", "C", "C++", "Java"]
        )
        self.combo.place(x=50, y=50)

        self.url_label = tk.Label(self.fetch_stock_items_frame, text="Enter Tally URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.fetch_stock_items_frame)
        self.url_entry.pack()

        self.submit_button = tk.Button(self.fetch_stock_items_frame, text="Fetch Data", command=self.fetch_data)
        self.submit_button.pack()

        self.back_button = tk.Button(self.fetch_stock_items_frame, text='Back', command=back_to_branch_page)
        self.back_button.pack()

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
                    opening_stock.append({"sub_location": sub_location, "stock": stock})

            items.append({
                "name": name,
                "desc": desc,
                "sell_price": sell_price,
                "quantity": opening_balance,
                "hsn_code": hsn_code,
                "opening_stock": opening_stock
            })
            stock_items.append(
                {
                    "Parent": parent,
                    "type_of_supply": type_of_supply,
                    "uom": uom,
                    "gst_rate": gst_rate,
                    "items": items
                }
            )

        output_json = json.dumps(stock_items, indent=4)
        print(output_json)