"""
🏥 MedStock360 - Configurações do Sistema
Arquivo de configuração centralizada
Versão: 3.0 Advanced
"""

import os
from datetime import timedelta

class Config:
    """Configurações principais do sistema"""
    
    # ==========================================
    # INFORMAÇÕES DO SISTEMA
    # ==========================================
    SYSTEM_NAME = "MedStock360 Advanced"
    SYSTEM_VERSION = "3.0"
    SYSTEM_SUBTITLE = "Sistema Hospitalar Completo Multi-usuário"
    
    # ==========================================
    # CONFIGURAÇÕES DE BANCO DE DADOS
    # ==========================================
    DATABASE_PATH = "data/medstock360.db"
    BACKUP_PATH = "backups/"
    LOGS_PATH = "logs/"
    
    # Backup automático (em horas)
    AUTO_BACKUP_INTERVAL = 6
    
    # Retenção de backups (em dias)
    BACKUP_RETENTION_DAYS = 30
    
    # ==========================================
    # CONFIGURAÇÕES DE SEGURANÇA
    # ==========================================
    
    # Senha padrão do administrador (MUDE IMEDIATAMENTE!)
    DEFAULT_ADMIN_PASSWORD = "admin123"
    
    # Configurações de senha
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_REQUIRE_UPPERCASE = False
    PASSWORD_REQUIRE_LOWERCASE = False
    PASSWORD_REQUIRE_NUMBERS = False
    PASSWORD_REQUIRE_SYMBOLS = False
    
    # Configurações de sessão
    SESSION_LIFETIME_HOURS = 8
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15
    
    # ==========================================
    # CONFIGURAÇÕES DE ESTOQUE
    # ==========================================
    
    # Alertas de estoque
    ESTOQUE_CRITICO = 10  # unidades
    ESTOQUE_BAIXO = 50    # unidades
    
    # Alertas de vencimento (em dias)
    VENCIMENTO_CRITICO = 7    # dias
    VENCIMENTO_ATENCAO = 30   # dias
    VENCIMENTO_ALERTA = 60    # dias
    
    # ==========================================
    # ANÁLISE PREDITIVA
    # ==========================================
    
    # Período para cálculo de consumo (em dias)
    PERIODO_ANALISE_CONSUMO = 30
    
    # Dias mínimos de estoque sugerido
    ESTOQUE_SUGERIDO_DIAS = 60
    
    # Mínimo de movimentações para análise
    MIN_MOVIMENTACOES_ANALISE = 3
    
    # ==========================================
    # CONFIGURAÇÕES DE INTERFACE
    # ==========================================
    
    # Tema da aplicação
    THEME = "light"  # "light" ou "dark"
    
    # Idioma
    LANGUAGE = "pt_BR"
    
    # Fuso horário
    TIMEZONE = "America/Sao_Paulo"
    
    # Formato de data
    DATE_FORMAT = "%d/%m/%Y"
    DATETIME_FORMAT = "%d/%m/%Y %H:%M"
    
    # ==========================================
    # CONFIGURAÇÕES DE RELATÓRIOS
    # ==========================================
    
    # Número máximo de itens por página
    ITEMS_PER_PAGE = 50
    
    # Formatos de exportação disponíveis
    EXPORT_FORMATS = ["CSV", "Excel", "PDF"]
    
    # ==========================================
    # CONFIGURAÇÕES DE EMAIL (OPCIONAL)
    # ==========================================
    
    # Servidor SMTP (descomente e configure se necessário)
    SMTP_SERVER = None  # "smtp.gmail.com"
    SMTP_PORT = None    # 587
    SMTP_USERNAME = None
    SMTP_PASSWORD = None
    SMTP_USE_TLS = True
    
    # Email do sistema
    SYSTEM_EMAIL = None  # "sistema@hospital.com"
    
    # ==========================================
    # CONFIGURAÇÕES AVANÇADAS
    # ==========================================
    
    # Modo debug (apenas para desenvolvimento)
    DEBUG_MODE = False
    
    # Log level
    LOG_LEVEL = "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR"
    
    # Cache de sessão (em segundos)
    CACHE_TIMEOUT = 3600  # 1 hora
    
    # Número máximo de tentativas de reconexão com banco
    MAX_DB_RETRIES = 3
    
    # ==========================================
    # PERFIS DE USUÁRIO E PERMISSÕES
    # ==========================================
    
    USER_ROLES = {
        'Administrador': {
            'usuarios': ['criar', 'editar', 'visualizar', 'excluir'],
            'medicamentos': ['criar', 'editar', 'visualizar', 'excluir'],
            'estoque': ['criar', 'editar', 'visualizar', 'excluir'],
            'pacientes': ['criar', 'editar', 'visualizar', 'excluir'],
            'consultas': ['criar', 'editar', 'visualizar', 'excluir'],
            'receitas': ['criar', 'editar', 'visualizar', 'excluir'],
            'relatorios': ['visualizar', 'exportar'],
            'analise_preditiva': ['visualizar']
        },
        'Farmacêutico': {
            'medicamentos': ['criar', 'editar', 'visualizar'],
            'estoque': ['criar', 'editar', 'visualizar'],
            'receitas': ['visualizar', 'dispensar'],
            'pacientes': ['visualizar'],
            'relatorios': ['visualizar'],
            'analise_preditiva': ['visualizar']
        },
        'Médico': {
            'pacientes': ['criar', 'editar', 'visualizar'],
            'consultas': ['criar', 'editar', 'visualizar'],
            'receitas': ['criar', 'editar', 'visualizar'],
            'medicamentos': ['visualizar'],
            'relatorios': ['visualizar']
        },
        'Enfermeiro': {
            'pacientes': ['visualizar', 'editar'],
            'consultas': ['visualizar'],
            'medicamentos': ['visualizar'],
            'estoque': ['visualizar'],
            'receitas': ['visualizar']
        }
    }
    
    # ==========================================
    # CATEGORIAS PADRÃO
    # ==========================================
    
    CATEGORIAS_MEDICAMENTOS = [
        "Analgésicos",
        "Anti-inflamatórios", 
        "Antibióticos",
        "Antidepressivos",
        "Anti-hipertensivos",
        "Vitaminas",
        "Controlados",
        "Outros"
    ]
    
    VIAS_ADMINISTRACAO = [
        "Oral",
        "Intravenosa",
        "Intramuscular", 
        "Subcutânea",
        "Tópica",
        "Oftálmica",
        "Nasal",
        "Retal",
        "Outras"
    ]
    
    TEMPERATURAS_ARMAZENAMENTO = [
        "Ambiente (15°C a 30°C)",
        "Refrigerado (2°C a 8°C)",
        "Congelado (-20°C)",
        "Controlada (20°C a 25°C)"
    ]
    
    LOCAIS_ARMAZENAMENTO = [
        "Farmácia Central",
        "Sala de Medicamentos",
        "Geladeira",
        "Cofre (Controlados)",
        "Almoxarifado",
        "UTI",
        "Pronto Socorro"
    ]
    
    TIPOS_CONSULTA = [
        "Consulta inicial",
        "Retorno",
        "Emergência",
        "Exame",
        "Procedimento",
        "Teleconsulta",
        "Outros"
    ]
    
    # ==========================================
    # CONFIGURAÇÕES DE DESENVOLVIMENTO
    # ==========================================
    
    # Para desenvolvedores: habilitar features experimentais
    ENABLE_EXPERIMENTAL_FEATURES = False
    
    # Para desenvolvedores: mostrar informações de debug
    SHOW_DEBUG_INFO = False

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def get_config_value(key, default=None):
    """Obter valor de configuração com fallback"""
    return getattr(Config, key, default)

