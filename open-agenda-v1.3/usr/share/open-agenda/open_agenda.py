#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██████╗  ██████╗ ███████╗    ██████╗  █████╗ ██████╗  █████╗ ██████╗  ║
║   ██╔════╝██╔══██╗██╔═══██╗██╔════╝   ██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗ ║
║   █████╗  ██████╔╝██║   ██║█████╗     ██║   ██║███████║██████╔╝███████║██████╔╝ ║
║   ██╔══╝  ██╔══██╗██║   ██║██╔══╝     ██║   ██║██╔══██║██╔══██╗██╔══██║██╔══██╗ ║
║   ██║     ██║  ██║╚██████╔╝███████╗   ╚██████╔╝██║  ██║██║  ██║██║  ██║██║  ██║ ║
║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ║
║                                                                              ║
║   Open-Agenda v1.3 - Ultra Modern 2025 Glass UI                              ║
║   © 2025 Open-Agenda Team - The Future of Calendars!                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Ultra Modern Features:
- ✨ Glassmorphism & Frosted Glass Effects
- 🌈 Vibrant Gradient Backgrounds  
- 💫 Smooth Animations & Transitions
- 🎭 Modern Floating Elements
- 🔮 Glowing Effects & Shadows
- 📱 Fully Responsive Design
- 🌙 Dark Mode with Neon Accents
- 📊 Interactive Dashboard
- 🎯 And much more!

Author: Open-Agenda Team
License: MIT
Version: 1.3.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
from datetime import datetime, date, timedelta
import calendar as cal
import math

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 ULTRA MODERN 2025 COLOR PALETTE
# ═══════════════════════════════════════════════════════════════════════════

class UltraModernColors:
    """Ultra-modern 2025 glassmorphism color palette"""
    
    # Dark Theme with Neon
    DARK = {
        # Backgrounds with transparency
        'bg_primary': '#0A0A0F',          # Deep space black
        'bg_secondary': '#12121A',        # Card background
        'bg_glass': '#1A1A2E99',          # Glass effect (60% opacity)
        'bg_glass_strong': '#1A1A2ECC',   # Strong glass
        
        # Accent gradients
        'accent_gradient_1': '#FF006E',   # Hot pink
        'accent_gradient_2': '#8338EC',   # Electric purple
        'accent_gradient_3': '#3A86FF',   # Electric blue
        'accent_gradient_4': '#06D6A0',   # Neon green
        
        # Neon glow
        'neon_pink': '#FF006E',
        'neon_purple': '#8338EC',
        'neon_blue': '#3A86FF',
        'neon_green': '#06D6A0',
        
        # Text
        'text_primary': '#FFFFFF',
        'text_secondary': '#B8B8D1',
        'text_muted': '#6B6B8D',
        
        # Semantic
        'success': '#00F5D4',
        'warning': '#FEE440',
        'danger': '#FF006E',
        'info': '#00BBF9',
        
        # Effects
        'glow': '#8338EC40',
        'border_glass': '#FFFFFF1A',
        'shadow': '#00000080',
    }
    
    # Light Theme
    LIGHT = {
        'bg_primary': '#F8F9FF',
        'bg_secondary': '#FFFFFF',
        'bg_glass': '#FFFFFF99',
        'bg_glass_strong': '#FFFFFFEE',
        
        'accent_gradient_1': '#FF4D8D',
        'accent_gradient_2': '#6B4EE6',
        'accent_gradient_3': '#2D7BF4',
        'accent_gradient_4': '#00C9A7',
        
        'neon_pink': '#FF4D8D',
        'neon_purple': '#6B4EE6',
        'neon_blue': '#2D7BF4',
        'neon_green': '#00C9A7',
        
        'text_primary': '#1A1A2E',
        'text_secondary': '#4A4A6A',
        'text_muted': '#8A8AAA',
        
        'success': '#00C9A7',
        'warning': '#F5B800',
        'danger': '#FF4D8D',
        'info': '#2D7BF4',
        
        'glow': '#6B4EE640',
        'border_glass': '#00000010',
        'shadow': '#00000020',
    }
    
    # Categories
    CATEGORIES = {
        'personal': {'color': '#FF006E', 'name': 'Personal', 'icon': '👤'},
        'work': {'color': '#3A86FF', 'name': 'Work', 'icon': '💼'},
        'family': {'color': '#06D6A0', 'name': 'Family', 'icon': '👨‍👩‍👧'},
        'health': {'color': '#FEE440', 'name': 'Health', 'icon': '🏥'},
        'education': {'color': '#8338EC', 'name': 'Education', 'icon': '📚'},
        'social': {'color': '#00BBF9', 'name': 'Social', 'icon': '🎉'},
        'finance': {'color': '#FF006E', 'name': 'Finance', 'icon': '💰'},
        'travel': {'color': '#FB5607', 'name': 'Travel', 'icon': '✈️'},
        'other': {'color': '#6B7280', 'name': 'Other', 'icon': '📌'},
    }


