import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import uuid
from gui.widgets import (
    COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_WARNING, FONT_SUBHEADING, FONT_BODY, FONT_MUTED,
    StyledButton, LabeledEntry, create_scrollable_tree
)
from models import GroceryEntry
import validators as val
import calculations as calc

class GroceryMgmtView:
    def __init__(self, parent_frame, manager, user_profile):
        self.parent = parent_frame
        self.manager = manager
        self.user = user_profile
        self.is_admin = (self.user.role == "admin")
        
        # State
        self.selected_month = datetime.now().strftime("%Y-%m")
        
        # Heading
        self.header_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.title_lbl = tk.Label(
            self.header_frame,
            text="Grocery Expenses & Meal Rates",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.title_lbl.pack(side="left")
        
        # Month Filter Combobox
        filter_frame = tk.Frame(self.header_frame, bg=self.parent["bg"])
        filter_frame.pack(side="right")
        
        tk.Label(filter_frame, text="Select Month: ", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=self.parent["bg"]).pack(side="left")
        self.month_combobox = ttk.Combobox(filter_frame, state="readonly", width=12, font=FONT_BODY)
        self.month_combobox.pack(side="left", padx=5)
        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_change)
        self.populate_months()
        
        # Split layout: Form on Left (Admins only), Table on Right
        self.body_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.body_frame.pack(fill="both", expand=True)
        
        if self.is_admin:
            # Form on left
            self.form_frame = tk.Frame(self.body_frame, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=15, pady=15, width=300)
            self.form_frame.pack(side="left", fill="y", padx=(0, 15))
            self.form_frame.pack_propagate(False)
            self.create_entry_form()
            
        # Table on right
        self.table_container = tk.Frame(self.body_frame, bg=self.parent["bg"])
        self.table_container.pack(side="left", fill="both", expand=True)
        
        cols = ("date", "item", "qty", "unit", "price", "total", "added_by")
        hdgs = ("Purchase Date", "Item Name", "Qty", "Unit", "Price/Unit", "Total Cost", "Added By")
        widths = {"date": 100, "qty": 60, "unit": 60, "price": 90, "total": 100}
        
        self.table_frame, self.tree = create_scrollable_tree(self.table_container, cols, hdgs, widths)
        self.table_frame.pack(fill="both", expand=True)
        
        # Summary Area at Bottom
        self.summary_card = tk.Frame(self.parent, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=15, pady=10)
        self.summary_card.pack(fill="x", pady=(15, 0))
        
        self.lbl_spent = tk.Label(self.summary_card, text="Total Spending: ৳0.00", font=("Segoe UI", 11, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
        self.lbl_spent.pack(side="left", padx=10)
        
        self.lbl_meals = tk.Label(self.summary_card, text="Total Meals Eaten: 0", font=("Segoe UI", 11, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD)
        self.lbl_meals.pack(side="left", padx=20)
        
        self.lbl_rate = tk.Label(self.summary_card, text="Calculated Meal Rate: ৳0.00 / meal", font=("Segoe UI", 11, "bold"), fg=COLOR_PRIMARY, bg=COLOR_CARD)
        self.lbl_rate.pack(side="left", padx=10)
        
        if self.is_admin:
            self.save_rate_btn = StyledButton(
                self.summary_card,
                text="Lock Meal Rate",
                command=self.lock_meal_rate,
                bg_color=COLOR_PRIMARY,
                hover_bg=COLOR_PRIMARY.replace("5C67F2", "4A54D4"),
                width=16
            )
            self.save_rate_btn.pack(side="right", padx=10)
            
        self.refresh_data()

    def populate_months(self):
        # Scan grocery dates to compile available months
        months = set()
        months.add(datetime.now().strftime("%Y-%m")) # Always show current month
        for entry in self.manager.grocery_list:
            if len(entry.date) >= 7:
                months.add(entry.date[:7])
        for p in self.manager.payments_list:
            months.add(p.month)
            
        sorted_months = sorted(list(months), reverse=True)
        self.month_combobox["values"] = sorted_months
        
        if self.selected_month in sorted_months:
            self.month_combobox.set(self.selected_month)
        else:
            self.month_combobox.set(sorted_months[0])
            self.selected_month = sorted_months[0]

    def on_month_change(self, event=None):
        self.selected_month = self.month_combobox.get()
        self.refresh_data()

    def create_entry_form(self):
        tk.Label(self.form_frame, text="LOG NEW PURCHASE", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(anchor="w", pady=(0, 15))
        
        self.f_date = LabeledEntry(self.form_frame, "Purchase Date (YYYY-MM-DD)")
        self.f_date.pack(fill="x", pady=4)
        self.f_date.set(datetime.now().strftime("%Y-%m-%d"))
        
        self.f_item = LabeledEntry(self.form_frame, "Item Name (e.g. Potatoes)")
        self.f_item.pack(fill="x", pady=4)
        
        self.f_qty = LabeledEntry(self.form_frame, "Quantity")
        self.f_qty.pack(fill="x", pady=4)
        
        # Unit selector
        lbl = tk.Label(self.form_frame, text="Measurement Unit", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD, anchor="w")
        lbl.pack(fill="x", pady=(4, 2))
        self.f_unit = ttk.Combobox(self.form_frame, values=("kg", "litre", "pcs"), state="readonly", font=FONT_BODY)
        self.f_unit.pack(fill="x", pady=(0, 4))
        self.f_unit.current(0)
        
        self.f_price = LabeledEntry(self.form_frame, "Price per Unit (৳)")
        self.f_price.pack(fill="x", pady=4)
        
        btn = StyledButton(
            self.form_frame,
            text="RECORD EXPENSE",
            command=self.save_grocery_entry,
            bg_color=COLOR_SUCCESS,
            hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"),
            width=18
        )
        btn.pack(pady=(15, 0))

    def save_grocery_entry(self):
        try:
            # Validate input fields
            date = val.validate_date(self.f_date.get())
            item = val.validate_dish_name(self.f_item.get())
            qty = val.validate_amount(self.f_qty.get())
            unit = self.f_unit.get()
            price = val.validate_amount(self.f_price.get())
            
            entry_id = "G" + str(uuid.uuid4().hex[:6]).upper()
            added_by = self.user.student_id
            
            # Create object
            new_entry = GroceryEntry(entry_id, date, item, qty, unit, price, added_by)
            self.manager.add_grocery(new_entry)
            
            messagebox.showinfo("Success", f"Logged '{item}' expense successfully!")
            
            # Reset form fields
            self.f_item.clear()
            self.f_qty.clear()
            self.f_price.clear()
            self.f_date.set(datetime.now().strftime("%Y-%m-%d"))
            self.f_unit.current(0)
            
            # Refresh list & months
            self.populate_months()
            self.refresh_data()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def refresh_data(self):
        # Filter groceries by selected month
        monthly_groceries = self.manager.get_groceries_by_month(self.selected_month)
        
        # Populate table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for idx, g in enumerate(monthly_groceries):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "",
                "end",
                iid=g.entry_id,
                values=(g.date, g.item_name, g.quantity, g.unit, f"৳ {g.unit_price:.2f}", f"৳ {g.total_cost:.2f}", g.added_by),
                tags=(tag,)
            )
            
        # Recalculate monthly statistics using NumPy functions
        total_spent = calc.get_total_monthly_expense(monthly_groceries)
        total_meals = self.manager.count_all_meals_in_month(self.selected_month)
        calculated_rate = calc.get_meal_rate(total_spent, total_meals)
        
        self.lbl_spent.config(text=f"Total Spending: ৳ {total_spent:.2f}")
        self.lbl_meals.config(text=f"Total Meals Eaten: {total_meals}")
        
        # Display rate: if rate is 0, show the configured rate.
        rate_to_show = calculated_rate if calculated_rate > 0 else self.manager.calculate_meal_rate(self.selected_month)
        self.lbl_rate.config(text=f"Calculated Meal Rate: ৳ {rate_to_show:.2f} / meal")

    def lock_meal_rate(self):
        # Calculate current rate
        monthly_groceries = self.manager.get_groceries_by_month(self.selected_month)
        total_spent = calc.get_total_monthly_expense(monthly_groceries)
        total_meals = self.manager.count_all_meals_in_month(self.selected_month)
        
        rate = calc.get_meal_rate(total_spent, total_meals)
        if rate <= 0:
            messagebox.showwarning("Warning", "Cannot lock a rate of ৳ 0.00. Please enter grocery expenses and meal logs first.")
            return
            
        if messagebox.askyesno("Confirm Lock Rate", f"Are you sure you want to lock the meal rate of {self.selected_month} to ৳ {rate:.2f}?\nThis rate will apply to all calculations for this month."):
            self.manager.config["meal_rate"] = rate
            self.manager.save_all()
            messagebox.showinfo("Success", f"Meal rate for {self.selected_month} successfully saved in global settings!")
            self.refresh_data()
