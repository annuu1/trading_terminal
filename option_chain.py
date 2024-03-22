import json
import customtkinter as ctk
import requests

# Controller class to manage dependencies and frame instances
class ApplicationController:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.create_header()

    def create_header(self):
        if 'header' not in self.frames:
            self.frames['header'] = Header(self, self.root)
        return self.frames['header']

    def create_option_chain_frame(self):
        # Always create a new instance of OptionChainFrame
        self.frames['option_chain_frame'] = OptionChainFrame(self, self.root)
        return self.frames['option_chain_frame']

    def get_selected_symbol(self):
        return self.frames['header'].indice.get()

    def display_option_chain(self):
        option_chain_frame = self.create_option_chain_frame()
        option_chain_frame.display_chain(self.get_selected_symbol(), self.frames['header'].expiry.get())

# Header frame class
class Header(ctk.CTkFrame):
    def __init__(self, controller, master):
        super().__init__(master)
        self.controller = controller
        self.grid(row=0, column=0, columnspan=5, sticky='nsew', pady=(2, 2))

        self.indice = ctk.CTkComboBox(self, values=['Select Index', 'NIFTY', 'BANKNIFTY', 'FINNIFTY'])
        self.indice.grid(row=0, column=0, padx=(2, 2), pady=(2, 2))
        self.indice.set(value="NIFTY")

        self.expiries = self.get_expiries()
        self.expiry = ctk.CTkComboBox(self, values=self.expiries)
        self.expiry.grid(row=0, column=1, padx=(2, 2), pady=(2, 2))
        self.expiry.set(value=self.expiries[0])

        self.option_chain_button = ctk.CTkButton(self, text="Show Option Chain", command=self.display_option_chain)
        self.option_chain_button.grid(row=0, column=2, padx=(2, 2), pady=(2, 2))

    def get_expiries(self):
        url = f'https://www.nseindia.com/api/option-chain-indices?symbol={self.indice.get()}'
        data = json.loads(Methods().get_data(url=url))['records']
        # print(data['expiryDates'])
        return data['expiryDates']
    def display_option_chain(self):
        self.controller.display_option_chain()



class MenuFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        # Set the width and height for the frame
        self.width = 30        
        # Configure the frame's width and height
        self.configure(width=self.width)

        self.grid(row = 1, column = 0, sticky = 'nsew',padx = (0, 1) , pady = (1,1))

        ctk.CTkLabel(self, text="help").grid(row = 0, column = 0)

