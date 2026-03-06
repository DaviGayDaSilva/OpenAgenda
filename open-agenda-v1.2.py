#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗  ██████╗ ██╗    ██╗██╗███╗   ██╗██████╗ ███████╗██████╗ ███████╗ ║
║   ██╔══██╗██╔═══██╗██║    ██║██║████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔════╝ ║
║   ██║  ██║██║   ██║██║ █╗ ██║██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝█████╗   ║
║   ██║  ██║██║   ██║██║███╗██║██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗██╔══╝   ║
║   ██████╔╝╚██████╔╝╚███╔███╔╝██║██║ ╚████║██████╔╝███████╗██║  ██║███████╗ ║
║   ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ║
║                                                                              ║
║   Open-Agenda v1.2 - Firefox-Style Modern UI                                ║
║   © 2025 Open-Agenda Team - Open Source & Free!                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Features:
- 🔥 Firefox-Style Modern UI (2025)
- 🎯 Rounded Corners & Glass Effect
- 📑 Tab-Based Navigation
- 💾 Auto-Save
- 🌙 Dark/Light Theme
- 🔍 Global Search
- 📊 Dashboard
- 📤 Export/Import
- 🎨 Categories & Priorities

Author: Open-Agenda Team
License: MIT
Version: 1.2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
import csv
from datetime import datetime, date, timedelta
import calendar as cal

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 FIREFOX-STYLE COLOR PALETTE (2025)
# ═══════════════════════════════════════════════════════════════════════════

class FirefoxColors:
    """Firefox-inspired modern color palette"""
    
    # Dark Theme (Primary)
    DARK = {
        # Backgrounds
        'bg_primary': '#1C1C1E',        # Main background
        'bg_secondary': '#2C2C2E',      # Card background
        'bg_tertiary': '#3A3A3C',       # Elevated surfaces
        'bg_hover': '#48484A',          # Hover states
        'bg_active': '#636366',          # Active states
        
        # Accent - Firefox Orange/Blue
        'accent_primary': '#FF7139',    # Firefox Orange
        'accent_secondary': '#007AFF',  # System Blue
        'accent_gradient_start': '#FF7139',
        'accent_gradient_end': '#FF4500',
        
        # Text
        'text_primary': '#FFFFFF',
        'text_secondary': '#EBEBF5',
        'text_tertiary': '#A1A1A6',
        'text_disabled': '#636366',
        
        # Semantic
        'success': '#30D158',
        'warning': '#FFD60A',
        'danger': '#FF453A',
        'info': '#64D2FF',
        
        # Borders
        'border': '#38383A',
        'border_light': '#48484A',
        
        # Glass effect
        'glass': '#1C1C1E99',
        'glass_border': '#FFFFFF1A',
    }
    
    # Light Theme
    LIGHT = {
        'bg_primary': '#F5F5F7',
        'bg_secondary': '#FFFFFF',
        'bg_tertiary': '#F0F0F2',
        'bg_hover': '#E5E5EA',
        'bg_active': '#D1D1D6',
        
        'accent_primary': '#FF6B2C',
        'accent_secondary': '#007AFF',
        'accent_gradient_start': '#FF6B2C',
        'accent_gradient_end': '#FF4500',
        
        'text_primary': '#1D1D1F',
        'text_secondary': '#6E6E73',
        'text_tertiary': '#A1A1A6',
        'text_disabled': '#C7C7CC',
        
        'success': '#34C759',
        'warning': '#FFCC00',
        'danger': '#FF3B30',
        'info': '#5AC8FA',
        
        'border': '#D1D1D6',
        'border_light': '#E5E5EA',
        
        'glass': '#FFFFFF99',
        'glass_border': '#0000001A',
    }
    
    # Category Colors
    CATEGORIES = {
        'personal': {'color': '#FF6B6B', 'name': 'Personal'},
        'work': {'color': '#4ECDC4', 'name': 'Work'},
        'family': {'color': '#95E1D3', 'name': 'Family'},
        'health': {'color': '#F9CA24', 'name': 'Health'},
        'education': {'color': '#A29BFE', 'name': 'Education'},
        'social': {'color': '#74B9FF', 'name': 'Social'},
        'finance': {'color': '#FD79A8', 'name': 'Finance'},
        'travel': {'color': '#FDCB6E', 'name': 'Travel'},
        'other': {'color': '#636E72', 'name': 'Other'},
    }


