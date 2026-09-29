import sqlite3
from pathlib import Path
from datetime import date

from models import Gerente, Posto, Turno


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "turnos.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gerentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS postos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia TEXT NOT NULL,
            gerente_id INTEGER NOT NULL,
            posto_id INTEGER NOT NULL,

            FOREIGN KEY (gerente_id)
                REFERENCES gerentes(id),

            FOREIGN KEY (posto_id)
                REFERENCES postos(id)
        )
    """)

    connection.commit()
    connection.close()


def get_gerentes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM gerentes
        ORDER BY nome
    """)

    resultados = cursor.fetchall()

    connection.close()

    return [
        Gerente(id=id_, nome=nome)
        for id_, nome in resultados
    ]


def get_postos():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM postos
        ORDER BY nome
    """)

    resultados = cursor.fetchall()

    connection.close()

    return [
        Posto(id=id_, nome=nome)
        for id_, nome in resultados
    ]


def criar_turno(gerente, posto):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO turnos (
            dia,
            gerente_id,
            posto_id
        )
        VALUES (?, ?, ?)
    """, (
        date.today().isoformat(),
        gerente.id,
        posto.id
    ))

    turno_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return Turno(
        id=turno_id,
        dia=date.today(),
        gerente=gerente,
        posto=posto
    )


def get_turnos():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            t.id,
            t.dia,
            g.id,
            g.nome,
            p.id,
            p.nome
        FROM turnos t
        INNER JOIN gerentes g
            ON t.gerente_id = g.id
        INNER JOIN postos p
            ON t.posto_id = p.id
        ORDER BY t.dia DESC, t.id DESC
    """)

    resultados = cursor.fetchall()

    connection.close()

    turnos = []

    for (
        turno_id,
        dia,
        gerente_id,
        gerente_nome,
        posto_id,
        posto_nome
    ) in resultados:

        gerente = Gerente(
            id=gerente_id,
            nome=gerente_nome
        )

        posto = Posto(
            id=posto_id,
            nome=posto_nome
        )

        turno = Turno(
            id=turno_id,
            dia=date.fromisoformat(dia),
            gerente=gerente,
            posto=posto
        )

        turnos.append(turno)

    return turnos

def atualizar_turno(turno_id, gerente, posto, dia):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE turnos
        SET dia = ?,
            gerente_id = ?,
            posto_id = ?
        WHERE id = ?
    """, (
        dia.isoformat() if hasattr(dia, "isoformat") else str(dia),
        gerente.id,
        posto.id,
        turno_id
    ))

    connection.commit()
    connection.close()


def apagar_turno(turno_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM turnos
        WHERE id = ?
    """, (turno_id,))

    connection.commit()
    connection.close()