class OptionChainFrame(ctk.CTkScrollableFrame):
    def __init__(self, controller, master):
        super().__init__(master)
        self.controller = controller
        self.menu_frame = MenuFrame(master=master)

        self.grid(row=1, column=1, columnspan=5, sticky='nsew', pady=(1, 2))
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        ctk.CTkLabel(self, text="Option Chain").grid(row=0, column=0, sticky='nsew')
        self.add_headers()

    def add_headers(self):
        # Define the headers list with the 'STRIKE' column in the middle
        headers_list = ['OI', 'CHNG IN OI', 'IV', 'LTP', 'CHNG', 'STRIKE', 'CHNG', 'LTP', 'IV', 'CHNG IN OI', 'OI']
        
        # Calculate the middle index for the 'STRIKE' column
        middle_index = len(headers_list) // 2
        
        # Create labels for headers before the 'STRIKE' column
        for idx in range(middle_index):
            ctk.CTkLabel(self, text=headers_list[idx], fg_color="Green").grid(row=0, column=idx, sticky = 'nsew')
        
        # Create the label for the 'STRIKE' column
        ctk.CTkLabel(self, text=headers_list[middle_index], fg_color="Yellow").grid(row=0, column=middle_index, sticky = 'nsew')
        
        # Create labels for headers after the 'STRIKE' column
        for idx in range(middle_index + 1, len(headers_list)):
            ctk.CTkLabel(self, text=headers_list[idx], fg_color="Red").grid(row=0, column=idx, sticky = 'nsew')


    def display_chain(self, symbol, expiry):
        url = f'https://www.nseindia.com/api/option-chain-indices?symbol={symbol}'

        labels = ['openInterest', 'changeinOpenInterest', 'impliedVolatility', 'lastPrice', 'change']
        ce_formatting_data = []
        pe_formatting_data = []
        call_row = 0
        put_row = 0

        data = json.loads(Methods().get_data(url=url))['records']['data'] #list of the chain data
        for i in range(len(data)):
            if data[i].get('expiryDate') == expiry:
                call_row += 1
                put_row += 1

                CE_data = data[i].get('CE')
                PE_data = data[i].get('PE')
                
                for j in range(len(labels)):
                    value_ce = round(CE_data.get(labels[j]),3)
                    ctk.CTkLabel(self, text= value_ce).grid(row = call_row, column = j)
                    ce_formatting_data.append({'row_number': call_row, 'label_idx': j, 'value': value_ce})

                ctk.CTkLabel(self, text= data[i].get('strikePrice'), fg_color='#514203').grid(row = call_row, column = 5, sticky = 'nsew')
            
                for j in range(len(labels)):
                    value_pe = round(PE_data.get(labels[len(labels)-1-j]),3)
                    ctk.CTkLabel(self, text= value_pe).grid(row = put_row, column = j+6)
                    pe_formatting_data.append({'row_number': call_row, 'label_idx': j+6, 'value': value_pe})

        self.format_data(ce_formatting_data, colors = ['#FD0707', '#FE3D3D', '#FC7543'], column_idx=[0,1])
        self.format_data(pe_formatting_data, colors = ['#017112', '#05A71D', '#02E023'], column_idx=[9,10])
        self.display_sideframe_data()

    def format_data(self, data_list, colors, column_idx=[0, 1], top_n=3):
            i = 0
            for i in range(len(column_idx)):
                # Filter out the data for the specific column
                column_data = [data for data in data_list if data['label_idx'] == column_idx[i]]
                
                # Sort the data by value in descending order
                sorted_data = sorted(column_data, key=lambda x: x['value'], reverse=True)
                
                # Get the top N values and their row numbers
                top_values = sorted_data[:top_n]
                
                # Apply color grading to the labels
                for idx, data in enumerate(top_values):
                    value, row_number = data['value'], data['row_number']
                    color = colors[idx] if idx < len(colors) else 'grey'  # Default color for values beyond top N
                    label = ctk.CTkLabel(self, text=value, fg_color=color)
                    label.grid(row=row_number, column=column_idx[i], sticky = 'nsew')  # Update this line if labels are stored differently
                
    def display_sideframe_data(self):
        selected_symbol = self.controller.get_selected_symbol()
        quote_data = self.get_quotes(selected_symbol)
        ltp = quote_data.get('last')
        ctk.CTkLabel(self.menu_frame, text=selected_symbol).grid(row = 0, column = 0)
        ctk.CTkLabel(self.menu_frame, text=ltp).grid(row = 1, column = 0)

    def get_quotes(self, symbol):
        indices_df = {"NIFTY": 'NIFTY 50', 'BANKNIFTY':"NIFTY BANK", 'FINNIFTY': 'NIFTY FIN SERVICE', 'MID CAP': "NIFTY MID SELECT"}
        url_indices = "https://www.nseindia.com/api/allIndices"
        indices_data = json.loads(Methods().get_data(url=url_indices)) #indices data
        for data in indices_data['data']:
            if data['indexSymbol'] ==indices_df[symbol]:
                return data
        return f'Error! No indice with name {symbol}'

class Methods:
    def __init__(self):
        # Urls for fetching Data
        self.url_oc      = "https://www.nseindia.com/option-chain"
        self.url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
        self.url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        self.url_indices = "https://www.nseindia.com/api/allIndices"
        # Headers
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                    'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                    'accept-encoding': 'gzip, deflate, br'}

        self.sess = requests.Session()
        self.cookies = dict()

    # Local methods
    def set_cookie(self):
        request = self.sess.get(self.url_oc, headers=self.headers, timeout=5)
        cookies = dict(request.cookies)

    def get_data(self, url):
        self.set_cookie()
        response = self.sess.get(url, headers=self.headers, timeout=5, cookies=self.cookies)
        if(response.status_code==401):
            self.set_cookie()
            response = self.sess.get(self.url_nf, headers=self.headers, timeout=5, cookies=self.cookies)
        if(response.status_code==200):
            return response.text
        return ""


# Main application window
class OptionChainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Option Chain")
        self.geometry("800x300")
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.controller = ApplicationController(self)
        self.header = self.controller.create_header()

if __name__ == "__main__":
    option_window = OptionChainWindow()
    option_window.mainloop()
