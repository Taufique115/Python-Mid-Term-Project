import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from gui.widgets import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_SUCCESS_HOVER, COLOR_WARNING, COLOR_DANGER, COLOR_BORDER,
    FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_MUTED, StyledButton, Card
)

class MemberDashboard:
    def __init__(self, root, manager, member_user):
        self.root = root
        self.manager = manager
        self.member = member_user
        
        # Configure root (Maximized Window Size)
        self.root.title("Member Portal - Student Mess Management System")
        try:
            self.root.state('zoomed')
        except Exception:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}")
        self.root.resizable(True, True)
        self.root.configure(bg=COLOR_BG)
        
        # Top panel
        self.top_panel = tk.Frame(self.root, bg=COLOR_PRIMARY, height=60)
        self.top_panel.pack(fill="x", side="top")
        self.top_panel.pack_propagate(False)
        
        # App Title in Header
        self.app_title_lbl = tk.Label(
            self.top_panel,
            text=f"🏠 {self.manager.config['mess_name']} | Member Portal",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg=COLOR_PRIMARY
        )
        self.app_title_lbl.pack(side="left", padx=20)
        
        # User details on right
        self.user_lbl = tk.Label(
            self.top_panel,
            text=f"Logged in as: {self.member.name} ({self.member.student_id})",
            font=FONT_BODY,
            fg="#FFFFFF",
            bg=COLOR_PRIMARY
        )
        self.user_lbl.pack(side="right", padx=20)
        
        # Main layout: Sidebar + Body
        self.main_container = tk.Frame(self.root, bg=COLOR_BG)
        self.main_container.pack(fill="both", expand=True)
        
        # Sidebar Frame
        self.sidebar = tk.Frame(self.main_container, bg=COLOR_CARD, width=210, highlightbackground=COLOR_BORDER, highlightthickness=1, bd=0)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)
        
        self.sidebar_buttons = []
        self.active_indicator = None
        
        self.create_sidebar_menu()
        
        # Main Body Content Frame (Dynamic)
        self.content_frame = tk.Frame(self.main_container, bg=COLOR_BG, padx=25, pady=25)
        self.content_frame.pack(fill="both", expand=True, side="left")
        
        # Load default screen (Member Home view)
        self.show_home_view()

    def create_sidebar_menu(self):
        menus = [
            ("🏠 Dashboard", self.show_home_view),
            ("🍽️ Meal Control", self.show_meal_calendar),
            ("📋 Weekly Menu", self.show_menu_mgmt),
            ("📝 Menu Suggestion", self.show_requests_mgmt),
            ("💰 My Bill & Dues", self.show_payment_mgmt),
        ]
        
        # Title in Sidebar
        sb_title = tk.Label(
            self.sidebar,
            text="MEMBER MENU",
            font=("Segoe UI", 9, "bold"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD,
            anchor="w",
            padx=15
        )
        sb_title.pack(fill="x", pady=(20, 10))
        
        for idx, (lbl, action) in enumerate(menus):
            # Create a frame for button + indicator
            btn_frame = tk.Frame(self.sidebar, bg=COLOR_CARD, height=42)
            btn_frame.pack(fill="x")
            btn_frame.pack_propagate(False)
            
            # Active indicator bar
            ind = tk.Frame(btn_frame, bg=COLOR_CARD, width=4)
            ind.pack(side="left", fill="y")
            
            btn = tk.Button(
                btn_frame,
                text=lbl,
                font=("Segoe UI", 10),
                fg=COLOR_TEXT_MAIN,
                bg=COLOR_CARD,
                activebackground="#EEF2FF",
                activeforeground=COLOR_PRIMARY,
                relief="flat",
                borderwidth=0,
                anchor="w",
                padx=15,
                cursor="hand2",
                command=lambda act=action, i=ind: self.navigate(act, i)
            )
            btn.pack(side="left", fill="both", expand=True)
            
            # Hover bindings
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#EEF2FF", fg=COLOR_PRIMARY))
            btn.bind("<Leave>", lambda e, b=btn: self._restore_btn_hover(b))
            
            # Set default indicator
            if idx == 0:
                self.active_indicator = ind
                self.active_indicator.config(bg=COLOR_PRIMARY)
                btn.config(font=("Segoe UI", 10, "bold"), fg=COLOR_PRIMARY, bg="#EEF2FF")
                self.active_btn = btn
                
            self.sidebar_buttons.append((btn, ind))
            
        # Spacer
        spacer = tk.Label(self.sidebar, bg=COLOR_CARD)
        spacer.pack(fill="both", expand=True)
        
        # Logout Button
        logout_btn = StyledButton(
            self.sidebar,
            text="🚪 LOG OUT",
            command=self.logout,
            bg_color=COLOR_CARD,
            fg_color=COLOR_DANGER,
            hover_bg=COLOR_BG,
            width=18
        )
        logout_btn.pack(pady=20)

    def _restore_btn_hover(self, btn):
        if btn == getattr(self, "active_btn", None):
            btn.config(bg="#EEF2FF", fg=COLOR_PRIMARY)
        else:
            btn.config(bg=COLOR_CARD, fg=COLOR_TEXT_MAIN)

    def navigate(self, action, indicator):
        # Reset all indicators
        for btn, ind in self.sidebar_buttons:
            ind.config(bg=COLOR_CARD)
            btn.config(font=("Segoe UI", 10), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
            
        # Highlight active
        indicator.config(bg=COLOR_PRIMARY)
        for btn, ind in self.sidebar_buttons:
            if ind == indicator:
                btn.config(font=("Segoe UI", 10, "bold"), fg=COLOR_PRIMARY, bg="#EEF2FF")
                self.active_btn = btn
                
        # Clear main content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Run action
        action()

    def show_home_view(self):
        # Title
        title_lbl = tk.Label(
            self.content_frame,
            text=f"Welcome back, {self.member.name}",
            font=FONT_HEADING,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG
        )
        title_lbl.pack(anchor="w", pady=(0, 20))
        
        # Cards Grid Frame
        grid_frame = tk.Frame(self.content_frame, bg=COLOR_BG)
        grid_frame.pack(fill="x", pady=10)
        grid_frame.columnconfigure((0, 1, 2), weight=1, uniform="equal")
        
        # Load statistics
        current_month = datetime.now().strftime("%Y-%m")
        
        # Count member meals this month with breakdown & cost calculation
        month_records = self.manager.get_monthly_meals(self.member.student_id, current_month)
        b_count = sum(1 for r in month_records if r.breakfast)
        l_count = sum(1 for r in month_records if r.lunch)
        d_count = sum(1 for r in month_records if r.dinner)
        total_meals = b_count + l_count + d_count
        
        meal_rate = self.manager.calculate_meal_rate(current_month)
        b_cost = b_count * meal_rate
        l_cost = l_count * meal_rate
        d_cost = d_count * meal_rate
        overall_cost = total_meals * meal_rate
        
        # Compute payments, dues, and advance balance
        monthly_payments = self.manager.get_monthly_payments(self.member.student_id, current_month)
        total_paid_month = sum(p.amount for p in monthly_payments)
        net_balance = total_paid_month - overall_cost
        
        if net_balance > 0:
            advance_amt = net_balance
            outstanding_due = 0.0
            card2_title = "ADVANCE BALANCE"
            card2_val = f"৳ {advance_amt:.2f}"
            card2_sub = f"• Outstanding Bill: ৳ 0.00\n• Advance Balance: ৳ {advance_amt:.2f}"
            card2_color = COLOR_SUCCESS
        elif net_balance < 0:
            advance_amt = 0.0
            outstanding_due = abs(net_balance)
            card2_title = "OUTSTANDING BILL"
            card2_val = f"৳ {outstanding_due:.2f}"
            card2_sub = f"• Outstanding Bill: ৳ {outstanding_due:.2f}\n• Advance Balance: ৳ 0.00"
            card2_color = COLOR_DANGER
        else:
            card2_title = "OUTSTANDING BILL"
            card2_val = "৳ 0.00"
            card2_sub = "• Outstanding Bill: ৳ 0.00\n• Advance Balance: ৳ 0.00"
            card2_color = COLOR_SUCCESS
        
        # Tomorrow's quick overview
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        tomorrow_record = self.manager.get_meal(self.member.student_id, tomorrow_str)
        
        if tomorrow_record:
            b_state = "ON" if tomorrow_record.breakfast else "OFF"
            l_state = "ON" if tomorrow_record.lunch else "OFF"
            d_state = "ON" if tomorrow_record.dinner else "OFF"
        else:
            b_state, l_state, d_state = "ON", "ON", "ON"
            
        t_val = "Tomorrow's Schedule"
        t_sub = f"• Breakfast: {b_state}\n• Lunch: {l_state}\n• Dinner: {d_state}"
        
        m_val = f"{total_meals} Meals (৳ {overall_cost:.2f})"
        m_sub = f"• Breakfast: ৳ {b_cost:.2f}\n• Lunch: ৳ {l_cost:.2f}\n• Dinner: ৳ {d_cost:.2f}"
        
        # Cards
        c1 = Card(grid_frame, title="Meals & Cost (Month)", value=m_val, subtitle=m_sub, highlight_color=COLOR_SUCCESS)
        c1.grid(row=0, column=0, padx=5, sticky="nsew")
        
        c2 = Card(grid_frame, title=card2_title, value=card2_val, subtitle=card2_sub, highlight_color=card2_color)
        c2.grid(row=0, column=1, padx=5, sticky="nsew")
        
        c3 = Card(grid_frame, title="Tomorrow's Meals", value=t_val, subtitle=t_sub, highlight_color=COLOR_PRIMARY)
        c3.grid(row=0, column=2, padx=5, sticky="nsew")
        
        # Detail panels
        detail_frame = tk.Frame(self.content_frame, bg=COLOR_BG)
        detail_frame.pack(fill="both", expand=True, pady=20)
        detail_frame.columnconfigure(0, weight=3) # Today's Meals Menu & Tomorrow's Quick Control
        detail_frame.columnconfigure(1, weight=2) # Hall Administration
        
        # Panel 1: Meal Controls
        p1 = tk.Frame(detail_frame, bg=COLOR_CARD, highlightbackground=COLOR_BORDER, highlightthickness=1, bd=0, padx=15, pady=15)
        p1.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        # Today's menu details
        tk.Label(p1, text="TODAY'S MENU SCHEDULE", font=FONT_SUBHEADING, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(anchor="w", pady=(0, 10))
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_menu = self.manager.get_menu(today_str)
        
        for meal_type in self.manager.MEAL_TYPES:
            f = tk.Frame(p1, bg=COLOR_CARD, pady=4)
            f.pack(fill="x")
            dishes = today_menu.get(meal_type, [])
            dishes_str = ", ".join(dishes) if dishes else "Not Configured"
            tk.Label(f, text=f"{meal_type}: ", font=("Segoe UI", 10, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(side="left")
            tk.Label(f, text=dishes_str, font=FONT_BODY, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(side="left")
            
        divider = tk.Frame(p1, bg=COLOR_BORDER, height=1)
        divider.pack(fill="x", pady=15)
        
        # Meal Serving Schedule (Timers) & Dynamic Upcoming Meal Badge
        now_time = datetime.now().time()
        if now_time < datetime.strptime("07:30", "%H:%M").time():
            upcoming_str = "Breakfast Meal (7:30 AM)"
        elif now_time < datetime.strptime("14:00", "%H:%M").time():
            upcoming_str = "Lunch Meal (2:00 PM)"
        elif now_time < datetime.strptime("22:00", "%H:%M").time():
            upcoming_str = "Dinner Meal (10:00 PM)"
        else:
            upcoming_str = "Breakfast Meal (7:30 AM)"

        t_hdr_frame = tk.Frame(p1, bg=COLOR_CARD)
        t_hdr_frame.pack(fill="x", pady=(0, 10))

        tk.Label(t_hdr_frame, text="MEAL SERVING SCHEDULE & TIMINGS", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(side="left")
        
        upcoming_badge = tk.Label(
            t_hdr_frame,
            text=f"⏳ Upcoming: {upcoming_str}",
            font=("Segoe UI", 9, "bold"),
            fg="#1E40AF",
            bg="#DBEAFE",
            padx=10,
            pady=3
        )
        upcoming_badge.pack(side="right")
        
        timings = [
            ("🌅 Breakfast Meal", "Served at 7:30 AM"),
            ("☀️ Lunch Meal", "Served at 2:00 PM"),
            ("🌙 Dinner Meal", "Served at 10:00 PM")
        ]
        
        for meal_name, serve_time in timings:
            t_frame = tk.Frame(p1, bg="#F8FAFC", highlightbackground=COLOR_BORDER, highlightthickness=1, bd=0, padx=12, pady=10)
            t_frame.pack(fill="x", pady=4)
            
            tk.Label(t_frame, text=meal_name, font=("Segoe UI", 10, "bold"), fg=COLOR_TEXT_MAIN, bg="#F8FAFC").pack(side="left")
            
            badge = tk.Label(t_frame, text=serve_time, font=("Segoe UI", 9, "bold"), fg="#FFFFFF", bg=COLOR_PRIMARY, padx=10, pady=4)
            badge.pack(side="right")
            
        # Panel 2: Mess Manager Contact Details
        p2 = tk.Frame(detail_frame, bg=COLOR_CARD, highlightbackground=COLOR_BORDER, highlightthickness=1, bd=0, padx=15, pady=15)
        p2.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        tk.Label(p2, text="MESS MANAGER CONTACT", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(anchor="w", pady=(0, 12))
        
        manager_info = [
            ("Manager Name", "Cristiano Messi Junior"),
            ("Contact Number", "01710112341"),
            ("Email Address", "cristianomessineymar@gmail.com"),
            ("Address Location", "House #11, Road #05, Block C,\nBashundhara, Dhaka")
        ]
        
        for field, val in manager_info:
            c_frame = tk.Frame(p2, bg=COLOR_CARD, pady=3)
            c_frame.pack(fill="x")
            
            tk.Label(c_frame, text=f"• {field}:", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, anchor="w").pack(fill="x")
            tk.Label(c_frame, text=val, font=("Segoe UI", 10, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD, anchor="w", justify="left").pack(fill="x", padx=(10, 0))
            
            divider_sub = tk.Frame(p2, bg=COLOR_BORDER, height=1)
            divider_sub.pack(fill="x", pady=3)

    def save_tomorrow_meals(self):
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")
        
        b = self.b_var.get()
        l = self.l_var.get()
        d = self.d_var.get()
        
        self.manager.set_meal(self.member.student_id, tomorrow_str, b, l, d)
        messagebox.showinfo("Success", f"Your meals for tomorrow ({tomorrow_str}) have been updated successfully!")
        
        # Refresh current view card stats
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.show_home_view()

    def show_meal_calendar(self):
        from gui.meal_calendar import MealCalendarView
        MealCalendarView(self.content_frame, self.manager, self.member)

    def show_menu_mgmt(self):
        from gui.menu_mgmt import MenuMgmtView
        MenuMgmtView(self.content_frame, self.manager, self.member)

    def show_requests_mgmt(self):
        from gui.requests_mgmt import RequestsMgmtView
        RequestsMgmtView(self.content_frame, self.manager, self.member)

    def show_payment_mgmt(self):
        from gui.payment_mgmt import PaymentMgmtView
        PaymentMgmtView(self.content_frame, self.manager, self.member)

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            from gui.login_window import LoginWindow
            LoginWindow(self.root, self.manager)
