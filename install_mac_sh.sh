#!/bin/bash

echo ""
echo "===================================="
echo "   MEDSTOCK360 - INSTALAÇÃO AUTOMÁTICA"
echo "===================================="
echo ""
echo "Instalando o sistema hospitalar..."
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo ""
    echo "Para instalar Python:"
    echo "Mac: brew install python3"
    echo "Ubuntu: sudo apt install python3 python3-pip"
    echo "CentOS: sudo yum install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[OK] Python3 encontrado!"
echo ""

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "Instalando pip..."
    python3 -m ensurepip --upgrade
fi

# Atualizar pip
echo "Atualizando pip..."
python3 -m pip install --upgrade pip

# Instalar dependências
echo ""
echo "Instalando dependências do sistema..."
echo ""

pip3 install streamlit
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao instalar Streamlit"
    exit 1
fi

pip3 install pandas
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao instalar Pandas"
    exit 1
fi

pip3 install plotly
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao instalar Plotly"
    exit 1
fi

pip3 install python-dateutil pytz

# Criar diretórios necessários
echo ""
echo "Criando estrutura de diretórios..."
mkdir -p data logs backups

# Tornar executável o script de execução
chmod +x executar_mac.sh

echo ""
echo "===================================="
echo "   INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "===================================="
echo ""
echo "Para executar o sistema:"
echo "./executar_mac.sh"
echo ""
echo "Ou execute manualmente:"
echo "streamlit run app.py"
echo ""
echo "Primeiro acesso:"
echo "Usuário: admin"
echo "Senha: admin123"
echo ""