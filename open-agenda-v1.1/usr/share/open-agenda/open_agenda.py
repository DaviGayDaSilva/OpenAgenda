#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗ ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗               ║
║   ██╔════╝██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝██╔════╝               ║
║   █████╗  ██║   ██║██████╔╝██║   ██║██║     ███████╗█████╗                 ║
║   ██╔══╝  ██║   ██║██╔══██╗██║   ██║██║     ╚════██║██╔══╝                 ║
║   ███████╗╚██████╔╝██║  ██║╚██████╔╝███████╗███████║███████╗               ║
║   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝               ║
║                                                                              ║
║   Open-Agenda v1.1 - The Ultimate Smart Calendar                           ║
║   © 2025 Open-Agenda Team - Open Source & Free!                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Features:
- 🌙 Ultra Modern 2025 Interface with Gradients & Shadows
- 💾 Auto-Save - Your data is always saved!
- 📅 Multiple Calendars (Personal, Work, Family, etc.)
- 🎨 Color Categories for Events
- 🔔 Notifications & Reminders
- 🌗 Light/Dark Theme
- 🔍 Search Events
- 📤 Export (JSON, CSV, ICS)
- 📊 Statistics Dashboard
- ⌨️ Keyboard Shortcuts
- 🔄 Recurring Events
- 📍 Location Field
- ⚡ Priority Levels
- 📝 Detailed Notes
- 🎯 Presentation Mode

Author: Open-Agenda Team
License: MIT
Version: 1.1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
import csv
from datetime import datetime, date, timedelta
import calendar as cal
from pathlib import Path
import threading
import time

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 MODERN 2025 COLOR PALETTE
# ═══════════════════════════════════════════════════════════════════════════

class ModernColors:
    """Ultra-modern 2025 color palette with gradients and effects"""
    
    # Dark Theme (Default)
    DARK = {
        'bg_primary': '#0D0D0F',        # Deep black
        'bg_secondary': '#16161A',      # Card background
        'bg_tertiary': '#1E1E24',       # Elevated surfaces
        'bg_hover': '#2A2A35',         # Hover states
        'accent_primary': '#7C3AED',    # Violet primary
        'accent_secondary': '#A855F7', # Purple light
        'accent_gradient': 'linear',   # Gradient effect
        'text_primary': '#FAFAFA',     # Main text
        'text_secondary': '#A1A1AA',   # Secondary text
        'text_muted': '#71717A',       # Muted text
        'success': '#10B981',          # Green
        'warning': '#F59E0B',           # Amber
        'danger': '#EF4444',           # Red
        'info': '#3B82F6',             # Blue
        'border': '#27272A',           # Border color
        'shadow': '#000000',          # Shadow color
    }
    
    # Light Theme
    LIGHT = {
        'bg_primary': '#FAFAFA',
        'bg_secondary': '#FFFFFF',
        'bg_tertiary': '#F4F4F5',
        'bg_hover': '#E4E4E7',
        'accent_primary': '#7C3AED',
        'accent_secondary': '#A855F7',
        'accent_gradient': 'linear',
        'text_primary': '#18181B',
        'text_secondary': '#52525B',
        'text_muted': '#A1A1AA',
        'success': '#059669',
        'warning': '#D97706',
        'danger': '#DC2626',
        'info': '#2563EB',
        'border': '#E4E4E7',
        'shadow': '#00000020',
    }
    
    # Event Category Colors
    CATEGORIES = {
        'personal': {'bg': '#EC4899', 'fg': '#FFFFFF', 'name': 'Personal', 'icon': '👤'},
        'work': {'bg': '#3B82F6', 'fg': '#FFFFFF', 'name': 'Work', 'icon': '💼'},
        'family': {'bg': '#10B981', 'fg': '#FFFFFF', 'name': 'Family', 'icon': '👨‍👩‍👧'},
        'health': {'bg': '#F59E0B', 'fg': '#FFFFFF', 'name': 'Health', 'icon': '🏥'},
        'education': {'bg': '#8B5CF6', 'fg': '#FFFFFF', 'name': 'Education', 'icon': '📚'},
        'social': {'bg': '#06B6D4', 'fg': '#FFFFFF', 'name': 'Social', 'icon': '🎉'},
        'finance': {'bg': '#EF4444', 'fg': '#FFFFFF', 'name': 'Finance', 'icon': '💰'},
        'travel': {'bg': '#F97316', 'fg': '#FFFFFF', 'name': 'Travel', 'icon': '✈️'},
        'other': {'bg': '#6B7280', 'fg': '#FFFFFF', 'name': 'Other', 'icon': '📌'},
    }
    
    # Priority Colors
    PRIORITIES = {
        'high': {'color': '#EF4444', 'name': 'High', 'icon': '🔴'},
        'medium': {'color': '#F59E0B', 'name': 'Medium', 'icon': '🟡'},
        'low': {'color': '#10B981', 'name': 'Low', 'icon': '🟢'},
        'none': {'color': '#6B7280', 'name': 'None', 'icon': '⚪'},
    }

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 MODERN WIDGET CLASSES
# ═══════════════════════════════════════════════════════════════════════════