# ═══════════════════════════════════════════════════════════════════════════
# ✨ CUSTOM WIDGETS - GLASSMORPHISM STYLE
# ═══════════════════════════════════════════════════════════════════════════

class GlassFrame(tk.Frame):
    """Glassmorphism frame with frosted glass effect"""
    
    def __init__(self, parent, opacity=0.6, border=True, corner_radius=16, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.corner_radius = corner_radius
        self.opacity = opacity
        self.border_enabled = border
        
        self.configure(
            bg=UltraModernColors.DARK['bg_glass_strong'],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        
        # Add border effect
        if border:
            self.border_canvas = tk.Canvas(self, bg='transparent', highlightthickness=0)
            self.border_canvas.pack(fill=tk.BOTH, expand=True)


class GradientButton(tk.Button):
    """Gradient button with glow effect"""
    
    def __init__(self, parent, text, command, icon='', corner_radius=12, **kwargs):
        self.command = command
        self.corner_radius = corner_radius
        
        super().__init__(
            parent, text=f"{icon} {text}".strip() if icon else text,
            command=command,
            font=('Segoe UI', 11, 'bold'),
            bg=UltraModernColors.DARK['accent_gradient_1'],
            fg='#FFFFFF',
            activebackground=UltraModernColors.DARK['accent_gradient_2'],
            activeforeground='#FFFFFF',
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2',
            **kwargs
        )
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
        # Glow effect
        self.configure(highlightbackground=UltraModernColors.DARK['neon_purple'])
    
    def on_enter(self, e):
        self.configure(bg=UltraModernColors.DARK['accent_gradient_2'])
    
    def on_leave(self, e):
        self.configure(bg=UltraModernColors.DARK['accent_gradient_1'])


class NeonEntry(tk.Entry):
    """Entry with neon glow effect"""
    
    def __init__(self, parent, placeholder='', **kwargs):
        self.placeholder = placeholder
        
        super().__init__(
            parent,
            font=('Segoe UI', 12),
            bg=UltraModernColors.DARK['bg_glass'],
            fg=UltraModernColors.DARK['text_primary'],
            insertbackground=UltraModernColors.DARK['neon_blue'],
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=0,
            **kwargs
        )
        
        self.configure(highlightbackground=UltraModernColors.DARK['neon_purple'],
                      highlightcolor=UltraModernColors.DARK['neon_blue'])
        
        if placeholder:
            self.insert(0, placeholder)
            self.configure(fg=UltraModernColors.DARK['text_muted'])
            self.bind('<FocusIn>', self.on_focus)
            self.bind('<FocusOut>', self.on_focus_out)
    
    def on_focus(self, e):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(fg=UltraModernColors.DARK['text_primary'])
    
    def on_focus_out(self, e):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(fg=UltraModernColors.DARK['text_muted'])


class GlassCard(tk.Frame):
    """Modern glass card with hover effect"""
    
    def __init__(self, parent, glow_color=None, **kwargs):
        super().__init__(
            parent,
            bg=UltraModernColors.DARK['bg_glass_strong'],
            relief=tk.FLAT,
            bd=0,
            **kwargs
        )
        
        self.glow_color = glow_color or UltraModernColors.DARK['neon_purple']
        
        # Add subtle glow border
        self.configure(highlightthickness=1,
                     highlightbackground=self.glow_color)


class FloatingLabel(tk.Label):
    """Floating label with animation effect"""
    
    def __init__(self, parent, text, size=14, weight='normal', color='primary', **kwargs):
        colors = {
            'primary': UltraModernColors.DARK['text_primary'],
            'secondary': UltraModernColors.DARK['text_secondary'],
            'accent': UltraModernColors.DARK['accent_gradient_2'],
            'neon': UltraModernColors.DARK['neon_pink'],
        }
        
        super().__init__(
            parent, text=text,
            font=('Segoe UI', size, weight),
            bg='transparent',
            fg=colors.get(color, colors['primary']),
            **kwargs
        )


# ═══════════════════════════════════════════════════════════════════════════
# 🗓️ MAIN APPLICATION - ULTRA MODERN
# ═══════════════════════════════════════════════════════════════════════════

class OpenAgendaV13:
    """Open-Agenda v1.3 - Ultra Modern Glass UI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Open-Agenda v1.3 - Ultra Modern")
        self.root.geometry("1300x850")
        self.root.configure(bg=UltraModernColors.DARK['bg_primary'])
        
        # Data
        self.data_file = "open_agenda_v13_data.json"
        self.events = {}
        self.current_date = date.today()
        self.selected_date = date.today()
        self.is_dark_theme = True
        self.colors = UltraModernColors.DARK.copy()
        
        # Animation state
        self.animation_phase = 0
        
        # Create UI
        self.create_ui()
        self.load_data()
        self.update_calendar()
        
        # Start animations
        self.animate()
        
        # Protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        """Create ultra-modern glass UI"""
        
        # ═══════════════════════════════════════════════════════════════════
        # 🌟 BACKGROUND GRADIENT EFFECT
        # ═══════════════════════════════════════════════════════════════════
        
        # Background canvas for gradient
        self.bg_canvas = tk.Canvas(self.root, bg=self.colors['bg_primary'], 
                                   highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # ═══════════════════════════════════════════════════════════════════
        # 💫 HEADER BAR
        # ═══════════════════════════════════════════════════════════════════
        
        self.header = GlassFrame(self.root, opacity=0.8, corner_radius=0)
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.pack_propagate(False)
        self.header.configure(height=70)
        
        # Logo
        self.logo = FloatingLabel(self.header, "✨ Open-Agenda", 22, 'bold', 'neon')
        self.logo.pack(side=tk.LEFT, padx=20)
        
        # Search bar (glass style)
        search_frame = GlassFrame(self.header, opacity=0.5, corner_radius=20)
        search_frame.pack(side=tk.LEFT, padx=30, fill=tk.X, expand=True)
        search_frame.pack_propagate(False)
        
        self.search_entry = tk.Entry(search_frame,
                                    font=('Segoe UI', 12),
                                    bg='transparent',
                                    fg=self.colors['text_primary'],
                                    relief=tk.FLAT,
                                    insertbackground=self.colors['neon_blue'])
        self.search_entry.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # Right side buttons
        btn_frame = tk.Frame(self.header, bg='transparent')
        btn_frame.pack(side=tk.RIGHT, padx=20)
        
        # Theme toggle (neon)
        self.theme_btn = tk.Label(btn_frame, text="🌙",
                                 font=('Segoe UI Emoji', 16),
                                 bg='transparent',
                                 fg=self.colors['neon_purple'],
                                 cursor='hand2')
        self.theme_btn.pack(side=tk.LEFT, padx=10)
        self.theme_btn.bind('<Button-1>', lambda e: self.toggle_theme())
        
        # New Event button (gradient)
        self.new_event_btn = GradientButton(btn_frame, "New Event",
                                           self.show_new_event_dialog,
                                           icon="➕", corner_radius=20)
        self.new_event_btn.pack(side=tk.LEFT, padx=10)
        
        # ═══════════════════════════════════════════════════════════════════
        # 🎯 MAIN CONTENT
        # ═══════════════════════════════════════════════════════════════════
        
        self.content = tk.Frame(self.root, bg='transparent')
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ═══════════════════════════════════════════════════════════════════
        # 📅 LEFT PANEL - Calendar
        # ═══════════════════════════════════════════════════════════════════
        
        self.cal_panel = GlassCard(self.content, glow_color=self.colors['neon_purple'])
        self.cal_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        self.cal_panel.pack_propagate(False)
        self.cal_panel.configure(width=420)
        
        # Calendar header
        cal_header = tk.Frame(self.cal_panel, bg='transparent')
        cal_header.pack(fill=tk.X, padx=20, pady=20)
        
        self.prev_btn = tk.Button(cal_header, text="◀",
                                 font=('Segoe UI', 12),
                                 bg=self.colors['bg_glass'],
                                 fg=self.colors['text_primary'],
                                 relief=tk.FLAT,
                                 command=self.prev_month)
        self.prev_btn.pack(side=tk.LEFT)
        
        self.month_label = FloatingLabel(cal_header, "", 18, 'bold', 'neon')
        self.month_label.pack(side=tk.LEFT, padx=15)
        
        self.next_btn = tk.Button(cal_header, text="▶",
                                 font=('Segoe UI', 12),
                                 bg=self.colors['bg_glass'],
                                 fg=self.colors['text_primary'],
                                 relief=tk.FLAT,
                                 command=self.next_month)
        self.next_btn.pack(side=tk.LEFT)
        
        today_btn = GradientButton(cal_header, "Today", self.go_to_today, icon="📅")
        today_btn.pack(side=tk.RIGHT)
        
        # Calendar grid
        cal_grid = tk.Frame(self.cal_panel, bg='transparent')
        cal_grid.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Day headers
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(days):
            FloatingLabel(cal_grid, day, 11, 'bold', 'secondary').grid(
                row=0, column=i, pady=8)
        
        self.cal_buttons = []
        
        # Calendar buttons container
        self.cal_buttons_frame = tk.Frame(cal_grid, bg='transparent')
        self.cal_buttons_frame.grid(row=1, column=0, columnspan=7, sticky='nsew')
        
        for i in range(7):
            cal_grid.columnconfigure(i, weight=1)
        
        # ═══════════════════════════════════════════════════════════════════
        # 📋 RIGHT PANEL - Events
        # ═══════════════════════════════════════════════════════════════════
        
        self.events_panel = GlassCard(self.content, glow_color=self.colors['neon_blue'])
        self.events_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Events header
        events_header = tk.Frame(self.events_panel, bg='transparent')
        events_header.pack(fill=tk.X, padx=20, pady=20)
        
        self.date_label = FloatingLabel(events_header, "", 20, 'bold', 'accent')
        self.date_label.pack(side=tk.LEFT)
        
        self.event_count = FloatingLabel(events_header, "0 events", 11, 'normal', 'secondary')
        self.event_count.pack(side=tk.RIGHT)
        
        # Add event form
        form_frame = GlassFrame(self.events_panel, opacity=0.4, corner_radius=12)
        form_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Time entry
        time_frame = tk.Frame(form_frame, bg='transparent')
        time_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        FloatingLabel(time_frame, "⏰", 14).pack(side=tk.LEFT)
        self.time_entry = NeonEntry(time_frame, placeholder="14:30")
        self.time_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Title entry
        title_frame = tk.Frame(form_frame, bg='transparent')
        title_frame.pack(fill=tk.X, padx=15, pady=5)
        
        FloatingLabel(title_frame, "📝", 14).pack(side=tk.LEFT)
        self.title_entry = NeonEntry(title_frame, placeholder="Event title...")
        self.title_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Category selector
        cat_frame = tk.Frame(form_frame, bg='transparent')
        cat_frame.pack(fill=tk.X, padx=15, pady=(5, 15))
        
        FloatingLabel(cat_frame, "🏷️", 14).pack(side=tk.LEFT)
        
        self.category_var = tk.StringVar(value='personal')
        self.category_menu = ttk.Combobox(cat_frame, textvariable=self.category_var,
                                         values=list(UltraModernColors.CATEGORIES.keys()),
                                         state='readonly',
                                         font=('Segoe UI', 10))
        self.category_menu.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Add button
        add_btn = GradientButton(form_frame, "Add Event", self.add_event, icon="➕")
        add_btn.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Events list
        list_frame = tk.Frame(self.events_panel, bg='transparent')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.events_listbox = tk.Listbox(list_frame,
                                        font=('Segoe UI', 11),
                                        bg=self.colors['bg_glass'],
                                        fg=self.colors['text_primary'],
                                        relief=tk.FLAT,
                                        bd=0,
                                        yscrollcommand=scrollbar.set,
                                        selectbackground=self.colors['accent_gradient_2'])
        self.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.events_listbox.yview)
        
        self.events_listbox.bind('<Double-Button-1>', self.delete_selected)
        
        # ═══════════════════════════════════════════════════════════════════
        # 📊 BOTTOM STATUS BAR
        # ═══════════════════════════════════════════════════════════════════
        
        self.status_bar = GlassFrame(self.root, opacity=0.6, corner_radius=0)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)
        self.status_bar.configure(height=35)
        
        self.status_label = FloatingLabel(self.status_bar, 
                                         "✨ Open-Agenda v1.3 • Auto-save enabled",
                                         10, 'normal', 'secondary')
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        self.save_status = FloatingLabel(self.status_bar, "💾 Saved", 10, 'normal', 'success')
        self.save_status.pack(side=tk.RIGHT, padx=20)
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.show_new_event_dialog())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus_set())
        self.root.bind('<Control-s>', lambda e: self.manual_save())
        self.root.bind('<Left>', lambda e: self.prev_month())
        self.root.bind('<Right>', lambda e: self.next_month())
    
    def animate(self):
        """Animate background elements"""
        self.animation_phase += 0.02
        
        # Update calendar
        self.update_calendar()
        
        # Continue animation
        self.root.after(50, self.animate)
    
    def update_calendar(self):
        """Update calendar display"""
        month_name = cal.month_name[self.current_date.month]
        self.month_label.configure(text=f"{month_name} {self.current_date.year}")
        
        # Clear old buttons
        for btn in self.cal_buttons:
            btn.destroy()
        self.cal_buttons = []
        
        calendar = cal.Calendar(firstweekday=6)
        month_days = calendar.monthdayscalendar(self.current_date.year, self.current_date.month)
        
        for week_idx, week in enumerate(month_days):
            for day_idx, day in enumerate(week):
                if day == 0:
                    btn = tk.Label(self.cal_buttons_frame, text="",
                                 bg='transparent')
                    btn.grid(row=week_idx, column=day_idx, padx=2, pady=2)
                    self.cal_buttons.append(btn)
                else:
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    
                    # Determine colors
                    if day_date == date.today():
                        bg = self.colors['accent_gradient_1']
                        fg = '#FFFFFF'
                    elif day_date == self.selected_date:
                        bg = self.colors['accent_gradient_2']
                        fg = '#FFFFFF'
                    elif day_date in self.events and self.events[day_date]:
                        bg = self.colors['accent_gradient_3']
                        fg = '#FFFFFF'
                    else:
                        bg = self.colors['bg_glass']
                        fg = self.colors['text_primary']
                    
                    btn = tk.Button(self.cal_buttons_frame, text=str(day),
                                   font=('Segoe UI', 10, 'bold'),
                                   bg=bg, fg=fg,
                                   relief=tk.FLAT,
                                   command=lambda d=day: self.select_date(d))
                    btn.grid(row=week_idx, column=day_idx, padx=2, pady=2, sticky='nsew')
                    self.cal_buttons.append(btn)
        
        # Update date label
        day_name = self.selected_date.strftime("%A, %B %d, %Y")
        self.date_label.configure(text=f"📅 {day_name}")
        
        # Update events list
        self.update_events_list()
    
    def update_events_list(self):
        """Update events listbox"""
        self.events_listbox.delete(0, tk.END)
        
        if self.selected_date in self.events and self.events[self.selected_date]:
            for event in sorted(self.events[self.selected_date], 
                               key=lambda x: x.get('time', '00:00')):
                cat = event.get('category', 'other')
                cat_info = UltraModernColors.CATEGORIES.get(cat, 
                              UltraModernColors.CATEGORIES['other'])
                
                text = f"{cat_info['icon']} {event.get('time', '00:00')} - {event['title']}"
                self.events_listbox.insert(tk.END, text)
            
            self.event_count.configure(
                text=f"{len(self.events[self.selected_date])} events"
            )
        else:
            self.events_listbox.insert(tk.END, "✨ No events for this day")
            self.events_listbox.insert(tk.END, "➕ Add your first event above!")
            self.event_count.configure(text="0 events")
    
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
        self.update_calendar()
    
    def next_month(self):
        """Next month"""
        if self.current_date.month == 12:
            self.current_date = date(self.current_date.year + 1, 1, 1)
        else:
            self.current_date = date(self.current_date.year, self.current_date.month + 1, 1)
        self.update_calendar()
    
    def go_to_today(self):
        """Go to today"""
        self.current_date = date.today()
        self.selected_date = date.today()
        self.update_calendar()
    
    def toggle_theme(self):
        """Toggle theme"""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.colors = UltraModernColors.DARK.copy()
            self.theme_btn.configure(text="🌙")
        else:
            self.colors = UltraModernColors.LIGHT.copy()
            self.theme_btn.configure(text="☀️")
        
        # Reload UI (simplified)
        self.root.configure(bg=self.colors['bg_primary'])
        self.update_calendar()
    
    def show_new_event_dialog(self):
        """Show new event dialog"""
        time_val = self.time_entry.get().strip()
        title = self.title_entry.get().strip()
        
        if not title or title == "Event title...":
            messagebox.showwarning("⚠️", "Please enter an event title!")
            return
        
        if not time_val or time_val == "14:30":
            time_val = "09:00"
        
        category = self.category_var.get() or 'personal'
        
        if self.selected_date not in self.events:
            self.events[self.selected_date] = []
        
        self.events[self.selected_date].append({
            'time': time_val,
            'title': title,
            'category': category,
            'created': datetime.now().isoformat()
        })
        
        self.events[self.selected_date].sort(key=lambda x: x.get('time', '00:00'))
        
        # Clear entries
        self.title_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        
        self.update_calendar()
        self.trigger_save()
        
        self.status_label.configure(text=f"✅ Added: {title}")
    
    def delete_selected(self, event=None):
        """Delete selected event"""
        selection = self.events_listbox.curselection()
        if not selection or not self.events.get(self.selected_date):
            return
        
        index = selection[0]
        if index < len(self.events[self.selected_date]):
            deleted = self.events[self.selected_date].pop(index)
            
            if not self.events[self.selected_date]:
                del self.events[self.selected_date]
            
            self.update_calendar()
            self.trigger_save()
            
            self.status_label.configure(text=f"🗑️ Deleted: {deleted['title']}")
    
    def on_search(self, event=None):
        """Search events"""
        query = self.search_entry.get().strip().lower()
        
        if not query:
            return
        
        results = []
        for event_date, events_list in self.events.items():
            for event in events_list:
                if query in event['title'].lower():
                    results.append((event_date, event))
        
        if results:
            msg = f"🔍 Found {len(results)} events:\n\n" + \
                  "\n".join([f"📅 {d.strftime('%Y-%m-%d')} - {e['title']}" 
                           for d, e in results[:5]])
            messagebox.showinfo("Search Results", msg)
    
    def trigger_save(self):
        """Trigger auto-save"""
        self.save_status.configure(text="⏳ Saving...", 
                                 fg=self.colors['warning'])
        self.root.after(1000, self.perform_save)
    
    def perform_save(self):
        """Save data"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = {k.isoformat(): v for k, v in self.events.items()}
                json.dump(data, f, indent=2)
            self.save_status.configure(text="💾 Saved", 
                                     fg=self.colors['success'])
        except Exception as e:
            self.save_status.configure(text="❌ Error", 
                                     fg=self.colors['danger'])
    
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
                print(f"Error loading: {e}")
    
    def on_closing(self):
        """On closing"""
        self.perform_save()
        self.root.destroy()


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    
    # Set window properties for modern look
    root.attributes('-alpha', 0.98)
    
    app = OpenAgendaV13(root)
    root.mainloop()


if __name__ == "__main__":
    main()
