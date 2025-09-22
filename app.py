"""
🏥 MedStock360 Advanced - Sistema Hospitalar Completo
Sistema de Gestão Hospitalar Multi-usuário
Versão: 3.0 Advanced Cloud Edition
"""

import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import uuid
from pathlib import Path
import time
import re

# Configuração da página
st.set_page_config(
    page_title="MedStock360 Advanced",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .user-info {
        background: #f0f2f6;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-success {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .medication-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
    .medication-location {
        background: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        color: #1976d2;
    }
    .ai-analysis {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)

# Classe para gerenciar banco de dados
class DatabaseManager:
    def __init__(self, db_path="medstock360.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nome_completo TEXT NOT NULL,
                email TEXT,
                perfil TEXT NOT NULL DEFAULT 'operador',
                crm TEXT,
                especialidade TEXT,
                telefone TEXT,
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP,
                permissoes TEXT DEFAULT '{}'
            )
        """)
        
        # Tabela de medicamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                principio_ativo TEXT,
                categoria TEXT,
                tipo TEXT,
                concentracao TEXT,
                forma_farmaceutica TEXT,
                via_administracao TEXT,
                controlado BOOLEAN DEFAULT 0,
                refrigerado BOOLEAN DEFAULT 0,
                prescricao_obrigatoria BOOLEAN DEFAULT 0,
                tarja TEXT,
                codigo_barras TEXT,
                fabricante TEXT,
                observacoes TEXT,
                ativo BOOLEAN DEFAULT 1,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cadastrado_por INTEGER,
                FOREIGN KEY (cadastrado_por) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de lotes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicamento_id INTEGER NOT NULL,
                numero_lote TEXT NOT NULL,
                data_fabricacao DATE,
                data_validade DATE NOT NULL,
                quantidade_inicial INTEGER NOT NULL,
                quantidade_atual INTEGER NOT NULL,
                preco_unitario REAL,
                fornecedor TEXT,
                local_armazenamento TEXT,
                setor TEXT,
                prateleira TEXT,
                posicao TEXT,
                observacoes TEXT,
                ativo BOOLEAN DEFAULT 1,
                responsavel_entrada INTEGER,
                data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id),
                FOREIGN KEY (responsavel_entrada) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de movimentações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lote_id INTEGER NOT NULL,
                tipo_movimento TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                motivo TEXT,
                observacoes TEXT,
                responsavel INTEGER NOT NULL,
                data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lote_id) REFERENCES lotes (id),
                FOREIGN KEY (responsavel) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de pacientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                cpf TEXT UNIQUE,
                rg TEXT,
                data_nascimento DATE,
                sexo TEXT,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                cidade TEXT,
                cep TEXT,
                plano_saude TEXT,
                numero_carteira TEXT,
                contato_emergencia TEXT,
                alergias TEXT,
                medicamentos_uso_continuo TEXT,
                historico_familiar TEXT,
                observacoes TEXT,
                ativo BOOLEAN DEFAULT 1,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cadastrado_por INTEGER,
                FOREIGN KEY (cadastrado_por) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de consultas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                medico_id INTEGER NOT NULL,
                data_consulta DATETIME NOT NULL,
                motivo TEXT,
                sintomas TEXT,
                diagnostico TEXT,
                observacoes TEXT,
                valor REAL,
                status TEXT DEFAULT 'agendada',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (medico_id) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de receitas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                medico_id INTEGER NOT NULL,
                consulta_id INTEGER,
                data_receita DATETIME NOT NULL,
                observacoes TEXT,
                validade_receita DATE,
                status TEXT DEFAULT 'ativa',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (medico_id) REFERENCES usuarios (id),
                FOREIGN KEY (consulta_id) REFERENCES consultas (id)
            )
        """)
        
        # Tabela de itens da receita
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receita_itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receita_id INTEGER NOT NULL,
                medicamento_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                posologia TEXT,
                observacoes TEXT,
                FOREIGN KEY (receita_id) REFERENCES receitas (id),
                FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id)
            )
        """)
        
        # Tabela de dispensações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispensacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receita_id INTEGER NOT NULL,
                lote_id INTEGER NOT NULL,
                quantidade_dispensada INTEGER NOT NULL,
                data_dispensacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responsavel INTEGER NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (receita_id) REFERENCES receitas (id),
                FOREIGN KEY (lote_id) REFERENCES lotes (id),
                FOREIGN KEY (responsavel) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de prontuário
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prontuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                consulta_id INTEGER,
                data_entrada DATETIME NOT NULL,
                tipo_entrada TEXT NOT NULL,
                descricao TEXT NOT NULL,
                medico_responsavel INTEGER,
                anexos TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (consulta_id) REFERENCES consultas (id),
                FOREIGN KEY (medico_responsavel) REFERENCES usuarios (id)
            )
        """)
        
        # Tabela de alertas inteligentes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas_inteligentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_alerta TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                titulo TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                paciente_id INTEGER,
                medicamento_id INTEGER,
                usuario_destinatario INTEGER,
                lido BOOLEAN DEFAULT 0,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_leitura TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                FOREIGN KEY (medicamento_id) REFERENCES medicamentos (id),
                FOREIGN KEY (usuario_destinatario) REFERENCES usuarios (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Criar usuário admin se não existir
        self.create_default_admin()
    
    def create_default_admin(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar se já existe admin
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE perfil = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Criar usuário admin padrão
            admin_password = hashlib.sha256("admin123".encode()).hexdigest()
            
            cursor.execute("""
                INSERT INTO usuarios (username, password_hash, nome_completo, perfil, permissoes)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "admin", admin_password, "Administrador do Sistema", "admin",
                json.dumps({"medicamentos": ["visualizar", "criar", "editar", "excluir"],
                           "estoque": ["visualizar", "criar", "editar"],
                           "pacientes": ["visualizar", "criar", "editar"],
                           "consultas": ["visualizar", "criar", "editar"],
                           "receitas": ["visualizar", "criar", "editar"],
                           "relatorios": ["visualizar", "gerar"],
                           "usuarios": ["visualizar", "criar", "editar", "excluir"]})
            ))
            
            conn.commit()
        
        conn.close()

# Funções de autenticação
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def login_user(username, password):
    conn = st.session_state.db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, username, password_hash, nome_completo, perfil, permissoes, email
        FROM usuarios 
        WHERE username = ? AND ativo = 1
    """, (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        return {
            'id': user[0],
            'username': user[1],
            'nome_completo': user[3],
            'perfil': user[4],
            'permissoes': json.loads(user[5] if user[5] else '{}'),
            'email': user[6]
        }
    return None

def show_login():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MedStock360 Advanced</h1>
        <p>Sistema Hospitalar Completo - Gestão Inteligente de Medicamentos</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Acesso ao Sistema")
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button("🚀 Entrar", use_container_width=True)
            with col2:
                demo_button = st.form_submit_button("📋 Acesso Demo", use_container_width=True)
            
            if login_button:
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.logged_in = True
                        st.session_state.permissions = user['permissoes']
                        
                        # Atualizar último acesso
                        conn = st.session_state.db_manager.get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?",
                            (user['id'],)
                        )
                        conn.commit()
                        conn.close()
                        
                        st.success("✅ Login realizado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos!")
                else:
                    st.error("❌ Preencha todos os campos!")
            
            if demo_button:
                # Login como admin para demonstração
                demo_user = login_user("admin", "admin123")
                if demo_user:
                    st.session_state.user = demo_user
                    st.session_state.logged_in = True
                    st.session_state.permissions = demo_user['permissoes']
                    st.success("✅ Acesso demo ativado!")
                    time.sleep(1)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("""
        **🔑 Acesso Demo:**
        - **Usuário:** admin
        - **Senha:** admin123
        
        **📊 Funcionalidades:**
        - Controle de estoque inteligente
        - Análise preditiva com IA
        - Gestão de pacientes
        - Receitas médicas
        - Relatórios avançados
        """)

def show_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="user-info">
            👤 <strong>{st.session_state.user['nome_completo']}</strong><br>
            🔧 {st.session_state.user['perfil'].title()}<br>
            📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🗂️ Menu Principal")
        
        # Menu baseado em permissões
        menu_options = []
        
        if 'medicamentos' in st.session_state.permissions:
            menu_options.append("📊 Dashboard")
            menu_options.append("💊 Medicamentos")
        
        if 'estoque' in st.session_state.permissions:
            menu_options.append("📦 Estoque")
        
        if 'pacientes' in st.session_state.permissions:
            menu_options.append("👥 Pacientes")
        
        if 'consultas' in st.session_state.permissions:
            menu_options.append("🏥 Consultas")
        
        if 'receitas' in st.session_state.permissions:
            menu_options.append("📋 Receitas")
        
        menu_options.append("🔮 Análise Preditiva")
        
        if 'relatorios' in st.session_state.permissions:
            menu_options.append("📈 Relatórios")
        
        if 'usuarios' in st.session_state.permissions:
            menu_options.append("👤 Usuários")
        
        menu_options.append("⚙️ Configurações")
        
        selected = st.selectbox("Escolha uma opção:", menu_options, key="main_menu")
        
        st.markdown("---")
        
        # Alertas rápidos
        show_quick_alerts()
        
        st.markdown("---")
        
        if st.button("🚪 Sair", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        return selected

def show_quick_alerts():
    st.markdown("### ⚠️ Alertas Rápidos")
    
    conn = st.session_state.db_manager.get_connection()
    
    # Medicamentos próximos ao vencimento
    query_vencimento = """
        SELECT COUNT(*) FROM lotes l
        JOIN medicamentos m ON l.medicamento_id = m.id
        WHERE l.ativo = 1 AND DATE(l.data_validade) <= DATE('now', '+30 days')
        AND l.quantidade_atual > 0
    """
    
    # Medicamentos com estoque baixo
    query_estoque_baixo = """
        SELECT COUNT(*) FROM lotes l
        JOIN medicamentos m ON l.medicamento_id = m.id
        WHERE l.ativo = 1 AND l.quantidade_atual > 0 AND l.quantidade_atual <= 10
    """
    
    # Medicamentos sem estoque
    query_sem_estoque = """
        SELECT COUNT(*) FROM lotes l
        JOIN medicamentos m ON l.medicamento_id = m.id
        WHERE l.ativo = 1 AND l.quantidade_atual = 0
    """
    
    vencimento = pd.read_sql(query_vencimento, conn).iloc[0, 0]
    estoque_baixo = pd.read_sql(query_estoque_baixo, conn).iloc[0, 0]
    sem_estoque = pd.read_sql(query_sem_estoque, conn).iloc[0, 0]
    
    conn.close()
    
    if vencimento > 0:
        st.warning(f"⚠️ {vencimento} próximos ao vencimento")
    
    if estoque_baixo > 0:
        st.warning(f"📦 {estoque_baixo} com estoque baixo")
    
    if sem_estoque > 0:
        st.error(f"🔴 {sem_estoque} sem estoque")
    
    if vencimento == 0 and estoque_baixo == 0 and sem_estoque == 0:
        st.success("✅ Tudo OK!")

def show_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard MedStock360</h1>
        <p>Visão geral inteligente do sistema</p>
    </div>
    """, unsafe_allow_html=True)
    
    conn = st.session_state.db_manager.get_connection()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    # Total de medicamentos
    total_medicamentos = pd.read_sql("SELECT COUNT(*) FROM medicamentos WHERE ativo = 1", conn).iloc[0, 0]
    
    # Total de lotes ativos
    total_lotes = pd.read_sql("SELECT COUNT(*) FROM lotes WHERE ativo = 1", conn).iloc[0, 0]
    
    # Total de pacientes
    total_pacientes = pd.read_sql("SELECT COUNT(*) FROM pacientes WHERE ativo = 1", conn).iloc[0, 0]
    
    # Movimentações hoje
    movimentacoes_hoje = pd.read_sql(
        "SELECT COUNT(*) FROM movimentacoes WHERE DATE(data_movimento) = DATE('now')", conn
    ).iloc[0, 0]
    
    with col1:
        st.metric("💊 Medicamentos", total_medicamentos)
    
    with col2:
        st.metric("📦 Lotes Ativos", total_lotes)
    
    with col3:
        st.metric("👥 Pacientes", total_pacientes)
    
    with col4:
        st.metric("📈 Movimentações Hoje", movimentacoes_hoje)
    
    # Gráficos do dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Medicamentos por Categoria")
        df_categorias = pd.read_sql("""
            SELECT categoria, COUNT(*) as quantidade
            FROM medicamentos 
            WHERE ativo = 1 AND categoria IS NOT NULL
            GROUP BY categoria
            ORDER BY quantidade DESC
        """, conn)
        
        if not df_categorias.empty:
            fig = px.pie(df_categorias, values='quantidade', names='categoria')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum dado disponível")
    
    with col2:
        st.markdown("### 📈 Movimentações dos Últimos 7 Dias")
        df_movimentacoes = pd.read_sql("""
            SELECT 
                DATE(data_movimento) as data,
                tipo_movimento,
                COUNT(*) as quantidade
            FROM movimentacoes 
            WHERE data_movimento >= DATE('now', '-7 days')
            GROUP BY DATE(data_movimento), tipo_movimento
            ORDER BY data
        """, conn)
        
        if not df_movimentacoes.empty:
            fig = px.bar(df_movimentacoes, x='data', y='quantidade', color='tipo_movimento')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum dado disponível")
    
    # Alertas críticos
    st.markdown("### 🚨 Alertas Críticos")
    
    # Medicamentos próximos ao vencimento
    df_vencimento = pd.read_sql("""
        SELECT 
            m.nome,
            l.numero_lote,
            l.data_validade,
            l.quantidade_atual,
            julianday(l.data_validade) - julianday('now') as dias_vencimento
        FROM lotes l
        JOIN medicamentos m ON l.medicamento_id = m.id
        WHERE l.ativo = 1 AND DATE(l.data_validade) <= DATE('now', '+30 days')
        AND l.quantidade_atual > 0
        ORDER BY l.data_validade
        LIMIT 5
    """, conn)
    
    if not df_vencimento.empty:
        st.markdown("#### ⚠️ Próximos ao Vencimento")
        for _, item in df_vencimento.iterrows():
            dias = int(item['dias_vencimento'])
            if dias <= 7:
                cor = "🔴"
            elif dias <= 15:
                cor = "🟡"
            else:
                cor = "🟠"
            
            st.warning(f"{cor} {item['nome']} (Lote: {item['numero_lote']}) - Vence em {dias} dias")
    
    # Medicamentos com estoque baixo
    df_estoque_baixo = pd.read_sql("""
        SELECT 
            m.nome,
            l.numero_lote,
            l.quantidade_atual,
            l.local_armazenamento
        FROM lotes l
        JOIN medicamentos m ON l.medicamento_id = m.id
        WHERE l.ativo = 1 AND l.quantidade_atual > 0 AND l.quantidade_atual <= 10
        ORDER BY l.quantidade_atual
        LIMIT 5
    """, conn)
    
    if not df_estoque_baixo.empty:
        st.markdown("#### 📦 Estoque Baixo")
        for _, item in df_estoque_baixo.iterrows():
            st.warning(f"📦 {item['nome']} - {item['quantidade_atual']} unidades restantes")
    
    conn.close()

def show_medicamentos():
    """Módulo de medicamentos"""
    st.markdown("## 💊 Gestão de Medicamentos")
    
    if 'criar' in st.session_state.permissions.get('medicamentos', []):
        tab1, tab2, tab3 = st.tabs(["📋 Lista de Medicamentos", "➕ Cadastrar Medicamento", "📊 Estatísticas"])
    else:
        tab1, tab2, tab3 = st.tabs(["📋 Lista de Medicamentos", "", "📊 Estatísticas"])
    
    with tab1:
        st.markdown("### 📋 Lista de Medicamentos Cadastrados")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Buscar medicamento", placeholder="Nome ou princípio ativo")
        
        with col2:
            conn = st.session_state.db_manager.get_connection()
            categorias = pd.read_sql("SELECT DISTINCT categoria FROM medicamentos WHERE categoria IS NOT NULL", conn)['categoria'].tolist()
            categoria_filter = st.selectbox("📂 Categoria", ["Todas"] + categorias)
        
        with col3:
            tipo_filter = st.selectbox("🏷️ Tipo", ["Todos", "Controlado", "Refrigerado", "Prescrição Obrigatória"])
        
        # Buscar medicamentos
        query = """
            SELECT 
                m.*,
                u.nome_completo as cadastrado_por_nome,
                COUNT(DISTINCT l.id) as total_lotes,
                SUM(l.quantidade_atual) as estoque_total
            FROM medicamentos m
            LEFT JOIN usuarios u ON m.cadastrado_por = u.id
            LEFT JOIN lotes l ON m.id = l.medicamento_id AND l.ativo = 1
            WHERE m.ativo = 1
        """
        params = []
        
        if search_term:
            query += " AND (m.nome LIKE ? OR m.principio_ativo LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if categoria_filter != "Todas":
            query += " AND m.categoria = ?"
            params.append(categoria_filter)
        
        if tipo_filter != "Todos":
            if tipo_filter == "Controlado":
                query += " AND m.controlado = 1"
            elif tipo_filter == "Refrigerado":
                query += " AND m.refrigerado = 1"
            elif tipo_filter == "Prescrição Obrigatória":
                query += " AND m.prescricao_obrigatoria = 1"
        
        query += " GROUP BY m.id ORDER BY m.nome"
        
        df_medicamentos = pd.read_sql(query, conn, params=params)
        conn.close()
        
        if not df_medicamentos.empty:
            st.info(f"📊 {len(df_medicamentos)} medicamentos encontrados")
            
            for _, med in df_medicamentos.iterrows():
                # Status do medicamento
                status_badges = []
                if med['controlado']:
                    status_badges.append("🔒 Controlado")
                if med['refrigerado']:
                    status_badges.append("❄️ Refrigerado")
                if med['prescricao_obrigatoria']:
                    status_badges.append("📋 Prescrição Obrigatória")
                
                status_text = " | ".join(status_badges) if status_badges else "📦 Comum"
                
                with st.expander(f"💊 {med['nome']} - {status_text}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📋 Informações Básicas**")
                        st.write(f"**Nome:** {med['nome']}")
                        st.write(f"**Princípio Ativo:** {med['principio_ativo'] or 'N/A'}")
                        st.write(f"**Categoria:** {med['categoria'] or 'N/A'}")
                        st.write(f"**Tipo:** {med['tipo'] or 'N/A'}")
                        st.write(f"**Concentração:** {med['concentracao'] or 'N/A'}")
                    
                    with col2:
                        st.markdown("**💊 Características**")
                        st.write(f"**Forma Farmacêutica:** {med['forma_farmaceutica'] or 'N/A'}")
                        st.write(f"**Via de Administração:** {med['via_administracao'] or 'N/A'}")
                        st.write(f"**Tarja:** {med['tarja'] or 'N/A'}")
                        st.write(f"**Fabricante:** {med['fabricante'] or 'N/A'}")
                        st.write(f"**Código de Barras:** {med['codigo_barras'] or 'N/A'}")
                    
                    with col3:
                        st.markdown("**📊 Estoque e Status**")
                        st.write(f"**Total de Lotes:** {med['total_lotes'] or 0}")
                        st.write(f"**Estoque Total:** {med['estoque_total'] or 0} unidades")
                        if med['cadastrado_por_nome']:
                            st.write(f"**Cadastrado por:** {med['cadastrado_por_nome']}")
                        if med['data_cadastro']:
                            data_cad = datetime.strptime(med['data_cadastro'], '%Y-%m-%d %H:%M:%S')
                            st.write(f"**Data Cadastro:** {data_cad.strftime('%d/%m/%Y')}")
                    
                    if med['observacoes']:
                        st.markdown("**📝 Observações:**")
                        st.write(med['observacoes'])
        else:
            st.info("Nenhum medicamento encontrado com os filtros aplicados.")
    
    if 'criar' in st.session_state.permissions.get('medicamentos', []):
        with tab2:
            st.markdown("### ➕ Cadastrar Novo Medicamento")
            
            with st.form("form_medicamento"):
                st.markdown("**📋 Informações Básicas**")
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("Nome do Medicamento *", placeholder="Ex: Paracetamol 500mg")
                    principio_ativo = st.text_input("Princípio Ativo", placeholder="Ex: Paracetamol")
                    categoria = st.selectbox("Categoria", [
                        "", "Analgésico", "Antibiótico", "Anti-inflamatório", "Antialérgico",
                        "Antidiabético", "Anti-hipertensivo", "Vitamina", "Suplemento", "Outro"
                    ])
                    tipo = st.selectbox("Tipo", [
                        "", "Medicamento", "Suplemento", "Vitamina", "Vacina", "Material Médico"
                    ])
                
                with col2:
                    concentracao = st.text_input("Concentração", placeholder="Ex: 500mg")
                    forma_farmaceutica = st.selectbox("Forma Farmacêutica", [
                        "", "Comprimido", "Cápsula", "Solução", "Suspensão", "Pomada",
                        "Creme", "Gel", "Spray", "Injetável", "Gotas"
                    ])
                    via_administracao = st.selectbox("Via de Administração", [
                        "", "Oral", "Tópica", "Intramuscular", "Intravenosa", "Subcutânea",
                        "Oftálmica", "Nasal", "Auricular", "Retal", "Vaginal"
                    ])
                    tarja = st.selectbox("Tarja", ["", "Sem Tarja", "Tarja Vermelha", "Tarja Preta"])
                
                st.markdown("**🏷️ Características Especiais**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    controlado = st.checkbox("🔒 Medicamento Controlado")
                with col2:
                    refrigerado = st.checkbox("❄️ Necessita Refrigeração")
                with col3:
                    prescricao_obrigatoria = st.checkbox("📋 Prescrição Obrigatória")
                
                st.markdown("**🏭 Informações Comerciais**")
                col1, col2 = st.columns(2)
                
                with col1:
                    fabricante = st.text_input("Fabricante", placeholder="Nome do fabricante")
                    codigo_barras = st.text_input("Código de Barras", placeholder="Ex: 7891234567890")
                
                with col2:
                    observacoes = st.text_area("Observações", placeholder="Informações adicionais...")
                
                submitted = st.form_submit_button("💾 Cadastrar Medicamento", use_container_width=True)
                
                if submitted:
                    if not nome:
                        st.error("❌ O nome do medicamento é obrigatório!")
                    else:
                        try:
                            conn = st.session_state.db_manager.get_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute("""
                                INSERT INTO medicamentos (
                                    nome, principio_ativo, categoria, tipo, concentracao,
                                    forma_farmaceutica, via_administracao, controlado, refrigerado,
                                    prescricao_obrigatoria, tarja, codigo_barras, fabricante,
                                    observacoes, cadastrado_por
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                nome, principio_ativo, categoria, tipo, concentracao,
                                forma_farmaceutica, via_administracao, controlado, refrigerado,
                                prescricao_obrigatoria, tarja, codigo_barras, fabricante,
                                observacoes, st.session_state.user['id']
                            ))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Medicamento cadastrado com sucesso!")
                            time.sleep(2)
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Erro ao cadastrar medicamento: {str(e)}")
    
    with tab3:
        st.markdown("### 📊 Estatísticas de Medicamentos")
        
        conn = st.session_state.db_manager.get_connection()
        
        # Estatísticas gerais
        total_medicamentos = pd.read_sql("SELECT COUNT(*) FROM medicamentos WHERE ativo = 1", conn).iloc[0, 0]
        controlados = pd.read_sql("SELECT COUNT(*) FROM medicamentos WHERE ativo = 1 AND controlado = 1", conn).iloc[0, 0]
        refrigerados = pd.read_sql("SELECT COUNT(*) FROM medicamentos WHERE ativo = 1 AND refrigerado = 1", conn).iloc[0, 0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💊 Total Medicamentos", total_medicamentos)
        with col2:
            st.metric("🔒 Controlados", controlados)
        with col3:
            st.metric("❄️ Refrigerados", refrigerados)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por categoria
            df_cat = pd.read_sql("""
                SELECT categoria, COUNT(*) as quantidade
                FROM medicamentos 
                WHERE ativo = 1 AND categoria IS NOT NULL
                GROUP BY categoria
                ORDER BY quantidade DESC
            """, conn)
            
            if not df_cat.empty:
                st.markdown("#### 📂 Por Categoria")
                fig = px.bar(df_cat, x='categoria', y='quantidade')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribuição por forma farmacêutica
            df_forma = pd.read_sql("""
                SELECT forma_farmaceutica, COUNT(*) as quantidade
                FROM medicamentos 
                WHERE ativo = 1 AND forma_farmaceutica IS NOT NULL
                GROUP BY forma_farmaceutica
                ORDER BY quantidade DESC
                LIMIT 10
            """, conn)
            
            if not df_forma.empty:
                st.markdown("#### 💊 Por Forma Farmacêutica")
                fig = px.pie(df_forma, values='quantidade', names='forma_farmaceutica')
                st.plotly_chart(fig, use_container_width=True)
        
        conn.close()

# FUNÇÕES ADICIONAIS DO SISTEMA (CONTINUAÇÃO DO CÓDIGO FORNECIDO)

def show_estoque():
    """Módulo de estoque avançado"""
    st.markdown("## 📦 Gestão de Estoque Inteligente")
    
    # Verificar permissões
    if 'criar' in st.session_state.permissions.get('estoque', []):
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Estoque Atual", "➕ Entrada de Lote", "📊 Movimentações", "🗺️ Mapa 3D"])
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Estoque Atual", "", "📊 Movimentações", "🗺️ Mapa 3D"])
    
    with tab1:
        st.markdown("### 📋 Estoque Atual com Localização Inteligente")
        
        # Filtros avançados
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search_term = st.text_input("🔍 Buscar medicamento", placeholder="Nome do medicamento")
        
        with col2:
            status_filter = st.selectbox("📊 Status", ["Todos", "Em estoque", "Estoque baixo", "Sem estoque", "Próximo ao vencimento"])
        
        with col3:
            conn = st.session_state.db_manager.get_connection()
            locais = pd.read_sql("SELECT DISTINCT local_armazenamento FROM lotes WHERE local_armazenamento IS NOT NULL", conn)['local_armazenamento'].tolist()
            local_filter = st.selectbox("📍 Local", ["Todos"] + locais)
        
        with col4:
            setor_filter = st.selectbox("🏢 Setor", ["Todos"] + 
                pd.read_sql("SELECT DISTINCT setor FROM lotes WHERE setor IS NOT NULL", conn)['setor'].tolist())
        
        # Query base avançada
        query = """
            SELECT 
                m.nome as medicamento,
                m.principio_ativo,
                m.controlado,
                l.numero_lote,
                l.data_validade,
                l.quantidade_atual,
                l.local_armazenamento,
                l.setor,
                l.prateleira,
                l.posicao,
                l.fornecedor,
                l.preco_unitario,
                julianday(l.data_validade) - julianday('now') as dias_vencimento,
                CASE 
                    WHEN l.quantidade_atual = 0 THEN 'Sem estoque'
                    WHEN l.quantidade_atual <= 10 THEN 'Estoque baixo'
                    WHEN DATE(l.data_validade) <= DATE('now', '+30 days') THEN 'Próximo ao vencimento'
                    ELSE 'Normal'
                END as status
            FROM lotes l
            JOIN medicamentos m ON l.medicamento_id = m.id
            WHERE l.ativo = 1 AND m.ativo = 1
        """
        params = []
        
        if search_term:
            query += " AND m.nome LIKE ?"
            params.append(f"%{search_term}%")
        
        if local_filter != "Todos":
            query += " AND l.local_armazenamento = ?"
            params.append(local_filter)
        
        if setor_filter != "Todos":
            query += " AND l.setor = ?"
            params.append(setor_filter)
        
        if status_filter != "Todos":
            if status_filter == "Em estoque":
                query += " AND l.quantidade_atual > 10"
            elif status_filter == "Estoque baixo":
                query += " AND l.quantidade_atual > 0 AND l.quantidade_atual <= 10"
            elif status_filter == "Sem estoque":
                query += " AND l.quantidade_atual = 0"
            elif status_filter == "Próximo ao vencimento":
                query += " AND DATE(l.data_validade) <= DATE('now', '+30 days') AND l.quantidade_atual > 0"
        
        query += " ORDER BY m.nome, l.data_validade"
        
        df_estoque = pd.read_sql(query, conn, params=params)
        conn.close()
        
        if not df_estoque.empty:
            # Resumo inteligente
            total_lotes = len(df_estoque)
            sem_estoque = len(df_estoque[df_estoque['quantidade_atual'] == 0])
            estoque_baixo = len(df_estoque[(df_estoque['quantidade_atual'] > 0) & (df_estoque['quantidade_atual'] <= 10)])
            proximo_vencimento = len(df_estoque[df_estoque['status'] == 'Próximo ao vencimento'])
            medicamentos_controlados = len(df_estoque[df_estoque['controlado'] == 1])
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("📦 Total de Lotes", total_lotes)
            with col2:
                st.metric("🔴 Sem Estoque", sem_estoque)
            with col3:
                st.metric("🟡 Estoque Baixo", estoque_baixo)
            with col4:
                st.metric("⚠️ Próximo Vencimento", proximo_vencimento)
            with col5:
                st.metric("🔒 Controlados", medicamentos_controlados)
            
            # Alertas inteligentes
            if sem_estoque > 0:
                st.markdown(f"""
                <div class="alert-danger">
                    🔴 <strong>CRÍTICO!</strong> {sem_estoque} lotes sem estoque precisam de reposição imediata.
                </div>
                """, unsafe_allow_html=True)
            
            if proximo_vencimento > 0:
                st.markdown(f"""
                <div class="alert-warning">
                    ⚠️ <strong>ALERTA!</strong> {proximo_vencimento} lotes próximos ao vencimento (30 dias).
                </div>
                """, unsafe_allow_html=True)
            
            # Lista avançada com localização
            st.markdown("### 📋 Lista Detalhada com Localização")
            
            for _, item in df_estoque.iterrows():
                # Cor baseada no status
                if item['status'] == 'Sem estoque':
                    status_color = '🔴'
                elif item['status'] == 'Estoque baixo':
                    status_color = '🟡'
                elif item['status'] == 'Próximo ao vencimento':
                    status_color = '⚠️'
                else:
                    status_color = '🟢'
                
                controlado_badge = ' 🔒' if item['controlado'] else ''
                
                with st.expander(f"{status_color} {item['medicamento']}{controlado_badge} - Lote: {item['numero_lote']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📊 Informações do Estoque**")
                        st.write(f"**Quantidade:** {item['quantidade_atual']} unidades")
                        st.write(f"**Status:** {item['status']}")
                        st.write(f"**Validade:** {item['data_validade']}")
                        if item['dias_vencimento'] and item['dias_vencimento'] > 0:
                            st.write(f"**Dias para vencer:** {int(item['dias_vencimento'])}")
                    
                    with col2:
                        st.markdown("**📍 Localização Física**")
                        st.write(f"**Local:** {item['local_armazenamento'] or 'N/A'}")
                        st.write(f"**Setor:** {item['setor'] or 'N/A'}")
                        st.write(f"**Prateleira:** {item['prateleira'] or 'N/A'}")
                        st.write(f"**Posição:** {item['posicao'] or 'N/A'}")
                        
                        # Localização completa
                        if item['local_armazenamento']:
                            localizacao = f"📍 {item['local_armazenamento']}"
                            if item['setor']:
                                localizacao += f" → {item['setor']}"
                            if item['prateleira']:
                                localizacao += f" → P{item['prateleira']}"
                            if item['posicao']:
                                localizacao += f" → {item['posicao']}"
                            
                            st.markdown(f"""
                            <div class="medication-location">
                                {localizacao}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("**💰 Informações Comerciais**")
                        st.write(f"**Fornecedor:** {item['fornecedor'] or 'N/A'}")
                        if item['preco_unitario']:
                            st.write(f"**Preço Unitário:** R$ {item['preco_unitario']:.2f}")
                            valor_total = item['quantidade_atual'] * item['preco_unitario']
                            st.write(f"**Valor Total:** R$ {valor_total:.2f}")
        else:
            st.info("Nenhum lote encontrado com os filtros aplicados.")
    
    if 'criar' in st.session_state.permissions.get('estoque', []):
        with tab2:
            st.markdown("### ➕ Entrada de Novo Lote com Localização")
            
            # Buscar medicamentos
            conn = st.session_state.db_manager.get_connection()
            medicamentos = pd.read_sql("SELECT id, nome FROM medicamentos WHERE ativo = 1 ORDER BY nome", conn)
            conn.close()
            
            if medicamentos.empty:
                st.warning("⚠️ Nenhum medicamento cadastrado. Cadastre medicamentos primeiro.")
            else:
                with st.form("form_lote_avancado"):
                    st.markdown("**📦 Informações do Lote**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        medicamento_options = {f"{row['nome']}": row['id'] for _, row in medicamentos.iterrows()}
                        medicamento_selecionado = st.selectbox("Medicamento *", list(medicamento_options.keys()))
                        numero_lote = st.text_input("Número do Lote *", placeholder="Ex: L123456")
                        data_fabricacao = st.date_input("Data de Fabricação")
                        data_validade = st.date_input("Data de Validade *")
                        quantidade_inicial = st.number_input("Quantidade *", min_value=1, value=1)
                    
                    with col2:
                        preco_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, step=0.01, format="%.2f")
                        fornecedor = st.text_input("Fornecedor", placeholder="Nome do fornecedor")
                        observacoes = st.text_area("Observações", placeholder="Informações adicionais...")
                    
                    st.markdown("**📍 Localização Física Detalhada**")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        local_armazenamento = st.selectbox("Local de Armazenamento *", [
                            "", "Farmácia Central", "Sala de Medicamentos", "Geladeira", 
                            "Cofre (Controlados)", "Almoxarifado", "UTI", "Pronto Socorro"
                        ])
                    
                    with col2:
                        setor = st.text_input("Setor", placeholder="Ex: A, B, C")
                    
                    with col3:
                        prateleira = st.text_input("Prateleira", placeholder="Ex: P1, P2")
                    
                    with col4:
                        posicao = st.text_input("Posição", placeholder="Ex: A1, B3")
                    
                    submitted = st.form_submit_button("💾 Registrar Entrada Completa", use_container_width=True)
                    
                    if submitted:
                        if not medicamento_selecionado or not numero_lote or not data_validade or not quantidade_inicial or not local_armazenamento:
                            st.error("❌ Preencha todos os campos obrigatórios!")
                        elif data_validade <= date.today():
                            st.error("❌ A data de validade deve ser futura!")
                        else:
                            try:
                                conn = st.session_state.db_manager.get_connection()
                                cursor = conn.cursor()
                                
                                medicamento_id = medicamento_options[medicamento_selecionado]
                                
                                # Inserir lote com localização
                                cursor.execute("""
                                    INSERT INTO lotes (
                                        medicamento_id, numero_lote, data_fabricacao, data_validade,
                                        quantidade_inicial, quantidade_atual, preco_unitario, fornecedor,
                                        local_armazenamento, setor, prateleira, posicao, observacoes, 
                                        responsavel_entrada
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    medicamento_id, numero_lote, data_fabricacao, data_validade,
                                    quantidade_inicial, quantidade_inicial, preco_unitario, fornecedor,
                                    local_armazenamento, setor, prateleira, posicao, observacoes,
                                    st.session_state.user['id']
                                ))
                                
                                lote_id = cursor.lastrowid
                                
                                # Registrar movimentação
                                cursor.execute("""
                                    INSERT INTO movimentacoes (
                                        lote_id, tipo_movimento, quantidade, motivo, responsavel
                                    ) VALUES (?, 'Entrada', ?, 'Entrada de novo lote', ?)
                                """, (lote_id, quantidade_inicial, st.session_state.user['id']))
                                
                                conn.commit()
                                conn.close()
                                
                                # Criar alerta inteligente se próximo ao vencimento
                                dias_para_vencer = (data_validade - date.today()).days
                                if dias_para_vencer <= 30:
                                    create_smart_alert(
                                        "estoque",
                                        "atencao" if dias_para_vencer > 7 else "urgente",
                                        "Medicamento próximo ao vencimento",
                                        f"Lote {numero_lote} vence em {dias_para_vencer} dias",
                                        medicamento_id=medicamento_id
                                    )
                                
                                st.success("✅ Lote registrado com localização completa!")
                                time.sleep(2)
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Erro ao registrar lote: {str(e)}")
    
    with tab3:
        st.markdown("### 📊 Histórico Inteligente de Movimentações")
        
        # Filtros avançados
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            data_inicio = st.date_input("Data Início", value=date.today() - timedelta(days=30))
        
        with col2:
            data_fim = st.date_input("Data Fim", value=date.today())
        
        with col3:
            tipo_movimento = st.selectbox("Tipo de Movimento", ["Todos", "Entrada", "Saída", "Ajuste", "Transferência"])
        
        with col4:
            medicamento_filtro = st.text_input("Filtrar Medicamento", placeholder="Nome do medicamento")
        
        # Buscar movimentações
        query = """
            SELECT 
                m.nome as medicamento,
                l.numero_lote,
                l.local_armazenamento,
                l.setor,
                mov.tipo_movimento,
                mov.quantidade,
                mov.motivo,
                mov.data_movimento,
                u.nome_completo as responsavel,
                mov.observacoes
            FROM movimentacoes mov
            JOIN lotes l ON mov.lote_id = l.id
            JOIN medicamentos m ON l.medicamento_id = m.id
            JOIN usuarios u ON mov.responsavel = u.id
            WHERE DATE(mov.data_movimento) BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if tipo_movimento != "Todos":
            query += " AND mov.tipo_movimento = ?"
            params.append(tipo_movimento)
        
        if medicamento_filtro:
            query += " AND m.nome LIKE ?"
            params.append(f"%{medicamento_filtro}%")
        
        query += " ORDER BY mov.data_movimento DESC"
        
        conn = st.session_state.db_manager.get_connection()
        df_movimentacoes = pd.read_sql(query, conn, params=params)
        
        # Estatísticas das movimentações
        if not df_movimentacoes.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                entradas = len(df_movimentacoes[df_movimentacoes['tipo_movimento'] == 'Entrada'])
                st.metric("📥 Entradas", entradas)
            
            with col2:
                saidas = len(df_movimentacoes[df_movimentacoes['tipo_movimento'] == 'Saída'])
                st.metric("📤 Saídas", saidas)
            
            with col3:
                ajustes = len(df_movimentacoes[df_movimentacoes['tipo_movimento'] == 'Ajuste'])
                st.metric("🔧 Ajustes", ajustes)
            
            # Gráfico de movimentações por dia
            st.markdown("### 📈 Movimentações por Dia")
            df_grafico = df_movimentacoes.copy()
            df_grafico['data'] = pd.to_datetime(df_grafico['data_movimento']).dt.date
            df_resumo = df_grafico.groupby(['data', 'tipo_movimento']).size().reset_index(name='quantidade')
            
            if not df_resumo.empty:
                fig = px.bar(df_resumo, x='data', y='quantidade', color='tipo_movimento', 
                           title="Movimentações por Tipo e Data")
                st.plotly_chart(fig, use_container_width=True)
            
            # Lista detalhada
            st.markdown("### 📋 Lista Detalhada")
            for _, mov in df_movimentacoes.iterrows():
                # Ícone baseado no tipo
                tipo_icons = {
                    'Entrada': '📥',
                    'Saída': '📤', 
                    'Ajuste': '🔧',
                    'Transferência': '🔄'
                }
                icon = tipo_icons.get(mov['tipo_movimento'], '📋')
                
                data_mov = datetime.strptime(mov['data_movimento'], '%Y-%m-%d %H:%M:%S')
                
                with st.expander(f"{icon} {mov['medicamento']} - {data_mov.strftime('%d/%m/%Y %H:%M')}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Medicamento:** {mov['medicamento']}")
                        st.write(f"**Lote:** {mov['numero_lote']}")
                        st.write(f"**Tipo:** {mov['tipo_movimento']}")
                        st.write(f"**Quantidade:** {mov['quantidade']}")
                    
                    with col2:
                        st.write(f"**Local:** {mov['local_armazenamento'] or 'N/A'}")
                        st.write(f"**Setor:** {mov['setor'] or 'N/A'}")
                        st.write(f"**Responsável:** {mov['responsavel']}")
                        st.write(f"**Data/Hora:** {data_mov.strftime('%d/%m/%Y %H:%M')}")
                    
                    with col3:
                        st.write(f"**Motivo:** {mov['motivo'] or 'N/A'}")
                        if mov['observacoes']:
                            st.write(f"**Observações:** {mov['observacoes']}")
        
        conn.close()
        
        if df_movimentacoes.empty:
            st.info("Nenhuma movimentação encontrada no período selecionado.")
    
    with tab4:
        st.markdown("### 🗺️ Mapa 3D do Estoque")
        
        st.markdown("""
        <div class="ai-analysis">
            🗺️ <strong>Visualização Inteligente do Estoque</strong><br>
            Mapa interativo mostrando a localização física de todos os medicamentos
        </div>
        """, unsafe_allow_html=True)
        
        # Buscar dados para o mapa
        conn = st.session_state.db_manager.get_connection()
        df_mapa = pd.read_sql("""
            SELECT 
                m.nome as medicamento,
                l.local_armazenamento,
                l.setor,
                l.prateleira,
                l.posicao,
                l.quantidade_atual,
                l.numero_lote,
                CASE 
                    WHEN l.quantidade_atual = 0 THEN 'Vazio'
                    WHEN l.quantidade_atual <= 10 THEN 'Baixo'
                    WHEN DATE(l.data_validade) <= DATE('now', '+30 days') THEN 'Vencendo'
                    ELSE 'Normal'
                END as status
            FROM lotes l
            JOIN medicamentos m ON l.medicamento_id = m.id
            WHERE l.ativo = 1 AND l.local_armazenamento IS NOT NULL
            ORDER BY l.local_armazenamento, l.setor, l.prateleira, l.posicao
        """, conn)
        conn.close()
        
        if not df_mapa.empty:
            # Agrupar por local
            locais_unicos = df_mapa['local_armazenamento'].unique()
            
            for local in locais_unicos:
                st.markdown(f"### 🏢 {local}")
                
                local_data = df_mapa[df_mapa['local_armazenamento'] == local]
                
                # Criar grid visual
                setores = local_data['setor'].unique()
                
                if len(setores) > 1:
                    cols = st.columns(len(setores))
                    
                    for i, setor in enumerate(setores):
                        if pd.notna(setor):
                            with cols[i]:
                                st.markdown(f"**🏢 Setor {setor}**")
                                
                                setor_data = local_data[local_data['setor'] == setor]
                                
                                for _, item in setor_data.iterrows():
                                    # Cor baseada no status
                                    if item['status'] == 'Vazio':
                                        cor = 'red'
                                    elif item['status'] == 'Baixo':
                                        cor = 'orange'
                                    elif item['status'] == 'Vencendo':
                                        cor = 'yellow'
                                    else:
                                        cor = 'green'
                                    
                                    st.markdown(f"""
                                    <div style="background-color: {cor}; padding: 0.3rem; margin: 0.2rem; border-radius: 3px; color: white; font-size: 0.8rem;">
                                        <strong>{item['medicamento'][:15]}...</strong><br>
                                        📍 P{item['prateleira'] or '?'}-{item['posicao'] or '?'}<br>
                                        📦 {item['quantidade_atual']} unidades
                                    </div>
                                    """, unsafe_allow_html=True)
                else:
                    # Layout simples para local sem setores
                    for _, item in local_data.iterrows():
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.write(f"**💊 {item['medicamento'][:20]}...**")
                        with col2:
                            st.write(f"📍 P{item['prateleira'] or '?'}-{item['posicao'] or '?'}")
                        with col3:
                            st.write(f"📦 {item['quantidade_atual']} un.")
                        with col4:
                            if item['status'] == 'Vazio':
                                st.write("🔴 Vazio")
                            elif item['status'] == 'Baixo':
                                st.write("🟡 Baixo")
                            elif item['status'] == 'Vencendo':
                                st.write("⚠️ Vencendo")
                            else:
                                st.write("🟢 OK")
                
                st.markdown("---")
        else:
            st.info("Nenhum medicamento com localização definida.")

def show_analise_preditiva():
    """Módulo de análise preditiva avançado com IA"""
    st.markdown("## 🔮 Análise Preditiva Inteligente")
    
    conn = st.session_state.db_manager.get_connection()
    
    # Buscar medicamentos com movimentação
    query = """
        SELECT 
            m.id,
            m.nome as medicamento,
            m.principio_ativo,
            m.categoria,
            SUM(l.quantidade_atual) as estoque_atual,
            COUNT(DISTINCT mov.id) as total_movimentacoes,
            AVG(CASE WHEN mov.tipo_movimento = 'Saída' THEN mov.quantidade ELSE 0 END) as consumo_medio,
            MAX(mov.data_movimento) as ultima_movimentacao
        FROM medicamentos m
        JOIN lotes l ON m.id = l.medicamento_id
        LEFT JOIN movimentacoes mov ON l.id = mov.lote_id
        WHERE m.ativo = 1 AND l.ativo = 1 AND l.quantidade_atual > 0
        GROUP BY m.id, m.nome, m.principio_ativo, m.categoria
        HAVING total_movimentacoes > 0
        ORDER BY consumo_medio DESC
    """
    
    df_medicamentos_pred = pd.read_sql(query, conn)
    
    if df_medicamentos_pred.empty:
        st.markdown("""
        <div class="ai-analysis">
            🤖 <strong>Sistema de Análise Preditiva</strong><br>
            Para usar a análise preditiva, você precisa de dados de movimentação.<br>
            📋 Cadastre medicamentos → 📦 Registre entradas → 📤 Registre saídas
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Como usar a análise preditiva:")
        st.markdown("""
        1. **Cadastre medicamentos** no sistema
        2. **Registre entradas** de lotes no estoque  
        3. **Registre saídas** (dispensações, receitas)
        4. **Aguarde alguns dias** para acumular histórico
        5. **Volte aqui** para ver as previsões inteligentes!
        """)
        conn.close()
        return
    
    # Dashboard de análise preditiva
    st.markdown("### 🤖 Dashboard Preditivo")
    
    # Métricas gerais
    total_medicamentos = len(df_medicamentos_pred)
    medicamentos_criticos = len(df_medicamentos_pred[df_medicamentos_pred['estoque_atual'] <= 10])
    medicamentos_sem_movimentacao = len(df_medicamentos_pred[df_medicamentos_pred['total_movimentacoes'] <= 2])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔮 Medicamentos Analisados", total_medicamentos)
    with col2:
        st.metric("🔴 Estoque Crítico", medicamentos_criticos)
    with col3:
        st.metric("📊 Baixa Movimentação", medicamentos_sem_movimentacao)
    with col4:
        previsoes_urgentes = 0  # Calculado abaixo
        st.metric("⚠️ Previsões Urgentes", previsoes_urgentes)
    
    # Análise individual por medicamento
    st.markdown("### 🔍 Análise Detalhada por Medicamento")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        categoria_filter = st.selectbox("📂 Filtrar por Categoria", 
            ["Todas"] + df_medicamentos_pred['categoria'].dropna().unique().tolist())
    
    with col2:
        urgencia_filter = st.selectbox("⚠️ Filtrar por Urgência", 
            ["Todas", "Crítico (< 7 dias)", "Atenção (< 15 dias)", "Normal (> 30 dias)"])
    
    # Processar cada medicamento
    medicamentos_processados = []
    
    for _, med in df_medicamentos_pred.iterrows():
        # Calcular consumo médio dos últimos 30 dias
        query_consumo = """
            SELECT 
                DATE(mov.data_movimento) as data,
                SUM(CASE WHEN mov.tipo_movimento = 'Saída' THEN mov.quantidade ELSE 0 END) as consumo_diario
            FROM movimentacoes mov
            JOIN lotes l ON mov.lote_id = l.id
            WHERE l.medicamento_id = ? 
            AND mov.data_movimento >= DATE('now', '-30 days')
            AND mov.tipo_movimento = 'Saída'
            GROUP BY DATE(mov.data_movimento)
            ORDER BY data DESC
        """
        
        df_consumo = pd.read_sql(query_consumo, conn, params=[med['id']])
        
        if not df_consumo.empty:
            consumo_medio_diario = df_consumo['consumo_diario'].mean()
            consumo_total_30dias = df_consumo['consumo_diario'].sum()
            
            # Previsões inteligentes
            if consumo_medio_diario > 0:
                dias_para_acabar = med['estoque_atual'] / consumo_medio_diario
                data_previsao_fim = datetime.now() + timedelta(days=int(dias_para_acabar))
                
                # Classificar urgência
                if dias_para_acabar < 7:
                    urgencia = "Crítico"
                    urgencia_cor = "🔴"
                elif dias_para_acabar < 15:
                    urgencia = "Atenção"
                    urgencia_cor = "🟡"
                elif dias_para_acabar < 30:
                    urgencia = "Baixo"
                    urgencia_cor = "🟠"
                else:
                    urgencia = "Normal"
                    urgencia_cor = "🟢"
                
                # Sugestões inteligentes de IA
                sugestoes = []
                if dias_para_acabar < 15:
                    quantidade_sugerida = consumo_medio_diario * 60  # 60 dias
                    sugestoes.append(f"Repor {quantidade_sugerida:.0f} unidades para 60 dias")
                
                if consumo_medio_diario > med['estoque_atual'] / 30:
                    sugestoes.append("Consumo acelerado detectado - monitorar de perto")
                
                if len(df_consumo) < 5:
                    sugestoes.append("Poucos dados históricos - previsão pode ser imprecisa")
                
                # Análise de tendência
                if len(df_consumo) >= 7:
                    consumo_recente = df_consumo.head(7)['consumo_diario'].mean()
                    consumo_anterior = df_consumo.tail(7)['consumo_diario'].mean()
                    
                    if consumo_recente > consumo_anterior * 1.2:
                        sugestoes.append("Tendência de aumento no consumo")
                    elif consumo_recente < consumo_anterior * 0.8:
                        sugestoes.append("Tendência de redução no consumo")
                
                medicamentos_processados.append({
                    'medicamento': med,
                    'consumo_medio_diario': consumo_medio_diario,
                    'dias_para_acabar': dias_para_acabar,
                    'data_previsao_fim': data_previsao_fim,
                    'urgencia': urgencia,
                    'urgencia_cor': urgencia_cor,
                    'sugestoes': sugestoes,
                    'df_consumo': df_consumo
                })
    
    # Aplicar filtros
    medicamentos_filtrados = medicamentos_processados.copy()
    
    if categoria_filter != "Todas":
        medicamentos_filtrados = [m for m in medicamentos_filtrados 
                                if m['medicamento']['categoria'] == categoria_filter]
    
    if urgencia_filter != "Todas":
        urgencia_map = {
            "Crítico (< 7 dias)": "Crítico",
            "Atenção (< 15 dias)": "Atenção", 
            "Normal (> 30 dias)": "Normal"
        }
        urgencia_target = urgencia_map[urgencia_filter]
        medicamentos_filtrados = [m for m in medicamentos_filtrados 
                                if m['urgencia'] == urgencia_target]
    
    # Contar previsões urgentes
    previsoes_urgentes = len([m for m in medicamentos_processados if m['urgencia'] in ["Crítico", "Atenção"]])
    
    # Exibir medicamentos processados
    if medicamentos_filtrados:
        for item in sorted(medicamentos_filtrados, key=lambda x: x['dias_para_acabar']):
            med = item['medicamento']
            
            st.markdown(f"""
            <div class="medicamento-card">
                <h4>{item['urgencia_cor']} {med['nome']} - {item['urgencia'].upper()}</h4>
                <p><strong>Previsão:</strong> Acabará em {int(item['dias_para_acabar'])} dias ({item['data_previsao_fim'].strftime('%d/%m/%Y')})</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔮 Ver Análise Completa"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📊 Métricas Atuais**")
                    st.write(f"**Estoque Atual:** {med['estoque_atual']} unidades")
                    st.write(f"**Consumo Médio:** {item['consumo_medio_diario']:.1f} unidades/dia")
                    st.write(f"**Dias Restantes:** {int(item['dias_para_acabar'])} dias")
                    st.write(f"**Categoria:** {med['categoria'] or 'N/A'}")
                
                with col2:
                    st.markdown("**🎯 Previsão Inteligente**")
                    st.write(f"**Data Prevista:** {item['data_previsao_fim'].strftime('%d/%m/%Y')}")
                    st.write(f"**Urgência:** {item['urgencia']}")
                    st.write(f"**Total Movimentações:** {med['total_movimentacoes']}")
                    if med['ultima_movimentacao']:
                        ultima = datetime.strptime(med['ultima_movimentacao'], '%Y-%m-%d %H:%M:%S')
                        st.write(f"**Última Movimentação:** {ultima.strftime('%d/%m/%Y')}")
                
                with col3:
                    st.markdown("**🤖 Sugestões da IA**")
                    if item['sugestoes']:
                        for sugestao in item['sugestoes']:
                            st.write(f"• {sugestao}")
                    else:
                        st.write("• Estoque adequado")
                        st.write("• Continuar monitoramento")
                
                # Alertas específicos
                if item['urgencia'] == "Crítico":
                    st.markdown(f"""
                    <div class="alert-danger">
                        🚨 <strong>AÇÃO URGENTE NECESSÁRIA!</strong><br>
                        Este medicamento pode acabar em menos de 7 dias. Solicite reposição imediatamente.
                    </div>
                    """, unsafe_allow_html=True)
                elif item['urgencia'] == "Atenção":
                    st.markdown(f"""
                    <div class="alert-warning">
                        ⚠️ <strong>Atenção Necessária!</strong><br>
                        Este medicamento precisa de reposição em breve. Planeje a compra.
                    </div>
                    """, unsafe_allow_html=True)
                
                # Gráfico de consumo
                if len(item['df_consumo']) > 1:
                    st.markdown("**📈 Tendência de Consumo (30 dias)**")
                    
                    fig = px.line(item['df_consumo'], x='data', y='consumo_diario', 
                                 title="Consumo Diário", markers=True)
                    fig.add_hline(y=item['consumo_medio_diario'], line_dash="dash", 
                                 annotation_text=f"Média: {item['consumo_medio_diario']:.1f}")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Simulador de cenários
                st.markdown("**🎲 Simulador de Cenários**")
                col1, col2 = st.columns(2)
                
                with col1:
                    novo_consumo = st.slider("Consumo Diário Simulado", 
                                           min_value=0.0, 
                                           max_value=item['consumo_medio_diario'] * 3,
                                           value=item['consumo_medio_diario'],
                                           step=0.1,
                                           key=f"sim_{med['id']}")
                
                with col2:
                    if novo_consumo > 0:
                        novos_dias = med['estoque_atual'] / novo_consumo
                        nova_data = datetime.now() + timedelta(days=int(novos_dias))
                        st.write(f"**Novo Cenário:**")
                        st.write(f"Durará {int(novos_dias)} dias")
                        st.write(f"Até {nova_data.strftime('%d/%m/%Y')}")
    else:
        st.info("Nenhum medicamento encontrado com os filtros aplicados.")
    
    conn.close()

def create_smart_alert(tipo_alerta, prioridade, titulo, mensagem, paciente_id=None, medicamento_id=None, usuario_destinatario=None):
    """Criar alerta inteligente"""
    try:
        conn = st.session_state.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO alertas_inteligentes (
                tipo_alerta, prioridade, titulo, mensagem, paciente_id, 
                medicamento_id, usuario_destinatario
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tipo_alerta, prioridade, titulo, mensagem, paciente_id, medicamento_id, usuario_destinatario))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar alerta: {e}")

def show_pacientes():
    """Módulo de pacientes com IA"""
    st.markdown("## 👥 Gestão Inteligente de Pacientes")
    
    # Verificar permissões
    if 'criar' in st.session_state.permissions.get('pacientes', []):
        tab1, tab2, tab3 = st.tabs(["📋 Lista de Pacientes", "➕ Cadastrar Paciente", "🤖 Insights de IA"])
    else:
        tab1, tab2, tab3 = st.tabs(["📋 Lista de Pacientes", "", "🤖 Insights de IA"])
    
    with tab1:
        st.markdown("### 📋 Pacientes com Informações Inteligentes")
        
        # Filtros avançados
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Buscar paciente", placeholder="Nome ou CPF")
        
        with col2:
            conn = st.session_state.db_manager.get_connection()
            planos = pd.read_sql("SELECT DISTINCT plano_saude FROM pacientes WHERE plano_saude IS NOT NULL", conn)['plano_saude'].tolist()
            plano_filter = st.selectbox("🏥 Plano de Saúde", ["Todos"] + planos)
        
        with col3:
            idade_filter = st.selectbox("👶 Faixa Etária", ["Todas", "Criança (0-12)", "Adolescente (13-17)", "Adulto (18-64)", "Idoso (65+)"])
        
        # Buscar pacientes com estatísticas
        query = """
            SELECT 
                p.*,
                u.nome_completo as cadastrado_por_nome,
                COUNT(DISTINCT c.id) as total_consultas,
                COUNT(DISTINCT r.id) as total_receitas,
                COUNT(DISTINCT pr.id) as total_prontuario,
                MAX(c.data_consulta) as ultima_consulta
            FROM pacientes p
            LEFT JOIN usuarios u ON p.cadastrado_por = u.id
            LEFT JOIN consultas c ON p.id = c.paciente_id
            LEFT JOIN receitas r ON p.id = r.paciente_id
            LEFT JOIN prontuario pr ON p.id = pr.paciente_id
            WHERE p.ativo = 1
        """
        params = []
        
        if search_term:
            query += " AND (p.nome_completo LIKE ? OR p.cpf LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if plano_filter != "Todos":
            query += " AND p.plano_saude = ?"
            params.append(plano_filter)
        
        query += " GROUP BY p.id ORDER BY p.nome_completo"
        
        df_pacientes = pd.read_sql(query, conn, params=params)
        
        # Aplicar filtro de idade
        if idade_filter != "Todas" and not df_pacientes.empty:
            hoje = datetime.now().date()
            df_pacientes_filtrados = []
            
            for _, pac in df_pacientes.iterrows():
                if pac['data_nascimento']:
                    nascimento = datetime.strptime(pac['data_nascimento'], '%Y-%m-%d').date()
                    idade = (hoje - nascimento).days // 365
                    
                    incluir = False
                    if idade_filter == "Criança (0-12)" and idade <= 12:
                        incluir = True
                    elif idade_filter == "Adolescente (13-17)" and 13 <= idade <= 17:
                        incluir = True
                    elif idade_filter == "Adulto (18-64)" and 18 <= idade <= 64:
                        incluir = True
                    elif idade_filter == "Idoso (65+)" and idade >= 65:
                        incluir = True
                    
                    if incluir:
                        df_pacientes_filtrados.append(pac)
            
            df_pacientes = pd.DataFrame(df_pacientes_filtrados)
        
        conn.close()
        
        if not df_pacientes.empty:
            # Estatísticas gerais
            total_pacientes = len(df_pacientes)
            pacientes_ativos = len(df_pacientes[df_pacientes['total_consultas'] > 0])
            pacientes_cronicos = len(df_pacientes[df_pacientes['medicamentos_uso_continuo'].notna()])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 Total de Pacientes", total_pacientes)
            with col2:
                st.metric("🏥 Pacientes Ativos", pacientes_ativos)
            with col3:
                st.metric("💊 Uso Contínuo", pacientes_cronicos)
            
            # Lista inteligente de pacientes
            for _, pac in df_pacientes.iterrows():
                # Calcular idade
                idade = "N/A"
                if pac['data_nascimento']:
                    nascimento = datetime.strptime(pac['data_nascimento'], '%Y-%m-%d').date()
                    idade = (datetime.now().date() - nascimento).days // 365
                
                # Status do paciente
                if pac['total_consultas'] == 0:
                    status_icon = "🆕"
                    status_text = "Novo"
                elif pac['ultima_consulta']:
                    ultima = datetime.strptime(pac['ultima_consulta'], '%Y-%m-%d %H:%M:%S')
                    dias_ultima = (datetime.now() - ultima).days
                    if dias_ultima > 90:
                        status_icon = "😴"
                        status_text = "Inativo"
                    else:
                        status_icon = "✅"
                        status_text = "Ativo"
                else:
                    status_icon = "📋"
                    status_text = "Pendente"
                
                # Card do paciente
                with st.expander(f"{status_icon} {pac['nome_completo']} ({idade} anos) - {status_text}"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("**👤 Dados Pessoais**")
                        st.write(f"**Nome:** {pac['nome_completo']}")
                        st.write(f"**CPF:** {pac['cpf'] or 'N/A'}")
                        st.write(f"**Idade:** {idade} anos")
                        st.write(f"**Sexo:** {pac['sexo'] or 'N/A'}")
                        st.write(f"**Telefone:** {pac['telefone'] or 'N/A'}")
                    
                    with col2:
                        st.markdown("**🏥 Informações Médicas**")
                        st.write(f"**Consultas:** {pac['total_consultas']}")
                        st.write(f"**Receitas:** {pac['total_receitas']}")
                        st.write(f"**Prontuário:** {pac['total_prontuario']} entradas")
                        if pac['ultima_consulta']:
                            ultima = datetime.strptime(pac['ultima_consulta'], '%Y-%m-%d %H:%M:%S')
                            st.write(f"**Última Consulta:** {ultima.strftime('%d/%m/%Y')}")
                    
                    with col3:
                        st.markdown("**🏠 Contato e Plano**")
                        st.write(f"**Email:** {pac['email'] or 'N/A'}")
                        st.write(f"**Cidade:** {pac['cidade'] or 'N/A'}")
                        st.write(f"**Plano:** {pac['plano_saude'] or 'N/A'}")
                        st.write(f"**Emergência:** {pac['contato_emergencia'] or 'N/A'}")
                    
                    with col4:
                        st.markdown("**⚕️ Condições Especiais**")
                        if pac['alergias']:
                            st.write(f"**🚨 Alergias:** {pac['alergias']}")
                        if pac['medicamentos_uso_continuo']:
                            st.write(f"**💊 Uso Contínuo:** {pac['medicamentos_uso_continuo']}")
                        if pac['historico_familiar']:
                            st.write(f"**👨‍👩‍👧‍👦 Histórico Familiar:** {pac['historico_familiar']}")
                    
                    # Insights de IA
                    insights = []
                    if idade != "N/A" and idade >= 65:
                        insights.append("👴 Paciente idoso - considerar cuidados especiais")
                    if pac['medicamentos_uso_continuo']:
                        insights.append("💊 Uso contínuo de medicamentos - verificar interações")
                    if pac['total_consultas'] > 10:
                        insights.append("🏥 Paciente frequente - considerar plano de cuidados")
                    if pac['alergias']:
                        insights.append("🚨 Paciente com alergias conhecidas")
                    
                    if insights
