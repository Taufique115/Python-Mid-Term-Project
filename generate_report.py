import os
import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
        print(f"'{package}' is already installed.")
    except ImportError:
        print(f"'{package}' not found. Attempting to install dynamically...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed '{package}'.")
        except Exception as e:
            print(f"Error installing '{package}': {e}")
            print("Please run 'pip install reportlab' manually in your command prompt.")
            sys.exit(1)

# Check and install reportlab if needed
install_and_import("reportlab")

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def build_pdf(filename="report/project_report.pdf"):
    print(f"Generating PDF Report at: {filename}...")
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # Setup document template
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#5C67F2'),
        alignment=1, # Centered
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#64748B'),
        alignment=1, # Centered
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    code_style = ParagraphStyle(
        'CodeStyleCustom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#E2E8F0'),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8
    )
    
    story = []
    
    # Document Header
    story.append(Paragraph("MESS MEMBER MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("AIUB Python Mid-Term Project Report | Summer 25-26", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Section 1: Member Info Table
    story.append(Paragraph("1. Project & Member Information", heading_style))
    member_data = [
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("Mess Member Management System (Tkinter + NumPy)", body_style)],
        [Paragraph("<b>Course Name:</b>", body_style), Paragraph("Programming in Python (CS Major Mid-Term Project)", body_style)],
        [Paragraph("<b>Group Members:</b>", body_style), Paragraph("AIUB Student Group", body_style)],
        [Paragraph("<b>Development Date:</b>", body_style), Paragraph("July 2026", body_style)],
    ]
    t1 = Table(member_data, colWidths=[2.0*inch, 5.0*inch])
    t1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(t1)
    story.append(Spacer(1, 15))
    
    # Section 2: Problem Statement & Objectives
    story.append(Paragraph("2. Problem Statement & Objectives", heading_style))
    p_statement = (
        "Hostel mess facilities in university environments, such as for AIUB students, face significant "
        "difficulties in managing meal logging, tracking daily groceries, compiling weekly menus, and reconciling "
        "balances. Traditional paper-based registers result in data inaccuracies, disputes, lack of transparent "
        "cost auditing, and food waste. "
        "<br/><br/>"
        "<b>Objectives:</b>"
        "<br/>"
        "• Establish a secure, role-based login system for Members and Mess Administrators."
        "<br/>"
        "• Automate meal ON/OFF scheduling with date constraints to prevent member backdating."
        "<br/>"
        "• Implement dynamic, transparent monthly meal rates based on actual grocery costs and meal logs."
        "<br/>"
        "• Provide a central approval flow for member feedback and weekly menu change proposals."
    )
    story.append(Paragraph(p_statement, body_style))
    story.append(Spacer(1, 15))
    
    # Section 3: Feature List & Target Users
    story.append(Paragraph("3. Feature List & Target Users", heading_style))
    features = (
        "<b>Target Users:</b> Hostel Mess Administrators (Provost, House Tutors) and Mess Members."
        "<br/><br/>"
        "<b>Core Features:</b>"
        "<br/>"
        "• <b>Admin Account Directory:</b> Create, update, search, and delete (CRUD) member profiles."
        "<br/>"
        "• <b>Interactive Meal Calendar:</b> View meal participation grids and toggle meal counts."
        "<br/>"
        "• <b>Grocery Ledger:</b> Track item costs and auto-calculate dynamic monthly meal rates."
        "<br/>"
        "• <b>Ledger Balance:</b> Log member cash payments, adjust dues, and audit financials."
        "<br/>"
        "• <b>Menu Change Requests:</b> Submit recommendations (Members) and approve proposals (Admins)."
    )
    story.append(Paragraph(features, body_style))
    story.append(Spacer(1, 15))
    
    # Section 4: Python Concepts Applied
    story.append(Paragraph("4. Python Concepts Applied (Week 1-5)", heading_style))
    concepts = (
        "• <b>Variables & Types:</b> Models map parameters using floats (amounts), strings (IDs), and booleans (meal ON/OFF)."
        "<br/>"
        "• <b>Operators:</b> Calculate meal cost metrics (quantity * unit price) and subtract payments to derive due amounts."
        "<br/>"
        "• <b>Branching (if-elif-else):</b> Direct users to appropriate role dashboards (Admin/Member) and check field ranges."
        "<br/>"
        "• <b>Loops (for):</b> Process lists of members, scan entries, and draw days in calendar grids."
        "<br/>"
        "• <b>Functions & Modularity:</b> Separated logic across specialized modules (main, models, manager, validators, etc.)."
    )
    story.append(Paragraph(concepts, body_style))
    story.append(Spacer(1, 15))
    
    # Section 5: Data Structures Explanation
    story.append(Paragraph("5. Data Structures Explanation", heading_style))
    structs = (
        "• <b>List:</b> Used for collections (e.g. students_list, grocery_list) that require ordering and iterative filtering."
        "<br/>"
        "• <b>Tuple:</b> Fixed options (e.g. MEAL_TYPES = ('Breakfast', 'Lunch', 'Dinner')) to prevent runtime alterations."
        "<br/>"
        "• <b>Set:</b> Quick index collections (e.g. student_id_set, used_request_ids) to prevent duplicates and enable O(1) checks."
        "<br/>"
        "• <b>Dictionary:</b> Configuration keys (e.g. config.json) and mapping lookups for menu lists by date."
    )
    story.append(Paragraph(structs, body_style))
    story.append(Spacer(1, 15))
    
    # Section 6: Object-Oriented Design (OOP)
    story.append(Paragraph("6. Object-Oriented Design (OOP)", heading_style))
    oop_desc = (
        "The project follows object-oriented programming. Data models are encapsulated in 6 distinct classes in models.py:"
        "<br/>"
        "• <b>Student:</b> Attributes: student_id, name, room_number, phone, join_date, role, password, total_due."
        "<br/>"
        "• <b>MealRecord:</b> Attributes: student_id, date, breakfast, lunch, dinner. Methods: count_meals()."
        "<br/>"
        "• <b>GroceryEntry:</b> Attributes: entry_id, date, item_name, quantity, unit, unit_price, total_cost, added_by."
        "<br/>"
        "• <b>MessManager:</b> Centralizes business logic. Manages list buffers, coordinates logins, and saves state to JSON."
    )
    story.append(Paragraph(oop_desc, body_style))
    story.append(Spacer(1, 15))
    
    # Section 7: File & Exception Handling
    story.append(Paragraph("7. File & Exception Handling", heading_style))
    files_desc = (
        "Data persistence is maintained across 6 JSON databases. The system handles standard edge cases gracefully:"
        "<br/>"
        "• <b>FileNotFoundError:</b> Handled in file_handler.py, returning empty structures and creating files on first write."
        "<br/>"
        "• <b>JSONDecodeError:</b> Catches corrupted/truncated database files, warning the user and initializing empty buffers."
        "<br/>"
        "• <b>ValueError:</b> Validates input fields, catching non-numeric values and format mismatches without crashing."
    )
    story.append(Paragraph(files_desc, body_style))
    story.append(Spacer(1, 15))
    
    # Section 8: Library Usage (NumPy & Tkinter)
    story.append(Paragraph("8. Library Usage (NumPy & Tkinter)", heading_style))
    lib_desc = (
        "• <b>Tkinter (GUI):</b> Formulates all visual elements, including Sidebar frames, treeviews, form fields, and widgets."
        "<br/>"
        "• <b>NumPy (Math & Stats):</b> Crucial math operations compiled using NumPy arrays in calculations.py:"
        "<br/>"
        "  - <i>get_average_daily_cost:</i> np.mean() computes average daily spending."
        "<br/>"
        "  - <i>get_grocery_statistics:</i> np.std() computes standard deviation of expenditures."
        "<br/>"
        "  - <i>get_due_summary:</i> np.sum(), np.mean(), and np.max() compile member billing balances."
    )
    story.append(Paragraph(lib_desc, body_style))
    story.append(Spacer(1, 15))
    
    # Section 9: Limitations & Improvements
    story.append(Paragraph("9. Limitations & Future Improvements", heading_style))
    limitations = (
        "• <b>Database Scaling:</b> JSON file storage is optimal for mid-term school projects but is not suitable for large concurrent "
        "hostel installations. Migrating to SQLite would improve transactional scale."
        "<br/>"
        "• <b>No Real-Time Server Sync:</b> Since this is a local desktop Tkinter app, it operates on a single file system. "
        "Integrating a lightweight REST API would support remote client connections."
    )
    story.append(Paragraph(limitations, body_style))
    
    # Build the document
    doc.build(story)
    print("PDF Generation Completed successfully.")

if __name__ == "__main__":
    build_pdf()