# ═══════════════════════════════════════════════════════════════════════════
# 🔧 CUSTOM WIDGETS - FIREFOX STYLE
# ═══════════════════════════════════════════════════════════════════════════

class FirefoxButton(tk.Frame):
    """Firefox-style rounded button"""
    
    def __init__(self, parent, text, command, icon='', bg=None, fg=None, 
                 hover_bg=None, corner_radius=8, **kwargs):
        super().__init__(parent, bg=bg or FirefoxColors.DARK['accent_primary'],
                        highlightthickness=0, bd=0, corner_radius=corner_radius)
        
        self.command = command
        self.default_bg = bg or FirefoxColors.DARK['accent_primary']
        self.hover_bg = hover_bg or FirefoxColors.DARK['accent_secondary']
        self.corner_radius = corner_radius
        
        self.canvas = tk.Canvas(self, bg=self.default_bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.text = f"{icon} {text}".strip() if icon else text
        
        self.label = tk.Label(self.canvas, text=self.text, 
                            font=('SF Pro Display', 12, 'bold') if os.name == 'nt' else ('Segoe UI', 11, 'bold'),
                            bg=self.default_bg, fg=fg or '#FFFFFF',
                            padx=16, pady=8)
        self.label.pack(padx=8, pady=4)
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.label.bind('<Enter>', self.on_enter)
        self.label.bind('<Leave>', self.on_leave)
        
        self.bind('<Button-1>', self.on_click)
        self.label.bind('<Button-1>', self.on_click)
    
    def on_enter(self, e):
        self.canvas.configure(bg=self.hover_bg)
        self.label.configure(bg=self.hover_bg)
    
    def on_leave(self, e):
        self.canvas.configure(bg=self.default_bg)
        self.label.configure(bg=self.default_bg)
    
    def on_click(self, e):
        self.command()


class FirefoxEntry(tk.Frame):
    """Firefox-style search/input field"""
    
    def __init__(self, parent, placeholder='', **kwargs):
        super().__init__(parent, bg=FirefoxColors.DARK['bg_tertiary'],
                        highlightthickness=0, bd=0, corner_radius=10)
        
        self.placeholder = placeholder
        
        self.entry = tk.Entry(self, 
                            font=('SF Pro Display', 13) if os.name == 'nt' else ('Segoe UI', 12),
                            bg=FirefoxColors.DARK['bg_tertiary'],
                            fg=FirefoxColors.DARK['text_primary'],
                            insertbackground=FirefoxColors.DARK['text_primary'],
                            relief=tk.FLAT, bd=0, highlightthickness=0)
        self.entry.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.configure(fg=FirefoxColors.DARK['text_tertiary'])
            self.entry.bind('<FocusIn>', self.on_focus)
            self.entry.bind('<FocusOut>', self.on_focus_out)
    
    def on_focus(self, e):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=FirefoxColors.DARK['text_primary'])
    
    def on_focus_out(self, e):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.configure(fg=FirefoxColors.DARK['text_tertiary'])
    
    def get(self):
        return self.entry.get()
    
    def delete(self, start, end):
        self.entry.delete(start, end)
    
    def insert(self, index, text):
        self.entry.insert(index, text)
    
    def focus_set(self):
        self.entry.focus_set()