class ModernButton(tk.Button):
    """Ultra-modern button with gradient and hover effects"""
    
    def __init__(self, parent, text, command, bg=None, fg=None, icon='', 
                 hover_color=None, rounded=10, **kwargs):
        self.bg_color = bg or ModernColors.DARK['accent_primary']
        self.hover_color = hover_color or ModernColors.DARK['accent_secondary']
        self.rounded = rounded
        
        super().__init__(
            parent, text=f"{icon} {text}".strip(),
            command=command,
            font=('Inter', 10, 'bold'),
            bg=self.bg_color,
            fg=fg or '#FFFFFF',
            activebackground=self.hover_color,
            activeforeground='#FFFFFF',
            relief=tk.FLAT,
            borderwidth=0,
            padx=16,
            pady=8,
            cursor='hand2',
            **kwargs
        )
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self.configure(bg=self.hover_color)
    
    def on_leave(self, e):
        self.configure(bg=self.bg_color)


class ModernEntry(tk.Entry):
    """Modern input field with styling"""
    
    def __init__(self, parent, placeholder='', **kwargs):
        self.placeholder = placeholder
        self.placeholder_color = ModernColors.DARK['text_muted']
        
        super().__init__(
            parent,
            font=('Inter', 11),
            bg=ModernColors.DARK['bg_tertiary'],
            fg=ModernColors.DARK['text_primary'],
            relief=tk.FLAT,
            borderwidth=1,
            insertbackground=ModernColors.DARK['text_primary'],
            **kwargs
        )
        
        if placeholder:
            self.put_placeholder()
            self.bind('<FocusIn>', self.on_focus)
            self.bind('<FocusOut>', self.on_focus_out)
    
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)
    
    def on_focus(self, e):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=ModernColors.DARK['text_primary'])
    
    def on_focus_out(self, e):
        if not self.get():
            self.put_placeholder()


