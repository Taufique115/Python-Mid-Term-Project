import tkinter as tk
from tkinter import messagebox
from gui.widgets import (
    COLOR_CARD, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER, FONT_SUBHEADING, FONT_BODY,
    StyledButton, LabeledEntry, create_scrollable_tree
)
from models import Student
import validators as val

class MemberMgmtView:
    def __init__(self, parent_frame, manager):
        self.parent = parent_frame
        self.manager = manager
        
        # Heading
        self.title_lbl = tk.Label(
            self.parent,
            text="Mess Member Directory",
            font=("Segoe UI", 16, "bold"),
            fg=COLOR_TEXT_MAIN,
            bg=self.parent["bg"]
        )
        self.title_lbl.pack(anchor="w", pady=(0, 15))
        
        # Search & Action bar
        self.bar = tk.Frame(self.parent, bg=self.parent["bg"])
        self.bar.pack(fill="x", pady=(0, 10))
        
        tk.Label(self.bar, text="Search Member: ", font=FONT_BODY, fg=COLOR_TEXT_MAIN, bg=self.parent["bg"]).pack(side="left")
        self.search_entry = tk.Entry(self.bar, font=FONT_BODY, width=25)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.handle_search)
        
        # Action Buttons
        self.add_btn = StyledButton(self.bar, "Add Member", self.open_add_dialog, bg_color=COLOR_SUCCESS, hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"))
        self.add_btn.pack(side="right", padx=5)
        
        self.edit_btn = StyledButton(self.bar, "Edit Member", self.open_edit_dialog, bg_color=COLOR_WARNING, hover_bg=COLOR_WARNING.replace("F59E0B", "D98006"))
        self.edit_btn.pack(side="right", padx=5)
        
        self.del_btn = StyledButton(self.bar, "Delete Member", self.handle_delete, bg_color=COLOR_DANGER, hover_bg=COLOR_DANGER.replace("EF4444", "DC2626"))
        self.del_btn.pack(side="right", padx=5)
        
        # Treeview Table
        cols = ("id", "name", "room", "phone", "join_date", "dues")
        hdgs = ("Member ID", "Full Name", "Room No.", "Phone Number", "Joined Date", "Total Dues")
        widths = {"id": 100, "room": 100, "join_date": 120, "dues": 120}
        
        self.table_frame, self.tree = create_scrollable_tree(self.parent, cols, hdgs, widths)
        self.table_frame.pack(fill="both", expand=True)
        
        # Populate records
        self.populate_table(self.manager.get_all_students())

    def populate_table(self, members_list):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        import datetime
        current_month = datetime.datetime.now().strftime("%Y-%m")
        
        for idx, m in enumerate(members_list):
            tag = "even" if idx % 2 == 0 else "odd"
            
            # Calculate dynamic due amount
            due_amt = self.manager.calculate_due(m.student_id, current_month)
            
            self.tree.insert(
                "",
                "end",
                iid=m.student_id,
                values=(m.student_id, m.name, m.room_number, m.phone, m.join_date, f"৳ {due_amt:.2f}"),
                tags=(tag,)
            )

    def handle_search(self, event=None):
        query = self.search_entry.get()
        results = self.manager.search_student(query)
        self.populate_table(results)

    def open_add_dialog(self):
        # Toplevel Dialog
        self.dialog = tk.Toplevel(self.parent.winfo_toplevel())
        self.dialog.title("Add New Mess Member")
        self.dialog.geometry("380x520")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLOR_CARD)
        
        tk.Label(self.dialog, text="Create Member Profile", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(pady=15)
        
        self.f_id = LabeledEntry(self.dialog, "Member ID (e.g. M011)")
        self.f_id.pack(fill="x", padx=30, pady=5)
        
        self.f_name = LabeledEntry(self.dialog, "Full Name")
        self.f_name.pack(fill="x", padx=30, pady=5)
        
        self.f_room = LabeledEntry(self.dialog, "Room Number (e.g. Room 302)")
        self.f_room.pack(fill="x", padx=30, pady=5)
        
        self.f_phone = LabeledEntry(self.dialog, "Phone (11 digits, starts with 01)")
        self.f_phone.pack(fill="x", padx=30, pady=5)
        
        self.f_pwd = LabeledEntry(self.dialog, "Login Password (min 4 characters)")
        self.f_pwd.pack(fill="x", padx=30, pady=5)
        
        # Save
        save = StyledButton(self.dialog, "SAVE RECORD", self.save_new_member, bg_color=COLOR_SUCCESS, hover_bg=COLOR_SUCCESS.replace("10B981", "0D9668"))
        save.pack(pady=20)

    def save_new_member(self):
        try:
            # Validate input fields using validator rules
            sid = val.validate_student_id(self.f_id.get(), self.manager.student_id_set, is_edit=False)
            name = val.validate_name(self.f_name.get())
            room = self.f_room.get()
            if not room:
                raise ValueError("Room number cannot be empty.")
            phone = val.validate_phone(self.f_phone.get())
            pwd = val.validate_password(self.f_pwd.get())
            
            import datetime
            join_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Create Student (Model remains Student internally)
            new_member = Student(sid, name, room, phone, join_date, "student", pwd)
            success = self.manager.add_student(new_member)
            
            if success:
                messagebox.showinfo("Success", f"Member {name} added successfully!", parent=self.dialog)
                self.dialog.destroy()
                self.populate_table(self.manager.get_all_students())
            else:
                messagebox.showerror("Error", "Could not add member. ID might already exist.", parent=self.dialog)
                
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e), parent=self.dialog)

    def open_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to edit.")
            return
            
        member_id = selected[0]
        member = None
        for s in self.manager.students_list:
            if s.student_id == member_id:
                member = s
                break
                
        if not member:
            return
            
        # Toplevel Dialog
        self.dialog = tk.Toplevel(self.parent.winfo_toplevel())
        self.dialog.title("Edit Member Profile")
        self.dialog.geometry("380x480")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLOR_CARD)
        
        tk.Label(self.dialog, text=f"Edit Profile: {member.student_id}", font=FONT_SUBHEADING, fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(pady=15)
        
        self.f_name = LabeledEntry(self.dialog, "Full Name")
        self.f_name.pack(fill="x", padx=30, pady=5)
        self.f_name.set(member.name)
        
        self.f_room = LabeledEntry(self.dialog, "Room Number")
        self.f_room.pack(fill="x", padx=30, pady=5)
        self.f_room.set(member.room_number)
        
        self.f_phone = LabeledEntry(self.dialog, "Phone Number")
        self.f_phone.pack(fill="x", padx=30, pady=5)
        self.f_phone.set(member.phone)
        
        self.f_pwd = LabeledEntry(self.dialog, "Login Password")
        self.f_pwd.pack(fill="x", padx=30, pady=5)
        self.f_pwd.set(member.password)
        
        # Save
        save = StyledButton(self.dialog, "UPDATE RECORD", lambda: self.save_edit_member(member_id), bg_color=COLOR_WARNING, hover_bg=COLOR_WARNING.replace("F59E0B", "D98006"))
        save.pack(pady=20)

    def save_edit_member(self, member_id):
        try:
            name = val.validate_name(self.f_name.get())
            room = self.f_room.get()
            if not room:
                raise ValueError("Room number cannot be empty.")
            phone = val.validate_phone(self.f_phone.get())
            pwd = val.validate_password(self.f_pwd.get())
            
            success = self.manager.update_student(member_id, name, room, phone, "student", pwd)
            if success:
                messagebox.showinfo("Success", "Member profile updated successfully!", parent=self.dialog)
                self.dialog.destroy()
                self.populate_table(self.manager.get_all_students())
            else:
                messagebox.showerror("Error", "Could not find member profile to update.", parent=self.dialog)
                
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e), parent=self.dialog)

    def handle_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to delete.")
            return
            
        member_id = selected[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete member {member_id}?\nAll meal records, payments, and suggestions for this member will be deleted."):
            success = self.manager.delete_student(member_id)
            if success:
                messagebox.showinfo("Success", "Member records deleted successfully!")
                self.populate_table(self.manager.get_all_students())
            else:
                messagebox.showerror("Error", "Could not delete member records.")
