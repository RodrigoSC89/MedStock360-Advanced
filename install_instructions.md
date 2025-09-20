# 🚀 Guia de Instalação SUPER SIMPLES

## Para quem NÃO é programador! 😊

---

## 📥 **MÉTODO 1: Instalação Automática (RECOMENDADO)**

### **Windows:**

1. **Baixe o Python:**
   - Vá em: https://python.org/downloads
   - Baixe a versão mais recente
   - ⚠️ **IMPORTANTE:** Marque "Add Python to PATH" durante a instalação

2. **Baixe o projeto:**
   - Vá em: https://github.com/SEU_USUARIO/medstock360
   - Clique no botão verde "Code" → "Download ZIP"
   - Extraia o ZIP em uma pasta (ex: `C:\medstock360`)

3. **Execute o instalador automático:**
   - Abra a pasta extraída
   - Clique duplo em `INSTALAR_WINDOWS.bat`
   - Aguarde a instalação (pode demorar alguns minutos)

4. **Execute o sistema:**
   - Clique duplo em `EXECUTAR_WINDOWS.bat`
   - O navegador abrirá automaticamente
   - Se não abrir, acesse: http://localhost:8501

### **Mac:**

1. **Instale o Python:**
   - Abra o Terminal (Cmd + Espaço, digite "Terminal")
   - Digite: `python3 --version`
   - Se não estiver instalado, vá em: https://python.org/downloads

2. **Baixe o projeto:**
   - Baixe o ZIP do GitHub
   - Extraia em uma pasta (ex: `~/medstock360`)

3. **Execute o instalador:**
   - Abra o Terminal
   - Navegue até a pasta: `cd ~/medstock360`
   - Execute: `chmod +x instalar_mac.sh && ./instalar_mac.sh`

4. **Execute o sistema:**
   - Execute: `./executar_mac.sh`

---

## 📥 **MÉTODO 2: Instalação Manual**

### **Se o método automático não funcionar:**

1. **Abra o Terminal/Prompt:**
   - **Windows:** Win + R, digite `cmd`
   - **Mac/Linux:** Abra o Terminal

2. **Navegue até a pasta do projeto:**
   ```bash
   cd caminho/para/medstock360
   ```

3. **Instale as dependências:**
   ```bash
   pip install streamlit pandas plotly sqlite3
   ```

4. **Execute o sistema:**
   ```bash
   streamlit run app.py
   ```

---

## 🔑 **Primeiro Acesso**

Após executar, acesse no navegador:
- **URL:** http://localhost:8501
- **Usuário:** `admin`
- **Senha:** `admin123`

---

## 🆘 **Problemas Comuns**

### ❌ **Erro: 'python' não é reconhecido**
**Solução:** Reinstale o Python marcando "Add to PATH"

### ❌ **Erro: 'pip' não é reconhecido**
**Solução:** 
```bash
python -m pip install streamlit pandas plotly
```

### ❌ **Erro: Permission denied (Mac/Linux)**
**Solução:**
```bash
sudo pip install streamlit pandas plotly
```

### ❌ **Sistema não abre no navegador**
**Solução:** Acesse manualmente: http://localhost:8501

### ❌ **Porta ocupada**
**Solução:** 
```bash
streamlit run app.py --server.port 8502
```
Depois acesse: http://localhost:8502

---

## 📞 **Precisa de Ajuda?**

1. **Verifique se seguiu todos os passos**
2. **Reinicie o computador** (resolve 90% dos problemas)
3. **Abra uma issue no GitHub** com prints do erro

---

## ✅ **Teste se Funcionou**

Após instalar, você deve ver:
- ✅ Página de login do MedStock360
- ✅ Consegue fazer login com admin/admin123
- ✅ Dashboard aparece com gráficos
- ✅ Todos os menus funcionam

---

## 🎯 **Próximos Passos**

1. **Mude a senha padrão**
2. **Cadastre usuários**
3. **Cadastre medicamentos**
4. **Configure o sistema**

---

**🎉 Pronto! Seu sistema hospitalar está funcionando!**