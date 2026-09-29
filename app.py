import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    create_tables,
    get_gerentes,
    get_postos,
    criar_turno,
    get_turnos,
    atualizar_turno,
    apagar_turno,
)

from seed import inserir_dados_iniciais


def inicializar_aplicacao():
    create_tables()
    inserir_dados_iniciais()


inicializar_aplicacao()


st.set_page_config(
    page_title="Gestão de Turnos",
    page_icon="📋",
    layout="wide",
)


# ---------------------------------------------------------------
# PALETAS E MAPAS DE CORES
# ---------------------------------------------------------------
PALETA_GERENTES = px.colors.qualitative.Dark24 + px.colors.qualitative.Set3
PALETA_POSTOS = px.colors.qualitative.Bold + px.colors.qualitative.Pastel


def construir_mapa_cores(nomes, paleta):
    """Atribui uma cor fixa a cada nome (ordem alfabética)."""
    nomes_ordenados = sorted(set(nomes))
    return {
        nome: paleta[i % len(paleta)]
        for i, nome in enumerate(nomes_ordenados)
    }


def mostrar_legenda_cores(mapa, titulo):
    """Mostra pequenos chips com o nome e a cor respetiva."""
    st.markdown(f"**{titulo}**")
    chips = " ".join(
        f"<span style='"
        f"display:inline-block;"
        f"padding:4px 10px;"
        f"margin:3px 4px 3px 0;"
        f"border-radius:14px;"
        f"background:{cor};"
        f"color:white;"
        f"font-size:0.85em;"
        f"font-weight:500;"
        f"'>{nome}</span>"
        for nome, cor in mapa.items()
    )
    st.markdown(chips, unsafe_allow_html=True)


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def turnos_para_dataframe(turnos, incluir_id=False):
    dados = []
    for t in turnos:
        linha = {
            "Data": pd.to_datetime(t.dia),
            "Gerente": t.gerente.nome,
            "Posto": t.posto.nome,
        }
        if incluir_id:
            linha = {"ID": t.id, **linha}
        dados.append(linha)
    return pd.DataFrame(dados)


def grafico_circular(contagens, titulo, color_map):
    df = contagens.reset_index()
    df.columns = ["Categoria", "Turnos"]
    df = df[df["Turnos"] > 0]

    fig = px.pie(
        df,
        names="Categoria",
        values="Turnos",
        hole=0.4,
        color="Categoria",
        color_discrete_map=color_map,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Turnos: %{value}<extra></extra>",
        marker=dict(line=dict(color="white", width=2)),
    )
    fig.update_layout(
        title=titulo,
        showlegend=True,
        margin=dict(t=50, b=10, l=10, r=10),
        height=420,
    )
    return fig


# ---------------------------------------------------------------
# DADOS BASE
# ---------------------------------------------------------------
st.title("📋 Gestão de Turnos")

gerentes = get_gerentes()
postos = get_postos()

mapa_cores_gerentes = construir_mapa_cores(
    [g.nome for g in gerentes],
    PALETA_GERENTES,
)
mapa_cores_postos = construir_mapa_cores(
    [p.nome for p in postos],
    PALETA_POSTOS,
)

aba_registar, aba_historico, aba_editar, aba_estatisticas = st.tabs(
    ["➕ Registar", "📋 Histórico", "✏️ Editar", "📊 Estatísticas"]
)


# ---------------------------------------------------------------
# ABA REGISTAR
# ---------------------------------------------------------------
with aba_registar:

    st.write(
        "Regista o gerente e o posto do turno. "
        "A data é preenchida automaticamente."
    )

    if not gerentes:
        st.error("Não existem gerentes registados na base de dados.")

    elif not postos:
        st.error("Não existem postos registados na base de dados.")

    else:

        col1, col2 = st.columns(2)

        with col1:
            gerente_selecionado = st.selectbox(
                "Gerente",
                gerentes,
                format_func=lambda g: g.nome,
                key="reg_gerente",
            )

        with col2:
            posto_selecionado = st.selectbox(
                "Posto",
                postos,
                format_func=lambda p: p.nome,
                key="reg_posto",
            )

        if st.button("Registar Turno", type="primary", width="stretch"):

            turno = criar_turno(gerente_selecionado, posto_selecionado)

            st.success(
                f"Turno registado com sucesso: "
                f"{turno.gerente.nome} → {turno.posto.nome} "
                f"({turno.dia.strftime('%d/%m/%Y')})"
            )


# ---------------------------------------------------------------
# ABA HISTÓRICO
# ---------------------------------------------------------------
with aba_historico:

    turnos = get_turnos()

    if not turnos:
        st.info("Ainda não existem turnos registados.")

    else:

        df = turnos_para_dataframe(turnos, incluir_id=False).copy()
        df["Data"] = df["Data"].dt.strftime("%d/%m/%Y")

        st.dataframe(df, width="stretch", hide_index=True)


