class Student:
    def __init__(self, student_id, name, room_number, phone, join_date, role, password, total_due=0.0):
        self.student_id = student_id
        self.name = name
        self.room_number = room_number
        self.phone = phone
        self.join_date = join_date
        self.role = role  # "admin" or "student"
        self.password = password
        self.total_due = float(total_due)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "room_number": self.room_number,
            "phone": self.phone,
            "join_date": self.join_date,
            "role": self.role,
            "password": self.password,
            "total_due": self.total_due
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            room_number=data["room_number"],
            phone=data["phone"],
            join_date=data["join_date"],
            role=data["role"],
            password=data["password"],
            total_due=data.get("total_due", 0.0)
        )

    def __str__(self):
        return f"Student(ID={self.student_id}, Name={self.name}, Room={self.room_number}, Role={self.role}, Due={self.total_due})"


class MealRecord:
    def __init__(self, student_id, date, breakfast=True, lunch=True, dinner=True):
        self.student_id = student_id
        self.date = date
        self.breakfast = bool(breakfast)
        self.lunch = bool(lunch)
        self.dinner = bool(dinner)

    def count_meals(self):
        # Counts how many meals are ON for this record (maximum 3)
        return sum([self.breakfast, self.lunch, self.dinner])

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "date": self.date,
            "breakfast": self.breakfast,
            "lunch": self.lunch,
            "dinner": self.dinner
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data["student_id"],
            date=data["date"],
            breakfast=data.get("breakfast", True),
            lunch=data.get("lunch", True),
            dinner=data.get("dinner", True)
        )

    def __str__(self):
        return f"MealRecord(StudentID={self.student_id}, Date={self.date}, B={self.breakfast}, L={self.lunch}, D={self.dinner})"


class MenuItem:
    def __init__(self, date, meal_type, dishes):
        self.date = date
        self.meal_type = meal_type  # "Breakfast", "Lunch", "Dinner"
        self.dishes = list(dishes) if isinstance(dishes, list) else [d.strip() for d in dishes.split(",") if d.strip()]

    def to_dict(self):
        return {
            "date": self.date,
            "meal_type": self.meal_type,
            "dishes": self.dishes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            date=data["date"],
            meal_type=data["meal_type"],
            dishes=data["dishes"]
        )

    def __str__(self):
        return f"MenuItem(Date={self.date}, Type={self.meal_type}, Dishes={', '.join(self.dishes)})"


class GroceryEntry:
    def __init__(self, entry_id, date, item_name, quantity, unit, unit_price, added_by, total_cost=None):
        self.entry_id = entry_id
        self.date = date
        self.item_name = item_name
        self.quantity = float(quantity)
        self.unit = unit  # "kg", "litre", "pcs"
        self.unit_price = float(unit_price)
        self.added_by = added_by
        if total_cost is not None:
            self.total_cost = float(total_cost)
        else:
            self.total_cost = self.calculate_total()

    def calculate_total(self):
        return self.quantity * self.unit_price

    def to_dict(self):
        return {
            "entry_id": self.entry_id,
            "date": self.date,
            "item_name": self.item_name,
            "quantity": self.quantity,
            "unit": self.unit,
            "unit_price": self.unit_price,
            "total_cost": self.total_cost,
            "added_by": self.added_by
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            entry_id=data["entry_id"],
            date=data["date"],
            item_name=data["item_name"],
            quantity=data["quantity"],
            unit=data["unit"],
            unit_price=data["unit_price"],
            added_by=data.get("added_by", "Admin"),
            total_cost=data.get("total_cost")
        )

    def __str__(self):
        return f"GroceryEntry(ID={self.entry_id}, Item={self.item_name}, Qty={self.quantity}{self.unit}, Cost={self.total_cost})"


class Payment:
    def __init__(self, payment_id, student_id, amount, date, month, method, note=""):
        self.payment_id = payment_id
        self.student_id = student_id
        self.amount = float(amount)
        self.date = date
        self.month = month  # "YYYY-MM"
        self.method = method  # "Cash", "bKash", etc.
        self.note = note

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "student_id": self.student_id,
            "amount": self.amount,
            "date": self.date,
            "month": self.month,
            "method": self.method,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            payment_id=data["payment_id"],
            student_id=data["student_id"],
            amount=data["amount"],
            date=data["date"],
            month=data["month"],
            method=data["method"],
            note=data.get("note", "")
        )

    def __str__(self):
        return f"Payment(ID={self.payment_id}, StudentID={self.student_id}, Amount={self.amount}, Month={self.month})"


class MenuRequest:
    def __init__(self, request_id, student_id, student_name, target_date, meal_type, current_dish, suggested_dish, status="Pending", submitted_on=""):
        self.request_id = request_id
        self.student_id = student_id
        self.student_name = student_name
        self.target_date = target_date
        self.meal_type = meal_type  # "Breakfast", "Lunch", "Dinner"
        self.current_dish = current_dish
        self.suggested_dish = suggested_dish
        self.status = status  # "Pending", "Approved", "Rejected"
        self.submitted_on = submitted_on

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "student_id": self.student_id,
            "student_name": self.student_name,
            "target_date": self.target_date,
            "meal_type": self.meal_type,
            "current_dish": self.current_dish,
            "suggested_dish": self.suggested_dish,
            "status": self.status,
            "submitted_on": self.submitted_on
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            request_id=data["request_id"],
            student_id=data["student_id"],
            student_name=data["student_name"],
            target_date=data["target_date"],
            meal_type=data["meal_type"],
            current_dish=data["current_dish"],
            suggested_dish=data["suggested_dish"],
            status=data.get("status", "Pending"),
            submitted_on=data.get("submitted_on", "")
        )

    def __str__(self):
        return f"MenuRequest(ID={self.request_id}, StudentID={self.student_id}, Date={self.target_date}, Meal={self.meal_type}, Status={self.status})"
