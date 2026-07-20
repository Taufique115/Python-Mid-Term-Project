import os
from models import Student, MealRecord, MenuItem, GroceryEntry, Payment, MenuRequest
import file_handler as fh
import calculations as calc

class MessManager:
    MEAL_TYPES = ("Breakfast", "Lunch", "Dinner")
    
    DEFAULT_WEEKLY_MENU = {
        "Saturday": {
            "Breakfast": ["Roti", "Vegetable"],
            "Lunch": ["Rice", "Pulse", "Vegetable", "Fish Curry"],
            "Dinner": ["Rice", "Pulse", "Vegetable", "Egg Curry"]
        },
        "Sunday": {
            "Breakfast": ["Khichuri"],
            "Lunch": ["Rice", "Pulse", "Vegetable", "Chicken Curry"],
            "Dinner": ["Rice", "Pulse", "Vegetable Curry"]
        },
        "Monday": {
            "Breakfast": ["Roti", "Pulse"],
            "Lunch": ["Rice", "Mashed Potato", "Egg Fry"],
            "Dinner": ["Rice", "Pulse", "Vegetable", "Fish Curry"]
        },
        "Tuesday": {
            "Breakfast": ["Khichuri"],
            "Lunch": ["Rice", "Pulse", "Vegetable", "Fish Curry"],
            "Dinner": ["Rice", "Vegetable", "Egg Curry"]
        },
        "Wednesday": {
            "Breakfast": ["Roti", "Vegetable"],
            "Lunch": ["Rice", "Pulse", "Vegetable"],
            "Dinner": ["Rice", "Pulse", "Vegetable", "Chicken Curry"]
        },
        "Thursday": {
            "Breakfast": ["Vegetable Khichuri"],
            "Lunch": ["Rice", "Pulse", "Vegetable", "Egg Curry"],
            "Dinner": ["Rice", "Pulse", "Fish Curry"]
        },
        "Friday": {
            "Breakfast": ["Roti", "Vegetable"],
            "Lunch": ["Biryani / Khichuri"],
            "Dinner": ["Rice", "Pulse", "Beef Curry"]
        }
    }
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            
        # File paths
        self.students_file = os.path.join(data_dir, "students.json")
        self.meals_file = os.path.join(data_dir, "meals.json")
        self.menu_file = os.path.join(data_dir, "menu.json")
        self.grocery_file = os.path.join(data_dir, "grocery.json")
        self.payments_file = os.path.join(data_dir, "payments.json")
        self.requests_file = os.path.join(data_dir, "requests.json")
        self.config_file = os.path.join(data_dir, "config.json")
        
        # Load config first
        self.config = fh.load_config(self.config_file)
        
        # Data lists
        self.students_list = []
        self.meal_records = []
        self.menu_items = []
        self.grocery_list = []
        self.payments_list = []
        self.requests_list = []
        
        # Sets for duplicate prevention
        self.student_id_set = set()
        self.used_request_ids = set()
        
        # Load all data
        self.load_all()
        
        # Auto-create admin and default students if students list is empty
        if not self.students_list:
            self._preseed_default_data()

    def _preseed_default_data(self):
        # Create default Admin
        admin = Student("admin01", "Mess Manager Cristiano Messi Junior", "Admin Office", "01710112341", "2025-01-01", "admin", "admin123")
        self.students_list.append(admin)
        self.student_id_set.add("admin01")
        
        # Create default Students
        students_data = [
            ("S001", "Adnan Chowdhury", "Room 302", "01812345678", "pass01"),
            ("S002", "Fahim Shahriar", "Room 304", "01511223344", "pass02"),
            ("S003", "Tasnim Rahman", "Room 401", "01988776655", "pass03"),
            ("S004", "Nusrat Jahan", "Room 405", "01722334455", "pass04"),
            ("S005", "Imtiaz Ahmed", "Room 201", "01344556677", "pass05"),
            ("S006", "Sadia Afrin", "Room 204", "01455667788", "pass06"),
            ("S007", "Tanvir Hasan", "Room 312", "01677889900", "pass07"),
            ("S008", "Mehnaz Karim", "Room 415", "01899001122", "pass08"),
            ("S009", "Zahidul Islam", "Room 310", "01900112233", "pass09"),
            ("S010", "Rayhan Chowdhury", "Room 205", "01500223344", "pass10")
        ]
        
        for sid, name, room, phone, pwd in students_data:
            s = Student(sid, name, room, phone, "2025-07-01", "student", pwd)
            self.students_list.append(s)
            self.student_id_set.add(sid)
            
        # Add some initial menu records for July 2025
        menu_items_seed = [
            # Sunday
            ("2025-07-06", "Breakfast", ["Paratha", "Egg Fry", "Dal"]),
            ("2025-07-06", "Lunch", ["Rice", "Beef Curry", "Dal"]),
            ("2025-07-06", "Dinner", ["Rice", "Fish Curry", "Vorta"]),
            # Monday
            ("2025-07-07", "Breakfast", ["Khichuri", "Egg Curry"]),
            ("2025-07-07", "Lunch", ["Rice", "Chicken Roast", "Dal"]),
            ("2025-07-07", "Dinner", ["Rice", "Egg Bhuna", "Vegetable"]),
        ]
        for dt, mt, dishes in menu_items_seed:
            self.menu_items.append(MenuItem(dt, mt, dishes))
            
        # Add some initial meal ON/OFF records
        for s in self.students_list:
            if s.role == "student":
                self.meal_records.append(MealRecord(s.student_id, "2025-07-06", True, True, True))
                self.meal_records.append(MealRecord(s.student_id, "2025-07-07", True, True, True))
                
        # Add demo grocery purchases for 2026-07 and 2026-08 matching weekly menu for 10 members
        demo_groceries = [
            ("G101", "2026-07-01", "Minikit Rice 50kg (2 Bags)", 2, "pcs", 3250.0, "admin01"),
            ("G102", "2026-07-03", "Soybean Oil 5L Can (2 Cans)", 2, "pcs", 850.0, "admin01"),
            ("G103", "2026-07-05", "Fresh Farm Chicken 18kg", 18, "kg", 210.0, "admin01"),
            ("G104", "2026-07-10", "Rui Fish 15kg", 15, "kg", 320.0, "admin01"),
            ("G105", "2026-07-12", "Farm Eggs (12 Crates / 360 pcs)", 12, "pcs", 360.0, "admin01"),
            ("G106", "2026-07-17", "Beef 12kg (Friday Special)", 12, "kg", 750.0, "admin01"),
            ("G107", "2026-07-20", "Masoor Dal (Pulse) 15kg", 15, "kg", 130.0, "admin01"),
            ("G108", "2026-07-22", "Atta (Flour) 25kg & Potatoes 25kg", 1, "lot", 2725.0, "admin01"),
            ("G109", "2026-07-24", "Polao Rice & Biryani Spices", 1, "lot", 2200.0, "admin01"),
            ("G110", "2026-07-26", "Fresh Mixed Vegetables (Weekly Batch)", 40, "kg", 40.0, "admin01"),
            ("G201", "2026-08-01", "Minikit Rice 50kg (2 Bags)", 2, "pcs", 3250.0, "admin01"),
            ("G202", "2026-08-02", "Soybean Oil 5L Can (2 Cans)", 2, "pcs", 850.0, "admin01"),
            ("G203", "2026-08-03", "Fresh Farm Chicken 18kg", 18, "kg", 210.0, "admin01"),
            ("G204", "2026-08-05", "Farm Eggs (12 Crates)", 12, "pcs", 360.0, "admin01"),
            ("G205", "2026-08-07", "Beef 12kg (Friday Special)", 12, "kg", 750.0, "admin01"),
        ]
        for gid, dt, name, qty, unit, price, by in demo_groceries:
            self.grocery_list.append(GroceryEntry(gid, dt, name, qty, unit, price, by))
        
        # Add some initial payments
        self.payments_list.append(Payment("P001", "S001", 1000.0, "2025-07-02", "2025-07", "bKash", "July advance"))
        self.payments_list.append(Payment("P002", "S002", 800.0, "2025-07-03", "2025-07", "Cash", "July bill"))
        self.payments_list.append(Payment("P003", "S003", 1200.0, "2025-07-04", "2025-07", "bKash", "Advance"))
        
        self.save_all()

    # --- Student Operations ---
    def add_student(self, student):
        if student.student_id in self.student_id_set:
            return False
        self.students_list.append(student)
        self.student_id_set.add(student.student_id)
        self.save_all()
        return True

    def get_all_students(self):
        return [s for s in self.students_list if s.role == "student"]

    def search_student(self, query):
        if not query:
            return self.get_all_students()
        q = str(query).lower().strip()
        results = []
        for s in self.students_list:
            if s.role == "student" and (q in s.student_id.lower() or q in s.name.lower()):
                results.append(s)
        return results

    def update_student(self, student_id, name, room_number, phone, role, password):
        for s in self.students_list:
            if s.student_id == student_id:
                s.name = name
                s.room_number = room_number
                s.phone = phone
                s.role = role
                s.password = password
                self.save_all()
                return True
        return False

    def delete_student(self, student_id):
        student_to_remove = None
        for s in self.students_list:
            if s.student_id == student_id:
                student_to_remove = s
                break
        if student_to_remove:
            self.students_list.remove(student_to_remove)
            self.student_id_set.discard(student_id)
            
            # Cascade delete meals and payments and requests
            self.meal_records = [r for r in self.meal_records if r.student_id != student_id]
            self.payments_list = [p for p in self.payments_list if p.student_id != student_id]
            self.requests_list = [r for r in self.requests_list if r.student_id != student_id]
            
            self.save_all()
            return True
        return False

    def authenticate(self, student_id, password):
        sid = str(student_id).strip()
        for s in self.students_list:
            if s.student_id == sid and s.password == password:
                return s
        return None

    # --- Meal Operations ---
    def set_meal(self, student_id, date, breakfast, lunch, dinner):
        for r in self.meal_records:
            if r.student_id == student_id and r.date == date:
                r.breakfast = bool(breakfast)
                r.lunch = bool(lunch)
                r.dinner = bool(dinner)
                self.save_all()
                return r
        new_record = MealRecord(student_id, date, breakfast, lunch, dinner)
        self.meal_records.append(new_record)
        self.save_all()
        return new_record

    def get_meal(self, student_id, date):
        for r in self.meal_records:
            if r.student_id == student_id and r.date == date:
                return r
        # Default for any active mess member is Meal ON (True, True, True)
        return MealRecord(student_id, date, True, True, True)

    def get_monthly_meals(self, student_id, month):
        # Returns meal records for student in month (up to current day for current month)
        from datetime import datetime
        import calendar
        try:
            yr, mo = map(int, month.split("-"))
            _, num_days = calendar.monthrange(yr, mo)
        except Exception:
            num_days = 30
            
        today_dt = datetime.now()
        current_month_str = today_dt.strftime("%Y-%m")
        
        if month == current_month_str:
            max_day = min(today_dt.day, num_days)
        elif month < current_month_str:
            max_day = num_days
        else:
            max_day = 0
            
        existing_map = {r.date: r for r in self.meal_records if r.student_id == student_id and r.date.startswith(month)}
        res = []
        for day_num in range(1, max_day + 1):
            date_str = f"{month}-{day_num:02d}"
            if date_str in existing_map:
                res.append(existing_map[date_str])
            else:
                res.append(MealRecord(student_id, date_str, True, True, True))
        return res

    def get_all_meals_on_date(self, date):
        b = 0
        l = 0
        d = 0
        active_students = self.get_all_students()
        for s in active_students:
            r = self.get_meal(s.student_id, date)
            if r:
                if r.breakfast: b += 1
                if r.lunch: l += 1
                if r.dinner: d += 1
        return b, l, d

    def count_total_meals(self, student_id, month):
        student_records = self.get_monthly_meals(student_id, month)
        return sum(r.count_meals() for r in student_records)

    def count_all_meals_in_month(self, month):
        active_students = self.get_all_students()
        total = 0
        for s in active_students:
            total += self.count_total_meals(s.student_id, month)
        return total

    # --- Menu Operations ---
    def set_menu(self, date, meal_type, dishes):
        # Normalize dishes to list
        if isinstance(dishes, str):
            dishes_list = [d.strip() for d in dishes.split(",") if d.strip()]
        else:
            dishes_list = list(dishes)
            
        for m in self.menu_items:
            if m.date == date and m.meal_type == meal_type:
                m.dishes = dishes_list
                self.save_all()
                return m
        new_item = MenuItem(date, meal_type, dishes_list)
        self.menu_items.append(new_item)
        self.save_all()
        return new_item

    def get_menu(self, date):
        # Returns a dict of {meal_type: dishes_list} for a given date
        menu_dict = {}
        for m in self.menu_items:
            if m.date == date:
                menu_dict[m.meal_type] = m.dishes
                
        from datetime import datetime
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            day_name = dt.strftime("%A")
            default_day = self.DEFAULT_WEEKLY_MENU.get(day_name, {})
        except Exception:
            default_day = {}
            
        res = {}
        for meal_type in self.MEAL_TYPES:
            if meal_type in menu_dict and menu_dict[meal_type]:
                res[meal_type] = menu_dict[meal_type]
            else:
                res[meal_type] = default_day.get(meal_type, [])
                
        return res

    def get_weekly_menu(self, start_date_obj):
        # start_date_obj is a datetime object or string. Let's support string.
        # We will parse it and fetch 7 days of menus.
        from datetime import datetime, timedelta
        if isinstance(start_date_obj, str):
            start = datetime.strptime(start_date_obj, "%Y-%m-%d")
        else:
            start = start_date_obj
            
        weekly = {}
        for i in range(7):
            day = start + timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            weekly[day_str] = self.get_menu(day_str)
        return weekly

    # --- Grocery Operations ---
    def add_grocery(self, entry):
        self.grocery_list.append(entry)
        self.save_all()
        return True

    def get_groceries_by_date(self, date):
        return [e for e in self.grocery_list if e.date == date]

    def get_groceries_by_month(self, month):
        return [e for e in self.grocery_list if e.date.startswith(month)]

    def get_monthly_expense(self, month):
        monthly = self.get_groceries_by_month(month)
        return calc.get_total_monthly_expense(monthly)

    def calculate_meal_rate(self, month):
        total_cost = self.get_monthly_expense(month)
        total_meals = self.count_all_meals_in_month(month)
        
        rate = calc.get_meal_rate(total_cost, total_meals)
        # If no rate is computed (e.g. no groceries entered yet for a future month),
        # return the default config rate.
        if rate <= 0:
            return self.config["meal_rate"]
        return rate

    # --- Payment Operations ---
    def record_payment(self, payment):
        self.payments_list.append(payment)
        self.save_all()
        return True

    def get_payments(self, student_id):
        return [p for p in self.payments_list if p.student_id == student_id]

    def get_monthly_payments(self, student_id, month):
        return [p for p in self.payments_list if p.student_id == student_id and p.month == month]

    def get_all_payments_in_month(self, month):
        return [p for p in self.payments_list if p.month == month]

    def calculate_due(self, student_id, month):
        """
        Dues = (Meals taken in month * Meal rate of month) - Payments in month + Carry-forward previous dues.
        Wait, to keep things simple and avoid complex recursion, let's define dues for a single month:
        due = (Meals taken * Rate) - Paid in month.
        Let's retrieve previous months to accumulate previous unpaid balances as well! That is even better.
        For simplicity, let's sum meals taken * monthly_rates for all time, and subtract all payments for all time.
        This represents the overall total dues of the student perfectly!
        Let's implement:
        Total Dues = (All time meals * rates) - (All time payments).
        This is robust, accurate, and completely avoids boundary issues.
        Let's calculate this overall due:
        """
        # Get all months in meal records
        months_set = set(r.date[:7] for r in self.meal_records if r.student_id == student_id)
        # Also include months in payments
        months_set.update(p.month for p in self.payments_list if p.student_id == student_id)
        
        total_billed = 0.0
        for m in sorted(list(months_set)):
            meals_count = self.count_total_meals(student_id, m)
            rate = self.calculate_meal_rate(m)
            total_billed += meals_count * rate
            
        total_paid = sum(p.amount for p in self.payments_list if p.student_id == student_id)
        
        overall_due = total_billed - total_paid
        return max(0.0, overall_due)

    # --- Request Operations ---
    def submit_request(self, request):
        # Prevent duplicate request IDs
        while request.request_id in self.used_request_ids:
            import uuid
            request.request_id = "R" + str(uuid.uuid4().hex[:6]).upper()
        self.requests_list.append(request)
        self.used_request_ids.add(request.request_id)
        self.save_all()
        return True

    def get_pending_requests(self):
        return [r for r in self.requests_list if r.status == "Pending"]

    def get_student_requests(self, student_id):
        return [r for r in self.requests_list if r.student_id == student_id]

    def approve_request(self, req_id):
        for r in self.requests_list:
            if r.request_id == req_id:
                r.status = "Approved"
                # Update weekly menu!
                self.set_menu(r.target_date, r.meal_type, r.suggested_dish)
                self.save_all()
                return True
        return False

    def reject_request(self, req_id):
        for r in self.requests_list:
            if r.request_id == req_id:
                r.status = "Rejected"
                self.save_all()
                return True
        return False

    def get_request_summary(self, date, meal_type):
        """
        Aggregates suggestions for a specific date/meal type.
        Returns a dictionary mapping dish name to the count of student requests.
        """
        summary = {}
        for r in self.requests_list:
            if r.target_date == date and r.meal_type == meal_type and r.status == "Pending":
                dish = r.suggested_dish.strip()
                summary[dish] = summary.get(dish, 0) + 1
        return summary

    # --- File Operations ---
    def save_all(self):
        fh.save_json(self.students_list, self.students_file)
        fh.save_json(self.meal_records, self.meals_file)
        fh.save_json(self.menu_items, self.menu_file)
        fh.save_json(self.grocery_list, self.grocery_file)
        fh.save_json(self.payments_list, self.payments_file)
        fh.save_json(self.requests_list, self.requests_file)
        fh.save_config(self.config, self.config_file)

    def load_all(self):
        self.students_list = fh.load_json(self.students_file, Student)
        self.meal_records = fh.load_json(self.meals_file, MealRecord)
        self.menu_items = fh.load_json(self.menu_file, MenuItem)
        self.grocery_list = fh.load_json(self.grocery_file, GroceryEntry)
        self.payments_list = fh.load_json(self.payments_file, Payment)
        self.requests_list = fh.load_json(self.requests_file, MenuRequest)
        
        # Sync sets
        self.student_id_set = set(s.student_id for s in self.students_list)
        self.used_request_ids = set(r.request_id for r in self.requests_list)
