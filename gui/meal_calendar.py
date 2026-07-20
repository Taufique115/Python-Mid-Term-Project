import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, timedelta
from gui.widgets import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_DANGER, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, StyledButton
)

class MealCalendarView:
    def __init__(self, parent_frame, manager, user_profile):
        self.parent = parent_frame
        self.manager = manager
        self.user = user_profile  # Can be Student or Admin
        self.is_admin = (self.user.role == "admin")
        
        # Selected Student (for Admin mode)
        self.selected_student_id = self.user.student_id if not self.is_admin else None
        
        # Calendar State
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        
        # Heading
        self.header_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.title_lbl = tk.Label(
            self.header_frame,
            text="Meal ON/OFF Calendar",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.title_lbl.pack(side="left")
        
        # If Admin, add student selector dropdown
        if self.is_admin:
            selector_frame = tk.Frame(self.header_frame, bg=self.parent["bg"])
            selector_frame.pack(side="right")
            
            tk.Label(selector_frame, text="Select Member: ", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=self.parent["bg"]).pack(side="left")
            self.student_combobox = ttk.Combobox(selector_frame, state="readonly", width=25, font=FONT_BODY)
            self.student_combobox.pack(side="left", padx=5)
            self.student_combobox.bind("<<ComboboxSelected>>", self.on_student_change)
            self.refresh_student_list()
        else:
            self.selected_student_id = self.user.student_id
            
        # Calendar Navigation & Display Frame
        self.cal_card = tk.Frame(self.parent, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=15, pady=15)
        self.cal_card.pack(fill="both", expand=True, pady=10)
        
        # Calendar Header: Left Arrow, Month Title, Right Arrow
        self.nav_frame = tk.Frame(self.cal_card, bg=COLOR_PRIMARY, padx=5, pady=5)
        self.nav_frame.pack(fill="x", pady=(0, 10))
        
        self.prev_btn = tk.Button(self.nav_frame, text="◀", font=("Segoe UI", 10, "bold"), fg="#FFFFFF", bg=COLOR_PRIMARY, activebackground=COLOR_PRIMARY, relief="flat", bd=0, cursor="hand2", command=self.prev_month)
        self.prev_btn.pack(side="left", padx=10)
        
        self.month_lbl = tk.Label(self.nav_frame, text="", font=FONT_SUBHEADING, fg="#FFFFFF", bg=COLOR_PRIMARY)
        self.month_lbl.pack(side="left", fill="x", expand=True)
        
        self.next_btn = tk.Button(self.nav_frame, text="▶", font=("Segoe UI", 10, "bold"), fg="#FFFFFF", bg=COLOR_PRIMARY, activebackground=COLOR_PRIMARY, relief="flat", bd=0, cursor="hand2", command=self.next_month)
        self.next_btn.pack(side="right", padx=10)
        
        # Grid Frame
        self.grid_frame = tk.Frame(self.cal_card, bg=COLOR_CARD)
        self.grid_frame.pack(fill="both", expand=True)
        
        # Warning footer for students
        if not self.is_admin:
            warning_lbl = tk.Label(
                self.parent,
                text="⚠️ NOTE: Members can toggle meals from today's date up to the end of the current month.",
                font=FONT_BODY,
                fg=COLOR_DANGER,
                bg=self.parent["bg"],
                pady=10
            )
            warning_lbl.pack(fill="x")
            
        self.draw_calendar()

    def refresh_student_list(self):
        students = self.manager.get_all_students()
        student_strings = [f"{s.student_id} - {s.name}" for s in students]
        self.student_combobox["values"] = student_strings
        if student_strings:
            self.student_combobox.current(0)
            self.selected_student_id = students[0].student_id

    def on_student_change(self, event=None):
        sel = self.student_combobox.get()
        if sel:
            self.selected_student_id = sel.split(" - ")[0]
            self.draw_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.draw_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.draw_calendar()

    def draw_calendar(self):
        # Clear existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        # Update month label
        month_name = calendar.month_name[self.current_month]
        self.month_lbl.config(text=f"{month_name.upper()} {self.current_year}")
        
        # Setup column headers (Sun - Sat)
        days_headers = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for col_idx, day_name in enumerate(days_headers):
            lbl = tk.Label(
                self.grid_frame,
                text=day_name,
                font=("Segoe UI", 9, "bold"),
                fg=COLOR_TEXT_MUTED,
                bg=COLOR_CARD,
                pady=5
            )
            lbl.grid(row=0, column=col_idx, sticky="ew")
            self.grid_frame.columnconfigure(col_idx, weight=1, uniform="equal")
            
        # Generate calendar days matrix
        cal = calendar.Calendar(firstweekday=6)  # 6 = Sunday
        month_days = cal.monthdayscalendar(self.current_year, self.current_month)
        
        # Ensure we have active student ID
        if not self.selected_student_id:
            lbl = tk.Label(self.grid_frame, text="Please add and select a member first.", font=FONT_BODY, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD)
            lbl.grid(row=1, column=0, columnspan=7, pady=40)
            return
            
        # Draw cells
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        
        for row_idx, week in enumerate(month_days):
            self.grid_frame.rowconfigure(row_idx + 1, weight=1, uniform="equal")
            for col_idx, day_num in enumerate(week):
                cell_frame = tk.Frame(
                    self.grid_frame,
                    bg=COLOR_CARD,
                    highlightbackground="#F1F5F9",
                    highlightthickness=1,
                    bd=0
                )
                cell_frame.grid(row=row_idx + 1, column=col_idx, sticky="nsew", padx=2, pady=2)
                
                if day_num == 0:
                    # Empty day placeholder
                    cell_frame.config(bg="#F8FAFC")
                    continue
                    
                # Format date string
                date_str = f"{self.current_year}-{self.current_month:02d}-{day_num:02d}"
                
                # Fetch meal record
                rec = self.manager.get_meal(self.selected_student_id, date_str)
                
                # Determine status & off meals
                b, l, d = True, True, True
                if rec:
                    b, l, d = rec.breakfast, rec.lunch, rec.dinner
                    
                offs = []
                if not b: offs.append("Breakfast")
                if not l: offs.append("Lunch")
                if not d: offs.append("Dinner")
                
                if not offs:
                    btn_text = "Meal ON"
                    bg_color = COLOR_SUCCESS
                else:
                    bg_color = COLOR_DANGER
                    if len(offs) == 1:
                        btn_text = f"{offs[0]} OFF"
                    elif len(offs) == 2:
                        short_map = {"Breakfast": "B", "Lunch": "L", "Dinner": "D"}
                        btn_text = f"{short_map[offs[0]]} & {short_map[offs[1]]} OFF"
                    else:
                        btn_text = "Meal OFF"
                        
                hover_color = bg_color.replace("10B981", "0D9668").replace("EF4444", "DC2626")
                
                # Day Number Label (centered)
                day_lbl = tk.Label(
                    cell_frame,
                    text=str(day_num),
                    font=("Segoe UI", 11, "bold"),
                    fg=COLOR_TEXT_MAIN,
                    bg=COLOR_CARD
                )
                day_lbl.pack(pady=(6, 2))
                
                # Editability logic: Admin can edit any date.
                # Students can edit today's date and any future date (up to month end and beyond).
                now_dt = datetime.now()
                cell_date = datetime(self.current_year, self.current_month, day_num).date()
                today_date = now_dt.date()
                
                is_editable = self.is_admin or (cell_date >= today_date)
                
                if is_editable:
                    btn = tk.Button(
                        cell_frame,
                        text=btn_text,
                        font=("Segoe UI", 9, "bold"),
                        fg="#FFFFFF",
                        bg=bg_color,
                        activebackground=hover_color,
                        activeforeground="#FFFFFF",
                        relief="flat",
                        borderwidth=0,
                        padx=5,
                        pady=4,
                        cursor="hand2",
                        command=lambda d=date_str, n=day_num: self.edit_day_meals(d, n)
                    )
                    btn.pack(fill="x", side="bottom", padx=4, pady=4)
                else:
                    # Locked past day display (solid green/red badge, white text, non-clickable)
                    lbl = tk.Label(
                        cell_frame,
                        text=btn_text,
                        font=("Segoe UI", 9, "bold"),
                        fg="#FFFFFF",
                        bg=bg_color,
                        padx=5,
                        pady=4
                    )
                    lbl.pack(fill="x", side="bottom", padx=4, pady=4)

    def edit_day_meals(self, date_str, day_num):
        # Open detailed checkboxes dialog
        self.dialog = tk.Toplevel(self.parent.winfo_toplevel())
        self.dialog.title("Edit Meals Selection")
        self.dialog.geometry("300x280")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLOR_CARD)
        
        tk.Label(
            self.dialog,
            text=f"Configure Meals: {date_str}",
            font=FONT_SUBHEADING,
            fg=COLOR_PRIMARY,
            bg=COLOR_CARD
        ).pack(pady=15)
        
        # Load current status
        rec = self.manager.get_meal(self.selected_student_id, date_str)
        b_val = tk.BooleanVar(value=True)
        l_val = tk.BooleanVar(value=True)
        d_val = tk.BooleanVar(value=True)
        
        if rec:
            b_val.set(rec.breakfast)
            l_val.set(rec.lunch)
            d_val.set(rec.dinner)
            
        chk_frame = tk.Frame(self.dialog, bg=COLOR_CARD)
        chk_frame.pack(fill="x", padx=40, pady=10)
        
        c_b = tk.Checkbutton(chk_frame, text="Breakfast", variable=b_val, font=FONT_BODY, bg=COLOR_CARD, anchor="w", fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD)
        c_b.pack(fill="x", pady=5)
        
        c_l = tk.Checkbutton(chk_frame, text="Lunch", variable=l_val, font=FONT_BODY, bg=COLOR_CARD, anchor="w", fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD)
        c_l.pack(fill="x", pady=5)
        
        c_d = tk.Checkbutton(chk_frame, text="Dinner", variable=d_val, font=FONT_BODY, bg=COLOR_CARD, anchor="w", fg=COLOR_TEXT_MAIN, activebackground=COLOR_CARD)
        c_d.pack(fill="x", pady=5)
        
        btn = StyledButton(
            self.dialog,
            text="SAVE CHANGES",
            command=lambda: self.save_day_meals(date_str, b_val.get(), l_val.get(), d_val.get()),
            bg_color=COLOR_SUCCESS,
            hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"),
            width=15
        )
        btn.pack(pady=15)

    def save_day_meals(self, date_str, b, l, d):
        self.manager.set_meal(self.selected_student_id, date_str, b, l, d)
        self.dialog.destroy()
        self.draw_calendar()
