import tkinter as tk
from tkinter import messagebox
from gui.widgets import (
    COLOR_BG, COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_DANGER, FONT_HEADING, FONT_SUBHEADING, FONT_BODY,
    StyledButton, LabeledEntry
)

class LoginWindow:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        # Configure root window (Default Maximized, resizable & minimizable)
        self.root.title("Portal Selection - Student Mess Management System")
        self.root.minsize(600, 500)
        self.root.resizable(True, True)
        try:
            self.root.state('zoomed')
        except Exception:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}")
        self.root.configure(bg=COLOR_BG)
        
        # Draw Landing Selection Screen initially
        self.show_landing_screen()

    def clear_screen(self):
        # Unbind Return key if bound
        self.root.unbind("<Return>")
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_landing_screen(self):
        self.clear_screen()
        self.root.title("Portal Selection - Student Mess Management System")
        
        # Draw shadow card
        self.card = tk.Frame(
            self.root, 
            bg=COLOR_CARD, 
            highlightbackground="#E2E8F0", 
            highlightthickness=1, 
            bd=0
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=460)
        
        # Headings
        tk.Label(
            self.card, 
            text="AIUB BLUE BIRD MESS", 
            font=FONT_HEADING, 
            fg=COLOR_PRIMARY, 
            bg=COLOR_CARD
        ).pack(pady=(40, 5))
        
        tk.Label(
            self.card, 
            text="Mess Member & Admin Portal", 
            font=FONT_BODY, 
            fg=COLOR_TEXT_MUTED, 
            bg=COLOR_CARD
        ).pack(pady=(0, 40))
        
        tk.Label(
            self.card, 
            text="SELECT LOGIN PORTAL TYPE", 
            font=("Segoe UI", 9, "bold"), 
            fg=COLOR_TEXT_MAIN, 
            bg=COLOR_CARD
        ).pack(pady=(0, 20))
        
        # Selection Buttons
        admin_btn = StyledButton(
            self.card,
            text="🔐 ADMINISTRATOR LOGIN",
            command=lambda: self.show_login_form("admin"),
            bg_color=COLOR_PRIMARY,
            hover_bg=COLOR_PRIMARY.replace("5C67F2", "4A54D4"),
            width=24
        )
        admin_btn.pack(pady=10)
        
        member_btn = StyledButton(
            self.card,
            text="👥 MESS MEMBER LOGIN",
            command=lambda: self.show_login_form("student"),
            bg_color=COLOR_SUCCESS,
            hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"),
            width=24
        )
        member_btn.pack(pady=10)
        
        # Footer
        tk.Label(
            self.card,
            text="AIUB Blue Bird Mess Management System Inc.",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_CARD
        ).pack(side="bottom", pady=25)

    def show_login_form(self, role):
        self.clear_screen()
        
        # Card container
        self.card = tk.Frame(
            self.root, 
            bg=COLOR_CARD, 
            highlightbackground="#E2E8F0", 
            highlightthickness=1, 
            bd=0
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=480)
        
        # Header text by role
        if role == "admin":
            title_text = "ADMINISTRATOR LOGIN"
            theme_color = COLOR_PRIMARY
            self.root.title("Admin Login - Student Mess Management System")
        else:
            title_text = "MESS MEMBER LOGIN"
            theme_color = COLOR_SUCCESS
            self.root.title("Member Login - Student Mess Management System")
            
        tk.Label(
            self.card, 
            text=title_text, 
            font=FONT_HEADING, 
            fg=theme_color, 
            bg=COLOR_CARD
        ).pack(pady=(35, 5))
        
        tk.Label(
            self.card, 
            text="Enter your access credentials below", 
            font=FONT_BODY, 
            fg=COLOR_TEXT_MUTED, 
            bg=COLOR_CARD
        ).pack(pady=(0, 25))
        
        # Fields
        label_id = "Admin Username" if role == "admin" else "Member ID (e.g. S001)"
        self.id_field = LabeledEntry(self.card, label_id)
        self.id_field.pack(fill="x", padx=35, pady=8)
        
        self.pwd_field = LabeledEntry(self.card, "Password", is_password=True)
        self.pwd_field.pack(fill="x", padx=35, pady=8)
        
        # Status Label for feedback
        self.error_lbl = tk.Label(
            self.card, 
            text="", 
            font=FONT_BODY, 
            fg="#EF4444", 
            bg=COLOR_CARD,
            wraplength=300
        )
        self.error_lbl.pack(pady=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.card, bg=COLOR_CARD)
        btn_frame.pack(pady=(5, 10))
        
        login_btn = StyledButton(
            btn_frame, 
            text="LOG IN", 
            command=lambda: self.handle_login(role),
            bg_color=theme_color,
            hover_bg=theme_color.replace("5C67F2", "4A54D4").replace("10B981", "0D9668"),
            width=12
        )
        login_btn.pack(side="left", padx=5)
        
        back_btn = StyledButton(
            btn_frame, 
            text="GO BACK", 
            command=self.show_landing_screen,
            bg_color="#E2E8F0",
            fg_color=COLOR_TEXT_MAIN,
            hover_bg="#CBD5E1",
            width=12
        )
        back_btn.pack(side="left", padx=5)
        
        # Bind Enter key to login
        self.root.bind("<Return>", lambda event: self.handle_login(role))

    def handle_login(self, target_role):
        username = self.id_field.get()
        password = self.pwd_field.get()
        
        # Reset error label
        self.error_lbl.config(text="")
        
        if not username or not password:
            self.error_lbl.config(text="Please fill in all fields.")
            return
            
        user = self.manager.authenticate(username, password)
        if user:
            # Check Role Separation
            if target_role == "admin" and user.role != "admin":
                self.error_lbl.config(text="❌ Access Denied: This portal is reserved for Administrators.")
                return
            if target_role == "student" and user.role != "student":
                # student is the internal representation of member
                self.error_lbl.config(text="❌ Access Denied: This portal is reserved for Mess Members.")
                return
                
            # Login successful: clear root and route
            self.root.unbind("<Return>")
            self.open_dashboard(user)
        else:
            self.error_lbl.config(text="❌ Invalid ID or password. Please try again.")

    def open_dashboard(self, user):
        # Clear the current selection screen
        for widget in self.root.winfo_children():
            widget.destroy()
            
        if user.role == "admin":
            from gui.admin_dashboard import AdminDashboard
            AdminDashboard(self.root, self.manager, user)
        else:
            from gui.member_dashboard import MemberDashboard
            MemberDashboard(self.root, self.manager, user)
