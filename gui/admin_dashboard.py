import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from gui.widgets import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER, COLOR_BORDER,
    FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_MUTED, StyledButton, Card
)
import calculations as calc

class AdminDashboard:
    def __init__(self, root, manager, admin_user):
        self.root = root
        self.manager = manager
        self.admin_user = admin_user
        
        # Configure root (Default Maximized Window Size, fully resizable & minimizable)
        self.root.title("Admin Panel - Student Mess Management System")
        self.root.minsize(1024, 600)
        self.root.resizable(True, True)
        try:
            self.root.state('zoomed')
        except Exception:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}")
        self.root.configure(bg=COLOR_BG)
        
        # Top panel
        self.top_panel = tk.Frame(self.root, bg=COLOR_PRIMARY, height=60)
        self.top_panel.pack(fill="x", side="top")
        self.top_panel.pack_propagate(False)
        
        # App Title in Header
        self.app_title_lbl = tk.Label(
            self.top_panel,
            text=f"🏠 {self.manager.config['mess_name']} | Admin Panel",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg=COLOR_PRIMARY
        )
        self.app_title_lbl.pack(side="left", padx=20)
        
        # User details on right
        welcome_title = "Mess Manager" if ("Mess Manager" in self.admin_user.name or "Provost" in self.admin_user.name) else self.admin_user.name
        self.user_lbl = tk.Label(
            self.top_panel,
            text=f"Welcome, {welcome_title} (Admin)",
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
        
        # Sidebar Buttons & active indicator trackers
        self.sidebar_buttons = []
        self.active_indicator = None
        
        self.create_sidebar_menu()
        
        # Main Body Content Frame (Dynamic)
        self.content_frame = tk.Frame(self.main_container, bg=COLOR_BG, padx=25, pady=25)
        self.content_frame.pack(fill="both", expand=True, side="left")
        
        # Load default screen (Dashboard view)
        self.show_dashboard_summary()

    def create_sidebar_menu(self):
        # Menu definitions: (Label, Action)
        menus = [
            ("🏠 Dashboard", self.show_dashboard_summary),
            ("👥 Manage Members", self.show_member_mgmt),
            ("🍽️ Meal Calendar", self.show_meal_calendar),
            ("📋 Weekly Menu", self.show_menu_mgmt),
            ("🛒 Grocery & Cost", self.show_grocery_mgmt),
            ("💰 Payments & Dues", self.show_payment_mgmt),
            ("📝 Menu Requests", self.show_requests_mgmt),
            ("📊 Statistical Reports", self.show_reports),
        ]
        
        # Title in Sidebar
        sb_title = tk.Label(
            self.sidebar,
            text="NAVIGATION",
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

    def show_dashboard_summary(self):
        # Title
        title_lbl = tk.Label(
            self.content_frame,
            text="Dashboard Overview",
            font=FONT_HEADING,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_BG
        )
        title_lbl.pack(anchor="w", pady=(0, 20))
        
        # Cards Grid Frame (5 Columns)
        grid_frame = tk.Frame(self.content_frame, bg=COLOR_BG)
        grid_frame.pack(fill="x", pady=10)
        grid_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="equal")
        
        # Get statistics values
        current_month = datetime.now().strftime("%Y-%m")
        
        members_count = len(self.manager.get_all_students())
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        b_count, l_count, d_count = self.manager.get_all_meals_on_date(today_str)
        today_meals = b_count + l_count + d_count
        
        monthly_total_meals = self.manager.count_all_meals_in_month(current_month)
        
        monthly_exp = self.manager.get_monthly_expense(current_month)
        
        # Calculate dues summary
        dues_summary = calc.get_due_summary(self.manager.get_all_students(), current_month, self.manager)
        total_dues = dues_summary["sum"]
        
        # Instantiate Cards (5 Top Cards)
        c1 = Card(grid_frame, title="Total Members", value=f"{members_count} Active", highlight_color=COLOR_PRIMARY)
        c1.grid(row=0, column=0, padx=4, sticky="nsew")
        
        c2 = Card(grid_frame, title="Today's Meals", value=f"{today_meals} Meals", highlight_color=COLOR_SUCCESS)
        c2.grid(row=0, column=1, padx=4, sticky="nsew")
        
        c3 = Card(grid_frame, title="Monthly Total Meals", value=f"{monthly_total_meals} Meals", highlight_color="#8B5CF6")
        c3.grid(row=0, column=2, padx=4, sticky="nsew")
        
        c4 = Card(grid_frame, title="Monthly Expense", value=f"৳ {monthly_exp:.2f}", highlight_color=COLOR_WARNING)
        c4.grid(row=0, column=3, padx=4, sticky="nsew")
        
        c5 = Card(grid_frame, title="Total Outstanding Dues", value=f"৳ {total_dues:.2f}", highlight_color=COLOR_DANGER)
        c5.grid(row=0, column=4, padx=4, sticky="nsew")
        
        # Detail panels
        detail_frame = tk.Frame(self.content_frame, bg=COLOR_BG)
        detail_frame.pack(fill="both", expand=True, pady=20)
        detail_frame.columnconfigure(0, weight=3) # Today's Meal Details
        detail_frame.columnconfigure(1, weight=2) # Mess Manager Contact
        
        # Panel 1: Today's meal levels
        p1 = tk.Frame(detail_frame, bg=COLOR_CARD, highlightbackground=COLOR_BORDER, highlightthickness=1, bd=0, padx=15, pady=15)
        p1.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        tk.Label(p1, text="TODAY'S MEAL PARTICIPATION DETAILS", font=FONT_SUBHEADING, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(anchor="w", pady=(0, 10))
        
        # Progress-like displays
        meal_labels = [("Breakfast", b_count), ("Lunch", l_count), ("Dinner", d_count)]
        for label, count in meal_labels:
            m_frame = tk.Frame(p1, bg=COLOR_CARD, pady=8)
            m_frame.pack(fill="x")
            
            # Text label + count
            tk.Label(m_frame, text=label, font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(side="left")
            
            rate = calc.get_meal_participation_rate(today_str, members_count, count)
            tk.Label(m_frame, text=f"{count} Members ({rate:.1f}%)", font=("Segoe UI", 10, "bold"), fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(side="right")
            
            # Progress track bar
            t_bar = tk.Frame(p1, bg="#E2E8F0", height=8)
            t_bar.pack(fill="x", pady=(0, 10))
            
            fill_width = int(rate) # 0 to 100
            if fill_width > 0:
                f_bar = tk.Frame(t_bar, bg=COLOR_PRIMARY, height=8)
                f_bar.place(x=0, y=0, relwidth=rate/100.0)
                
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
            c_frame = tk.Frame(p2, bg=COLOR_CARD, pady=4)
            c_frame.pack(fill="x")
            
            tk.Label(c_frame, text=f"• {field}:", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, anchor="w").pack(fill="x")
            tk.Label(c_frame, text=val, font=("Segoe UI", 10, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD, anchor="w", justify="left").pack(fill="x", padx=(10, 0))
            
            divider_sub = tk.Frame(p2, bg=COLOR_BORDER, height=1)
            divider_sub.pack(fill="x", pady=4)

    def show_member_mgmt(self):
        from gui.member_mgmt import MemberMgmtView
        MemberMgmtView(self.content_frame, self.manager)

    def show_meal_calendar(self):
        from gui.meal_calendar import MealCalendarView
        MealCalendarView(self.content_frame, self.manager, self.admin_user)

    def show_menu_mgmt(self):
        from gui.menu_mgmt import MenuMgmtView
        MenuMgmtView(self.content_frame, self.manager, self.admin_user)

    def show_grocery_mgmt(self):
        from gui.grocery_mgmt import GroceryMgmtView
        GroceryMgmtView(self.content_frame, self.manager, self.admin_user)

    def show_payment_mgmt(self):
        from gui.payment_mgmt import PaymentMgmtView
        PaymentMgmtView(self.content_frame, self.manager, self.admin_user)

    def show_requests_mgmt(self):
        from gui.requests_mgmt import RequestsMgmtView
        RequestsMgmtView(self.content_frame, self.manager, self.admin_user)

    def show_reports(self):
        from gui.reports import ReportsView
        ReportsView(self.content_frame, self.manager)

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            from gui.login_window import LoginWindow
            LoginWindow(self.root, self.manager)
