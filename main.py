import tkinter as tk
import os
from manager import MessManager
from gui.login_window import LoginWindow
from gui.widgets import COLOR_BG

def main():
    # Ensure data and report directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("report", exist_ok=True)
    
    # Initialize Business Logic Manager
    # This automatically loads previous data from files and seeds defaults if empty
    manager = MessManager(data_dir="data")
    
    # Create Root Window (Maximized Window Size)
    root = tk.Tk()
    root.title("Mess Member Management System")
    try:
        root.state('zoomed')
    except Exception:
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"{sw}x{sh}")
    root.configure(bg=COLOR_BG)
    
    # Icon or styling configurations could go here if available
    # Set default app-wide styles
    root.option_add("*Font", "{Segoe UI} 10")
    
    # Initialize the Login Interface
    LoginWindow(root, manager)
    
    # Start Event Loop
    root.mainloop()

if __name__ == "__main__":
    main()
