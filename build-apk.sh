#!/bin/bash
# OpenAgenda v1.4.1 - Build APK (Flutter)
# Execute este script onde tem Flutter e Android SDK

echo "📱 OpenAgenda v1.4.1 - Build APK"
echo "=============================="

# Verifica Flutter
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter não encontrado. Instale em: https://flutter.dev"
    exit 1
fi

# Verifica Android SDK
if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
    echo "⚠️ ANDROID_HOME não configurado. Configure o Android SDK."
    exit 1
fi

cd /workspace/project/OpenAgenda/open_agenda_flutter

# Atualiza versão
sed -i 's/version: 1.4.0/version: 1.4.1/' pubspec.yaml

# Build APK
echo "🔨 Compilando APK..."
flutter build apk --debug

if [ $? -eq 0 ]; then
    echo "✅ APK criado em: build/app/outputs/flutter-apk/app-debug.apk"
else
    echo "❌ Erro na compilação"
    exit 1
fi