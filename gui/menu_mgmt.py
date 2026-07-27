import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from gui.widgets import (
    COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_WARNING, FONT_SUBHEADING, FONT_BODY,
    StyledButton, LabeledEntry, create_scrollable_tree
)
import validators as val

class MenuMgmtView:
    def __init__(self, parent_frame, manager, user_profile):
        self.parent = parent_frame
        self.manager = manager
        self.user = user_profile
        self.is_admin = (self.user.role == "admin")
        
        # Current Date state (week beginning)
        now = datetime.now()
        # Find start of current week (e.g. Sunday)
        idx = (now.weekday() + 1) % 7 # Mon=0, Tue=1 ... Sun=6 -> Sun=0, Mon=1
        self.week_start = now - timedelta(days=idx)
        
        # Heading
        self.header_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.title_lbl = tk.Label(
            self.header_frame,
            text="Weekly Meal Menu Schedule",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.title_lbl.pack(side="left")
        
        # Week Nav Frame
        self.nav_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.nav_frame.pack(fill="x", pady=(0, 10))
        
        self.prev_btn = StyledButton(self.nav_frame, "◀ Previous Week", self.prev_week, width=15)
        self.prev_btn.pack(side="left")
        
        self.week_lbl = tk.Label(
            self.nav_frame,
            text="",
            font=FONT_SUBHEADING,
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.week_lbl.pack(side="left", fill="x", expand=True)
        
        self.next_btn = StyledButton(self.nav_frame, "Next Week ▶", self.next_week, width=15)
        self.next_btn.pack(side="right")
        
        # Actions for admin
        if self.is_admin:
            self.edit_btn = StyledButton(self.nav_frame, "Edit Selected Row", self.open_edit_dialog, bg_color=COLOR_WARNING, hover_bg=COLOR_WARNING.replace("F59E0B", "D98006"), width=18)
            self.edit_btn.pack(side="right", padx=10)
            
        # Treeview Table
        cols = ("date", "day", "breakfast", "lunch", "dinner")
        hdgs = ("Date", "Day of Week", "Breakfast Menu", "Lunch Menu", "Dinner Menu")
        widths = {"date": 110, "day": 110}
        
        self.table_frame, self.tree = create_scrollable_tree(self.parent, cols, hdgs, widths)
        self.table_frame.pack(fill="both", expand=True)
        
        # Add custom highlight tag for today
        self.tree.tag_configure("today", background="#EEF2FF", foreground="#4F46E5", font=("Segoe UI", 10, "bold"))
        
        self.update_menu_display()

    def prev_week(self):
        self.week_start -= timedelta(days=7)
        self.update_menu_display()

    def next_week(self):
        self.week_start += timedelta(days=7)
        self.update_menu_display()

    def update_menu_display(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        end_date = self.week_start + timedelta(days=6)
        self.week_lbl.config(
            text=f"Week: {self.week_start.strftime('%d %b %Y')}  to  {end_date.strftime('%d %b %Y')}"
        )
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # Fetch 7 days menu
        weekly_menu = self.manager.get_weekly_menu(self.week_start)
        
        for i in range(7):
            curr_date = self.week_start + timedelta(days=i)
            date_str = curr_date.strftime("%Y-%m-%d")
            day_name = curr_date.strftime("%A")
            
            day_menu = weekly_menu.get(date_str, {})
            b_dish = ", ".join(day_menu.get("Breakfast", []))
            l_dish = ", ".join(day_menu.get("Lunch", []))
            d_dish = ", ".join(day_menu.get("Dinner", []))
            
            # Setup tags
            tags = ()
            if date_str == today_str:
                tags = ("today",)
            else:
                tags = ("even",) if i % 2 == 0 else ("odd",)
                
            self.tree.insert(
                "",
                "end",
                iid=date_str,
                values=(date_str, day_name, b_dish or "Not Configured", l_dish or "Not Configured", d_dish or "Not Configured"),
                tags=tags
            )

    def open_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a date row to edit.")
            return
            
        date_str = selected[0]
        
        # Toplevel Dialog
        self.dialog = tk.Toplevel(self.parent.winfo_toplevel())
        self.dialog.title(f"Configure Menu: {date_str}")
        self.dialog.geometry("380x420")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLOR_CARD)
        
        tk.Label(
            self.dialog,
            text=f"Edit Weekly Menu: {date_str}",
            font=FONT_SUBHEADING,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD
        ).pack(pady=15)
        
        # Load current
        curr_menu = self.manager.get_menu(date_str)
        
        self.f_b = LabeledEntry(self.dialog, "Breakfast dishes (comma separated)")
        self.f_b.pack(fill="x", padx=30, pady=5)
        self.f_b.set(", ".join(curr_menu.get("Breakfast", [])))
        
        self.f_l = LabeledEntry(self.dialog, "Lunch dishes (comma separated)")
        self.f_l.pack(fill="x", padx=30, pady=5)
        self.f_l.set(", ".join(curr_menu.get("Lunch", [])))
        
        self.f_d = LabeledEntry(self.dialog, "Dinner dishes (comma separated)")
        self.f_d.pack(fill="x", padx=30, pady=5)
        self.f_d.set(", ".join(curr_menu.get("Dinner", [])))
        
        # Save btn
        save = StyledButton(
            self.dialog,
            text="SAVE SCHEDULE",
            command=lambda: self.save_schedule(date_str),
            bg_color=COLOR_SUCCESS,
            hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"),
            width=15
        )
        save.pack(pady=20)

    def save_schedule(self, date_str):
        b_txt = self.f_b.get()
        l_txt = self.f_l.get()
        d_txt = self.f_d.get()
        
        # Validate (optional, could be empty if they want to clear it, but let's allow it or validate length)
        # We will split on commas
        self.manager.set_menu(date_str, "Breakfast", b_txt)
        self.manager.set_menu(date_str, "Lunch", l_txt)
        self.manager.set_menu(date_str, "Dinner", d_txt)
        
        messagebox.showinfo("Success", f"Meal schedule updated for {date_str}!", parent=self.dialog)
        self.dialog.destroy()
        self.update_menu_display()
