# 🏥 MedStock360 Advanced - Sistema de Controle de Medicamentos

## 📋 Sobre o Sistema

O **MedStock360 Advanced** é um sistema completo de gestão hospitalar focado no controle inteligente de medicamentos, estoque e atendimento a pacientes. O sistema oferece:

- 💊 **Gestão Completa de Medicamentos** - Cadastro com informações farmacêuticas detalhadas
- 📦 **Controle de Estoque Inteligente** - Sistema de lotes com localização física 3D
- 🔮 **Análise Preditiva com IA** - Previsões de consumo e alertas inteligentes
- 👥 **Gestão de Pacientes** - Prontuário eletrônico integrado
- 🏥 **Sistema de Consultas** - Agendamento e controle de atendimentos
- 📋 **Receitas Médicas** - Prescrição eletrônica com controle de dispensação
- 📈 **Relatórios Avançados** - Análises estatísticas e exportação de dados
- 👤 **Multi-usuário** - Sistema de permissões por perfis (Admin, Médico, Operador)

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Instalação das Dependências

```bash
pip install streamlit pandas sqlite3 plotly hashlib json pathlib datetime uuid
```

### 2. Estrutura de Arquivos

Crie uma pasta para o projeto e adicione os seguintes arquivos:

```
medstock360/
├── app.py              # Arquivo principal (código fornecido)
├── README.md           # Este arquivo
└── medstock360.db      # Banco de dados (criado automaticamente)
```

### 3. Executar o Sistema

```bash
# Navegar para a pasta do projeto
cd medstock360

# Executar o aplicativo
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`

## 🔐 Acesso Inicial

### Usuário Padrão

- **Usuário:** `admin`
- **Senha:** `admin123`
- **Perfil:** Administrador (acesso total)

### Primeiro Uso

1. Acesse com o usuário admin
2. Vá em **👤 Usuários** → **➕ Cadastrar Usuário** 
3. Crie usuários específicos para sua equipe
4. Configure as permissões adequadas para cada perfil

## 👥 Perfis de Usuário

### 👑 Administrador
- Acesso total ao sistema
- Gerenciamento de usuários
- Configurações avançadas
- Relatórios completos

### 👨‍⚕️ Médico
- Gestão de pacientes
- Agendamento de consultas
- Prescrição de receitas
- Acesso ao prontuário
- Visualização de medicamentos

### 👤 Operador
- Controle de estoque
- Movimentações de medicamentos
- Cadastro básico de pacientes
- Relatórios básicos

## 📊 Funcionalidades Principais

### 💊 Gestão de Medicamentos

**Cadastro Completo:**
- Nome comercial e princípio ativo
- Categoria farmacológica
- Forma farmacêutica e concentração
- Via de administração
- Informações sobre tarja e controle
- Necessidade de refrigeração
- Dados do fabricante

**Recursos Avançados:**
- Código de barras
- Alertas para medicamentos controlados
- Classificação por categorias
- Busca inteligente

### 📦 Controle de Estoque

**Sistema de Lotes:**
- Números de lote únicos
- Datas de fabricação e validade
- Controle de quantidades (inicial/atual)
- Preços unitários e fornecedores

**Localização Física 3D:**
- Local de armazenamento
- Setor específico
- Prateleira numerada
- Posição exata
- Mapa visual interativo

**Alertas Inteligentes:**
- Medicamentos próximos ao vencimento (30 dias)
- Estoque baixo (≤ 10 unidades)
- Medicamentos sem estoque
- Sugestões de reposição

### 🔮 Análise Preditiva

**IA Integrada:**
- Análise de padrões de consumo
- Previsão de quando medicamentos irão acabar
- Sugestões inteligentes de reposição
- Identificação de tendências

**Cenários Simulados:**
- Simulador de diferentes taxas de consumo
- Projeções para 30, 60, 90 dias
- Alertas por urgência (Crítico, Atenção, Normal)

