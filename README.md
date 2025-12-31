# Stock Price Calculator - GUI Application

This Python application calculates various price points and metrics for stock investments based on user input. It is built using `customtkinter` for an enhanced graphical interface.

## Features

- Input stock price, number of shares, brokerage details, and profit/loss percentages.
- Calculates:
  - Total investment amount.
  - Selling price per share for desired profit or loss.
  - Total profit or loss.
- Clean, user-friendly GUI with dark mode.

---

## Prerequisites

Ensure you have Python installed along with the following modules:
- `customtkinter`
- `tkinter`

Install `customtkinter` via pip if not already installed:
```bash
pip install customtkinter
```

---

## How to Run

1. Save the code to a file, e.g., `stock_calculator.py`.
2. Run the script:
   ```bash
   python stock_calculator.py
   ```
3. The GUI window will appear. Fill in the input fields and press "Calculate" to see the results.

---

## Inputs

| Input Field                 | Description                                               | Data Type |
|-----------------------------|-----------------------------------------------------------|-----------|
| **Current Stock Price ($)** | The price of a single share of stock currently.           | Float     |
| **Number of Shares**        | The total number of shares you own.                      | Float     |
| **Desired Profit (%)**      | Your desired profit percentage.                          | Float     |
| **Desired Loss (%)**        | Your acceptable loss percentage.                         | Float     |
| **Brokerage Constant ($)**  | The fixed brokerage fee applied to each transaction.     | Float     |
| **Brokerage Percentage (%)**| The percentage-based brokerage fee per transaction.      | Float     |

---

## Outputs

| Output Field                             | Description                                                                 |
|------------------------------------------|-----------------------------------------------------------------------------|
| **Total Investment ($)**                 | The total amount invested in the stock (Price × Shares).                   |
| **Price per share to sell for profit ($)**| The minimum price per share required to achieve the desired profit.         |
| **Total Profit ($)**                     | The total profit calculated for the specified number of shares.            |
| **Price per share to sell for loss ($)** | The price per share required to cap the loss at the specified percentage.  |
| **Total Loss ($)**                       | The total loss calculated for the specified number of shares.              |

---

## How It Works

1. **Input Validation**: Ensures all inputs are numeric and within valid ranges.
2. **Calculations**:
   - **Investment**: Calculated as `Current Price × Number of Shares`.
   - **Profit/Loss Selling Price**:
     - Factors in both fixed and percentage-based brokerage fees.
     - Considers desired profit or loss percentages.
   - **Brokerage Threshold**: Determines whether to use fixed or percentage-based brokerage.
   - **Final Profit/Loss**: Considers total costs and fees for accurate results.
3. **Dynamic Output**: Updates the GUI with calculated values in real-time.

---

## Error Handling

- Displays an error message if:
  - Non-numeric values are entered.
  - Percentage values are invalid (e.g., negative percentages).

---

## GUI Layout

### Inputs
- Labels and input fields for all required parameters.
- Neatly arranged for ease of use.

### Outputs
- Real-time display of investment, profit, and loss results.
- Color-coded output:
  - **Green** for profit-related values.
  - **Red** for loss-related values.

---

## Example Usage

1. Enter the following:
   - **Current Stock Price**: 100
   - **Number of Shares**: 10
   - **Desired Profit**: 20
   - **Desired Loss**: 10
   - **Brokerage Constant**: 2
   - **Brokerage Percentage**: 0.5
2. Press "Calculate".
3. View results:
   - Total Investment: `$1000.00`
   - Profit Price per Share: `$122.00`
   - Total Profit: `$220.00`
   - Loss Price per Share: `$98.00`
   - Total Loss: `$20.00`

---

## Notes

- This tool is for educational purposes and may not account for all trading scenarios.
- Verify calculations independently for critical financial decisions.

---

## Rust Implementation

A Rust version of this application is available in the `stock_calculator_rs` directory. It uses `egui` for a high-performance, cross-platform GUI.

### How to Run (Rust)

1. **Install Rust**: Ensure you have Rust and Cargo installed from [rustup.rs](https://rustup.rs/).
2. **Navigate to the directory**:
   ```powershell
   cd stock_calculator_rs
   ```
3. **Run**:
   ```powershell
   cargo run --release
   ```

### Troubleshooting
If you encounter a `dlltool.exe` not found error (common on Windows MinGW setups), add the following to your PATH:
```powershell
$env:PATH = "C:\msys64\ucrt64\bin;$env:PATH"
```
