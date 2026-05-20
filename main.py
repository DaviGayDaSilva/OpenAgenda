#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAgenda v1.4.1 - Kivy Version
Compatible with Android APK build
Novidades: Painel de Notícias + Assistente Virtual
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

# GNews API Key (free tier)
GNEWS_API_KEY = "f33486a8579758c2746e042a1632b4ea"

class GlassButton(Button):
    pass

class GlassCard(BoxLayout):
    pass

class HomeScreen(Screen):
    def on_enter(self):
        self.update_weather()
        self.update_events()
        self.update_news()
    
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
    
    def update_news(self):
        """Atualiza o painel de notícias com API externa (GNews)."""
        container = self.ids.news_container
        container.clear_widgets()
        
        # Cabeçalho do painel de notícias
        header = Label(
            text='📰 Últimas Noticias',
            color=COLORS['text_light'],
            font_size=16,
            size_hint_y=None,
            height=30
        )
        container.add_widget(header)
        
        # Busca notícias da API GNews
        try:
            r = requests.get(
                f"https://gnews.io/api/v4/top-headlines?country=br&lang=pt&max=3",
                headers={"Authorization": f"Bearer {GNEWS_API_KEY}"},
                timeout=8
            )
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                
                for article in articles:
                    news_card = BoxLayout(
                        orientation='vertical',
                        size_hint_y=None,
                        padding=10,
                        spacing=5
                    )
                    with news_card.canvas.before:
                        Color(*COLORS['glass'])
                        RoundedRectangle(size=news_card.size, pos=news_card.pos, radius=[10])
                    
                    title_label = Label(
                        text=article.get('title', 'Sem titulo')[:40] + '...' if len(article.get('title', '')) > 40 else article.get('title', 'Sem titulo'),
                        color=COLORS['text_light'],
                        font_size=13
                    )
                    
                    desc_label = Label(
                        text=article.get('description', '')[:60] + ('...' if len(article.get('description', ''))) > 60 else article.get('description', ''),
                        color=COLORS['text_light'],
                        font_size=11,
                        opacity=0.7
                    )
                    
                    source_label = Label(
                        text=f"📰 {article.get('source', {}).get('name', '')}",
                        color=COLORS['secondary'],
                        font_size=10,
                        size_hint_y=None,
                        height=15
                    )
                    
                    news_card.add_widget(title_label)
                    news_card.add_widget(desc_label)
                    news_card.add_widget(source_label)
                    container.add_widget(news_card)
            else:
                raise Exception("API error")
        except:
            # Fallback: mostra eventos locais se API falhar
            self._show_local_events(container)
    
    def _show_local_events(self, container):
        """Mostra eventos locais como fallback."""
        events = store.get('events') if store.exists('events') else {'list': []}
        
        if not events['list']:
            no_events = Label(
                text='Nenhum evento.\nConfigure a API GNews!',
                color=COLORS['text_light'],
                font_size=14
            )
            container.add_widget(no_events)
            return
        
        for e in events['list'][:3]:
            news_card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                padding=10,
                spacing=5
            )
            with news_card.canvas.before:
                Color(*COLORS['glass'])
                RoundedRectangle(size=news_card.size, pos=news_card.pos, radius=[10])
            
            title_label = Label(
                text=f"📅 {e.get('title', 'Sem titulo')}",
                color=COLORS['text_light'],
                font_size=13
            )
            
            date_label = Label(
                text=e.get('date', '--/--/----'),
                color=COLORS['secondary'],
                font_size=11
            )
            
            news_card.add_widget(title_label)
            news_card.add_widget(date_label)
            container.add_widget(news_card)

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