# ---------------------------------------------------------------
# ABA EDITAR / APAGAR
# ---------------------------------------------------------------
with aba_editar:

    st.subheader("✏️ Editar ou apagar turno")

    turnos = get_turnos()

    if not turnos:
        st.info("Ainda não existem turnos registados.")

    elif not gerentes or not postos:
        st.error("Faltam gerentes ou postos na base de dados.")

    else:

        opcoes = {
            f"#{t.id} • {t.dia.strftime('%d/%m/%Y')} • "
            f"{t.gerente.nome} → {t.posto.nome}": t
            for t in turnos
        }

        escolha = st.selectbox(
            "Seleciona o turno a editar",
            list(opcoes.keys()),
            key="edit_turno",
        )
        turno_sel = opcoes[escolha]

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            idx_gerente = next(
                (i for i, g in enumerate(gerentes)
                 if g.id == turno_sel.gerente.id),
                0,
            )
            gerente_novo = st.selectbox(
                "Gerente",
                gerentes,
                index=idx_gerente,
                format_func=lambda g: g.nome,
                key="edit_gerente",
            )

        with col2:
            idx_posto = next(
                (i for i, p in enumerate(postos)
                 if p.id == turno_sel.posto.id),
                0,
            )
            posto_novo = st.selectbox(
                "Posto",
                postos,
                index=idx_posto,
                format_func=lambda p: p.nome,
                key="edit_posto",
            )

        with col3:
            data_nova = st.date_input(
                "Data",
                value=turno_sel.dia,
                key="edit_data",
            )

        st.divider()

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button(
                "💾 Guardar alterações",
                type="primary",
                width="stretch",
            ):
                atualizar_turno(
                    turno_sel.id,
                    gerente_novo,
                    posto_novo,
                    data_nova,
                )
                st.success("Turno atualizado com sucesso.")
                st.rerun()

        with col_b:
            apagar_confirmado = st.checkbox(
                "Confirmo que quero apagar este turno",
                key="confirmar_apagar",
            )

            if st.button(
                "🗑️ Apagar turno",
                width="stretch",
                disabled=not apagar_confirmado,
            ):
                apagar_turno(turno_sel.id)
                st.success("Turno apagado.")
                st.rerun()


# ---------------------------------------------------------------
# ABA ESTATÍSTICAS
# ---------------------------------------------------------------
with aba_estatisticas:

    turnos = get_turnos()

    if not turnos:
        st.info("Ainda não existem turnos para gerar estatísticas.")

    else:

        df = turnos_para_dataframe(turnos)
        df["Mês"] = df["Data"].dt.strftime("%Y-%m")

        contagem_postos = (
            df["Posto"].value_counts().sort_values(ascending=False)
        )
        contagem_gerentes = (
            df["Gerente"].value_counts().sort_values(ascending=False)
        )

        posto_top = contagem_postos.idxmax()
        gerente_top = contagem_gerentes.idxmax()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total de turnos", int(len(df)))
        c2.metric(
            "🏆 Posto mais frequente",
            posto_top,
            f"{int(contagem_postos.max())} turnos",
        )
        c3.metric(
            "🤝 Gerente com quem mais trabalhaste",
            gerente_top,
            f"{int(contagem_gerentes.max())} turnos",
        )

        st.divider()

        col_p, col_g = st.columns(2)

        with col_p:
            fig_postos = grafico_circular(
                contagem_postos,
                "Turnos por posto",
                mapa_cores_postos,
            )
            st.plotly_chart(fig_postos, width="stretch")

        with col_g:
            fig_gerentes = grafico_circular(
                contagem_gerentes,
                "Turnos por gerente",
                mapa_cores_gerentes,
            )
            st.plotly_chart(fig_gerentes, width="stretch")

        st.divider()

        st.subheader("🎨 Legenda de cores")
        col_lg, col_lp = st.columns(2)
        with col_lg:
            mostrar_legenda_cores(
                mapa_cores_gerentes,
                "Gerentes",
            )
        with col_lp:
            mostrar_legenda_cores(
                mapa_cores_postos,
                "Postos",
            )

        st.divider()

        st.subheader("Turnos por mês")
        por_mes = df.groupby("Mês").size().sort_index()
        por_mes = por_mes[por_mes > 0]
        st.bar_chart(por_mes, color="#54A24B")

        st.divider()

        with st.expander("📄 Ver tabela detalhada"):
            detalhe = (
                df.groupby(["Gerente", "Posto"])
                .size()
                .reset_index(name="Nº de turnos")
                .sort_values("Nº de turnos", ascending=False)
            )
            detalhe = detalhe[detalhe["Nº de turnos"] > 0]
            st.dataframe(detalhe, width="stretch", hide_index=True)