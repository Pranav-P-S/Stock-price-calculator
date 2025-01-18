import customtkinter as ctk
from tkinter import messagebox

# Function to calculate prices
def calculate_prices():
    try:
        # Fetch input values
        current_price = float(current_price_entry.get())  # Current stock price
        num_shares = float(num_shares_entry.get())  # Number of shares
        desired_profit_percentage = float(desired_profit_percentage_entry.get())  # Desired profit in percentage
        desired_loss_percentage = float(desired_loss_percentage_entry.get())  # Desired loss in percentage
        brokerage_constant = float(brokerage_constant_entry.get())  # Constant brokerage fee
        brokerage_percentage = float(brokerage_percentage_entry.get())  # Percentage-based brokerage fee
        
        # Validation for brokerage logic and loss condition
        if brokerage_percentage < 0 :
            messagebox.showerror("Input Error", "Please check your values for valid percentages.")
            return
        
        
        # Calculate the total invested amount (initial price * number of shares)
        total_invested_amount = current_price * num_shares
        
        #calculation of threshold for constant % calculation
        threshold = (brokerage_constant * 100) / brokerage_percentage
        if current_price > threshold :
            initial_brokerage = brokerage_constant
        else :
            initial_brokerage = (brokerage_percentage * current_price)/100
            
        #selling price calculation profit
        sell_profit_p = ((100 + desired_profit_percentage)/(100-brokerage_percentage))*current_price + ((100*initial_brokerage)/(100-brokerage_percentage))
        sell_profit_c = ((100 + desired_profit_percentage)/100)*current_price + initial_brokerage + brokerage_constant
        
        #selling price calculation loss
        sell_loss_p = ((100 - desired_loss_percentage)/(100-brokerage_percentage))*current_price + ((100*initial_brokerage)/(100-brokerage_percentage))
        sell_loss_c = ((100 - desired_loss_percentage)/100)*current_price + initial_brokerage + brokerage_constant
        
        #finalisation
        if sell_profit_p>sell_profit_c :
            profit_brokerage = brokerage_constant
            profit_price = sell_profit_c
        else :
            profit_brokerage = (brokerage_percentage/100)*sell_profit_p
            profit_price = sell_profit_p
            
        
        if sell_loss_p>sell_loss_c :
            loss_brokerage = brokerage_constant
            loss_price = sell_loss_c
        else :
            loss_brokerage = (brokerage_percentage/100)*sell_loss_p
            loss_price = sell_loss_p
        
        #total calcualation
        profit_per_share = profit_price - current_price - initial_brokerage - profit_brokerage
        total_profit = num_shares * profit_per_share
        loss_per_share = loss_price - current_price - initial_brokerage - loss_brokerage
        total_loss = num_shares * loss_per_share
            
        # Update the output fields with calculated values
        total_investment_label.configure(text=f"Total Investment: ${total_invested_amount:.2f}")
        profit_price_label.configure(text=f"Price per share to sell for profit: ${profit_price:.2f}", text_color="green")
        total_profit_label.configure(text=f"Total Profit: ${total_profit:.2f}")
        loss_price_label.configure(text=f"Price per share to sell for loss: ${loss_price:.2f}", text_color="red")
        total_loss_label.configure(text=f"Total Loss: ${total_loss:.2f}")
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")

# Setup the main GUI window
root = ctk.CTk()
root.title("Stock Price Calculation")
root.geometry("600x900")  # Set the window size to 600x900
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Set theme to dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Create a clean rounded font style
font_style = ("Arial", 14, "bold")  # Use a bold rounded font style for everything

# Create a frame for the input fields
inputs_frame = ctk.CTkFrame(root)
inputs_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

# Create labels and input fields with custom styles
current_price_label = ctk.CTkLabel(inputs_frame, text="Current Stock Price ($):", width=250, height=40, anchor="w", text_color="white", font=font_style)
current_price_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
current_price_entry = ctk.CTkEntry(inputs_frame, width=250, height=40, border_width=2, border_color="white", corner_radius=15, font=font_style)
current_price_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

num_shares_label = ctk.CTkLabel(inputs_frame, text="Number of Shares:", width=250, height=40, anchor="w", text_color="white", font=font_style)
num_shares_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
num_shares_entry = ctk.CTkEntry(inputs_frame, width=250, height=40, border_width=2, border_color="white", corner_radius=15, font=font_style)
num_shares_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

desired_profit_percentage_label = ctk.CTkLabel(inputs_frame, text="Desired Profit (%):", width=250, height=40, anchor="w", text_color="white", font=font_style)
desired_profit_percentage_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
desired_profit_percentage_entry = ctk.CTkEntry(inputs_frame, width=250, height=40, border_width=2, border_color="white", corner_radius=15, font=font_style)
desired_profit_percentage_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

desired_loss_percentage_label = ctk.CTkLabel(inputs_frame, text="Desired Loss (%):", width=250, height=40, anchor="w", text_color="white", font=font_style)
desired_loss_percentage_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
desired_loss_percentage_entry = ctk.CTkEntry(inputs_frame, width=250, height=40, border_width=2, border_color="white", corner_radius=15, font=font_style)
desired_loss_percentage_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

brokerage_constant_label = ctk.CTkLabel(inputs_frame, text="Brokerage Constant ($):", width=250, height=40, anchor="w", text_color="white", font=font_style)
brokerage_constant_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
brokerage_constant_entry = ctk.CTkEntry(inputs_frame, width=250, height=40, border_width=2, border_color="white", corner_radius=15, font=font_style)
brokerage_constant_entry.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

brokerage_percentage_label = ctk.CTkLabel(inputs_frame, text="Brokerage Percentage (%):", width=250, height=40, anchor="w", text_color="white", font=font_style)
brokerage_percentage_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
brokerage_percentage_entry = ctk.CTkEntry(inputs_frame, width=250, height=40, border_width=2, border_color="white", corner_radius=15, font=font_style)
brokerage_percentage_entry.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

# Create a button to calculate the prices and center it horizontally
calculate_button = ctk.CTkButton(root, text="Calculate", width=200, height=40, corner_radius=25, fg_color="black", border_width=2, border_color="grey", font=font_style, command=calculate_prices)
calculate_button.grid(row=6, column=0, columnspan=2, pady=20, sticky="n", padx=150)  # Center the button with padding

# Output labels in clean boxes
output_frame = ctk.CTkFrame(root, width=500, height=200, corner_radius=25)
output_frame.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
output_frame.grid_rowconfigure(0, weight=1)
output_frame.grid_columnconfigure(0, weight=1)

# Output labels in the specified order
total_investment_label = ctk.CTkLabel(output_frame, text="Total Investment: $0.00", width=300, height=40, anchor="w", text_color="white", font=font_style)
total_investment_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

profit_price_label = ctk.CTkLabel(output_frame, text="Price per share to sell for profit: $0.00", width=300, height=40, anchor="w", text_color="green", font=font_style)
profit_price_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

total_profit_label = ctk.CTkLabel(output_frame, text="Total Profit: $0.00", width=300, height=40, anchor="w", text_color="green", font=font_style)
total_profit_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

loss_price_label = ctk.CTkLabel(output_frame, text="Price per share to sell for loss: $0.00", width=300, height=40, anchor="w", text_color="red", font=font_style)
loss_price_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

total_loss_label = ctk.CTkLabel(output_frame, text="Total Loss: $0.00", width=300, height=40, anchor="w", text_color="red", font=font_style)
total_loss_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

# Start the GUI event loop
root.mainloop()
