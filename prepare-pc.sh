#!/bin/bash
# OpenAgenda v1.4 - PC Compile Helper
# Execute este script para preparar arquivos para compilação no PC

echo "📦 Preparando arquivos para compilação no PC..."

# Criar diretório
mkdir -p open-agenda-pc

# Copiar arquivos necessários
cp open-agenda-v1.4.py open-agenda-pc/
cp buildozer.spec open-agenda-pc/
cp install-android.sh open-agenda-pc/
cp requirements-android.txt open-agenda-pc/
cp open-agenda-icon.png open-agenda-pc/

# Compactar
tar -czvf OpenAgenda-1.4.0-pc.tar.gz open-agenda-pc/

echo ""
echo "✅ Arquivo criado: OpenAgenda-1.4.0-pc.tar.gz"
echo ""
echo "📋 Instruções para compilação no PC:"
echo "======================================"
echo ""
echo "1. Extraia o arquivo no seu PC:"
echo "   tar -xzf OpenAgenda-1.4.0-pc.tar.gz"
echo ""
echo "2. Instale as dependências (Linux/Ubuntu):"
echo "   sudo apt update"
echo "   sudo apt install python3 python3-pip openjdk-17-jdk"
echo "   pip3 install buildozer cython"
echo ""
echo "3. Configure o Android SDK:"
echo "   - Baixe Android Studio"
echo "   - Instale SDK, NDK (versão 21 ou 22)"
echo "   - Defina variáveis de ambiente:"
echo "     export ANDROID_HOME=~/Android/Sdk"
echo "     export ANDROID_NDK_HOME=~/Android/Sdk/ndk/21.x.x"
echo ""
echo "4. Compile:"
echo "   cd open-agenda-pc"
echo "   buildozer android"
echo ""
echo "5. APK será gerada em:"
echo "   bin/openagenda-1.4.0-arm64-v8a-release-0.1.apk"
echo ""
