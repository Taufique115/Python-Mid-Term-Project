import tkinter as tk
from tkinter import ttk

# Global Theme Colors (Claymorphism 3D Theme)
COLOR_BG = "#EEF2F6"       # Soft clay body background
COLOR_CARD = "#F8FAFC"     # Soft plush white card
COLOR_TEXT_MAIN = "#1E293B" # Dark Slate for headings
COLOR_TEXT_MUTED = "#64748B"# Cool Gray for labels
COLOR_PRIMARY = "#6366F1"   # Clay Indigo theme
COLOR_PRIMARY_HOVER = "#4F46E5"
COLOR_SUCCESS = "#10B981"   # Emerald green
COLOR_SUCCESS_HOVER = "#059669"
COLOR_WARNING = "#F59E0B"   # Warm Amber
COLOR_DANGER = "#EF4444"    # Coral red
COLOR_DANGER_HOVER = "#DC2626"
COLOR_BORDER = "#CBD5E1"    # Soft clay border

# Fonts
FONT_HEADING = ("Segoe UI", 16, "bold")
FONT_SUBHEADING = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_MUTED = ("Segoe UI", 9)
FONT_CARD_VAL = ("Segoe UI", 20, "bold")

class StyledButton(tk.Button):
    """
    A custom styled button with flat borders, hand cursor, and hover effects.
    """
    def __init__(self, parent, text, command=None, bg_color=COLOR_PRIMARY, fg_color="#FFFFFF", hover_bg=COLOR_PRIMARY_HOVER, width=15, **kwargs):
        self.hover_bg = hover_bg
        self.normal_bg = bg_color
        
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=self.normal_bg,
            fg=fg_color,
            activebackground=hover_bg,
            activeforeground=fg_color,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=15,
            pady=8,
            width=width,
            **kwargs
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event):
        self.config(bg=self.hover_bg)
        
    def _on_leave(self, event):
        self.config(bg=self.normal_bg)


class Card(tk.Frame):
    """
    A modern container representing a card with white background and subtle borders.
    """
    def __init__(self, parent, title="", value="", subtitle="", icon=None, highlight_color=None, **kwargs):
        super().__init__(
            parent,
            bg=COLOR_CARD,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            bd=0,
            padx=15,
            pady=15,
            **kwargs
        )
        
        # Grid layout
        self.columnconfigure(0, weight=1)
        
        if highlight_color:
            bar = tk.Frame(self, bg=highlight_color, height=4)
            bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            
        row_offset = 1 if highlight_color else 0
        
        if title:
            self.title_lbl = tk.Label(
                self,
                text=title.upper(),
                font=("Segoe UI", 9, "bold"),
                fg=COLOR_TEXT_MUTED,
                bg=COLOR_CARD,
                anchor="w"
            )
            self.title_lbl.grid(row=row_offset, column=0, sticky="w")
            
        if value:
            val_font = FONT_CARD_VAL if len(value) <= 10 and "\n" not in value else ("Segoe UI", 12, "bold")
            self.value_lbl = tk.Label(
                self,
                text=value,
                font=val_font,
                fg=COLOR_TEXT_MAIN,
                bg=COLOR_CARD,
                anchor="w",
                justify="left"
            )
            self.value_lbl.grid(row=row_offset + 1, column=0, sticky="w", pady=(4, 0))

        if subtitle:
            self.sub_lbl = tk.Label(
                self,
                text=subtitle,
                font=("Segoe UI", 9),
                fg=COLOR_TEXT_MUTED,
                bg=COLOR_CARD,
                anchor="w",
                justify="left"
            )
            self.sub_lbl.grid(row=row_offset + 2, column=0, sticky="w", pady=(4, 0))


class LabeledEntry(tk.Frame):
    """
    A field container packing a title label and a styled entry field.
    """
    def __init__(self, parent, label_text, is_password=False, **kwargs):
        super().__init__(parent, bg=COLOR_CARD, **kwargs)
        
        self.label = tk.Label(
            self,
            text=label_text,
            font=FONT_BODY,
            fg=COLOR_TEXT_MAIN,
            bg=COLOR_CARD,
            anchor="w"
        )
        self.label.pack(fill="x", anchor="w", pady=(0, 5))
        
        show_char = "*" if is_password else ""
        self.entry = tk.Entry(
            self,
            font=FONT_BODY,
            fg=COLOR_TEXT_MAIN,
            bg="#F8FAFC",
            relief="solid",
            highlightthickness=0,
            bd=1,
            show=show_char
        )
        # Add basic borders using system properties
        self.entry.config(highlightbackground=COLOR_BORDER, highlightcolor=COLOR_PRIMARY)
        self.entry.pack(fill="x", ipady=6, ipadx=4)
        
    def get(self):
        return self.entry.get().strip()
        
    def set(self, val):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(val))
        
    def clear(self):
        self.entry.delete(0, tk.END)


def configure_treeview_style():
    """
    Configure ttk Treeview to have a modern look matching the app style.
    """
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure(
        "Treeview",
        background=COLOR_CARD,
        foreground=COLOR_TEXT_MAIN,
        fieldbackground=COLOR_CARD,
        font=FONT_BODY,
        rowheight=34
    )
    style.map(
        "Treeview",
        background=[("selected", COLOR_PRIMARY)],
        foreground=[("selected", "#FFFFFF")]
    )
    style.configure(
        "Treeview.Heading",
        background="#EEF2FF",
        foreground=COLOR_PRIMARY,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        borderwidth=0
    )
    style.map(
        "Treeview.Heading",
        background=[("active", "#E0E7FF")]
    )


def create_scrollable_tree(parent, columns, headings, column_widths=None):
    """
    Helper function to create a styled Treeview with vertical scrollbar.
    """
    configure_treeview_style()
    
    frame = tk.Frame(parent, bg=COLOR_CARD)
    
    tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
    
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    
    # Configure Columns
    for idx, col in enumerate(columns):
        tree.heading(col, text=headings[idx])
        if column_widths and col in column_widths:
            tree.column(col, width=column_widths[col], anchor="center")
        else:
            tree.column(col, anchor="w")
            
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    
    # Enable alternating row colors
    tree.tag_configure("even", background="#F8FAFC")
    tree.tag_configure("odd", background="#FFFFFF")
    
    return frame, tree
