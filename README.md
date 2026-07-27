# 🏠 AIUB Blue Bird Mess Management System (SmartMess AIUB)

> **CS Major Mid-Term Project | Programming in Python**  
> *AIUB Student Mess Management System with Dual Interfaces (Tkinter Desktop Application + Claymorphism 3D Web Portal)*

---

## 🌟 Overview

**SmartMess AIUB** is an automated, role-based dining and financial management solution designed for university student hostels. It replaces manual paper ledgers with real-time meal scheduling, dynamic advance balance tracking, statistical grocery auditing, and automated report generation.

---

## ✨ Features

### 👤 Part 1: Student & Member Portal (Pushed: 07/20/2026)
* **🔐 Secure Authentication:** Role-isolated login portal for Mess Members.
* **🍽️ Daily Meal Control:** Toggles for Breakfast (7:30 AM), Lunch (2:00 PM), and Dinner (10:00 PM) with real-time participation updates.
* **💰 Dynamic Advance Balance:** Automatically tracks excess payments (`Paid > Bill`) as Advance Balance and deducts meal costs in real-time as meals are taken.
* **💳 Payment Gateway Integration:** Supports **bKash**, **Nagad**, and **Cash** (paid to manager by hand) with instant transaction history logging.
* **📝 Menu Requests:** Dish suggestion submission and voting system.

### 👑 Part 2: Admin Panel & Financial Auditing (Pushed: 07/27/2026)
* **📊 5 KPI Summary Cards:** Live tracking of Total Active Members (10), Today's Meals (30), Monthly Total Meals (810), Monthly Expense (৳ 38,575.00), and Outstanding Dues.
* **🛒 Grocery & Cost Auditing:** Calculates exact monthly meal rates using **NumPy** statistical algorithms (৳ 47.68 / meal for July 2026).
* **📋 Weekly Menu Management:** Interactive 7-day schedule with active day highlighting (`2026-07-27`) and admin inline editing.
* **👤 Mess Manager Profile:** Manager details for **Cristiano Messi Junior** (01710112341, `cristianomessineymar@gmail.com`, Bashundhara, Dhaka).
* **📄 Automated PDF Reports:** Generates statistical summary reports (`report/project_report.pdf`).
* **🌐 High-Performance Claymorphic Web Portal:** Responsive 3D web dashboard (`index.html`) with live digital clock and role switcher.

---

## 🚀 Installation & Running

### Prerequisites
* Python 3.10+
* NumPy (`pip install numpy`)
* ReportLab (`pip install reportlab` - optional for PDF generation)

### Quick Run
```bash
# Double-click the Windows batch launcher:
run_app.bat

# Or run directly via terminal:
python main.py
```

### Web Portal Run
Simply open `index.html` in any modern web browser!

---

## 📁 Repository Structure
```
Python Project_1/
│
├── main.py                  # Application Entry Point
├── manager.py               # Business Logic & Data Manager
├── models.py                # OOP Data Classes (Student, MealRecord, Payment, etc.)
├── calculations.py          # NumPy Statistical Algorithms & Auditing
├── file_handler.py          # JSON File Persistence
├── validators.py            # Input Validation Rules
├── generate_report.py       # PDF Report Generator
├── run_app.bat              # One-Click Application Launcher
│
├── gui/                     # Tkinter Desktop GUI Components
│   ├── widgets.py           # Claymorphism Theme & Custom Widgets
│   ├── login_window.py      # Authentication & Portal Selection
│   ├── admin_dashboard.py   # Admin Panel & Summary Overview
│   ├── member_dashboard.py  # Member Portal & Advance Balance Card
│   ├── menu_mgmt.py         # Weekly Menu Schedule
│   ├── grocery_mgmt.py      # Grocery Purchases & Meal Rate
│   ├── payment_mgmt.py      # Billing & Payments
│   ├── meal_calendar.py     # Daily Meal Toggles
│   ├── member_mgmt.py       # Member Roster Management
│   ├── requests_mgmt.py     # Menu Suggestions & Voting
│   └── reports.py           # Reports & PDF Generator
│
├── data/                    # JSON Database Files
│   ├── students.json
│   ├── meals.json
│   ├── menu.json
│   ├── grocery.json
│   ├── payments.json
│   ├── requests.json
│   └── config.json
│
├── index.html               # Claymorphism Web Portal
├── styles.css               # Claymorphism 3D CSS Styles
└── app.js                   # Web Portal Logic & Live Clock
```

---

## 🎓 Author & Credits
* **Project Name:** AIUB Blue Bird Mess Management System
* **Institution:** American International University-Bangladesh (AIUB)
* **Manager Contact:** Cristiano Messi Junior (01710112341 | `cristianomessineymar@gmail.com`)
