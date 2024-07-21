#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script sumarizes all Deposits and Withdrawals of your IBKR (Interactive Brokers) PRO account.
"""

__author__ = "Martin Pucovski"
__copyright__ = "Copyright 2024, Martin Pucovski"
__credits__ = ["Martin Pucovski"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Martin Pucovski"
__email__ = "N/A"
__status__ = "Production"

import configparser
import datetime
import logging
from pathlib import Path
import sys
import os
import tkinter as tk
from tkinter import font, messagebox
from get_data import GetData

# -------------------------------------------------- #
# SET INITIAL CONSTANTS

# Get config file name from argument
if len(sys.argv) > 1:
    CONFIG_NAME = sys.argv[1]
else:
    CONFIG_NAME = "config_DEFAULT.ini"

PROJECT_DIRECTORY = Path(os.getcwd())
LOGS_FOLDER = "logs"
DATA_FOLDER = "data"  # Define data folder
DATA_PATH = Path(PROJECT_DIRECTORY) / DATA_FOLDER

# Ensure the config directory exists
CONFIG_FOLDER = "config"
CONFIG_PATH = Path(PROJECT_DIRECTORY) / CONFIG_FOLDER
CONFIG_PATH.mkdir(parents=True, exist_ok=True)

# Ensure the data directory exists
DATA_PATH.mkdir(parents=True, exist_ok=True)

# Create the default config file if it does not exist
default_config_file = CONFIG_PATH / "config_DEFAULT.ini"
if not default_config_file.exists():
    with open(default_config_file, 'w') as config_file:
        config_file.write("[DEFAULT]\n")
        config_file.write("Project_Environment = PROD\n")
        config_file.write("Loggin_Level = INFO\n")

# -------------------------------------------------- #
# READ CONFIG FILE

# Read main config file
config = configparser.ConfigParser()
config_path = Path(PROJECT_DIRECTORY) / "config" / CONFIG_NAME
config.read(config_path)
config_default = config["DEFAULT"]

# -------------------------------------------------- #
# SET LOGGING

# Ensure the logs directory exists
logs_directory = Path(PROJECT_DIRECTORY) / LOGS_FOLDER
logs_directory.mkdir(parents=True, exist_ok=True)

current_date = datetime.datetime.now().strftime("%Y%m%d")
log_file_name = f"log_{current_date}.log"
log_file = logs_directory / log_file_name

file_handler = logging.FileHandler(
    filename=log_file, mode="a", encoding=None, delay=False)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(handlers=handlers,
                    encoding='utf-8',
                    level=os.environ.get(
                        "LOGLEVEL", config_default['Loggin_Level']),
                    format='%(asctime)s:%(levelname)s:%(message)s')

# -------------------------------------------------- #

logging.info("# ------------------------------ #")

def check_data_folder_empty(folder_path):
    """Check if the data folder is empty."""
    return not any(folder_path.iterdir())


def format_number_with_spaces(number):
    """Formats a number with a space as thousands separator."""
    try:
        number_str = f"{float(number):,.2f}"
        # Replace commas with spaces
        formatted_number = number_str.replace(",", " ")
        return formatted_number
    except ValueError:
        return number


def main():
    """
    Main function of the script
    """
    logging.info("Script started")

    # Check if the data folder is empty
    data_folder_empty = not any(DATA_PATH.iterdir())  # Check if the folder is empty

    placeholder = GetData("data")

    sum_deposits = placeholder.sum_deposits()
    last_nav = placeholder.last_nav()
    sum_withdrawals = placeholder.sum_withdrawals()

    # Create the main window
    window = tk.Tk()
    window.title("IBKR Report Analyzer")
    window.configure(bg="#f0f0f0")

    # Define window size
    window_width = 460
    window_height = 280

    # Set the fixed window size
    window.geometry(f"{window_width}x{window_height}")

    # Define a custom font
    custom_font = font.Font(family="Helvetica", size=12, weight="bold")

    # Function to create a styled table row
    def create_table_row(row, text, value, value_bg="#ffffff"):
        text_label = tk.Label(window, text=text, font=custom_font, bg="#f0f0f0", fg="#333333", pady=10, padx=5, relief="solid", borderwidth=1, anchor="w")
        text_label.grid(row=row, column=0, sticky="ew", padx=(20, 5))
        
        formatted_value = format_number_with_spaces(value)
        value_label = tk.Label(window, text=formatted_value, font=custom_font, bg=value_bg, fg="#333333", pady=10, padx=5, relief="solid", borderwidth=1, anchor="e")
        value_label.grid(row=row, column=1, sticky="ew", padx=(5, 20))

    # Add a title label
    title_label = tk.Label(window, text="IBKR Report Summary", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#003366", pady=10)
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # Create table rows for each piece of data
    create_table_row(1, "Sum of all deposits:", format_number_with_spaces(f"{sum_deposits:.2f}"))
    create_table_row(2, "Sum of all withdrawals:", format_number_with_spaces(f"{sum_withdrawals:.2f}"))
    create_table_row(3, "Last NAV:", format_number_with_spaces(f"{last_nav:.2f}"))

    # Calculate and create table row for unrealized profit
    calculated_profit = float(last_nav) - float(sum_deposits)
    if calculated_profit > 0:
        profit_bg = "#d4edda"  # light green
    elif calculated_profit < 0:
        profit_bg = "#f8d7da"  # light red
    else:
        profit_bg = "#ffffff"  # white

    create_table_row(4, "Unrealized Profit:", format_number_with_spaces(f"{calculated_profit:.2f}"), value_bg=profit_bg)

    # Create a notification label for empty data folder
    notification_label = tk.Label(window, text="", font=("Helvetica", 12, "italic"), fg="#ff0000", bg="#f0f0f0")
    notification_label.grid(row=5, column=0, columnspan=2, pady=(10, 20))
    
    if data_folder_empty:
        notification_label.config(text="Warning: The data folder is empty.")

    # Configure column weights to make sure they expand equally
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Center the window on the screen
    window.update_idletasks()  # Update the window to get its final size

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry to center it on the screen
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Start the main event loop
    window.mainloop()

    # Print statements for console output
    print(f"Sum of all deposits: {format_number_with_spaces(f'{sum_deposits:.2f}')}")
    print(f"Sum of all withdrawals: {format_number_with_spaces(f'{sum_withdrawals:.2f}')}")
    print(f"Last NAV: {format_number_with_spaces(f'{last_nav:.2f}')}")
    print(f"Unrealized Profit: {format_number_with_spaces(f'{calculated_profit:.2f}')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)


logging.info("Script ended")
logging.info("# ------------------------------ #")