class FirefoxTab(tk.Frame):
    """Firefox-style tab button"""
    
    def __init__(self, parent, text, command, icon='', is_active=False, **kwargs):
        super().__init__(parent, bg=FirefoxColors.DARK['bg_primary'], bd=0)
        
        self.command = command
        self.is_active = is_active
        
        self.canvas = tk.Canvas(self, bg=FirefoxColors.DARK['bg_primary'], 
                               highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.text = f"{icon} {text}" if icon else text
        
        self.label = tk.Label(self.canvas, text=self.text,
                            font=('SF Pro Display', 12) if os.name == 'nt' else ('Segoe UI', 11),
                            bg=FirefoxColors.DARK['bg_primary'],
                            fg=FirefoxColors.DARK['text_secondary'],
                            padx=16, pady=10)
        self.label.pack()
        
        self.bind('<Button-1>', lambda e: self.command())
    
    def set_active(self, active):
        self.is_active = active
        if active:
            self.label.configure(fg=FirefoxColors.DARK['accent_primary'])
            self.canvas.configure(bg=FirefoxColors.DARK['bg_secondary'])
        else:
            self.label.configure(fg=FirefoxColors.DARK['text_secondary'])
            self.canvas.configure(bg=FirefoxColors.DARK['bg_primary'])


class FirefoxSidebarButton(tk.Frame):
    """Firefox-style sidebar icon button"""
    
    def __init__(self, parent, icon, command, tooltip='', is_active=False, **kwargs):
        super().__init__(parent, bg=FirefoxColors.DARK['bg_primary'],
                        width=48, height=48, bd=0)
        
        self.command = command
        
        self.btn = tk.Label(self, text=icon, font=('Segoe UI Emoji', 18),
                          bg=FirefoxColors.DARK['bg_primary'],
                          fg=FirefoxColors.DARK['text_secondary'],
                          width=3, height=2, bd=0, cursor='hand2')
        self.btn.pack(pady=4)
        
        self.btn.bind('<Button-1>', lambda e: self.command())
        self.btn.bind('<Enter>', self.on_enter)
        self.btn.bind('<Leave>', self.on_leave)
        
        if is_active:
            self.set_active(True)
    
    def on_enter(self, e):
        if not self.is_active:
            self.btn.configure(bg=FirefoxColors.DARK['bg_hover'])
    
    def on_leave(self, e):
        if not self.is_active:
            self.btn.configure(bg=FirefoxColors.DARK['bg_primary'])
    
    def set_active(self, active):
        self.is_active = active
        if active:
            self.btn.configure(bg=FirefoxColors.DARK['accent_primary'], 
                            fg='#FFFFFF')
        else:
            self.btn.configure(bg=FirefoxColors.DARK['bg_primary'],
                            fg=FirefoxColors.DARK['text_secondary'])


class FirefoxCard(tk.Frame):
    """Firefox-style rounded card"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 
                        bg=FirefoxColors.DARK['bg_secondary'],
                        highlightthickness=0, bd=0,
                        corner_radius=12)


# ═══════════════════════════════════════════════════════════════════════════
# 🗓️ MAIN APPLICATION - FIREFOX STYLE
# ═══════════════════════════════════════════════════════════════════════════

class OpenAgendaV12:
    """Open-Agenda v1.2 - Firefox-Style Modern UI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Open-Agenda v1.2")
        self.root.geometry("1200x800")
        self.root.configure(bg=FirefoxColors.DARK['bg_primary'])
        
        # Data
        self.data_file = "open_agenda_v12_data.json"
        self.events = {}
        self.current_view = "calendar"
        self.current_date = date.today()
        self.selected_date = date.today()
        self.is_dark_theme = True
        self.colors = FirefoxColors.DARK.copy()
        
        # Create UI
        self.create_ui()
        self.load_data()
        self.update_view()
        
        # Protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        """Create Firefox-style UI"""
        
        # ═══════════════════════════════════════════════════════════════
        # 📑 TAB BAR (Firefox Style)
        # ═══════════════════════════════════════════════════════════════
        
        self.tab_bar = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=48)
        self.tab_bar.pack(fill=tk.X)
        self.tab_bar.pack_propagate(False)
        
        # App Icon/Logo
        self.app_icon = tk.Label(self.tab_bar, text="🔥",
                               font=('Segoe UI Emoji', 16),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['accent_primary'])
        self.app_icon.pack(side=tk.LEFT, padx=12)
        
        # Tab: Calendar
        self.tab_calendar = FirefoxTab(self.tab_bar, "Calendar", 
                                        lambda: self.switch_view("calendar"),
                                        icon="📅")
        self.tab_calendar.pack(side=tk.LEFT)
        self.tab_calendar.set_active(True)
        
        # Tab: Events
        self.tab_events = FirefoxTab(self.tab_bar, "Events",
                                    lambda: self.switch_view("events"),
                                    icon="📋")
        self.tab_events.pack(side=tk.LEFT)
        
        # Tab: Dashboard
        self.tab_dashboard = FirefoxTab(self.tab_bar, "Dashboard",
                                        lambda: self.switch_view("dashboard"),
                                        icon="📊")
        self.tab_dashboard.pack(side=tk.LEFT)
        
        # Tab: Settings
        self.tab_settings = FirefoxTab(self.tab_bar, "Settings",
                                       lambda: self.switch_view("settings"),
                                       icon="⚙️")
        self.tab_settings.pack(side=tk.LEFT)
        
        # Spacer
        tk.Frame(self.tab_bar, bg=self.colors['bg_secondary']).pack(side=tk.LEFT, expand=True)
        
        # Search Bar
        self.search_entry = FirefoxEntry(self.tab_bar, placeholder="Search events...")
        self.search_entry.configure(bg=self.colors['bg_tertiary'])
        self.search_entry.entry.configure(bg=self.colors['bg_tertiary'])
        self.search_entry.pack(side=tk.LEFT, padx=(0, 8), pady=6, fill=tk.X, expand=True)
        self.search_entry.entry.bind('<KeyRelease>', self.on_search)
        
        # Theme Toggle
        self.theme_btn = tk.Label(self.tab_bar, text="🌙",
                                font=('Segoe UI Emoji', 14),
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text_secondary'],
                                cursor='hand2')
        self.theme_btn.pack(side=tk.LEFT, padx=8)
        self.theme_btn.bind('<Button-1>', lambda e: self.toggle_theme())
        
        # New Event Button
        self.new_event_btn = FirefoxButton(self.tab_bar, "New Event",
                                          self.show_new_event_dialog,
                                          icon="➕",
                                          bg=self.colors['accent_primary'])
        self.new_event_btn.pack(side=tk.LEFT, padx=12, pady=6)
        
        # ═══════════════════════════════════════════════════════════════
        # 🎯 MAIN CONTENT AREA
        # ═══════════════════════════════════════════════════════════════
        
        self.content_area = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.content_area.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(self.content_area, bg=self.colors['bg_primary'], width=64)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Sidebar buttons
        self.sidebar_calendar = FirefoxSidebarButton(self.sidebar, "📅",
                                                      lambda: self.switch_view("calendar"),
                                                      is_active=True)
        self.sidebar_calendar.pack()
        
        self.sidebar_events = FirefoxSidebarButton(self.sidebar, "📋",
                                                     lambda: self.switch_view("events"))
        self.sidebar_events.pack()
        
        self.sidebar_dashboard = FirefoxSidebarButton(self.sidebar, "📊",
                                                      lambda: self.switch_view("dashboard"))
        self.sidebar_dashboard.pack()
        
        self.sidebar_settings = FirefoxSidebarButton(self.sidebar, "⚙️",
                                                      lambda: self.switch_view("settings"))
        self.sidebar_settings.pack()
        
        # Main View Container
        self.main_view = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        self.main_view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create views
        self.calendar_view = None
        self.events_view = None
        self.dashboard_view = None
        self.settings_view = None
        
        # ═══════════════════════════════════════════════════════════════
        # 📊 STATUS BAR
        # ═══════════════════════════════════════════════════════════════
        
        self.status_bar = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=32)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_bar,
                                    text="🔥 Open-Agenda v1.2 • Auto-save enabled",
                                    font=('SF Pro Display', 10) if os.name == 'nt' else ('Segoe UI', 10),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_tertiary'])
        self.status_label.pack(side=tk.LEFT, padx=16)
        
        self.save_status = tk.Label(self.status_bar, text="💾 Saved",
                                    font=('Segoe UI', 10),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['success'])
        self.save_status.pack(side=tk.RIGHT, padx=16)
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.show_new_event_dialog())
        self.root.bind('<Control-f>', lambda e: self.search_entry.entry.focus_set())
        self.root.bind('<Control-s>', lambda e: self.manual_save())
        self.root.bind('<Control-t>', lambda e: self.go_to_today())
        self.root.bind('<Left>', lambda e: self.prev_month())
        self.root.bind('<Right>', lambda e: self.next_month())
    
    def switch_view(self, view_name):
        """Switch between views"""
        self.current_view = view_name
        
        # Update sidebar
        self.sidebar_calendar.set_active(view_name == "calendar")
        self.sidebar_events.set_active(view_name == "events")
        self.sidebar_dashboard.set_active(view_name == "dashboard")
        self.sidebar_settings.set_active(view_name == "settings")
        
        # Update tab bar
        self.tab_calendar.set_active(view_name == "calendar")
        self.tab_events.set_active(view_name == "events")
        self.tab_dashboard.set_active(view_name == "dashboard")
        self.tab_settings.set_active(view_name == "settings")
        
        # Update main view
        self.update_view()
    
    def update_view(self):
        """Update the current view"""
        # Clear main view
        for widget in self.main_view.winfo_children():
            widget.destroy()
        
        if self.current_view == "calendar":
            self.create_calendar_view()
        elif self.current_view == "events":
            self.create_events_view()
        elif self.current_view == "dashboard":
            self.create_dashboard_view()
        elif self.current_view == "settings":
            self.create_settings_view()
    
    def create_calendar_view(self):
        """Create calendar view"""
        # Header
        header = tk.Frame(self.main_view, bg=self.colors['bg_primary'])
        header.pack(fill=tk.X)
        
        nav_btn = tk.Button(header, text="◀", font=('Segoe UI', 14),
                          bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                          relief=tk.FLAT, command=self.prev_month)
        nav_btn.pack(side=tk.LEFT)
        
        self.month_label = tk.Label(header, text="",
                                  font=('SF Pro Display', 18, 'bold') if os.name == 'nt' else ('Segoe UI', 16, 'bold'),
                                  bg=self.colors['bg_primary'],
                                  fg=self.colors['text_primary'])
        self.month_label.pack(side=tk.LEFT, padx=20)
        
        nav_btn2 = tk.Button(header, text="▶", font=('Segoe UI', 14),
                            bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                            relief=tk.FLAT, command=self.next_month)
        nav_btn2.pack(side=tk.LEFT)
        
        today_btn = FirefoxButton(header, "Today", self.go_to_today, icon="📅",
                                 bg=self.colors['accent_primary'])
        today_btn.pack(side=tk.RIGHT)
        
        # Calendar Grid
        cal_frame = FirefoxCard(self.main_view)
        cal_frame.pack(fill=tk.BOTH, expand=True, pady=16)
        
        # Days header
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(days):
            tk.Label(cal_frame, text=day,
                    font=('SF Pro Display', 11, 'bold') if os.name == 'nt' else ('Segoe UI', 10, 'bold'),
                    bg=self.colors['bg_secondary'],
                    fg=self.colors['text_tertiary']).grid(row=0, column=i, padx=4, pady=8)
        
        self.cal_buttons = []
        
        # Calendar grid
        calendar = cal.Calendar(firstweekday=6)
        month_days = calendar.monthdayscalendar(self.current_date.year, self.current_date.month)
        
        for week_idx, week in enumerate(month_days):
            for day_idx, day in enumerate(week):
                if day == 0:
                    tk.Label(cal_frame, text="",
                            bg=self.colors['bg_secondary']).grid(row=week_idx+1, column=day_idx, padx=2, pady=2)
                else:
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    
                    bg = self.colors['accent_primary'] if day_date == date.today() else self.colors['bg_tertiary']
                    fg = '#FFFFFF' if day_date == date.today() else self.colors['text_primary']
                    
                    btn = tk.Button(cal_frame, text=str(day),
                                   font=('SF Pro Display', 11) if os.name == 'nt' else ('Segoe UI', 10),
                                   bg=bg, fg=fg, relief=tk.FLAT,
                                   command=lambda d=day: self.select_date(d))
                    btn.grid(row=week_idx+1, column=day_idx, padx=2, pady=2, sticky='nsew')
                    self.cal_buttons.append(btn)
        
        # Selected date events
        self.selected_events_frame = FirefoxCard(self.main_view)
        self.selected_events_frame.pack(fill=tk.X, pady=(0, 16))
        
        self.selected_date_label = tk.Label(self.selected_events_frame,
                                           text="",
                                           font=('SF Pro Display', 14, 'bold') if os.name == 'nt' else ('Segoe UI', 13, 'bold'),
                                           bg=self.colors['bg_secondary'],
                                           fg=self.colors['text_primary'])
        self.selected_date_label.pack(anchor=tk.W, padx=16, pady=(12, 8))
        
        self.events_list_label = tk.Label(self.selected_events_frame,
                                         text="No events",
                                         font=('SF Pro Display', 11) if os.name == 'nt' else ('Segoe UI', 10),
                                         bg=self.colors['bg_secondary'],
                                         fg=self.colors['text_tertiary'])
        self.events_list_label.pack(anchor=tk.W, padx=16, pady=(0, 12))
        
        self.update_calendar()
    
    def create_events_view(self):
        """Create events list view"""
        # Header
        tk.Label(self.main_view, text="📋 All Events",
                font=('SF Pro Display', 20, 'bold') if os.name == 'nt' else ('Segoe UI', 18, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        # Events container
        events_container = FirefoxCard(self.main_view)
        events_container.pack(fill=tk.BOTH, expand=True, pady=16)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(events_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.events_listbox = tk.Listbox(events_container,
                                        font=('SF Pro Display', 12) if os.name == 'nt' else ('Segoe UI', 11),
                                        bg=self.colors['bg_secondary'],
                                        fg=self.colors['text_primary'],
                                        relief=tk.FLAT, bd=0,
                                        yscrollcommand=scrollbar.set)
        self.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scrollbar.config(command=self.events_listbox.yview)
        
        self.update_events_list()
    
    def create_dashboard_view(self):
        """Create dashboard view"""
        # Header
        tk.Label(self.main_view, text="📊 Dashboard",
                font=('SF Pro Display', 20, 'bold') if os.name == 'nt' else ('Segoe UI', 18, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        # Stats Grid
        stats_frame = tk.Frame(self.main_view, bg=self.colors['bg_primary'])
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=16)
        
        # Calculate stats
        total_events = sum(len(e) for e in self.events.values())
        days_with_events = len(self.events)
        
        # Cards
        self.create_stat_card(stats_frame, "Total Events", str(total_events), "📅", 0, 0)
        self.create_stat_card(stats_frame, "Days with Events", str(days_with_events), "📆", 0, 1)
        self.create_stat_card(stats_frame, "This Month", str(self.get_month_events()), "🗓️", 1, 0)
        self.create_stat_card(stats_frame, "Upcoming", str(self.get_upcoming_events()), "⏰", 1, 1)
    
    def create_stat_card(self, parent, title, value, icon, row, col):
        """Create a stat card"""
        card = FirefoxCard(parent)
        card.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
        
        tk.Label(card, text=icon, font=('Segoe UI Emoji', 24),
                bg=self.colors['bg_secondary'],
                fg=self.colors['accent_primary']).pack(pady=(16, 8))
        
        tk.Label(card, text=value,
                font=('SF Pro Display', 28, 'bold') if os.name == 'nt' else ('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']).pack()
        
        tk.Label(card, text=title,
                font=('SF Pro Display', 12) if os.name == 'nt' else ('Segoe UI', 11),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_tertiary']).pack(pady=(0, 16))
        
        parent.columnconfigure(col, weight=1)
        parent.rowconfigure(row, weight=1)
    
    def create_settings_view(self):
        """Create settings view"""
        # Header
        tk.Label(self.main_view, text="⚙️ Settings",
                font=('SF Pro Display', 20, 'bold') if os.name == 'nt' else ('Segoe UI', 18, 'bold'),
                bg=self.colors['bg_primary'],
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor=tk.W)
        
        settings_container = FirefoxCard(self.main_view)
        settings_container.pack(fill=tk.BOTH, expand=True, pady=16)
        
        # Theme toggle
        theme_frame = tk.Frame(settings_container, bg=self.colors['bg_secondary'])
        theme_frame.pack(fill=tk.X, padx=16, pady=16)
        
        tk.Label(theme_frame, text="🌗 Theme",
                font=('SF Pro Display', 13) if os.name == 'nt' else ('Segoe UI', 12),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        theme_toggle = tk.Button(theme_frame, text="Toggle Dark/Light",
                                command=self.toggle_theme,
                                bg=self.colors['accent_primary'],
                                fg='#FFFFFF',
                                relief=tk.FLAT)
        theme_toggle.pack(side=tk.RIGHT)
        
        # Export/Import
        tk.Label(settings_container, text="📤 Export / Import",
                font=('SF Pro Display', 14, 'bold') if os.name == 'nt' else ('Segoe UI', 13, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']).pack(anchor=tk.W, padx=16, pady=(8, 8))
        
        btn_frame = tk.Frame(settings_container, bg=self.colors['bg_secondary'])
        btn_frame.pack(padx=16, pady=(0, 16))
        
        FirefoxButton(btn_frame, "Export JSON", self.export_json, icon="📄",
                     bg=self.colors['info']).pack(side=tk.LEFT, padx=4)
        FirefoxButton(btn_frame, "Export CSV", self.export_csv, icon="📊",
                     bg=self.colors['success']).pack(side=tk.LEFT, padx=4)
        FirefoxButton(btn_frame, "Import", self.import_data, icon="📥",
                     bg=self.colors['warning']).pack(side=tk.LEFT, padx=4)
    
    def update_calendar(self):
        """Update calendar view"""
        month_name = cal.month_name[self.current_date.month]
        self.month_label.configure(text=f"{month_name} {self.current_date.year}")
        
        # Update selected date
        day_name = self.selected_date.strftime("%A, %B %d, %Y")
        self.selected_date_label.configure(text=f"📅 {day_name}")
        
        # Update events
        if self.selected_date in self.events and self.events[self.selected_date]:
            events_text = "\n".join([f"⏰ {e['time']} - {e['title']}" 
                                    for e in self.events[self.selected_date]])
            self.events_list_label.configure(text=events_text, fg=self.colors['text_primary'])
        else:
            self.events_list_label.configure(text="No events for this day. Click 'New Event' to add one!",
                                           fg=self.colors['text_tertiary'])
    
    def update_events_list(self):
        """Update events list"""
        self.events_listbox.delete(0, tk.END)
        
        sorted_events = []
        for event_date, events_list in self.events.items():
            for event in events_list:
                sorted_events.append((event_date, event))
        
        sorted_events.sort(key=lambda x: (x[0], x[1].get('time', '00:00')))
        
        for event_date, event in sorted_events:
            text = f"📅 {event_date.strftime('%Y-%m-%d')} ⏰ {event.get('time', '00:00')} - {event['title']}"
            self.events_listbox.insert(tk.END, text)
        
        if not sorted_events:
            self.events_listbox.insert(tk.END, "No events yet. Create your first event!")
    
    def get_month_events(self):
        """Get events count for current month"""
        count = 0
        for event_date, events_list in self.events.items():
            if event_date.year == self.current_date.year and event_date.month == self.current_date.month:
                count += len(events_list)
        return count
    
    def get_upcoming_events(self):
        """Get upcoming events count (next 7 days)"""
        count = 0
        today = date.today()
        for i in range(7):
            check_date = today + timedelta(days=i)
            if check_date in self.events:
                count += len(self.events[check_date])
        return count
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🎯 NAVIGATION
    # ═══════════════════════════════════════════════════════════════════════
    
    def select_date(self, day):
        """Select a date"""
        self.selected_date = date(self.current_date.year, self.current_date.month, day)
        self.update_calendar()
    
    def prev_month(self):
        """Previous month"""
        if self.current_date.month == 1:
            self.current_date = date(self.current_date.year - 1, 12, 1)
        else:
            self.current_date = date(self.current_date.year, self.current_date.month - 1, 1)
        self.update_view()
    
    def next_month(self):
        """Next month"""
        if self.current_date.month == 12:
            self.current_date = date(self.current_date.year + 1, 1, 1)
        else:
            self.current_date = date(self.current_date.year, self.current_date.month + 1, 1)
        self.update_view()
    
    def go_to_today(self):
        """Go to today"""
        self.current_date = date.today()
        self.selected_date = date.today()
        self.update_view()
    
    def toggle_theme(self):
        """Toggle theme"""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.colors = FirefoxColors.DARK.copy()
            self.theme_btn.configure(text="🌙")
        else:
            self.colors = FirefoxColors.LIGHT.copy()
            self.theme_btn.configure(text="☀️")
        
        # Recreate UI
        self.root.configure(bg=self.colors['bg_primary'])
        self.create_ui()
        self.load_data()
        self.update_view()
    
    def on_search(self, event=None):
        """Search events"""
        query = self.search_entry.get().lower()
        
        if not query or query == "search events...":
            return
        
        # Filter events
        results = []
        for event_date, events_list in self.events.items():
            for event in events_list:
                if (query in event['title'].lower() or
                    query in event_date.strftime('%Y-%m-%d').lower()):
                    results.append((event_date, event))
        
        if results:
            messagebox.showinfo("Search Results", 
                             f"Found {len(results)} events:\n\n" + 
                             "\n".join([f"📅 {d.strftime('%Y-%m-%d')} - {e['title']}" 
                                       for d, e in results[:10]]))
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📝 EVENT MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════
    
    def show_new_event_dialog(self):
        """Show new event dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ New Event")
        dialog.geometry("400x450")
        dialog.configure(bg=self.colors['bg_primary'])
        
        # Form
        tk.Label(dialog, text="📅 New Event",
                font=('SF Pro Display', 16, 'bold') if os.name == 'nt' else ('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(pady=16)
        
        # Date
        tk.Label(dialog, text="Date:",
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']).pack(anchor=tk.W, padx=20)
        
        date_entry = FirefoxEntry(dialog, placeholder=f"{self.selected_date.strftime('%Y-%m-%d')}")
        date_entry.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        # Time
        tk.Label(dialog, text="Time:",
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']).pack(anchor=tk.W, padx=20)
        
        time_entry = FirefoxEntry(dialog, placeholder="14:30")
        time_entry.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        # Title
        tk.Label(dialog, text="Title:",
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']).pack(anchor=tk.W, padx=20)
        
        title_entry = FirefoxEntry(dialog, placeholder="Event title...")
        title_entry.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        # Category
        tk.Label(dialog, text="Category:",
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']).pack(anchor=tk.W, padx=20)
        
        category_var = tk.StringVar(value="personal")
        category_menu = ttk.Combobox(dialog, textvariable=category_var,
                                    values=list(FirefoxColors.CATEGORIES.keys()),
                                    state='readonly')
        category_menu.pack(fill=tk.X, padx=20, pady=(0, 12))
        
        # Add button
        def add_event():
            try:
                event_date = datetime.strptime(date_entry.get(), "%Y-%m-%d").date()
            except:
                event_date = self.selected_date
            
            time_val = time_entry.get() or "09:00"
            title = title_entry.get()
            
            if not title:
                messagebox.showwarning("Warning", "Please enter a title!")
                return
            
            if event_date not in self.events:
                self.events[event_date] = []
            
            self.events[event_date].append({
                'time': time_val,
                'title': title,
                'category': category_var.get(),
                'created': datetime.now().isoformat()
            })
            
            self.events[event_date].sort(key=lambda x: x.get('time', '00:00'))
            
            dialog.destroy()
            self.update_view()
            self.trigger_save()
        
        FirefoxButton(dialog, "Add Event", add_event, icon="➕",
                     bg=self.colors['success']).pack(pady=20)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 💾 DATA MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════
    
    def trigger_save(self):
        """Trigger auto-save"""
        self.save_status.configure(text="⏳ Saving...", fg=self.colors['warning'])
        self.root.after(1000, self.perform_save)
    
    def perform_save(self):
        """Save data"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = {k.isoformat(): v for k, v in self.events.items()}
                json.dump(data, f, indent=2)
            self.save_status.configure(text="💾 Saved", fg=self.colors['success'])
        except Exception as e:
            self.save_status.configure(text="❌ Error", fg=self.colors['danger'])
    
    def manual_save(self):
        """Manual save"""
        self.perform_save()
        self.status_label.configure(text="💾 Saved manually")
    
    def load_data(self):
        """Load data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = {date.fromisoformat(k): v for k, v in data.items()}
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def export_json(self):
        """Export JSON"""
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                               initialfile="open_agenda_export.json")
        if filename:
            with open(filename, 'w') as f:
                json.dump({k.isoformat(): v for k, v in self.events.items()}, f, indent=2)
            messagebox.showinfo("Success", "Exported successfully!")
    
    def export_csv(self):
        """Export CSV"""
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                               initialfile="open_agenda_export.csv")
        if filename:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Time', 'Title', 'Category'])
                for d, events in self.events.items():
                    for e in events:
                        writer.writerow([d.isoformat(), e.get('time', ''), e['title'], 
                                       e.get('category', 'other')])
            messagebox.showinfo("Success", "Exported successfully!")
    
    def import_data(self):
        """Import data"""
        filename = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                self.events = {date.fromisoformat(k): v for k, v in json.load(f).items()}
            self.update_view()
            messagebox.showinfo("Success", "Imported successfully!")
    
    def on_closing(self):
        """On close"""
        self.perform_save()
        self.root.destroy()


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    app = OpenAgendaV12(root)
    root.mainloop()


if __name__ == "__main__":
    main()
