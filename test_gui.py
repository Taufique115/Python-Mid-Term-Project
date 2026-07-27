import tkinter as tk
import sys
import traceback
from manager import MessManager
from gui.admin_dashboard import AdminDashboard

def test_admin_navigation():
    print("Starting GUI Navigation Diagnostic...")
    root = tk.Tk()
    root.withdraw() # Hide the window since we are running headless
    
    manager = MessManager(data_dir="data")
    admin_user = manager.authenticate("admin01", "admin123")
    
    if not admin_user:
        print("Error: Admin user not found.")
        sys.exit(1)
        
    dashboard = AdminDashboard(root, manager, admin_user)
    
    # We want to iterate through the menus and call them
    menus = [
        ("Dashboard", dashboard.show_dashboard_summary),
        ("Manage Members", dashboard.show_member_mgmt),
        ("Meal Calendar", dashboard.show_meal_calendar),
        ("Weekly Menu", dashboard.show_menu_mgmt),
        ("Grocery & Cost", dashboard.show_grocery_mgmt),
        ("Payments & Dues", dashboard.show_payment_mgmt),
        ("Menu Requests", dashboard.show_requests_mgmt),
        ("Statistical Reports", dashboard.show_reports),
    ]
    
    success = True
    for name, action in menus:
        print(f"Testing view: {name}...")
        try:
            # Clear content frame
            for widget in dashboard.content_frame.winfo_children():
                widget.destroy()
            # Call action
            action()
            print(f"  [OK] {name} rendered without exceptions.")
        except Exception as e:
            print(f"  [ERROR] ERROR in {name}: {e}")
            traceback.print_exc()
            success = False
            
    root.destroy()
    if success:
        print("All views rendered successfully in test!")
    else:
        print("Some views failed to render.")

from gui.member_dashboard import MemberDashboard

def test_member_navigation():
    print("\nStarting Member Dashboard Navigation Diagnostic...")
    root = tk.Tk()
    root.withdraw()
    
    manager = MessManager(data_dir="data")
    member_user = manager.authenticate("S001", "pass01")
    
    if not member_user:
        print("Error: Member user S001 not found.")
        sys.exit(1)
        
    dashboard = MemberDashboard(root, manager, member_user)
    
    menus = [
        ("Member Dashboard", dashboard.show_home_view),
        ("Meal Calendar", dashboard.show_meal_calendar),
        ("Weekly Menu", dashboard.show_menu_mgmt),
        ("Menu Requests", dashboard.show_requests_mgmt),
        ("Payments & Dues", dashboard.show_payment_mgmt),
    ]
    
    success = True
    for name, action in menus:
        print(f"Testing member view: {name}...")
        try:
            for widget in dashboard.content_frame.winfo_children():
                widget.destroy()
            action()
            print(f"  [OK] {name} rendered without exceptions.")
        except Exception as e:
            print(f"  [ERROR] ERROR in {name}: {e}")
            traceback.print_exc()
            success = False
            
    root.destroy()
    if success:
        print("All Member views rendered successfully!")
    else:
        print("Some Member views failed to render.")

if __name__ == "__main__":
    test_admin_navigation()
    test_member_navigation()
