import customtkinter as ctk
import yfinance as yf
import pandas_ta as ta

class FinancialAnalyzer(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Financial Analyzer")
        self.geometry("800x600")

        # List to hold all condition blocks and connectors
        self.condition_blocks = []
        self.condition_connectors = []

        # Button to add a new condition block
        self.add_condition_button = ctk.CTkButton(self, text="Add Condition", command=self.add_condition_block)
        self.add_condition_button.pack()

        # Button to perform the calculation
        self.calculate_button = ctk.CTkButton(self, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        # Label to display the results
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack()

        # Initially add one condition block
        self.add_condition_block()

    def add_condition_block(self):
        # Create a new frame for the condition block
        condition_frame = ctk.CTkFrame(self)
        condition_frame.pack(pady=10)

        # Dropdown for selecting the first indicator
        indicator1_dropdown = ctk.CTkComboBox(condition_frame, values=["SMA", "EMA", "RSI"])
        indicator1_dropdown.pack(side='left')

        # Entry for the parameters of the first indicator
        params1_entry = ctk.CTkEntry(condition_frame)
        params1_entry.pack(side='left')

        # Dropdown for selecting the conditional operator
        operator_dropdown = ctk.CTkComboBox(condition_frame, values=[">", "<", "==", ">=", "<="])
        operator_dropdown.pack(side='left')

        # Dropdown for selecting the second indicator or value
        indicator2_dropdown = ctk.CTkComboBox(condition_frame, values=["SMA", "EMA", "RSI", "Value"])
        indicator2_dropdown.pack(side='left')

        # Entry for the parameters of the second indicator or value
        params2_entry = ctk.CTkEntry(condition_frame)
        params2_entry.pack(side='left')

        # Add the condition block to the list
        self.condition_blocks.append((indicator1_dropdown, params1_entry, operator_dropdown, indicator2_dropdown, params2_entry))

        # If this is not the first condition, add a connector dropdown
        if len(self.condition_blocks) > 0:
            connector_dropdown = ctk.CTkComboBox(self, values=["","AND", "OR"])
            connector_dropdown.pack(pady=5)
            self.condition_connectors.append(connector_dropdown)

    def calculate(self):
        print(self.condition_blocks)
        # Placeholder for the overall result
        overall_result = None

        # Fetch data from yfinance
        ticker = 'AAPL'  # Placeholder for the ticker symbol
        data = yf.download(ticker, period='7d')

        # Iterate over each condition block and evaluate
        for i, block in enumerate(self.condition_blocks):
            indicator1, params1, operator, indicator2, params2 = block

            # Calculate the first indicator
            indicator1_data = self.calculate_indicator(data, indicator1.get(), params1.get())

            # Calculate the second indicator or get the value
            if indicator2.get().lower() == "value":
                indicator2_data = float(params2.get())  # Directly use the entered value
            else:
                indicator2_data = self.calculate_indicator(data, indicator2.get(), params2.get())

            # Evaluate the condition for the current block
            result = self.evaluate_condition(indicator1_data, operator.get(), indicator2_data)

            # Combine the result with the overall result using the selected connector
            if overall_result is None:
                overall_result = result
            else:
                connector = self.condition_connectors[i-1].get()
                if connector == "AND":
                    overall_result = overall_result and result
                elif connector == "OR":
                    overall_result = overall_result or result

        # Display the overall result
        self.result_label.configure(text = f"Overall Result: {overall_result}")

    def calculate_indicator(self, data, indicator, params):
        # Placeholder function to calculate indicators
        # You will need to implement the actual calculation logic based on the selected indicator and parameters
        return 0  # Placeholder return value

    def evaluate_condition(self, value1, operator, value2):
        # Placeholder function to evaluate the condition
        # You will need to implement the actual evaluation logic based on the operator
        return False  # Placeholder return value

if __name__ == '__main__':
    app = FinancialAnalyzer()
    app.mainloop()
