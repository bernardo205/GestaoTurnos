from database import get_connection


GERENTES_INICIAIS = [
    "Andre Miguel",
    "Andre Ribeiro",
    "Mariana",
    "Estela",
    "Vitoria",
    "Rita",
    "Raquel",
]

POSTOS_INICIAIS = [
    "Iniciador",
    "Condimentador",
    "Finalizador",
    "Fritadeira",
    "Grelhador",
    "Batata",
    "Caixa",
    "Drive 1",
    "Drive 2",
    "Speaker 2",
    "Bebidas",
    "Runner",
    "Expedidor",
    "Apresentador",
    "Sala",
    "SAM",

]


def inserir_dados_iniciais():
    connection = get_connection()
    cursor = connection.cursor()

    for nome in GERENTES_INICIAIS:
        cursor.execute(
            """
            INSERT OR IGNORE INTO gerentes (nome)
            VALUES (?)
            """,
            (nome,)
        )

    for nome in POSTOS_INICIAIS:
        cursor.execute(
            """
            INSERT OR IGNORE INTO postos (nome)
            VALUES (?)
            """,
            (nome,)
        )

    connection.commit()
    connection.close()