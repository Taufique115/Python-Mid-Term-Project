import numpy as np

def get_average_daily_cost(grocery_list):
    """
    Returns the mean cost of grocery purchases.
    Uses numpy.mean.
    """
    if not grocery_list:
        return 0.0
    costs = np.array([float(entry.total_cost) for entry in grocery_list])
    return float(np.mean(costs))

def get_total_monthly_expense(grocery_list):
    """
    Returns the total expense of groceries for a month.
    Uses numpy.sum.
    """
    if not grocery_list:
        return 0.0
    costs = np.array([float(entry.total_cost) for entry in grocery_list])
    return float(np.sum(costs))

def get_grocery_statistics(grocery_list):
    """
    Returns standard statistical measures for grocery purchases:
    Total, Mean, Median, Standard Deviation, Max, Min, and count of entries.
    Uses numpy operations.
    """
    if not grocery_list:
        return {
            "total": 0.0,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "max": 0.0,
            "min": 0.0,
            "count": 0
        }
    costs = np.array([float(entry.total_cost) for entry in grocery_list])
    return {
        "total": float(np.sum(costs)),
        "mean": float(np.mean(costs)),
        "median": float(np.median(costs)),
        "std": float(np.std(costs)),
        "max": float(np.max(costs)),
        "min": float(np.min(costs)),
        "count": len(costs)
    }

def get_meal_rate(total_cost, total_meals):
    """
    Calculates the meal rate = total_cost / total_meals.
    Guarded against division by zero.
    """
    if total_meals <= 0:
        return 0.0
    return float(total_cost) / float(total_meals)

def get_student_meal_stats(meal_records):
    """
    Given a list of MealRecord objects for a student, returns:
    - Total breakfast count
    - Total lunch count
    - Total dinner count
    - Total meals taken
    - Daily average meals
    Uses NumPy summation and mean.
    """
    if not meal_records:
        return {
            "breakfast": 0,
            "lunch": 0,
            "dinner": 0,
            "total": 0,
            "average": 0.0
        }
        
    # Convert records into matrix: rows = days, columns = [breakfast, lunch, dinner]
    data = np.array([
        [int(r.breakfast), int(r.lunch), int(r.dinner)] for r in meal_records
    ])
    
    # Calculate sum along columns (meals types)
    sums = np.sum(data, axis=0)
    total_meals_per_day = np.sum(data, axis=1)
    
    return {
        "breakfast": int(sums[0]),
        "lunch": int(sums[1]),
        "dinner": int(sums[2]),
        "total": int(np.sum(sums)),
        "average": float(np.mean(total_meals_per_day))
    }

def get_highest_spender_month(payments):
    """
    Returns the maximum single payment amount made.
    Uses numpy.max.
    """
    if not payments:
        return 0.0
    amounts = np.array([float(p.amount) for p in payments])
    return float(np.max(amounts))

def get_due_summary(all_students, current_month, manager):
    """
    Computes summary metrics (total sum, mean, max) of outstanding dues across all students.
    Uses NumPy arrays.
    """
    if not all_students:
        return {"sum": 0.0, "mean": 0.0, "max": 0.0, "count": 0}
        
    dues = np.array([
        float(manager.calculate_due(student.student_id, current_month))
        for student in all_students
    ])
    
    return {
        "sum": float(np.sum(dues)),
        "mean": float(np.mean(dues)),
        "max": float(np.max(dues)),
        "count": len(dues)
    }

def get_monthly_trend(grocery_list, months_list):
    """
    Computes total expenditures for a list of target months (format: YYYY-MM).
    Returns a numpy array of monthly expenditure totals.
    """
    totals = []
    for month in months_list:
        monthly_entries = [
            e for e in grocery_list if e.date.startswith(month)
        ]
        totals.append(get_total_monthly_expense(monthly_entries))
    return np.array(totals)

def get_meal_participation_rate(date, total_students, ate_count):
    """
    Calculates meal participation percentage for a date.
    """
    if total_students <= 0:
        return 0.0
    # Use simple percentage
    return (float(ate_count) / float(total_students)) * 100.0