def is_debug_mode():
    """Verificar se está em modo debug"""
    return Config.DEBUG_MODE

def get_database_path():
    """Obter caminho do banco de dados"""
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    return Config.DATABASE_PATH

def get_backup_path():
    """Obter caminho dos backups"""
    os.makedirs(Config.BACKUP_PATH, exist_ok=True)
    return Config.BACKUP_PATH

def get_logs_path():
    """Obter caminho dos logs"""
    os.makedirs(Config.LOGS_PATH, exist_ok=True)
    return Config.LOGS_PATH

# ==========================================
# VALIDAÇÕES
# ==========================================

def validate_config():
    """Validar configurações do sistema"""
    errors = []
    
    # Validar caminhos
    if not Config.DATABASE_PATH:
        errors.append("DATABASE_PATH não pode estar vazio")
    
    # Validar configurações de estoque
    if Config.ESTOQUE_CRITICO >= Config.ESTOQUE_BAIXO:
        errors.append("ESTOQUE_CRITICO deve ser menor que ESTOQUE_BAIXO")
    
    # Validar configurações de vencimento
    if Config.VENCIMENTO_CRITICO >= Config.VENCIMENTO_ATENCAO:
        errors.append("VENCIMENTO_CRITICO deve ser menor que VENCIMENTO_ATENCAO")
    
    return errors

# Executar validação na importação
_config_errors = validate_config()
if _config_errors:
    print("⚠️ AVISOS DE CONFIGURAÇÃO:")
    for error in _config_errors:
        print(f"  - {error}")
    print()

# ==========================================
# CONFIGURAÇÕES ESPECÍFICAS POR AMBIENTE
# ==========================================

# Detectar ambiente
ENVIRONMENT = os.getenv('MEDSTOCK_ENV', 'production')

if ENVIRONMENT == 'development':
    Config.DEBUG_MODE = True
    Config.LOG_LEVEL = "DEBUG"
    Config.SHOW_DEBUG_INFO = True
elif ENVIRONMENT == 'testing':
    Config.DATABASE_PATH = "data/test_medstock360.db"
    Config.DEBUG_MODE = True

print(f"🏥 MedStock360 v{Config.SYSTEM_VERSION} - Ambiente: {ENVIRONMENT}")
print(f"📁 Banco de dados: {Config.DATABASE_PATH}")
print(f"🔧 Modo debug: {'Ativo' if Config.DEBUG_MODE else 'Inativo'}")
print()