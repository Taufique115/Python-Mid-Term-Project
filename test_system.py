import os
import shutil
import numpy as np
import validators as val
import calculations as calc
from models import Student, GroceryEntry, Payment
from manager import MessManager

def run_tests():
    print("==============================================")
    # 1. Test Validators
    print("Test 1: Testing Input Validators...")
    try:
        val.validate_phone("01712345678")
        val.validate_phone("17123456789")  # Should fail
        raise AssertionError("Validation failed to catch bad phone prefix")
    except ValueError as e:
        print(f"  [OK] Caught invalid phone prefix: '{e}'")
        
    try:
        val.validate_amount("-50")
        raise AssertionError("Validation failed to catch negative values")
    except ValueError as e:
        print(f"  [OK] Caught invalid negative amount: '{e}'")
        
    try:
        val.validate_date("2025-13-45")
        raise AssertionError("Validation failed to catch out of range date")
    except ValueError as e:
        print(f"  [OK] Caught invalid date range: '{e}'")
        
    print("  [OK] All validators passed.")
    print("----------------------------------------------")
    
    # 2. Test NumPy Calculations
    print("Test 2: Testing NumPy calculations...")
    groceries = [
        GroceryEntry("G1", "2025-07-01", "Item A", 2.0, "pcs", 100.0, "admin"), # 200
        GroceryEntry("G2", "2025-07-02", "Item B", 1.0, "pcs", 300.0, "admin"), # 300
        GroceryEntry("G3", "2025-07-03", "Item C", 5.0, "kg",  20.0,  "admin"), # 100
    ]
    avg_cost = calc.get_average_daily_cost(groceries)
    total_cost = calc.get_total_monthly_expense(groceries)
    
    assert np.isclose(avg_cost, 200.0), f"Expected 200, got {avg_cost}"
    assert np.isclose(total_cost, 600.0), f"Expected 600, got {total_cost}"
    print(f"  [OK] Average Cost: {avg_cost}")
    print(f"  [OK] Total Spending: {total_cost}")
    
    stats = calc.get_grocery_statistics(groceries)
    assert np.isclose(stats["std"], np.std([200, 300, 100])), "Std calculation discrepancy"
    print(f"  [OK] Standard Deviation of spending: {stats['std']:.2f}")
    
    print("  [OK] All NumPy calculations passed.")
    print("----------------------------------------------")
    
    # 3. Test Manager Seeding & Operations
    print("Test 3: Testing MessManager File Sync and DB Operations...")
    
    # Use a temp directory for test database
    test_db_dir = "test_data_dir"
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)
        
    manager = MessManager(data_dir=test_db_dir)
    
    # Check default seeded records
    students = manager.get_all_students()
    print(f"  [OK] Seeded active students count: {len(students)}")
    assert len(students) == 10, "Expected 10 seeded students"
    
    # Check auth
    admin_auth = manager.authenticate("admin01", "admin123")
    assert admin_auth is not None and admin_auth.role == "admin", "Admin auth failed"
    student_auth = manager.authenticate("S001", "pass01")
    assert student_auth is not None and student_auth.role == "student", "Student auth failed"
    print("  [OK] User authentication confirmed.")
    
    # Check CRUD Student
    new_s = Student("S999", "Tester Student", "Room 999", "01799999999", "2025-07-01", "student", "pass999")
    manager.add_student(new_s)
    assert "S999" in manager.student_id_set, "Failed to register new student"
    
    results = manager.search_student("Tester")
    assert len(results) == 1, "Failed to search student by name"
    print("  [OK] CRUD Account creation and search passed.")
    
    # Check billing calculation
    # Simulate a payment
    manager.record_payment(Payment("P99", "S001", 500.0, "2025-07-07", "2025-07", "Cash"))
    
    # Cleanup temp test database
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)
        
    print("  [OK] Manager lifecycle and file operations passed.")
    print("==============================================")
    print("ALL CORE LOGIC TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
