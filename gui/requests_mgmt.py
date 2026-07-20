import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import uuid
from gui.widgets import (
    COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER, FONT_SUBHEADING, FONT_BODY, FONT_MUTED,
    StyledButton, LabeledEntry, create_scrollable_tree
)
from models import MenuRequest
import validators as val

class RequestsMgmtView:
    def __init__(self, parent_frame, manager, user_profile):
        self.parent = parent_frame
        self.manager = manager
        self.user = user_profile
        self.is_admin = (self.user.role == "admin")
        
        # Heading
        self.header_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.title_lbl = tk.Label(
            self.header_frame,
            text="Menu Change Feedback & Requests",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.title_lbl.pack(side="left")
        
        # Grid container
        self.body_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.body_frame.pack(fill="both", expand=True)
        
        if not self.is_admin:
            # Student Layout: Left form to submit request, Right list of personal requests
            self.body_frame.columnconfigure(0, weight=2)
            self.body_frame.columnconfigure(1, weight=3)
            
            # Form on Left
            self.form_box = tk.Frame(self.body_frame, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=15, pady=15)
            self.form_box.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
            self.create_student_form()
            
            # Table on Right
            self.table_box = tk.Frame(self.body_frame, bg=self.parent["bg"])
            self.table_box.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
            
            tk.Label(self.table_box, text="MY SENT REQUEST HISTORY", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=self.parent["bg"]).pack(anchor="w", pady=(0, 5))
            
            cols = ("id", "date", "meal", "suggested", "status")
            hdgs = ("Req ID", "Target Date", "Meal Type", "Suggested Dish", "Status")
            widths = {"id": 80, "date": 100, "meal": 80, "status": 90}
            
            self.table_frame, self.tree = create_scrollable_tree(self.table_box, cols, hdgs, widths)
            self.table_frame.pack(fill="both", expand=True)
            self.refresh_student_table()
            
        else:
            # Admin Layout: Left summary card, Right pending list table
            self.body_frame.columnconfigure(0, weight=2)
            self.body_frame.columnconfigure(1, weight=3)
            
            # Summary Box on Left
            self.summary_box = tk.Frame(self.body_frame, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=15, pady=15)
            self.summary_box.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
            
            tk.Label(self.summary_box, text="DISH POPULARITY RATINGS", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(anchor="w", pady=(0, 5))
            tk.Label(self.summary_box, text="Check popular items requested for next week:", font=FONT_MUTED, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor="w", pady=(0, 15))
            
            self.summary_text = tk.Text(self.summary_box, font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg="#F8FAFC", wrap="word", relief="solid", bd=1, highlightthickness=0)
            self.summary_text.pack(fill="both", expand=True)
            
            # Table on Right
            self.table_box = tk.Frame(self.body_frame, bg=self.parent["bg"])
            self.table_box.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
            
            # Header with Approve / Reject action buttons
            act_bar = tk.Frame(self.table_box, bg=self.parent["bg"])
            act_bar.pack(fill="x", pady=(0, 5))
            
            tk.Label(act_bar, text="PENDING CHANGE PROPOSALS", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=self.parent["bg"]).pack(side="left", pady=(0, 5))
            
            self.rej_btn = StyledButton(act_bar, "Reject", self.reject_req, bg_color=COLOR_DANGER, hover_bg=COLOR_DANGER.replace("EF4444", "DC2626"), width=10)
            self.rej_btn.pack(side="right", padx=5)
            
            self.app_btn = StyledButton(act_bar, "Approve", self.approve_req, bg_color=COLOR_SUCCESS, hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"), width=10)
            self.app_btn.pack(side="right", padx=5)
            
            cols = ("id", "student", "date", "meal", "current", "suggested")
            hdgs = ("Req ID", "Member Name", "Target Date", "Meal Type", "Current Dish", "Suggested Dish")
            widths = {"id": 65, "date": 85, "meal": 80}
            
            self.table_frame, self.tree = create_scrollable_tree(self.table_box, cols, hdgs, widths)
            self.table_frame.pack(fill="both", expand=True)
            
            self.refresh_admin_view()

    # --- Student Form Functions ---
    def create_student_form(self):
        tk.Label(self.form_box, text="SUBMIT MENU SUGGESTION", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(anchor="w", pady=(0, 15))
        
        self.f_date = LabeledEntry(self.form_box, "Target Date (YYYY-MM-DD)")
        self.f_date.pack(fill="x", pady=4)
        
        # Tomorrow's date default
        tomorrow = datetime.now() + timedelta(days=1)
        self.f_date.set(tomorrow.strftime("%Y-%m-%d"))
        
        self.f_date.entry.bind("<FocusOut>", self.on_date_or_meal_change)
        
        # Meal type
        lbl = tk.Label(self.form_box, text="Meal Type Selection", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD, anchor="w")
        lbl.pack(fill="x", pady=(4, 2))
        self.f_meal = ttk.Combobox(self.form_box, values=self.manager.MEAL_TYPES, state="readonly", font=FONT_BODY)
        self.f_meal.pack(fill="x", pady=(0, 4))
        self.f_meal.current(1) # Lunch default
        self.f_meal.bind("<<ComboboxSelected>>", self.on_date_or_meal_change)
        
        self.f_curr = LabeledEntry(self.form_box, "Current Planned Dishes (Auto)")
        self.f_curr.pack(fill="x", pady=4)
        self.f_curr.entry.config(state="readonly")
        
        self.f_sugg = LabeledEntry(self.form_box, "Your Suggested Dish")
        self.f_sugg.pack(fill="x", pady=4)
        
        btn = StyledButton(
            self.form_box,
            text="SUBMIT PROPOSAL",
            command=self.submit_suggestion,
            bg_color=COLOR_SUCCESS,
            hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"),
            width=18
        )
        btn.pack(pady=(15, 0))
        
        # Initial fill
        self.on_date_or_meal_change()

    def on_date_or_meal_change(self, event=None):
        date_str = self.f_date.get()
        meal_type = self.f_meal.get()
        
        # Temporarily enable entry to update text
        self.f_curr.entry.config(state="normal")
        self.f_curr.clear()
        
        if date_str and meal_type:
            menu = self.manager.get_menu(date_str)
            dishes = menu.get(meal_type, [])
            dishes_str = ", ".join(dishes) if dishes else "No dishes planned yet"
            self.f_curr.set(dishes_str)
            
        self.f_curr.entry.config(state="readonly")

    def submit_suggestion(self):
        try:
            date = val.validate_date(self.f_date.get())
            meal = self.f_meal.get()
            current = self.f_curr.get()
            suggested = val.validate_dish_name(self.f_sugg.get())
            
            # Limit requests to future dates
            dt = datetime.strptime(date, "%Y-%m-%d")
            if dt.date() <= datetime.now().date():
                raise ValueError("Suggestions must be submitted for future dates only.")
                
            req_id = "R" + str(uuid.uuid4().hex[:6]).upper()
            submitted = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Create Suggestion
            req = MenuRequest(req_id, self.user.student_id, self.user.name, date, meal, current, suggested, "Pending", submitted)
            self.manager.submit_request(req)
            
            messagebox.showinfo("Success", f"Suggestion for '{suggested}' submitted successfully!")
            self.f_sugg.clear()
            self.refresh_student_table()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def refresh_student_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        history = self.manager.get_student_requests(self.user.student_id)
        for idx, r in enumerate(history):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "",
                "end",
                iid=r.request_id,
                values=(r.request_id, r.target_date, r.meal_type, r.suggested_dish, r.status),
                tags=(tag,)
            )

    # --- Admin Functions ---
    def refresh_admin_view(self):
        # Refresh tree table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        pending = self.manager.get_pending_requests()
        for idx, r in enumerate(pending):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "",
                "end",
                iid=r.request_id,
                values=(r.request_id, r.student_name, r.target_date, r.meal_type, r.current_dish, r.suggested_dish),
                tags=(tag,)
            )
            
        # Refresh summary text (Dish popularity counting)
        self.summary_text.config(state="normal")
        self.summary_text.delete(1.0, tk.END)
        
        # Aggregate suggestions grouped by date & meal
        # Gather all pending requests and compile a breakdown
        groupings = {}
        for r in pending:
            key = f"{r.meal_type} on {r.target_date}"
            if key not in groupings:
                groupings[key] = {}
            dish = r.suggested_dish.strip().title()
            groupings[key][dish] = groupings[key].get(dish, 0) + 1
            
        if not groupings:
            self.summary_text.insert(tk.END, "No pending suggestions. Menus are balanced!")
        else:
            for sched, votes in sorted(groupings.items()):
                self.summary_text.insert(tk.END, f"📌 {sched}:\n", "header_tag")
                # Sort votes descending
                sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
                for dish, count in sorted_votes:
                    star = " ⭐" if count >= 3 else ""
                    self.summary_text.insert(tk.END, f"  • {dish} → {count} requests{star}\n")
                self.summary_text.insert(tk.END, "\n")
                
        self.summary_text.tag_config("header_tag", font=("Segoe UI", 10, "bold"), foreground=COLOR_PRIMARY)
        self.summary_text.config(state="disabled")

    def approve_req(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request row to approve.")
            return
            
        req_id = selected[0]
        if messagebox.askyesno("Confirm Approval", f"Approve proposal {req_id}?\nThis will automatically overwrite the weekly meal schedule with the suggested dish."):
            success = self.manager.approve_request(req_id)
            if success:
                messagebox.showinfo("Success", f"Proposal {req_id} approved and meal schedule updated!")
                self.refresh_admin_view()
            else:
                messagebox.showerror("Error", "Could not complete approval.")

    def reject_req(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request row to reject.")
            return
            
        req_id = selected[0]
        if messagebox.askyesno("Confirm Rejection", f"Are you sure you want to reject proposal {req_id}?"):
            success = self.manager.reject_request(req_id)
            if success:
                messagebox.showinfo("Success", f"Proposal {req_id} rejected.")
                self.refresh_admin_view()
            else:
                messagebox.showerror("Error", "Could not complete rejection.")
