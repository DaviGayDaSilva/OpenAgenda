#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAgenda v1.4 - Kivy Version
Compatible with Android APK build
"""

import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.storage.jsonstore import JsonStore
import requests
import threading
import datetime

# Store para dados locais
store = JsonStore('openagenda.json')

# Cores (Glassmorphism)
COLORS = {
    'bg_dark': [0.05, 0.05, 0.1, 1],
    'bg_light': [0.95, 0.95, 0.97, 1],
    'primary': [0.3, 0.5, 0.9, 1],
    'secondary': [0.2, 0.8, 0.7, 1],
    'accent': [1.0, 0.5, 0.3, 1],
    'glass': [1, 1, 1, 0.15],
    'text_light': [1, 1, 1, 1],
    'text_dark': [0.1, 0.1, 0.15, 1],
}

API_KEY = "cc4577b215b574d3700c5be607a104c1"

class GlassButton(Button):
    pass

class GlassCard(BoxLayout):
    pass

class HomeScreen(Screen):
    def on_enter(self):
        self.update_weather()
        self.update_events()
    
    def update_weather(self):
        try:
            r = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q=SaoPaulo&appid={API_KEY}&units=metric",
                timeout=5
            )
            if r.status_code == 200:
                data = r.json()
                temp = int(data['main']['temp'])
                desc = data['weather'][0]['description'].title()
                self.ids.weather_label.text = f"🌤️ {temp}°C - {desc}"
        except:
            self.ids.weather_label.text = "🌤️ --°C"
    
    def update_events(self):
        events = store.get('events') if store.exists('events') else {'list': []}
        self.ids.event_count.text = f"📅 {len(events['list'])} eventos"

class AddEventScreen(Screen):
    def save_event(self):
        title = self.ids.title_input.text
        date = self.ids.date_input.text
        time = self.ids.time_input.text
        desc = self.ids.desc_input.text
        
        if not title or not date:
            return
        
        events = store.get('events') if store.exists('events') else {'list': []}
        events['list'].append({
            'title': title,
            'date': date,
            'time': time,
            'desc': desc
        })
        store.put('events', events)
        
        self.ids.title_input.text = ""
        self.ids.date_input.text = ""
        self.ids.time_input.text = ""
        self.ids.desc_input.text = ""
        
        self.manager.current = 'home'

class EventListScreen(Screen):
    def on_enter(self):
        self.load_events()
    
    def load_events(self):
        events = store.get('events') if store.exists('events') else {'list': []}
        container = self.ids.events_container
        container.clear_widgets()
        
        for e in events['list']:
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=10)
            with card.canvas.before:
                Color(*COLORS['glass'])
                RoundedRectangle(size=card.size, pos=card.pos, radius=[10])
            card.add_widget(Label(text=f"📅 {e['date']}\n{e['title']}", color=COLORS['text_light']))
            container.add_widget(card)

class SettingsScreen(Screen):
    def on_enter(self):
        theme = store.get('theme') if store.exists('theme') else {'mode': 'dark'}
        self.ids.theme_spinner.text = theme['mode'].title()

class OpenAgendaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddEventScreen(name='add'))
        sm.add_widget(EventListScreen(name='list'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    Window.clearcolor = COLORS['bg_dark']
    OpenAgendaApp().run()
