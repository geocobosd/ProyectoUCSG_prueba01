import streamlit as st
import pandas as pd

import plotly.express as px  # ← Uncomment this line

#Import prueba
st.title("Proyecto final UCG")
st.sidebar.title("Parámetros")
st.sidebar.image("LogoPhyton.png")

#TITULO DE LA APLICACION

st.set_page_config(page_title="Análisis de Clientes Bancarios", layout="wide")
st.write("Aplicación para cargar, explorar, analizar y visualizar información financiera de clientes bancarios.")


# Carga de datos
st.sidebar.header("1. Carga del dataset")
archivo = st.sidebar.file_uploader("Suba el archivo CSV", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    # Previsualización
    st.header("2. Previsualización del dataset")
    st.dataframe(df.head())

    # Información general
    st.header("3. Exploración inicial de datos")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total de clientes", df.shape[0])
    col2.metric("Total de columnas", df.shape[1])
    col3.metric("Regiones", df["region"].nunique())

    st.subheader("Tipos de datos")
    st.dataframe(df.dtypes.astype(str))

    st.subheader("Valores nulos")
    st.dataframe(df.isnull().sum())

    # Selección de variables
    st.header("4. Selección de variables para análisis")

    categoricas = [
        "region",
        "ciudad",
        "estado_deuda_prestamo",
        "tarjeta",
        "ha_hecho_refinanciamientos"
    ]

    numericas = [
        "sueldo",
        "cargas_familiares",
        "saldo_deuda_prestamo",
        "saldo_deuda_tarjetas",
        "monto_inversiones"
    ]

    cat_sel = st.multiselect(
        "Seleccione 2 variables categóricas",
        categoricas,
        default=["region", "estado_deuda_prestamo"],
        max_selections=2
    )

    num_sel = st.multiselect(
        "Seleccione 2 variables numéricas",
        numericas,
        default=["sueldo", "saldo_deuda_prestamo"],
        max_selections=2
    )

    # Filtros
    st.header("5. Filtros interactivos")

    region = st.multiselect(
        "Filtrar por región",
        df["region"].unique(),
        default=df["region"].unique()
    )

    ciudad = st.multiselect(
        "Filtrar por ciudad",
        df["ciudad"].unique(),
        default=df["ciudad"].unique()
    )

    df_filtrado = df[
        (df["region"].isin(region)) &
        (df["ciudad"].isin(ciudad))
    ]

    st.write("Clientes filtrados:", df_filtrado.shape[0])
    st.dataframe(df_filtrado)

    # Gráficas categóricas
    st.header("6. Gráficas de variables categóricas")

    for cat in cat_sel:
        fig = px.histogram(
            df_filtrado,
            x=cat,
            title=f"Distribución de clientes por {cat}"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Gráficas numéricas
    st.header("7. Análisis de variables numéricas")

    for num in num_sel:
        fig = px.histogram(
            df_filtrado,
            x=num,
            nbins=30,
            title=f"Distribución de {num}"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Relación entre numéricas
    if len(num_sel) == 2:
        st.subheader("Relación entre variables numéricas")
        fig = px.scatter(
            df_filtrado,
            x=num_sel[0],
            y=num_sel[1],
            color="region",
            title=f"Relación entre {num_sel[0]} y {num_sel[1]}"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Indicadores financieros
    st.header("8. Indicadores financieros")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Sueldo promedio",
        round(df_filtrado["sueldo"].mean(), 2)
    )

    col2.metric(
        "Deuda préstamo promedio",
        round(df_filtrado["saldo_deuda_prestamo"].mean(), 2)
    )

    col3.metric(
        "Inversión promedio",
        round(df_filtrado["monto_inversiones"].mean(), 2)
    )

    # Resultados
    st.header("9. Resultados del análisis")

    st.write("""
    Con esta aplicación se puede analizar el perfil financiero de los clientes,
    identificar diferencias por región y ciudad, revisar niveles de deuda,
    inversiones, cargas familiares y comportamiento de refinanciamiento.
    """)

else:
    st.info("Suba un archivo CSV para iniciar el análisis.")
