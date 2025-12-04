from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="SGHSS - API VidaPlus",
    description="Sistema de Gestão Hospitalar - Projeto Multidisciplinar 2025",
    version="1.1.0"
)

# --- MODELOS DE DADOS (As Entidades) ---
class Paciente(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    email: str

class Medico(BaseModel):
    id: Optional[int] = None
    nome: str
    crm: str
    especialidade: str

class Consulta(BaseModel):
    id: Optional[int] = None
    id_paciente: int
    id_medico: int
    data_horario: str  # Ex: "2025-10-10 14:00"
    motivo: str

# --- BANCO DE DADOS (Simulado em Memória) ---
# Usamos listas para guardar os dados enquanto o programa roda
db_pacientes: List[Paciente] = []
db_medicos: List[Medico] = []
db_consultas: List[Consulta] = []

# --- ROTAS GERAIS ---
@app.get("/", tags=["Status"])
def home():
    return {"status": "Sistema VidaPlus operando normalmente"}

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

# --- ROTAS DE CONSULTAS (Lógica de Negócio) ---
@app.get("/consultas", tags=["Agendamentos"])
def listar_consultas():
    return db_consultas

@app.post("/consultas", tags=["Agendamentos"], status_code=201)
def agendar_consulta(consulta: Consulta):
    # 1. Validar se o paciente existe
    paciente_encontrado = False
    for p in db_pacientes:
        if p.id == consulta.id_paciente:
            paciente_encontrado = True
            break
    
    if not paciente_encontrado:
        raise HTTPException(status_code=404, detail="Paciente não encontrado!")

    # 2. Validar se o médico existe
    medico_encontrado = False
    for m in db_medicos:
        if m.id == consulta.id_medico:
            medico_encontrado = True
            break
            
    if not medico_encontrado:
        raise HTTPException(status_code=404, detail="Médico não encontrado!")

    # 3. Se tudo ok, agendar
    consulta.id = len(db_consultas) + 1
    db_consultas.append(consulta)
    return consulta