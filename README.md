[readme_medstock.md](https://github.com/user-attachments/files/22436823/readme_medstock.md)
# 🏥 MedStock360 Advanced

## Sistema Hospitalar Completo Multi-usuário

### 📋 Descrição

O **MedStock360** é um sistema completo de gestão hospitalar que oferece controle de medicamentos, estoque, pacientes, consultas e receitas médicas. Desenvolvido para ser simples de usar, mas poderoso em funcionalidades.

---

## ✨ Funcionalidades Principais

### 🔐 **Sistema de Usuários**
- ✅ Login seguro com diferentes perfis
- ✅ Perfis: Administrador, Médico, Farmacêutico, Enfermeiro
- ✅ Permissões específicas por perfil
- ✅ Multi-usuário simultâneo

### 💊 **Gestão de Medicamentos**
- ✅ Cadastro completo de medicamentos
- ✅ Controle de princípio ativo, fabricante, categoria
- ✅ Informações de apresentação (comprimido, xarope, etc.)
- ✅ Via de administração (oral, intramuscular, etc.)
- ✅ Medicamentos controlados
- ✅ Registro ANVISA

### 📦 **Controle de Estoque Inteligente**
- ✅ Gestão por lotes com validade
- ✅ Controle de localização física
- ✅ Alertas automáticos de estoque baixo
- ✅ Alertas de medicamentos próximos ao vencimento
- ✅ **🔮 Análise Preditiva de Consumo**
- ✅ Histórico completo de movimentações

### 🔮 **Análise Preditiva (NOVO!)**
- ✅ Previsão de quando medicamentos vão acabar
- ✅ Cálculo baseado no consumo histórico
- ✅ Sugestões automáticas de reposição
- ✅ Alertas inteligentes por prioridade
- ✅ Gráficos de consumo em tempo real

### 👥 **Gestão de Pacientes**
- ✅ Cadastro completo de pacientes
- ✅ Histórico médico
- ✅ Informações de convênio
- ✅ Contatos de emergência

### 📅 **Agendamento de Consultas**
- ✅ Agenda por médico
- ✅ Controle de status das consultas
- ✅ Histórico de consultas
- ✅ Integração com receitas

### 📝 **Receitas Médicas Digitais**
- ✅ Prescrição eletrônica
- ✅ Controle de medicamentos prescritos
- ✅ Dosagem e instruções de uso
- ✅ Histórico de receitas por paciente

### 📊 **Relatórios e Dashboard**
- ✅ Dashboard executivo com gráficos
- ✅ Relatórios de medicamentos
- ✅ Relatórios de estoque
- ✅ Relatórios de pacientes e consultas
- ✅ Exportação de dados

---

## 🚀 Como Instalar e Usar

### 📋 **Pré-requisitos**
- Python 3.8 ou superior
- Computador com Windows, Mac ou Linux

### 💻 **Instalação Simples**

1. **Baixe o projeto:**
   ```bash
   git clone https://github.com/SEU_USUARIO/medstock360.git
   cd medstock360
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o sistema:**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador:**
   - Abra: `http://localhost:8501`

### 🔑 **Primeiro Acesso**
- **Usuário:** `admin`
- **Senha:** `admin123`

**⚠️ IMPORTANTE:** Mude a senha padrão após o primeiro login!

---

## 👥 **Perfis de Usuário**

### 👑 **Administrador**
- Acesso total ao sistema
- Gerencia usuários
- Relatórios completos
- Configurações do sistema

### 👨‍⚕️ **Médico**
- Gestão de pacientes
- Agendamento de consultas
- Prescrição de receitas
- Consulta de medicamentos

### 💊 **Farmacêutico**
- Gestão de medicamentos
- Controle de estoque
- Dispensação de medicamentos
- Relatórios farmacêuticos

### 👩‍⚕️ **Enfermeiro**
- Consulta de pacientes
- Visualização de receitas
- Consulta de estoque
- Suporte às consultas

---

## 📁 **Estrutura de Arquivos**

```
medstock360/
│
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── README.md             # Este arquivo
│
├── data/                 # Banco de dados (criado automaticamente)
│   └── medstock360.db
│
├── logs/                 # Logs do sistema (criado automaticamente)
│
└── backups/              # Backups automáticos (criado automaticamente)
```

---

## 🔧 **Configurações Importantes**

### 📊 **Análise Preditiva**
O sistema calcula automaticamente:
- **Consumo médio diário** baseado nos últimos 30 dias
- **Previsão de término** do estoque atual
- **Alertas inteligentes:**
  - 🚨 Crítico: menos de 7 dias
  - ⚠️ Atenção: menos de 15 dias
  - ✅ OK: mais de 30 dias

### 🔄 **Backup Automático**
- Backup automático a cada 6 horas
- Arquivos salvos na pasta `backups/`
- Retenção de 30 dias de backups

---

## 🎯 **Como Usar Cada Módulo**

### 1️⃣ **Cadastrar Medicamentos**
1. Acesse "💊 Medicamentos"
2. Clique em "➕ Cadastrar Medicamento"
3. Preencha todas as informações
4. Salve

### 2️⃣ **Controlar Estoque**
1. Acesse "📦 Estoque"
2. Para nova entrada: "➕ Entrada de Lote"
3. Monitore alertas automáticos
4. Use "🔮 Análise Preditiva" para previsões

### 3️⃣ **Cadastrar Pacientes**
1. Acesse "👥 Pacientes"
2. Clique em "➕ Cadastrar Paciente"
3. Complete todos os dados
4. Salve

### 4️⃣ **Agendar Consultas**
1. Acesse "📅 Consultas"
2. Clique em "➕ Agendar Consulta"
3. Selecione paciente e médico
4. Defina data/hora

### 5️⃣ **Prescrever Receitas**
1. Acesse "📝 Receitas"
2. Clique em "➕ Nova Receita"
3. Selecione paciente
4. Adicione medicamentos com dosagem
5. Salve a receita

---

## 📈 **Alertas Automáticos**

### 🔴 **Estoque Crítico**
- Medicamentos com quantidade ≤ 10 unidades
- Aparecem no dashboard principal

### ⚠️ **Próximo ao Vencimento**
- Medicamentos que vencem em 30 dias
- Alertas visuais em todas as telas

### 🔮 **Previsão de Término**
- Baseada no consumo histórico
- Cálculo automático diário
- Sugestões de reposição

---

## 🛠️ **Solução de Problemas**

### ❓ **Não consegue fazer login?**
- Verifique usuário e senha
- Use credenciais padrão: `admin` / `admin123`

### ❓ **Sistema lento?**
- Feche abas desnecessárias do navegador
- Reinicie o aplicativo

### ❓ **Erro ao instalar?**
- Verifique se o Python está instalado
- Execute: `pip install --upgrade pip`
- Tente novamente: `pip install -r requirements.txt`

### ❓ **Perdeu dados?**
- Verifique a pasta `backups/`
- Restaure backup mais recente

---

## 📞 **Suporte**

### 🔧 **Problemas Técnicos**
1. Verifique a seção "Solução de Problemas"
2. Consulte os logs na pasta `logs/`
3. Abra uma issue no GitHub

### 💡 **Sugestões de Melhorias**
- Abra uma issue no GitHub com suas ideias
- Descreva detalhadamente a funcionalidade

---

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🎉 **Versão Atual: 3.0**

### ✨ **Novidades da v3.0:**
- 🔮 **Análise Preditiva de Medicamentos**
- 📊 **Dashboard melhorado com gráficos interativos**
- 🎯 **Alertas inteligentes por prioridade**
- 👥 **Sistema multi-usuário robusto**
- 📱 **Interface responsiva**
- 🔒 **Segurança aprimorada**

### 🗓️ **Próximas Atualizações (v3.1):**
- 📱 Notificações push
- 📧 Envio de alertas por email
- 📊 Relatórios em PDF
- 🔗 Integração com sistemas externos
- 📱 App mobile

---

## 🌟 **Contribua!**

Ajude a melhorar o MedStock360:
1. Faça um Fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

**Desenvolvido com ❤️ para facilitar a gestão hospitalar!**

---

### 📸 **Screenshots**

*Dashboard Principal:*
![Dashboard](screenshots/dashboard.png)

*Análise Preditiva:*
![Análise Preditiva](screenshots/analise-preditiva.png)

*Gestão de Medicamentos:*
![Medicamentos](screenshots/medicamentos.png)

---

**MedStock360 - Transformando a gestão hospitalar! 🏥✨**
