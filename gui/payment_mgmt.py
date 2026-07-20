import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import uuid
from gui.widgets import (
    COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER, FONT_SUBHEADING, FONT_BODY, FONT_MUTED,
    StyledButton, LabeledEntry, create_scrollable_tree
)
from models import Payment
import validators as val

class PaymentMgmtView:
    def __init__(self, parent_frame, manager, user_profile):
        self.parent = parent_frame
        self.manager = manager
        self.user = user_profile
        self.is_admin = (self.user.role == "admin")
        
        # State
        self.selected_student_id = self.user.student_id if not self.is_admin else None
        self.selected_month = datetime.now().strftime("%Y-%m")
        
        # Heading
        self.header_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.header_frame.pack(fill="x", pady=(0, 8))
        
        self.title_lbl = tk.Label(
            self.header_frame,
            text="Payments & Member Billing Ledgers",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.title_lbl.pack(side="left")
        
        # Selectors (Student & Month)
        self.sel_frame = tk.Frame(self.header_frame, bg=self.parent["bg"])
        self.sel_frame.pack(side="right")
        
        # Month combobox (Whole Year selector)
        tk.Label(self.sel_frame, text="Month: ", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=self.parent["bg"]).pack(side="left")
        self.month_combo = ttk.Combobox(self.sel_frame, state="readonly", width=10, font=FONT_BODY)
        self.month_combo.pack(side="left", padx=5)
        self.month_combo.bind("<<ComboboxSelected>>", self.on_month_change)
        self.populate_months()
        
        if self.is_admin:
            # Student combobox
            tk.Label(self.sel_frame, text="Member: ", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=self.parent["bg"]).pack(side="left", padx=(10, 0))
            self.student_combo = ttk.Combobox(self.sel_frame, state="readonly", width=20, font=FONT_BODY)
            self.student_combo.pack(side="left", padx=5)
            self.student_combo.bind("<<ComboboxSelected>>", self.on_student_change)
            self.populate_students()
            
        # Outer body container
        self.body_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.body_frame.pack(fill="both", expand=True)
        
        # Left Side: Billing Card and Payment Form (Compact to ensure PAY NOW is 100% visible)
        self.left_side = tk.Frame(self.body_frame, bg=self.parent["bg"], width=340)
        self.left_side.pack(side="left", fill="both", padx=(0, 12))
        
        # Billing details box
        self.bill_card = tk.Frame(self.left_side, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=12, pady=10)
        self.bill_card.pack(fill="x", pady=(0, 8))
        
        tk.Label(self.bill_card, text="ACCOUNT SUMMARY CARD", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor="w", pady=(0, 6))
        
        self.lbl_meals = tk.Label(self.bill_card, text="Meals Taken: 0", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
        self.lbl_meals.pack(anchor="w", pady=1)
        
        self.lbl_rate = tk.Label(self.bill_card, text="Rate Per Meal: ৳0.00", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
        self.lbl_rate.pack(anchor="w", pady=1)
        
        self.lbl_total_bill = tk.Label(self.bill_card, text="Monthly Total Bill: ৳0.00", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
        self.lbl_total_bill.pack(anchor="w", pady=1)
        
        self.lbl_paid = tk.Label(self.bill_card, text="Paid This Month: ৳0.00", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
        self.lbl_paid.pack(anchor="w", pady=1)
        
        # Explicit Advance Balance line (in marked position)
        self.lbl_advance = tk.Label(self.bill_card, text="Advance Balance: ৳ 0.00", font=("Segoe UI", 10, "bold"), fg=COLOR_SUCCESS, bg=COLOR_CARD)
        self.lbl_advance.pack(anchor="w", pady=1)
        
        # Outstanding Due highlight
        self.lbl_due = tk.Label(self.bill_card, text="OUTSTANDING DUE: ৳0.00", font=("Segoe UI", 11, "bold"), fg=COLOR_DANGER, bg=COLOR_CARD)
        self.lbl_due.pack(anchor="w", pady=(4, 0))
        
        # Payment Form Container (Members only)
        if not self.is_admin:
            self.form_box = tk.Frame(self.left_side, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=12, pady=10)
            self.form_box.pack(fill="x")
            self.create_payment_form()
            
        # Right Side: History treeview
        self.right_side = tk.Frame(self.body_frame, bg=self.parent["bg"])
        self.right_side.pack(side="left", fill="both", expand=True)
        
        tk.Label(self.right_side, text="PAYMENT TRANSACTION HISTORY", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=self.parent["bg"]).pack(anchor="w", pady=(0, 4))
        
        cols = ("id", "date", "month", "amount", "method", "note")
        hdgs = ("Payment ID", "Paid Date", "Target Month", "Amount (৳)", "Payment Method", "Reference Note")
        widths = {"id": 100, "date": 100, "month": 80, "amount": 100}
        
        self.table_frame, self.tree = create_scrollable_tree(self.right_side, cols, hdgs, widths)
        self.table_frame.pack(fill="both", expand=True)
        
        self.refresh_billing_and_table()

    def populate_months(self):
        # Populate all 12 months for current year, previous year, and next year (Whole Year option)
        curr_year = datetime.now().year
        months = set()
        for y in [curr_year - 1, curr_year, curr_year + 1]:
            for m in range(1, 13):
                months.add(f"{y}-{m:02d}")
                
        for p in self.manager.payments_list:
            if p.month:
                months.add(p.month)
        for r in self.manager.meal_records:
            if r.date:
                months.add(r.date[:7])
                
        sorted_months = sorted(list(months), reverse=True)
        self.month_combo["values"] = sorted_months
        
        if self.selected_month in sorted_months:
            self.month_combo.set(self.selected_month)
        else:
            self.month_combo.set(sorted_months[0])
            self.selected_month = sorted_months[0]

    def populate_students(self):
        students = self.manager.get_all_students()
        strings = [f"{s.student_id} - {s.name}" for s in students]
        self.student_combo["values"] = strings
        if strings:
            self.student_combo.current(0)
            self.selected_student_id = students[0].student_id

    def on_month_change(self, event=None):
        self.selected_month = self.month_combo.get()
        self.refresh_billing_and_table()
        if not self.is_admin:
            self.render_method_fields()

    def on_student_change(self, event=None):
        sel = self.student_combo.get()
        if sel:
            self.selected_student_id = sel.split(" - ")[0]
            self.refresh_billing_and_table()
            if not self.is_admin:
                self.render_method_fields()

    def create_payment_form(self):
        tk.Label(self.form_box, text="MAKE DUES PAYMENT", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(anchor="w", pady=(0, 2))
        tk.Label(self.form_box, text="Select your payment method:", font=FONT_MUTED, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor="w", pady=(0, 6))
        
        # Selected method state
        self.selected_method = tk.StringVar(value="bKash")
        
        # Payment Method selector buttons (bKash, Nagad, Cash)
        method_frame = tk.Frame(self.form_box, bg=COLOR_CARD)
        method_frame.pack(fill="x", pady=(0, 6))
        method_frame.columnconfigure((0, 1, 2), weight=1, uniform="equal")
        
        self.method_btns = {}
        methods = [("bKash", "#D12053"), ("Nagad", "#E23528"), ("Cash", "#10B981")]
        
        for idx, (m_name, m_color) in enumerate(methods):
            btn = tk.Button(
                method_frame,
                text=m_name,
                font=("Segoe UI", 9, "bold"),
                bg=m_color if m_name == "bKash" else "#F1F5F9",
                fg="#FFFFFF" if m_name == "bKash" else COLOR_TEXT_MAIN,
                activebackground=m_color,
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                cursor="hand2",
                pady=5,
                command=lambda name=m_name, col=m_color: self.set_payment_method(name, col)
            )
            btn.grid(row=0, column=idx, padx=2, sticky="ew")
            self.method_btns[m_name] = btn
            
        # Form Container for dynamic fields
        self.dynamic_fields_frame = tk.Frame(self.form_box, bg=COLOR_CARD)
        self.dynamic_fields_frame.pack(fill="x", pady=2)
        
        self.render_method_fields()

    def set_payment_method(self, method_name, color):
        self.selected_method.set(method_name)
        methods = [("bKash", "#D12053"), ("Nagad", "#E23528"), ("Cash", "#10B981")]
        for m_name, m_color in methods:
            if m_name == method_name:
                self.method_btns[m_name].config(bg=m_color, fg="#FFFFFF")
            else:
                self.method_btns[m_name].config(bg="#F1F5F9", fg=COLOR_TEXT_MAIN)
        self.render_method_fields()

    def render_method_fields(self):
        for w in self.dynamic_fields_frame.winfo_children():
            w.destroy()
            
        method = self.selected_method.get()
        
        # Calculate current due to pre-fill
        due = self.manager.calculate_due(self.selected_student_id, self.selected_month) if self.selected_student_id else 0.0
        default_amt = f"{max(0.0, due):.2f}" if due > 0 else "0.00"
        
        if method in ("bKash", "Nagad"):
            row1 = tk.Frame(self.dynamic_fields_frame, bg=COLOR_CARD)
            row1.pack(fill="x", pady=2)
            row1.columnconfigure((0, 1), weight=1)
            
            self.f_amount = LabeledEntry(row1, "Amount (৳)")
            self.f_amount.grid(row=0, column=0, padx=(0, 3), sticky="ew")
            self.f_amount.set(default_amt)
            
            self.f_acc_num = LabeledEntry(row1, f"{method} Number")
            self.f_acc_num.grid(row=0, column=1, padx=(3, 0), sticky="ew")
            self.f_acc_num.set("01710112341")
            
            pay_bg = "#D12053" if method == "bKash" else "#E23528"
        else: # Cash
            self.f_amount = LabeledEntry(self.dynamic_fields_frame, "Amount (৳)")
            self.f_amount.pack(fill="x", pady=2)
            self.f_amount.set(default_amt)
            pay_bg = "#10B981"
            
        # Reference Note Field
        self.f_ref = LabeledEntry(self.dynamic_fields_frame, "Reference Note")
        self.f_ref.pack(fill="x", pady=2)
        if method in ("bKash", "Nagad"):
            self.f_ref.set("Monthly bill payment")
        else:
            self.f_ref.set("Paid to manager by hand")
            
        # Prominent PAY NOW Button (Guaranteed Visible)
        pay_btn = StyledButton(
            self.dynamic_fields_frame,
            text=f"PAY NOW ({method})",
            command=self.save_payment,
            bg_color=pay_bg,
            hover_bg=pay_bg,
            width=22
        )
        pay_btn.pack(pady=(8, 2))

    def save_payment(self):
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Please select a member first.")
            return
            
        try:
            amt = val.validate_amount(self.f_amount.get())
            method = self.selected_method.get()
            
            note_val = self.f_ref.get().strip() if hasattr(self, 'f_ref') else ""
            if not note_val:
                if method in ("bKash", "Nagad") and hasattr(self, 'f_acc_num'):
                    note_val = f"Mobile: {self.f_acc_num.get().strip()}"
                else:
                    note_val = "Paid to manager by hand"
                
            pay_id = "P" + str(uuid.uuid4().hex[:6]).upper()
            today_str = datetime.now().strftime("%Y-%m-%d")
            
            # Calculate due before payment to check for advance amount
            current_due = self.manager.calculate_due(self.selected_student_id, self.selected_month)
            
            new_payment = Payment(pay_id, self.selected_student_id, amt, today_str, self.selected_month, method, note_val)
            self.manager.record_payment(new_payment)
            
            # Detailed confirmation message with Advance Amount detection
            if current_due > 0 and amt > current_due:
                extra = amt - current_due
                msg = f"Payment of ৳ {amt:.2f} via {method} recorded successfully!\n\n• ৳ {current_due:.2f} cleared outstanding dues.\n• ৳ {extra:.2f} added to your ADVANCE BALANCE!\n\nTransaction ID: {pay_id}"
            elif current_due <= 0:
                msg = f"Payment of ৳ {amt:.2f} via {method} recorded successfully as ADVANCE BALANCE!\n\nTransaction ID: {pay_id}"
            else:
                msg = f"Payment of ৳ {amt:.2f} via {method} recorded successfully!\n\nTransaction ID: {pay_id}"
                
            messagebox.showinfo("Payment Successful", msg)
            
            self.populate_months()
            self.refresh_billing_and_table()
            self.render_method_fields()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def refresh_billing_and_table(self):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not self.selected_student_id:
            return
            
        # Get billing stats
        meals_count = self.manager.count_total_meals(self.selected_student_id, self.selected_month)
        meal_rate = self.manager.calculate_meal_rate(self.selected_month)
        total_bill = meals_count * meal_rate
        
        monthly_payments = self.manager.get_monthly_payments(self.selected_student_id, self.selected_month)
        total_paid_month = sum(p.amount for p in monthly_payments)
        
        # Dynamic Advance Balance & Outstanding Due calculation
        net_balance = total_paid_month - total_bill
        
        if net_balance > 0:
            advance_amt = net_balance
            due_amt = 0.0
        elif net_balance < 0:
            advance_amt = 0.0
            due_amt = abs(net_balance)
        else:
            advance_amt = 0.0
            due_amt = 0.0
            
        # Populate bill details labels
        self.lbl_meals.config(text=f"Meals Taken: {meals_count}")
        self.lbl_rate.config(text=f"Rate Per Meal: ৳ {meal_rate:.2f}")
        self.lbl_total_bill.config(text=f"Monthly Total Bill: ৳ {total_bill:.2f}")
        self.lbl_paid.config(text=f"Paid This Month: ৳ {total_paid_month:.2f}")
        
        self.lbl_advance.config(text=f"Advance Balance: ৳ {advance_amt:.2f}")
        
        if due_amt > 0:
            self.lbl_due.config(text=f"OUTSTANDING DUE: ৳ {due_amt:.2f}", fg=COLOR_DANGER)
        else:
            self.lbl_due.config(text="OUTSTANDING DUE: ৳ 0.00", fg=COLOR_SUCCESS)
            
        # Populate transactions table
        student_payments = self.manager.get_payments(self.selected_student_id)
        for idx, p in enumerate(student_payments):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "",
                "end",
                iid=p.payment_id,
                values=(p.payment_id, p.date, p.month, f"৳ {p.amount:.2f}", p.method, p.note or "N/A"),
                tags=(tag,)
            )
