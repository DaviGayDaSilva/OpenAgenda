# 📱 OpenAgenda v1.4.1 - Guia de Compilação

## Novidades v1.4.1
- 📰 Painel de Notícias via GNews API
- 🤖 Assistente Virtual (chat local)

---

## Opção 1: Compilar APK (Android)

### Requisitos:
- Flutter SDK: https://flutter.dev
- Android SDK: https://developer.android.com/studio

### Comandos:
```bash
# Clone e prepare
cd open_agenda_flutter

# Atualize API Keys em lib/main.dart:
# - GNEWS_API_KEY = "sua-chave-em-gnews.io"

# Compile
flutter build apk --debug

# APK estará em: build/app/outputs/flutter-apk/app-debug.apk
```

---

## Opção 2: Compilar AppImage (Linux)

### Requisitos:
- Flutter SDK
- appimagetool

### Comandos:
```bash
cd open_agenda_flutter
flutter config --enable-linux-desktop
flutter build linux --release

# Use appimagetool para criar AppImage
# https://github.com/AppImage/AppImageKit
```

---

## Notas Importantes

### GNews API:
1. Cadastre-se em https://gnews.io
2. Obtenha sua API key gratuita
3. Edite o arquivo lib/main.dart:
```dart
const String GNEWS_API_KEY = "SUA-CHAVE-AQUI";
```

### Kivy (PC/Linux):
Já está compilado! Arquivos em:
- OpenAgenda-1.4.1.py
- open-agenda_1.4.1_all.deb
- OpenAgenda-1.4.1-pc.tar.gz