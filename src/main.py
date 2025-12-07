from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid # Biblioteca para gerar tokens

app = FastAPI(
    title="SGHSS - API VidaPlus",
    description="Sistema de Gestão Hospitalar - Projeto Desenvolvimento Back-end.",
    version="1.2.0" 
)

# --- DADOS ---
class Paciente(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    email: str
    senha: str 

class Medico(BaseModel):
    id: Optional[int] = None
    nome: str
    crm: str
    especialidade: str

class Consulta(BaseModel):
    id: Optional[int] = None
    id_paciente: int
    id_medico: int
    data_horario: str
    motivo: str

#  Login
class LoginData(BaseModel):
    email: str
    senha: str

# --- BANCO DE DADOS (Memória) ---
db_pacientes: List[Paciente] = []
db_medicos: List[Medico] = []
db_consultas: List[Consulta] = []

# --- ROTAS GERAIS ---
@app.get("/", tags=["Status"])
def home():
    return {"status": "Sistema VidaPlus operando normalmente"}

# --- ROTAS DE AUTENTICAÇÃO  ---
@app.post("/login", tags=["Segurança (Auth)"])
def login(dados: LoginData):
    # 1. Procura o usuário no banco de pacientes
    usuario_encontrado = False
    
    # Verifica se existe alguém com esse email e senha
    for p in db_pacientes:
        if p.email == dados.email and p.senha == dados.senha:
            usuario_encontrado = True
            break
    
    # 2. Se sim, gera um token
    if usuario_encontrado:
        token_f = str(uuid.uuid4()) # Gera algo como "a8098c1a-f86e-11da-bd1a..."
        return {
            "mensagem": "Login realizado com sucesso",
            "token": token_f,
            "tipo": "Bearer"
        }
    else:
        # Se errou senha ou email
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

# --- ROTAS DE PACIENTES ---
@app.get("/pacientes", tags=["Pacientes"])
def listar_pacientes():
    return db_pacientes

@app.post("/pacientes", tags=["Pacientes"], status_code=201)
def criar_paciente(paciente: Paciente):
    paciente.id = len(db_pacientes) + 1
    db_pacientes.append(paciente)
    return paciente

# --- ROTAS DE MÉDICOS ---
@app.get("/medicos", tags=["Médicos"])
def listar_medicos():
    return db_medicos

@app.post("/medicos", tags=["Médicos"], status_code=201)
def criar_medico(medico: Medico):
    medico.id = len(db_medicos) + 1
    db_medicos.append(medico)
    return medico

# --- ROTAS DE CONSULTAS ---
@app.post("/consultas", tags=["Agendamentos"], status_code=201)
def agendar_consulta(consulta: Consulta):
    # Validações simplificadas
    if consulta.id_paciente > len(db_pacientes) or consulta.id_medico > len(db_medicos):
         raise HTTPException(status_code=404, detail="Paciente ou Médico não encontrado")
    
    consulta.id = len(db_consultas) + 1
    db_consultas.append(consulta)
    return consulta

@app.get("/consultas", tags=["Agendamentos"])
def listar_consultas():
    return db_consultas