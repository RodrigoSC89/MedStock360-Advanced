#!/bin/bash

echo ""
echo "===================================="
echo "      MEDSTOCK360 - INICIANDO..."
echo "===================================="
echo ""
echo "Verificando sistema..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo "Execute primeiro: ./instalar_mac.sh"
    exit 1
fi

# Verificar se Streamlit está instalado
if ! pip3 show streamlit &> /dev/null; then
    echo "[ERRO] Streamlit não instalado!"
    echo "Execute primeiro: ./instalar_mac.sh"
    exit 1
fi

# Verificar se app.py existe
if [ ! -f "app.py" ]; then
    echo "[ERRO] Arquivo app.py não encontrado!"
    echo "Certifique-se de estar na pasta correta do projeto."
    exit 1
fi

echo "[OK] Sistema verificado com sucesso!"
echo ""
echo "Iniciando MedStock360..."
echo ""
echo "===================================="
echo "  ACESSE NO NAVEGADOR:"
echo "  http://localhost:8501"
echo ""
echo "  PRIMEIRO ACESSO:"
echo "  Usuário: admin"
echo "  Senha: admin123"
echo "===================================="
echo ""
echo "Para parar o sistema, pressione Ctrl+C"
echo ""

# Executar Streamlit
streamlit run app.py --server.port 8501 --server.address localhost

echo ""
echo "Sistema finalizado."