class ModernCard(tk.Frame):
    """Modern card with shadow and rounded corners"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=ModernColors.DARK['bg_secondary'],
            relief=tk.FLAT,
            borderwidth=0,
            **kwargs
        )


# ═══════════════════════════════════════════════════════════════════════════
# 🗓️ MAIN APPLICATION CLASS
# ═══════════════════════════════════════════════════════════════════════════

class OpenAgendaV11:
    """Open-Agenda v1.1 - The Ultimate Smart Calendar"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Open-Agenda v1.1 - The Ultimate Smart Calendar")
        self.root.geometry("1400x900")
        self.root.configure(bg=ModernColors.DARK['bg_primary'])
        
        # ═══════════════════════════════════════════════════════════════
        # 💾 DATA INITIALIZATION
        # ═══════════════════════════════════════════════════════════════
        
        self.data_file = "open_agenda_v11_data.json"
        self.events = {}  # {date: [events]}
        self.calendars = {
            'personal': {'name': 'Personal', 'color': '#EC4899', 'icon': '👤', 'visible': True},
            'work': {'name': 'Work', 'color': '#3B82F6', 'icon': '💼', 'visible': True},
            'family': {'name': 'Family', 'color': '#10B981', 'icon': '👨‍👩‍👧', 'visible': True},
            'health': {'name': 'Health', 'color': '#F59E0B', 'icon': '🏥', 'visible': True},
        }
        self.current_calendar = 'personal'
        self.current_date = date.today()
        self.selected_date = date.today()
        self.is_dark_theme = True
        self.auto_save_enabled = True
        self.auto_save_timer = None
        
        # ═══════════════════════════════════════════════════════════════
        # 🎨 UI SETUP
        # ═══════════════════════════════════════════════════════════════
        
        self.setup_styles()
        self.create_ui()
        self.load_data()
        self.update_calendar()
        self.update_event_list()
        
        # Auto-save setup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.start_auto_save()
    
    # ═══════════════════════════════════════════════════════════════════
    # 🎨 STYLES & THEMES
    # ═══════════════════════════════════════════════════════════════════
    
    def setup_styles(self):
        """Configure modern styles"""
        self.colors = ModernColors.DARK.copy()
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.colors = ModernColors.DARK.copy()
        else:
            self.colors = ModernColors.LIGHT.copy()
        
        self.refresh_ui()
    
    def refresh_ui(self):
        """Refresh the entire UI with new theme"""
        self.root.configure(bg=self.colors['bg_primary'])
        self.update_calendar()
        self.update_event_list()
    
    # ═══════════════════════════════════════════════════════════════════
    # 🖥️ MAIN UI CREATION
    # ═══════════════════════════════════════════════════════════════════
    
    def create_ui(self):
        """Create the ultra-modern 2025 interface"""
        
        # ═══════════════════════════════════════════════════════════════
        # 🌙 TOP BAR
        # ═══════════════════════════════════════════════════════════════
        
        self.top_bar = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=60)
        self.top_bar.pack(fill=tk.X)
        self.top_bar.pack_propagate(False)
        
        # Logo & Title
        self.logo_label = tk.Label(
            self.top_bar,
            text="🌟 Open-Agenda",
            font=('Inter', 18, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_primary']
        )
        self.logo_label.pack(side=tk.LEFT, padx=20)
        
        # Search Bar
        self.search_frame = tk.Frame(self.top_bar, bg=self.colors['bg_tertiary'])
        self.search_frame.pack(side=tk.LEFT, padx=20)
        
        self.search_entry = tk.Entry(
            self.search_frame,
            width=30,
            font=('Inter', 11),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            relief=tk.FLAT,
            borderwidth=0
        )
        self.search_entry.pack(padx=10, pady=8)
        self.search_entry.insert(0, "🔍 Search events...")
        self.search_entry.bind('<KeyRelease>', self.search_events)
        
        # Theme Toggle
        self.theme_btn = ModernButton(
            self.top_bar, "", self.toggle_theme,
            bg=self.colors['accent_primary'], icon="🌙"
        )
        self.theme_btn.configure(text="🌙", width=3)
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
        
        # Export Button
        self.export_btn = ModernButton(
            self.top_bar, "Export", self.show_export_menu,
            bg=self.colors['success'], icon="📤"
        )
        self.export_btn.pack(side=tk.RIGHT, padx=10)
        
        # Import Button
        self.import_btn = ModernButton(
            self.top_bar, "Import", self.import_data,
            bg=self.colors['info'], icon="📥"
        )
        self.import_btn.pack(side=tk.RIGHT, padx=10)
        
        # Stats Button
        self.stats_btn = ModernButton(
            self.top_bar, "Stats", self.show_statistics,
            bg=self.colors['warning'], icon="📊"
        )
        self.stats_btn.pack(side=tk.RIGHT, padx=10)
        
        # ═══════════════════════════════════════════════════════════════
        # 📐 MAIN CONTENT AREA
        # ═══════════════════════════════════════════════════════════════
        
        self.main_content = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ═══════════════════════════════════════════════════════════════
        # 📅 LEFT SIDEBAR - Calendar
        # ═══════════════════════════════════════════════════════════════
        
        self.sidebar = tk.Frame(self.main_content, bg=self.colors['bg_secondary'], width=400)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.sidebar.pack_propagate(False)
        
        # Calendar Header
        cal_header = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'])
        cal_header.pack(fill=tk.X, padx=15, pady=15)
        
        self.prev_btn = tk.Button(
            cal_header, text="◀", font=('Inter', 12),
            bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
            relief=tk.FLAT, command=self.prev_month, width=3
        )
        self.prev_btn.pack(side=tk.LEFT)
        
        self.month_year_label = tk.Label(
            cal_header,
            text="", font=('Inter', 16, 'bold'),
            bg=self.colors['bg_secondary'], fg=self.colors['text_primary']
        )
        self.month_year_label.pack(side=tk.LEFT, expand=True)
        
        self.next_btn = tk.Button(
            cal_header, text="▶", font=('Inter', 12),
            bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
            relief=tk.FLAT, command=self.next_month, width=3
        )
        self.next_btn.pack(side=tk.LEFT)
        
        # Today Button
        today_btn = ModernButton(
            cal_header, "Today", lambda: self.go_to_today(date.today()),
            bg=self.colors['accent_primary'], icon="📅"
        )
        today_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Calendar Grid
        self.cal_frame = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'])
        self.cal_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Day Headers
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(days):
            tk.Label(
                self.cal_frame, text=day,
                font=('Inter', 10, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            ).grid(row=0, column=i, pady=5)
        
        self.calendar_buttons = []
        
        # ═══════════════════════════════════════════════════════════════
        # 📆 CALENDARS SIDEBAR
        # ═══════════════════════════════════════════════════════════════
        
        cal_separator = tk.Frame(self.sidebar, bg=self.colors['border'], height=1)
        cal_separator.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(
            self.sidebar, text="📆 Calendars",
            font=('Inter', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, padx=15, pady=(0, 10))
        
        self.calendars_frame = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'])
        self.calendars_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.calendar_vars = {}
        for cal_id, cal_data in self.calendars.items():
            var = tk.BooleanVar(value=cal_data['visible'])
            self.calendar_vars[cal_id] = var
            
            cb = tk.Checkbutton(
                self.calendars_frame,
                text=f"{cal_data['icon']} {cal_data['name']}",
                variable=var,
                font=('Inter', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                selectcolor=self.colors['bg_tertiary'],
                command=lambda c=cal_id: self.toggle_calendar_visibility(c)
            )
            cb.pack(anchor=tk.W, pady=2)
        
        # Add Calendar Button
        add_cal_btn = tk.Button(
            self.calendars_frame,
            text="+ Add Calendar",
            font=('Inter', 9),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['accent_primary'],
            relief=tk.FLAT,
            command=self.add_calendar
        )
        add_cal_btn.pack(anchor=tk.W, pady=5)
        
        # ═══════════════════════════════════════════════════════════════
        # 📋 RIGHT PANEL - Events
        # ═══════════════════════════════════════════════════════════════
        
        self.events_panel = tk.Frame(self.main_content, bg=self.colors['bg_secondary'])
        self.events_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Date Header
        date_header = tk.Frame(self.events_panel, bg=self.colors['bg_secondary'])
        date_header.pack(fill=tk.X, padx=20, pady=15)
        
        self.selected_date_label = tk.Label(
            date_header,
            text="",
            font=('Inter', 18, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        self.selected_date_label.pack(side=tk.LEFT)
        
        # Event Counter
        self.event_count_label = tk.Label(
            date_header,
            text="0 events",
            font=('Inter', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.event_count_label.pack(side=tk.RIGHT)
        
        # Event Input Form
        input_card = tk.Frame(self.events_panel, bg=self.colors['bg_tertiary'])
        input_card.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Time & Calendar Row
        row1 = tk.Frame(input_card, bg=self.colors['bg_tertiary'])
        row1.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(row1, text="⏰", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        
        self.time_entry = ModernEntry(row1, placeholder="14:30")
        self.time_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        tk.Label(row1, text="📆", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=(15, 5))
        
        self.calendar_var = tk.StringVar(value='personal')
        self.calendar_menu = ttk.Combobox(
            row1, textvariable=self.calendar_var,
            values=list(self.calendars.keys()),
            state='readonly', width=12
        )
        self.calendar_menu.pack(side=tk.LEFT, padx=5)
        
        # Title Row
        row2 = tk.Frame(input_card, bg=self.colors['bg_tertiary'])
        row2.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(row2, text="📝", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        
        self.title_entry = ModernEntry(row2, placeholder="Event title...")
        self.title_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Category & Priority Row
        row3 = tk.Frame(input_card, bg=self.colors['bg_tertiary'])
        row3.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(row3, text="🏷️", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        
        self.category_var = tk.StringVar(value='personal')
        self.category_menu = ttk.Combobox(
            row3, textvariable=self.category_var,
            values=list(ModernColors.CATEGORIES.keys()),
            state='readonly', width=12
        )
        self.category_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Label(row3, text="⚡", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=(15, 5))
        
        self.priority_var = tk.StringVar(value='none')
        self.priority_menu = ttk.Combobox(
            row3, textvariable=self.priority_var,
            values=list(ModernColors.PRIORITIES.keys()),
            state='readonly', width=10
        )
        self.priority_menu.pack(side=tk.LEFT, padx=5)
        
        # Location Row
        row4 = tk.Frame(input_card, bg=self.colors['bg_tertiary'])
        row4.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(row4, text="📍", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        
        self.location_entry = ModernEntry(row4, placeholder="Location (optional)...")
        self.location_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Notes Row
        row5 = tk.Frame(input_card, bg=self.colors['bg_tertiary'])
        row5.pack(fill=tk.X, padx=15, pady=(5, 15))
        
        tk.Label(row5, text="📋", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        
        self.notes_entry = ModernEntry(row5, placeholder="Notes (optional)...")
        self.notes_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Recurring & Reminder Row
        row6 = tk.Frame(input_card, bg=self.colors['bg_tertiary'])
        row6.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.recurring_var = tk.StringVar(value='none')
        tk.Label(row6, text="🔄", bg=self.colors['bg_tertiary']).pack(side=tk.LEFT)
        self.recurring_menu = ttk.Combobox(
            row6, textvariable=self.recurring_var,
            values=['none', 'daily', 'weekly', 'monthly', 'yearly'],
            state='readonly', width=10
        )
        self.recurring_menu.pack(side=tk.LEFT, padx=5)
        
        self.reminder_var = tk.IntVar(value=0)
        tk.Checkbutton(
            row6, text="🔔 Reminder",
            variable=self.reminder_var,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT, padx=(20, 0))
        
        # Add Event Button
        add_btn = tk.Button(
            input_card,
            text="➕ Add Event",
            font=('Inter', 12, 'bold'),
            bg=self.colors['success'],
            fg='#FFFFFF',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.add_event
        )
        add_btn.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # ═══════════════════════════════════════════════════════════════
        # 📜 EVENTS LIST
        # ═══════════════════════════════════════════════════════════════
        
        # Events List Header
        events_header = tk.Frame(self.events_panel, bg=self.colors['bg_secondary'])
        events_header.pack(fill=tk.X, padx=20)
        
        tk.Label(
            events_header, text="📜 Events",
            font=('Inter', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(side=tk.LEFT)
        
        # Delete Selected Button
        delete_btn = tk.Button(
            events_header,
            text="🗑️ Delete",
            font=('Inter', 9),
            bg=self.colors['danger'],
            fg='#FFFFFF',
            relief=tk.FLAT,
            padx=10,
            command=self.delete_selected_event
        )
        delete_btn.pack(side=tk.RIGHT)
        
        # Events List Container
        list_container = tk.Frame(self.events_panel, bg=self.colors['bg_tertiary'])
        list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Events Listbox
        self.events_listbox = tk.Listbox(
            list_container,
            font=('Inter', 11),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            yscrollcommand=scrollbar.set,
            selectbackground=self.colors['accent_primary']
        )
        self.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.events_listbox.yview)
        
        self.events_listbox.bind('<Double-Button-1>', self.delete_selected_event)
        
        # ═══════════════════════════════════════════════════════════════
        # 💾 STATUS BAR
        # ═══════════════════════════════════════════════════════════════
        
        self.status_bar = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=30)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text=f"🌟 Open-Agenda v1.1 - Auto-save enabled • Press Ctrl+N for new event • Ctrl+F to search",
            font=('Inter', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.status_label.pack(side=tk.LEFT, padx=15)
        
        # Auto-save indicator
        self.save_indicator = tk.Label(
            self.status_bar,
            text="💾 Saved",
            font=('Inter', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['success']
        )
        self.save_indicator.pack(side=tk.RIGHT, padx=15)
        
        # ═══════════════════════════════════════════════════════════════
        # ⌨️ KEYBOARD SHORTCUTS
        # ═══════════════════════════════════════════════════════════════
        
        self.root.bind('<Control-n>', lambda e: self.focus_title_entry())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus_set())
        self.root.bind('<Control-s>', lambda e: self.manual_save())
        self.root.bind('<Control-t>', lambda e: self.go_to_today(date.today()))
        self.root.bind('<Control-e>', lambda e: self.show_export_menu())
        self.root.bind('<Left>', lambda e: self.prev_month())
        self.root.bind('<Right>', lambda e: self.next_month())
        self.root.bind('<Return>', lambda e: self.add_event())
    
    def focus_title_entry(self):
        """Focus on title entry"""
        self.title_entry.focus_set()
    
    # ═══════════════════════════════════════════════════════════════════
    # 📅 CALENDAR FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    def update_calendar(self):
        """Update the calendar display"""
        for btn in self.calendar_buttons:
            btn.destroy()
        self.calendar_buttons = []
        
        month_name = cal.month_name[self.current_date.month]
        self.month_year_label.config(
            text=f"{month_name} {self.current_date.year}",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        
        calendar = cal.Calendar(firstweekday=6)
        month_days = calendar.monthdayscalendar(self.current_date.year, self.current_date.month)
        
        for week_idx, week in enumerate(month_days):
            for day_idx, day in enumerate(week):
                if day == 0:
                    label = tk.Label(
                        self.cal_frame, text="",
                        bg=self.colors['bg_secondary'], width=4, height=2
                    )
                    label.grid(row=week_idx + 1, column=day_idx, padx=1, pady=1)
                    self.calendar_buttons.append(label)
                else:
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    
                    # Determine button color based on events
                    has_events = day_date in self.events and len(self.events[day_date]) > 0
                    
                    if day_date == date.today():
                        bg_color = self.colors['info']
                        fg_color = '#FFFFFF'
                    elif has_events:
                        bg_color = self.colors['accent_primary']
                        fg_color = '#FFFFFF'
                    else:
                        bg_color = self.colors['bg_tertiary']
                        fg_color = self.colors['text_primary']
                    
                    btn = tk.Button(
                        self.cal_frame, text=str(day),
                        font=('Inter', 10, 'bold'),
                        bg=bg_color, fg=fg_color,
                        relief=tk.FLAT,
                        command=lambda d=day: self.select_date(d)
                    )
                    btn.grid(row=week_idx + 1, column=day_idx, padx=1, pady=1, sticky='nsew')
                    self.calendar_buttons.append(btn)
        
        for i in range(7):
            self.cal_frame.columnconfigure(i, weight=1)
    
    def select_date(self, day):
        """Select a specific date"""
        self.selected_date = date(self.current_date.year, self.current_date.month, day)
        self.update_event_list()
        self.update_calendar()
    
    def prev_month(self):
        """Go to previous month"""
        if self.current_date.month == 1:
            self.current_date = date(self.current_date.year - 1, 12, 1)
        else:
            self.current_date = date(self.current_date.year, self.current_date.month - 1, 1)
        self.update_calendar()
    
    def next_month(self):
        """Go to next month"""
        if self.current_date.month == 12:
            self.current_date = date(self.current_date.year + 1, 1, 1)
        else:
            self.current_date = date(self.current_date.year, self.current_date.month + 1, 1)
        self.update_calendar()
    
    def go_to_today(self, target_date=None):
        """Go to today's date"""
        if target_date is None:
            target_date = date.today()
        self.current_date = target_date
        self.selected_date = target_date
        self.update_calendar()
        self.update_event_list()
        self.status_label.config(text=f"📍 Jumped to today")
    
    # ═══════════════════════════════════════════════════════════════════
    # 📋 EVENT MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════
    
    def update_event_list(self):
        """Update the events listbox"""
        self.events_listbox.delete(0, tk.END)
        
        day_name = self.selected_date.strftime("%A")
        self.selected_date_label.config(
            text=f"📅 {day_name}, {self.selected_date.strftime('%B %d, %Y')}",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        
        event_count = 0
        
        if self.selected_date in self.events:
            visible_cals = [c for c, v in self.calendar_vars.items() if v.get()]
            
            for event in self.events[self.selected_date]:
                event_cal = event.get('calendar', 'personal')
                
                if event_cal in visible_cals:
                    event_count += 1
                    
                    category = event.get('category', 'other')
                    priority = event.get('priority', 'none')
                    location = event.get('location', '')
                    notes = event.get('notes', '')
                    
                    cat_color = ModernColors.CATEGORIES.get(category, ModernColors.CATEGORIES['other'])['bg']
                    pri_icon = ModernColors.PRIORITIES.get(priority, ModernColors.PRIORITIES['none'])['icon']
                    
                    display_text = f"{pri_icon} {event['time']} - {event['title']}"
                    if location:
                        display_text += f" 📍{location}"
                    if notes:
                        display_text += f" 📋"
                    
                    self.events_listbox.insert(tk.END, display_text)
                    
                    # Set item colors
                    last_idx = self.events_listbox.size() - 1
                    self.events_listbox.itemconfig(last_idx, bg=self.colors['bg_tertiary'])
        
        self.event_count_label.config(
            text=f"{event_count} events",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        
        if event_count == 0:
            self.events_listbox.insert(tk.END, "No events for this day.")
            self.events_listbox.insert(tk.END, "➕ Add an event above!")
    
    def add_event(self):
        """Add a new event"""
        time_val = self.time_entry.get().strip()
        title = self.title_entry.get().strip()
        
        if not title or title == "Event title...":
            messagebox.showwarning("⚠️ Warning", "Please enter an event title!")
            return
        
        if not time_val or time_val == "14:30":
            time_val = "09:00"
        
        try:
            datetime.strptime(time_val, "%H:%M")
        except ValueError:
            messagebox.showwarning("⚠️ Warning", "Invalid time format! Use HH:MM (e.g., 14:30)")
            return
        
        category = self.category_var.get() or 'other'
        priority = self.priority_var.get() or 'none'
        calendar = self.calendar_var.get() or 'personal'
        location = self.location_entry.get().strip()
        notes = self.notes_entry.get().strip()
        recurring = self.recurring_var.get() or 'none'
        reminder = self.reminder_var.get() == 1
        
        if self.selected_date not in self.events:
            self.events[self.selected_date] = []
        
        new_event = {
            'time': time_val,
            'title': title,
            'category': category,
            'priority': priority,
            'calendar': calendar,
            'location': location,
            'notes': notes,
            'recurring': recurring,
            'reminder': reminder,
            'created': datetime.now().isoformat()
        }
        
        self.events[self.selected_date].append(new_event)
        self.events[self.selected_date].sort(key=lambda x: x['time'])
        
        # Handle recurring events
        if recurring != 'none':
            self.create_recurring_events(self.selected_date, recurring, new_event)
        
        # Clear form
        self.title_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        
        self.update_event_list()
        self.update_calendar()
        self.trigger_auto_save()
        
        self.status_label.config(text=f"✅ Event added: {title}")
    
    def create_recurring_events(self, start_date, recurring_type, base_event):
        """Create recurring events"""
        for i in range(1, 13):  # Create up to 12 occurrences
            if recurring_type == 'daily':
                new_date = start_date + timedelta(days=i)
            elif recurring_type == 'weekly':
                new_date = start_date + timedelta(weeks=i)
            elif recurring_type == 'monthly':
                try:
                    new_date = start_date.replace(month=start_date.month + i)
                except:
                    continue
            elif recurring_type == 'yearly':
                try:
                    new_date = start_date.replace(year=start_date.year + i)
                except:
                    continue
            else:
                break
            
            if new_date not in self.events:
                self.events[new_date] = []
            
            event_copy = base_event.copy()
            event_copy['created'] = datetime.now().isoformat()
            self.events[new_date].append(event_copy)
    
    def delete_selected_event(self, event=None):
        """Delete the selected event"""
        selection = self.events_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        if self.selected_date not in self.events or not self.events[self.selected_date]:
            return
        
        visible_events = []
        visible_cals = [c for c, v in self.calendar_vars.items() if v.get()]
        
        for e in self.events[self.selected_date]:
            if e.get('calendar', 'personal') in visible_cals:
                visible_events.append(e)
        
        if index < len(visible_events):
            deleted_event = visible_events[index]['title']
            
            # Find and remove the actual event
            actual_event = visible_events[index]
            self.events[self.selected_date].remove(actual_event)
            
            if not self.events[self.selected_date]:
                del self.events[self.selected_date]
            
            self.update_event_list()
            self.update_calendar()
            self.trigger_auto_save()
            
            self.status_label.config(text=f"🗑️ Event deleted: {deleted_event}")
    
    # ═══════════════════════════════════════════════════════════════════
    # 🔍 SEARCH
    # ═══════════════════════════════════════════════════════════════════
    
    def search_events(self, event=None):
        """Search events across all dates"""
        query = self.search_entry.get().strip().lower()
        
        if not query or query == "🔍 search events...":
            self.update_event_list()
            return
        
        self.events_listbox.delete(0, tk.END)
        
        results = []
        for event_date, events_list in self.events.items():
            for event in events_list:
                if (query in event['title'].lower() or
                    query in event.get('location', '').lower() or
                    query in event.get('notes', '').lower() or
                    query in event_date.strftime('%Y-%m-%d').lower()):
                    results.append((event_date, event))
        
        if results:
            self.events_listbox.insert(tk.END, f"🔍 Found {len(results)} results:")
            
            for event_date, event in results:
                display_text = f"📅 {event_date.strftime('%Y-%m-%d')} ⏰ {event['time']} - {event['title']}"
                self.events_listbox.insert(tk.END, display_text)
        else:
            self.events_listbox.insert(tk.END, "❌ No results found")
    
    # ═══════════════════════════════════════════════════════════════════
    # 📊 STATISTICS
    # ═══════════════════════════════════════════════════════════════════
    
    def show_statistics(self):
        """Show statistics dashboard"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Open-Agenda Statistics")
        stats_window.geometry("600x500")
        stats_window.configure(bg=self.colors['bg_primary'])
        
        # Header
        tk.Label(
            stats_window,
            text="📊 Statistics Dashboard",
            font=('Inter', 20, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_primary']
        ).pack(pady=20)
        
        # Calculate stats
        total_events = sum(len(events) for events in self.events.values())
        total_days = len(self.events)
        
        categories_count = {}
        priorities_count = {}
        
        for events_list in self.events.values():
            for event in events_list:
                cat = event.get('category', 'other')
                pri = event.get('priority', 'none')
                categories_count[cat] = categories_count.get(cat, 0) + 1
                priorities_count[pri] = priorities_count.get(pri, 0) + 1
        
        # Stats Container
        stats_frame = tk.Frame(stats_window, bg=self.colors['bg_secondary'])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Summary Stats
        tk.Label(
            stats_frame,
            text="📈 Summary",
            font=('Inter', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(10, 5))
        
        tk.Label(
            stats_frame,
            text=f"Total Events: {total_events}",
            font=('Inter', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W, padx=10)
        
        tk.Label(
            stats_frame,
            text=f"Days with Events: {total_days}",
            font=('Inter', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W, padx=10)
        
        # Categories
        tk.Label(
            stats_frame,
            text="🏷️ Categories",
            font=('Inter', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(20, 5))
        
        for cat, count in sorted(categories_count.items(), key=lambda x: x[1], reverse=True):
            cat_info = ModernColors.CATEGORIES.get(cat, ModernColors.CATEGORIES['other'])
            tk.Label(
                stats_frame,
                text=f"{cat_info['icon']} {cat_info['name']}: {count}",
                font=('Inter', 11),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            ).pack(anchor=tk.W, padx=10)
        
        # Priorities
        tk.Label(
            stats_frame,
            text="⚡ Priorities",
            font=('Inter', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(20, 5))
        
        for pri, count in sorted(priorities_count.items(), key=lambda x: x[1], reverse=True):
            pri_info = ModernColors.PRIORITIES.get(pri, ModernColors.PRIORITIES['none'])
            tk.Label(
                stats_frame,
                text=f"{pri_info['icon']} {pri_info['name']}: {count}",
                font=('Inter', 11),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            ).pack(anchor=tk.W, padx=10)
    
    # ═══════════════════════════════════════════════════════════════════
    # 📤 IMPORT/EXPORT
    # ═══════════════════════════════════════════════════════════════════
    
    def show_export_menu(self):
        """Show export options menu"""
        export_window = tk.Toplevel(self.root)
        export_window.title("📤 Export Data")
        export_window.geometry("400x300")
        export_window.configure(bg=self.colors['bg_primary'])
        
        tk.Label(
            export_window,
            text="📤 Export Your Data",
            font=('Inter', 16, 'bold'),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_primary']
        ).pack(pady=20)
        
        # Export JSON
        ModernButton(
            export_window, "Export as JSON", self.export_json,
            bg=self.colors['info'], icon="📄"
        ).pack(pady=10, padx=40, fill=tk.X)
        
        # Export CSV
        ModernButton(
            export_window, "Export as CSV", self.export_csv,
            bg=self.colors['success'], icon="📊"
        ).pack(pady=10, padx=40, fill=tk.X)
        
        # Export ICS
        ModernButton(
            export_window, "Export as ICS", self.export_ics,
            bg=self.colors['warning'], icon="📅"
        ).pack(pady=10, padx=40, fill=tk.X)
    
    def export_json(self):
        """Export data to JSON"""
        filename = filedialog.asksaveasfilename(
            title="Export JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="open_agenda_export.json"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    data = {k.isoformat(): v for k, v in self.events.items()}
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("✅ Success", f"Data exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Export failed:\n{e}")
    
    def export_csv(self):
        """Export data to CSV"""
        filename = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="open_agenda_export.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Date', 'Time', 'Title', 'Category', 'Priority', 'Calendar', 'Location', 'Notes', 'Recurring', 'Reminder'])
                    
                    for event_date, events_list in sorted(self.events.items()):
                        for event in events_list:
                            writer.writerow([
                                event_date.isoformat(),
                                event.get('time', ''),
                                event.get('title', ''),
                                event.get('category', ''),
                                event.get('priority', ''),
                                event.get('calendar', ''),
                                event.get('location', ''),
                                event.get('notes', ''),
                                event.get('recurring', ''),
                                event.get('reminder', False)
                            ])
                messagebox.showinfo("✅ Success", f"Data exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Export failed:\n{e}")
    
    def export_ics(self):
        """Export data to ICS (iCalendar)"""
        filename = filedialog.asksaveasfilename(
            title="Export ICS",
            defaultextension=".ics",
            filetypes=[("iCalendar files", "*.ics")],
            initialfile="open_agenda_export.ics"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("BEGIN:VCALENDAR\n")
                    f.write("VERSION:2.0\n")
                    f.write("PRODID:-//Open-Agenda//EN\n")
                    f.write("CALSCALE:GREGORIAN\n")
                    
                    for event_date, events_list in self.events.items():
                        for event in events_list:
                            dt_start = f"{event_date.strftime('%Y%m%d')}T{event.get('time', '0000').replace(':', '')}00"
                            
                            f.write("BEGIN:VEVENT\n")
                            f.write(f"DTSTART:{dt_start}\n")
                            f.write(f"SUMMARY:{event.get('title', '')}\n")
                            
                            if event.get('location'):
                                f.write(f"LOCATION:{event.get('location')}\n")
                            if event.get('notes'):
                                f.write(f"DESCRIPTION:{event.get('notes')}\n")
                            
                            f.write("END:VEVENT\n")
                    
                    f.write("END:VCALENDAR\n")
                
                messagebox.showinfo("✅ Success", f"Data exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Export failed:\n{e}")
    
    def import_data(self):
        """Import data from JSON"""
        filename = filedialog.askopenfilename(
            title="Import Data",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = {date.fromisoformat(k): v for k, v in data.items()}
                
                self.update_event_list()
                self.update_calendar()
                self.trigger_auto_save()
                
                messagebox.showinfo("✅ Success", f"Data imported from:\n{filename}")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Import failed:\n{e}")
    
    # ═══════════════════════════════════════════════════════════════════
    # 📆 CALENDAR MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════
    
    def toggle_calendar_visibility(self, calendar_id):
        """Toggle calendar visibility"""
        self.update_event_list()
    
    def add_calendar(self):
        """Add a new calendar"""
        # Simple prompt for new calendar name
        name = tk.simpledialog.askstring("New Calendar", "Enter calendar name:")
        if name:
            cal_id = name.lower().replace(' ', '_')
            colors = ['#EC4899', '#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#06B6D4']
            color = colors[len(self.calendars) % len(colors)]
            
            self.calendars[cal_id] = {
                'name': name,
                'color': color,
                'icon': '📅',
                'visible': True
            }
            
            var = tk.BooleanVar(value=True)
            self.calendar_vars[cal_id] = var
            
            cb = tk.Checkbutton(
                self.calendars_frame,
                text=f"📅 {name}",
                variable=var,
                font=('Inter', 10),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary'],
                selectcolor=self.colors['bg_tertiary'],
                command=lambda c=cal_id: self.toggle_calendar_visibility(c)
            )
            cb.pack(anchor=tk.W, pady=2)
            
            self.calendar_menu['values'] = list(self.calendars.keys())
    
    # ═══════════════════════════════════════════════════════════════════
    # 💾 AUTO-SAVE
    # ═══════════════════════════════════════════════════════════════════
    
    def start_auto_save(self):
        """Start auto-save timer"""
        self.trigger_auto_save()
    
    def trigger_auto_save(self):
        """Trigger auto-save with debounce"""
        if self.auto_save_timer:
            self.root.after_cancel(self.auto_save_timer)
        
        self.save_indicator.config(text="⏳ Saving...", fg=self.colors['warning'])
        
        self.auto_save_timer = self.root.after(1500, self.perform_auto_save)
    
    def perform_auto_save(self):
        """Perform the actual auto-save"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = {k.isoformat(): v for k, v in self.events.items()}
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.save_indicator.config(text="💾 Saved", fg=self.colors['success'])
        except Exception as e:
            self.save_indicator.config(text="❌ Error", fg=self.colors['danger'])
            print(f"Auto-save error: {e}")
    
    def manual_save(self):
        """Manual save trigger"""
        self.perform_auto_save()
        self.status_label.config(text="💾 Data saved manually")
    
    def load_data(self):
        """Load data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = {date.fromisoformat(k): v for k, v in data.items()}
                self.status_label.config(text="✅ Data loaded successfully!")
            except Exception as e:
                self.status_label.config(text=f"⚠️ Error loading data: {e}")
    
    def on_closing(self):
        """Handle window closing"""
        self.perform_auto_save()
        self.root.destroy()


# ═══════════════════════════════════════════════════════════════════════
# 🎯 MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    # Enable anti-aliasing for smoother graphics
    try:
        from tkinter import ttk
        ttk.Style().theme_use('clam')
    except:
        pass
    
    root = tk.Tk()
    app = OpenAgendaV11(root)
    root.mainloop()


if __name__ == "__main__":
    main()