### 👥 Gestão de Pacientes

**Dados Completos:**
- Informações pessoais e contato
- Dados médicos e alergias
- Medicamentos de uso contínuo
- Histórico familiar
- Plano de saúde

**Insights Automáticos:**
- Identificação de pacientes idosos
- Alertas para alergias conhecidas
- Sugestões baseadas no histórico

### 🏥 Sistema de Consultas

**Agendamento:**
- Data e hora específicas
- Associação paciente-médico
- Motivo da consulta
- Valor da consulta

**Controle de Status:**
- Agendada
- Realizada
- Cancelada

### 📋 Receitas Médicas

**Prescrição Eletrônica:**
- Múltiplos medicamentos por receita
- Posologia detalhada
- Observações médicas
- Controle de validade

**Dispensação Controlada:**
- Rastreamento de medicamentos dispensados
- Histórico completo
- Integração com estoque

### 📈 Relatórios e Análises

**Relatórios Padrão:**
- Movimentações de estoque
- Análise de validades
- Consumo por medicamento
- Desempenho por fornecedor

**Exportação de Dados:**
- Formato CSV
- Arquivos ZIP com múltiplas tabelas
- Backup completo do sistema

## 🛠️ Configurações Avançadas

### Backup Automático
- Geração de backups do banco de dados
- Download de arquivos de backup
- Restauração de dados

### Segurança
- Senhas criptografadas (SHA-256)
- Sistema de permissões granular
- Logs de acesso por usuário
- Reset seguro de senhas

### Personalização
- Configuração de alertas
- Personalização de relatórios
- Ajuste de parâmetros de IA

## 📱 Interface do Usuário

### Design Responsivo
- Layout otimizado para desktop e tablet
- Sidebar com navegação intuitiva
- Cards informativos com métricas
- Gráficos interativos

### Recursos Visuais
- Código de cores para status (Verde, Amarelo, Vermelho)
- Ícones intuitivos para cada funcionalidade
- Alertas visuais destacados
- Mapa 3D do estoque

## 🔧 Solução de Problemas

### Erro de Dependências
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências individualmente
pip install streamlit
pip install pandas
pip install plotly
```

### Erro de Banco de Dados
- O banco SQLite é criado automaticamente
- Se houver problemas, delete o arquivo `medstock360.db`
- O sistema recriará com dados padrão

### Performance
- Para grandes volumes de dados, considere usar PostgreSQL
- Otimize consultas SQL se necessário
- Configure cache para relatórios pesados

## 📞 Suporte e Manutenção

### Atualizações
- Backup regular dos dados
- Teste em ambiente de desenvolvimento
- Documentação de mudanças

### Monitoramento
- Logs de erro do Streamlit
- Monitoramento de uso de recursos
- Verificação de integridade dos dados

## 🎯 Roadmap de Melhorias

### Próximas Versões
- [ ] Integração com APIs de laboratórios
- [ ] Módulo financeiro completo
- [ ] App mobile complementar
- [ ] Dashboard em tempo real
- [ ] Integração com equipamentos IoT
- [ ] Relatórios com Business Intelligence
- [ ] Sistema de notificações push
- [ ] Auditoria completa de ações

### Integrações Futuras
- [ ] Sistema de código de barras/QR Code
- [ ] Integração com ANVISA
- [ ] Conectividade com sistemas hospitalares (HIS)
- [ ] API REST para terceiros

## 📄 Licença

Este sistema foi desenvolvido para uso em ambiente hospitalar e farmacêutico.

## 🤝 Contribuições

Para melhorias e sugestões:
1. Documente bugs encontrados
2. Sugira novas funcionalidades
3. Teste em diferentes cenários
4. Forneça feedback da experiência do usuário

---

**MedStock360 Advanced** - Transformando a gestão hospitalar com tecnologia e inteligência artificial.

*Versão 3.0 - Sistema Completo de Gestão Hospitalar*
