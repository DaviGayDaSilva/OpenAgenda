#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open-Agenda - A Smart Local Calendar & Task Manager
The best agenda in the world - Open Source, intelligent and easy to use!

Author: Open-Agenda Team
License: MIT
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, date
import calendar
from pathlib import Path

# Application configuration
APP_NAME = "Open-Agenda"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Open-Agenda Team"
DEFAULT_DATA_FILE = "open_agenda_data.json"

# Colors - Modern dark theme
COLORS = {
    'primary': '#6C5CE7',
    'secondary': '#A29BFE',
    'accent': '#00CEC9',
    'background': '#2D3436',
    'surface': '#353B48',
    'surface_light': '#3D4452',
    'text': '#DFE6E9',
    'text_secondary': '#B2BEC3',
    'success': '#00B894',
    'warning': '#FDCB6E',
    'danger': '#E17055',
    'today': '#74B9FF'
}

class OpenAgenda:
    """Main application class for Open-Agenda"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION} - The Best Agenda in the World!")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['background'])
        
        # Data storage
        self.events = {}  # {date: [events]}
        self.data_file = DEFAULT_DATA_FILE
        self.current_date = date.today()
        self.selected_date = date.today()
        
        # Setup UI
        self.setup_styles()
        self.create_ui()
        self.load_data()
        self.update_calendar()
        self.update_event_list()
        
        # Auto-save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       font=('Helvetica', 24, 'bold'),
                       foreground=COLORS['text'],
                       background=COLORS['background'])
        
        style.configure('Header.TLabel',
                       font=('Helvetica', 14, 'bold'),
                       foreground=COLORS['text'],
                       background=COLORS['background'])
        
        style.configure('Surface.TFrame',
                       background=COLORS['surface'])
    
    def create_ui(self):
        """Create the main user interface"""
        main_frame = ttk.Frame(self.root, style='Surface.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text=f"🌟 {APP_NAME} 🌟",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle = ttk.Label(main_frame,
                            text="A Smart Local Calendar & Task Manager - Open Source",
                            font=('Helvetica', 12),
                            foreground=COLORS['text_secondary'],
                            background=COLORS['background'])
        subtitle.pack(pady=(0, 20))
        
        # Content area
        content_frame = ttk.Frame(main_frame, style='Surface.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Calendar frame
        calendar_frame = ttk.Frame(content_frame, style='Surface.TFrame')
        calendar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Month/Year navigation
        nav_frame = ttk.Frame(calendar_frame, style='Surface.TFrame')
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.prev_btn = tk.Button(nav_frame, text="◀",
                                  font=('Helvetica', 14),
                                  bg=COLORS['surface'],
                                  fg=COLORS['text'],
                                  command=self.prev_month,
                                  relief=tk.FLAT,
                                  width=3)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.month_year_label = tk.Label(nav_frame,
                                         font=('Helvetica', 16, 'bold'),
                                         bg=COLORS['background'],
                                         fg=COLORS['text'],
                                         width=20)
        self.month_year_label.pack(side=tk.LEFT, expand=True)
        
        self.next_btn = tk.Button(nav_frame, text="▶",
                                  font=('Helvetica', 14),
                                  bg=COLORS['surface'],
                                  fg=COLORS['text'],
                                  command=self.next_month,
                                  relief=tk.FLAT,
                                  width=3)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Calendar grid
        self.calendar_frame = tk.Frame(calendar_frame, bg=COLORS['surface'])
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Day headers
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(days):
            label = tk.Label(self.calendar_frame, text=day,
                           font=('Helvetica', 10, 'bold'),
                           bg=COLORS['primary'],
                           fg='white',
                           width=4,
                           height=2)
            label.grid(row=0, column=i, padx=1, pady=1, sticky='nsew')
        
        self.calendar_buttons = []
        
        # Events frame
        events_frame = ttk.Frame(content_frame, style='Surface.TFrame')
        events_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.selected_date_label = tk.Label(events_frame,
                                           font=('Helvetica', 14, 'bold'),
                                           bg=COLORS['background'],
                                           fg=COLORS['accent'])
        self.selected_date_label.pack(pady=(0, 10), anchor=tk.W)
        
        # Event input area
        input_frame = tk.Frame(events_frame, bg=COLORS['surface'])
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(input_frame, text="Time:",
                bg=COLORS['surface'],
                fg=COLORS['text'],
                font=('Helvetica', 10)).pack(side=tk.LEFT, padx=5)
        
        self.time_entry = tk.Entry(input_frame, width=10,
                                   font=('Helvetica', 10),
                                   bg=COLORS['surface_light'],
                                   fg=COLORS['text'],
                                   relief=tk.FLAT)
        self.time_entry.pack(side=tk.LEFT, padx=5)
        self.time_entry.insert(0, "09:00")
        
        tk.Label(input_frame, text="Event:",
                bg=COLORS['surface'],
                fg=COLORS['text'],
                font=('Helvetica', 10)).pack(side=tk.LEFT, padx=5)
        
        self.event_entry = tk.Entry(input_frame, width=25,
                                    font=('Helvetica', 10),
                                    bg=COLORS['surface_light'],
                                    fg=COLORS['text'],
                                    relief=tk.FLAT)
        self.event_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.event_entry.bind('<Return>', lambda e: self.add_event())
        
        add_btn = tk.Button(input_frame, text="+ Add Event",
                           font=('Helvetica', 10, 'bold'),
                           bg=COLORS['success'],
                           fg='white',
                           command=self.add_event,
                           relief=tk.FLAT,
                           padx=10)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Events list
        list_frame = tk.Frame(events_frame, bg=COLORS['surface'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.events_listbox = tk.Listbox(list_frame,
                                        font=('Helvetica', 11),
                                        bg=COLORS['surface_light'],
                                        fg=COLORS['text'],
                                        relief=tk.FLAT,
                                        yscrollcommand=scrollbar.set)
        self.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.events_listbox.yview)
        
        self.events_listbox.bind('<Double-Button-1>', self.delete_selected_event)
        
        # Action buttons
        actions_frame = ttk.Frame(events_frame, style='Surface.TFrame')
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        load_btn = tk.Button(actions_frame,
                            text="📂 Load File",
                            font=('Helvetica', 10),
                            bg=COLORS['warning'],
                            fg=COLORS['background'],
                            command=self.load_from_file,
                            relief=tk.FLAT,
                            padx=10)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(actions_frame,
                            text="💾 Save File",
                            font=('Helvetica', 10),
                            bg=COLORS['primary'],
                            fg='white',
                            command=self.save_to_file,
                            relief=tk.FLAT,
                            padx=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame,
                              text="🗑️ Delete Selected",
                              font=('Helvetica', 10),
                              bg=COLORS['danger'],
                              fg='white',
                              command=self.delete_selected_event,
                              relief=tk.FLAT,
                              padx=10)
        delete_btn.pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_label = tk.Label(main_frame,
                                    text=f"Ready - {APP_NAME} v{APP_VERSION}",
                                    font=('Helvetica', 9),
                                    bg=COLORS['surface'],
                                    fg=COLORS['text_secondary'])
        self.status_label.pack(fill=tk.X, pady=(10, 0))
    
    def update_calendar(self):
        """Update the calendar display"""
        for btn in self.calendar_buttons:
            btn.destroy()
        self.calendar_buttons = []
        
        month_name = calendar.month_name[self.current_date.month]
        self.month_year_label.config(text=f"{month_name} {self.current_date.year}")
        
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(self.current_date.year, self.current_date.month)
        
        for week_idx, week in enumerate(month_days):
            for day_idx, day in enumerate(week):
                if day == 0:
                    label = tk.Label(self.calendar_frame, text="",
                                    bg=COLORS['surface'], width=4, height=2)
                    label.grid(row=week_idx + 1, column=day_idx, padx=1, pady=1)
                    self.calendar_buttons.append(label)
                else:
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    
                    if day_date == date.today():
                        bg_color = COLORS['today']
                        fg_color = 'white'
                    elif day_date in self.events and self.events[day_date]:
                        bg_color = COLORS['primary']
                        fg_color = 'white'
                    else:
                        bg_color = COLORS['surface_light']
                        fg_color = COLORS['text']
                    
                    btn = tk.Button(self.calendar_frame, text=str(day),
                                   font=('Helvetica', 10), bg=bg_color, fg=fg_color,
                                   relief=tk.FLAT,
                                   command=lambda d=day: self.select_date(d))
                    btn.grid(row=week_idx + 1, column=day_idx, padx=1, pady=1, sticky='nsew')
                    self.calendar_buttons.append(btn)
        
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(len(month_days) + 1):
            self.calendar_frame.rowconfigure(i, weight=1)
    
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
    
    def update_event_list(self):
        """Update the events listbox"""
        self.events_listbox.delete(0, tk.END)
        
        day_name = self.selected_date.strftime("%A")
        self.selected_date_label.config(
            text=f"📅 {day_name}, {self.selected_date.strftime('%B %d, %Y')}"
        )
        
        if self.selected_date in self.events:
            for event in self.events[self.selected_date]:
                display_text = f"⏰ {event['time']} - {event['title']}"
                self.events_listbox.insert(tk.END, display_text)
        
        if self.events_listbox.size() == 0:
            self.events_listbox.insert(tk.END, "No events for this day.")
            self.events_listbox.insert(tk.END, "Add an event above! 🎉")
    
    def add_event(self):
        """Add a new event"""
        time_val = self.time_entry.get().strip()
        title = self.event_entry.get().strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter an event title!")
            return
        
        if not time_val:
            time_val = "00:00"
        
        try:
            datetime.strptime(time_val, "%H:%M")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid time format! Use HH:MM (e.g., 09:00)")
            return
        
        if self.selected_date not in self.events:
            self.events[self.selected_date] = []
        
        self.events[self.selected_date].append({
            'time': time_val,
            'title': title,
            'created': datetime.now().isoformat()
        })
        
        self.events[self.selected_date].sort(key=lambda x: x['time'])
        
        self.event_entry.delete(0, tk.END)
        
        self.update_event_list()
        self.update_calendar()
        self.save_data()
        
        self.status_label.config(text=f"Event added: {title}")
    
    def delete_selected_event(self, event=None):
        """Delete the selected event"""
        selection = self.events_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        if self.selected_date not in self.events or not self.events[self.selected_date]:
            return
        
        if index < len(self.events[self.selected_date]):
            deleted_event = self.events[self.selected_date][index]['title']
            del self.events[self.selected_date][index]
            
            if not self.events[self.selected_date]:
                del self.events[self.selected_date]
            
            self.update_event_list()
            self.update_calendar()
            self.save_data()
            
            self.status_label.config(text=f"Event deleted: {deleted_event}")
    
    def load_data(self):
        """Load data from default file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = {date.fromisoformat(k): v for k, v in data.items()}
                self.status_label.config(text="Data loaded successfully!")
            except Exception as e:
                self.status_label.config(text=f"Error loading data: {e}")
    
    def save_data(self):
        """Save data to default file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = {k.isoformat(): v for k, v in self.events.items()}
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.status_label.config(text="Data saved automatically!")
        except Exception as e:
            self.status_label.config(text=f"Error saving data: {e}")
    
    def load_from_file(self):
        """Load data from a user-selected file"""
        filename = filedialog.askopenfilename(
            title="Load Agenda Data",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = {date.fromisoformat(k): v for k, v in data.items()}
                
                self.update_event_list()
                self.update_calendar()
                
                messagebox.showinfo("Success", f"Data loaded from:\n{filename}")
                self.status_label.config(text=f"Data loaded from file!")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file:\n{e}")
    
    def save_to_file(self):
        """Save data to a user-selected file"""
        filename = filedialog.asksaveasfilename(
            title="Save Agenda Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="my_agenda.json"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    data = {k.isoformat(): v for k, v in self.events.items()}
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Data saved to:\n{filename}")
                self.status_label.config(text=f"Data saved to file!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file:\n{e}")
    
    def on_closing(self):
        """Handle window closing"""
        self.save_data()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = OpenAgenda(root)
    root.mainloop()


if __name__ == "__main__":
    main()