# Base de conhecimento do assistente virtual
ASSISTANT_KNOWLEDGE = {
    'evento': 'Para criar um evento, vá para "Adicionar Evento" e preencha os campos: título, data, hora e descrição.',
    'adicionar': 'Para adicionar um evento, vá para a tela "Adicionar Evento" e preencha os campos necessários.',
    'criar': 'Para criar um evento, use a função "Adicionar Evento" no menu principal.',
    'calendário': 'Você pode ver todos os seus eventos na aba "Ver Eventos". Lá aparecem todos os eventos salvos.',
    'lista': 'A lista de eventos mostra todos os eventos que você cadastrou. Clique em "Ver Eventos" para acessar.',
    'excluir': 'No momento, para excluir eventos você precisa acceder aos dados diretamente.',
    'tema': 'Em Configurações você pode escolher entre tema Dark ou Light.',
    'tema escuro': 'Em Configurações você pode escolher entre tema Dark ou Light.',
    'tema claro': 'Em Configurações você pode escolher entre tema Dark ou Light.',
    ' clima': 'O aplicativo mostra o clima atual de São Paulo na tela inicial.',
    'tempo': 'O aplicativo mostra o clima atual de São Paulo na tela inicial.',
    'chuva': 'O aplicativo mostra o clima atual de São Paulo na tela inicial.',
    'quente': 'O aplicativo mostra a temperatura atual de São Paulo.',
    'frio': 'O aplicativo mostra a temperatura atual de São Paulo.',
    'data': 'Para adicionar um evento, informe a data no formato DD/MM/AAAA.',
    'hora': 'Para adicionar um evento, informe a hora no formato HH:MM.',
    'ajuda': 'Sou o assistente virtual do OpenAgenda! Posso responder dúvidas sobre como usar o aplicativo.',
    'oi': 'Olá! Sou o assistente虚拟 do OpenAgenda! Como posso ajudar você hoje?',
    'olá': 'Olá! Sou o assistente virtual do OpenAgenda! Como posso ajudar você hoje?',
    'qual seu nome': 'Eu sou o Assistente OpenAgenda! Estou aqui para ajudar você a usar o aplicativo.',
    'nome': 'Eu sou o Assistente OpenAgenda! Estou aqui para ajudar você a usar o aplicativo.',
    'funcionalidade': 'O OpenAgenda permite 관리ar seus eventos pessoais, verificar o clima e muito mais!',
    'o que consegue': 'Posso ajudar com: criar eventos, ver calendário, configurar temas e informações do clima.',
    'oque faz': 'O OpenAgenda permite gerenciar seus eventos pessoais, verificar o clima e muito mais!',
    'para que serve': 'O OpenAgenda sirve para gerenciar seus eventos e compromissos de forma simples.',
    'sobre': 'OpenAgenda v1.4.1 - Seu assistente pessoal para gerenciamento de eventos e compromissos.',
    'versão': 'OpenAgenda versão 1.4.1 - Novidades: Painel de Notícias e Assistente Virtual.',
    'versao': 'OpenAgenda versão 1.4.1 - Novidades: Painel de Notícias e Assistente Virtual.',
}

def get_assistant_response(message):
    """Responde mensagens do usuário usando a base de conhecimento."""
    message = message.lower()
    
    # Procura palavras-chave na mensagem
    for key, response in ASSISTANT_KNOWLEDGE.items():
        if key in message:
            return response
    
    # Resposta padrão
    return 'Desculpe, não entendi. Tente perguntar de outra forma ou peça ajuda!'

class AssistantScreen(Screen):
    def on_enter(self):
        self.load_chat_history()
    
    def load_chat_history(self):
        """Carrega histórico de chat salvo."""
        history = store.get('chat_history') if store.exists('chat_history') else {'messages': []}
        container = self.ids.chat_container
        container.clear_widgets()
        
        # Mensagem de boas-vindas
        welcome = BoxLayout(orientation='vertical', size_hint_y=None, padding=10)
        welcome.add_widget(Label(
            text='🤖 Olá! Sou o Assistente OpenAgenda!\nPosso tirar dúvidas sobre o app.\nComo posso ajudar?', 
            color=COLORS['text_light'],
            font_size=14
        ))
        container.add_widget(welcome)
        
        for msg in history['messages']:
            self.add_message(msg['text'], msg['is_user'])
    
    def send_message(self):
        """Envia mensagem do usuário e obtém resposta."""
        user_input = self.ids.user_input
        
        if not user_input.text.strip():
            return
        
        # Adiciona mensagem do usuário
        self.add_message(user_input.text, is_user=True)
        
        # Obtém resposta do assistente
        response = get_assistant_response(user_input.text)
        self.add_message(response, is_user=False)
        
        # Salva no histórico
        history = store.get('chat_history') if store.exists('chat_history') else {'messages': []}
        history['messages'].append({'text': user_input.text, 'is_user': True})
        history['messages'].append({'text': response, 'is_user': False})
        
        # Limita histórico a 20 mensagens
        if len(history['messages']) > 20:
            history['messages'] = history['messages'][-20:]
        
        store.put('chat_history', history)
        
        # Limpa input
        user_input.text = ""
    
    def add_message(self, text, is_user):
        """Adiciona mensagem ao chat."""
        container = self.ids.chat_container
        
        msg_box = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            padding=10,
            spacing=5
        )
        
        with msg_box.canvas.before:
            Color(*COLORS['glass'])
            RoundedRectangle(size=msg_box.size, pos=msg_box.pos, radius=[10])
        
        # Nome do remetente
        sender = "Você" if is_user else "🤖 Assistente"
        label = Label(
            text=sender,
            color=COLORS['secondary'] if is_user else COLORS['accent'],
            font_size=12,
            size_hint_y=None,
            height=20
        )
        msg_box.add_widget(label)
        
        # Texto da mensagem
        msg_label = Label(
            text=text,
            color=COLORS['text_light'],
            font_size=14,
            text_size=(container.width - 40, None)
        )
        msg_box.add_widget(msg_label)
        
        container.add_widget(msg_box)

class OpenAgendaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddEventScreen(name='add'))
        sm.add_widget(EventListScreen(name='list'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(AssistantScreen(name='assistant'))
        return sm

if __name__ == '__main__':
    Window.clearcolor = COLORS['bg_dark']
    OpenAgendaApp().run()
