from dataclasses import dataclass
from datetime import date


@dataclass
class Gerente:
    id: int
    nome: str


@dataclass
class Posto:
    id: int
    nome: str


@dataclass
class Turno:
    id: int
    dia: date
    gerente: Gerente
    posto: Posto