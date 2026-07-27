import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime
import numpy as np
from gui.widgets import (
    COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER, FONT_SUBHEADING, FONT_BODY, FONT_MUTED,
    StyledButton
)
import calculations as calc

class ReportsView:
    def __init__(self, parent_frame, manager):
        self.parent = parent_frame
        self.manager = manager
        
        # State
        self.selected_month = datetime.now().strftime("%Y-%m")
        
        # Heading
        self.header_frame = tk.Frame(self.parent, bg=self.parent["bg"])
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.title_lbl = tk.Label(
            self.header_frame,
            text="NumPy Analytics & Statistics Panel",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.title_lbl.pack(side="left")
        
        # Month Filter Combobox & Export button
        ctrl_frame = tk.Frame(self.header_frame, bg=self.parent["bg"])
        ctrl_frame.pack(side="right")
        
        tk.Label(ctrl_frame, text="Select Month: ", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=self.parent["bg"]).pack(side="left")
        self.month_combobox = ttk.Combobox(ctrl_frame, state="readonly", width=12, font=FONT_BODY)
        self.month_combobox.pack(side="left", padx=5)
        self.month_combobox.bind("<<ComboboxSelected>>", self.on_month_change)
        
        self.export_btn = StyledButton(
            ctrl_frame,
            text="Export Text Report",
            command=self.export_txt_report,
            bg_color=COLOR_SUCCESS,
            hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"),
            width=18
        )
        self.export_btn.pack(side="left", padx=10)
        
        self.populate_months()
        
        # Scrollable Text Area to present stats report nicely
        self.report_card = tk.Frame(self.parent, bg=COLOR_CARD, highlightbackground="#E2E8F0", highlightthickness=1, bd=0, padx=20, pady=20)
        self.report_card.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar
        self.text_scroll = ttk.Scrollbar(self.report_card)
        self.text_scroll.pack(side="right", fill="y")
        
        self.report_text = tk.Text(
            self.report_card,
            font=("Courier New", 10),
            fg=COLOR_TEXT_MAIN,
            bg="#F8FAFC",
            wrap="none",
            relief="solid",
            bd=1,
            highlightthickness=0,
            yscrollcommand=self.text_scroll.set
        )
        self.report_text.pack(side="left", fill="both", expand=True)
        self.text_scroll.config(command=self.report_text.yview)
        
        # Define Text Tags for color-coding
        self.report_text.tag_config("title", font=("Segoe UI", 14, "bold"), foreground=COLOR_PRIMARY)
        self.report_text.tag_config("header", font=("Segoe UI", 11, "bold"), foreground=COLOR_PRIMARY)
        self.report_text.tag_config("highlight", font=("Courier New", 10, "bold"), foreground=COLOR_SUCCESS)
        self.report_text.tag_config("danger", font=("Courier New", 10, "bold"), foreground=COLOR_DANGER)
        
        self.generate_and_display_stats()

    def populate_months(self):
        months = set()
        months.add(datetime.now().strftime("%Y-%m"))
        for entry in self.manager.grocery_list:
            if len(entry.date) >= 7:
                months.add(entry.date[:7])
        for p in self.manager.payments_list:
            months.add(p.month)
        for r in self.manager.meal_records:
            months.add(r.date[:7])
            
        sorted_months = sorted(list(months), reverse=True)
        self.month_combobox["values"] = sorted_months
        self.month_combobox.set(self.selected_month)

    def on_month_change(self, event=None):
        self.selected_month = self.month_combobox.get()
        self.generate_and_display_stats()

    def compile_report_string(self):
        # 1. Gather Grocery Stats
        monthly_groceries = self.manager.get_groceries_by_month(self.selected_month)
        grocery_stats = calc.get_grocery_statistics(monthly_groceries)
        
        # 2. Gather Student Dues Stats
        students = self.manager.get_all_students()
        dues_stats = calc.get_due_summary(students, self.selected_month, self.manager)
        
        # 3. Gather Meals Stats
        total_meals = self.manager.count_all_meals_in_month(self.selected_month)
        calculated_rate = calc.get_meal_rate(grocery_stats["total"], total_meals)
        
        active_students = len(students)
        avg_meals_student = total_meals / active_students if active_students > 0 else 0.0
        
        # 4. Gather Payments Stats
        monthly_payments = self.manager.get_all_payments_in_month(self.selected_month)
        total_collected = sum(p.amount for p in monthly_payments)
        max_payment = calc.get_highest_spender_month(monthly_payments)
        
        # 5. Daily Attendance Trends
        today_str = datetime.now().strftime("%Y-%m-%d")
        b_count, l_count, d_count = self.manager.get_all_meals_on_date(today_str)
        today_meals = b_count + l_count + d_count
        participation_rate = calc.get_meal_participation_rate(today_str, active_students, today_meals / 3.0 if today_meals > 0 else 0)
        
        # Build Text
        lines = []
        lines.append(f"==========================================================================")
        lines.append(f"                 MESS MEMBER MANAGEMENT SYSTEM ANALYTICS                ")
        lines.append(f"                   MONTHLY REPORT: {self.selected_month}                  ")
        lines.append(f"            Report Compiled on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}            ")
        lines.append(f"==========================================================================")
        lines.append("")
        
        lines.append(f"--- 👥 MEMBER ACCOUNT METRICS ---")
        lines.append(f"  • Total Registered Members   : {active_students} Members")
        lines.append(f"  • Active Meals Count (Month) : {total_meals} Meals")
        lines.append(f"  • Average Meals per Member   : {avg_meals_student:.2f} Meals")
        lines.append("")
        
        lines.append(f"--- 🛒 GROCERY & EXPENDITURES SUMMARY (NumPy Powered) ---")
        lines.append(f"  • Total Grocery Cost         : ৳ {grocery_stats['total']:.2f}")
        lines.append(f"  • Average Purchase Size      : ৳ {grocery_stats['mean']:.2f}")
        lines.append(f"  • Median Purchase Size       : ৳ {grocery_stats['median']:.2f}")
        lines.append(f"  • Standard Deviation of Cost : ৳ {grocery_stats['std']:.2f}")
        lines.append(f"  • Max Single Purchase Value  : ৳ {grocery_stats['max']:.2f}")
        lines.append(f"  • Min Single Purchase Value  : ৳ {grocery_stats['min']:.2f}")
        lines.append(f"  • Purchase Transaction Volume: {grocery_stats['count']} Entries")
        lines.append(f"  • Calculated Unit Meal Rate  : ৳ {calculated_rate:.4f} per meal")
        lines.append("")
        
        lines.append(f"--- 💰 COLLECTIONS & OUTSTANDING DUES (NumPy Powered) ---")
        lines.append(f"  • Total Payments Collected   : ৳ {total_collected:.2f}")
        lines.append(f"  • Max Single Member Payment  : ৳ {max_payment:.2f}")
        lines.append(f"  • Total Outstanding Balances : ৳ {dues_stats['sum']:.2f}")
        lines.append(f"  • Average Dues Outstanding   : ৳ {dues_stats['mean']:.2f}")
        lines.append(f"  • Highest Single Dues Account: ৳ {dues_stats['max']:.2f}")
        lines.append("")
        
        lines.append(f"--- 🍽️ DAILY PARTICIPATION STATISTICS ---")
        lines.append(f"  • Todays Date                : {today_str}")
        lines.append(f"  • Todays Active Eaters (Avg) : {today_meals / 3.0:.1f} / {active_students} members")
        lines.append(f"  • Attendance Breakdown       : Breakfast: {b_count} | Lunch: {l_count} | Dinner: {d_count}")
        lines.append(f"  • Participation Percentage   : {participation_rate:.2f}%")
        lines.append("")
        lines.append(f"==========================================================================")
        lines.append(f"                       AIUB Blue Mess Management Inc.                     ")
        lines.append(f"==========================================================================")
        
        return "\n".join(lines)

    def generate_and_display_stats(self):
        self.report_text.config(state="normal")
        self.report_text.delete(1.0, tk.END)
        
        report_str = self.compile_report_string()
        self.report_text.insert(tk.END, report_str)
        
        # Color specific lines to make it look excellent
        self.apply_formatting_tags()
        
        self.report_text.config(state="disabled")

    def apply_formatting_tags(self):
        # Look for headers and totals to apply color tags
        text_content = self.report_text.get(1.0, tk.END)
        lines = text_content.split("\n")
        
        for idx, line in enumerate(lines):
            line_num = idx + 1
            if line.startswith("---") or line.startswith("==="):
                self.report_text.tag_add("header", f"{line_num}.0", f"{line_num}.end")
            if "Total Outstanding Balances" in line or "Calculated Unit Meal Rate" in line:
                self.report_text.tag_add("highlight", f"{line_num}.30", f"{line_num}.end")
            if "Highest Single Dues Account" in line and not "৳ 0.00" in line:
                self.report_text.tag_add("danger", f"{line_num}.30", f"{line_num}.end")

    def export_txt_report(self):
        try:
            report_dir = "report"
            if not os.path.exists(report_dir):
                os.makedirs(report_dir, exist_ok=True)
                
            filename = os.path.join(report_dir, f"mess_monthly_report_{self.selected_month.replace('-', '_')}.txt")
            
            report_str = self.compile_report_string()
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_str)
                
            messagebox.showinfo("Export Successful", f"Monthly Report exported successfully to:\n{os.path.abspath(filename)}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write file: {str(e)}")
