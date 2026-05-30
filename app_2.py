import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

st.title("Proyecto final UCG")
st.sidebar.title("Parámetros")
st.sidebar.image("LogoPhyton.png")

# 1.- cargar un dataset
st.sidebar.header("1. Carga del dataset")
archivo = st.sidebar.file_uploader("Suba el archivo CSV", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)

    st.success("Dataset cargado correctamente")

    # Previsualización
    st.header("2. Previsualización del dataset")
    st.dataframe(df.head())


full_data = pd.read_csv("Churn_Modelling.csv", index_col=0)
st.header("2. Previsualización del dataset")
st.dataframe(full_data.head())

# 2.- Exploración inicial de Datos
modulo = st.sidebar.selectbox("Exploración inicial de Datos.. Seleccione:", ["1.-Relación de Clientes Activos versus Clientes que se han ido", "2.-Relación de Años de permanencia laboral versus Clientes que se han ido", "3.-Relación de Número de Productos versus Clientes que se han ido", "4.-Relación de Género del Cliente versus Clientes que se han ido", "5.-Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)", "6.-Graficar la distribución de edades según el estado de abandono","7.-Selección de variables para análisis"] )

if modulo  == "1.-Relación de Clientes Activos versus Clientes que se han ido":
    # 2.1. Relación de Miembros Activos versus Clientes que se han ido
    st.subheader("2.1. Relación de Clientes Activos versus Clientes que se han ido")
    resultado = (
        full_data.groupby("IsActiveMember")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.2. Relación de Años de permanencia laboral versus Clientes que se han ido
elif modulo  == "2.-Relación de Años de permanencia laboral versus Clientes que se han ido":
    st.subheader("\n2.2. Relación de Años de permanencia laboral versus Clientes que se han ido")
    resultado = (
        full_data.groupby("Tenure")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.3. Relación de Número de Productos versus Clientes que se han ido
elif modulo  == "3.-Relación de Número de Productos versus Clientes que se han ido":
    st.subheader("\n2.3. Relación de Número de Productos versus Clientes que se han ido")
    resultado = (
        full_data.groupby("NumOfProducts")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.4. Relación de Género del Cliente versus Clientes que se han ido
elif modulo  == "4.-Relación de Género del Cliente versus Clientes que se han ido":
    st.subheader("\n2.4. Relación de Género del Cliente versus Clientes que se han ido")
    resultado = (
        full_data.groupby("Gender")["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )
    resultado["Exited"] = resultado["Exited"].astype(str) + "%"
    st.dataframe(resultado)
# 2.5. Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)
elif modulo  == "5.-Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)":
    st.write("Distribución de Clientes:")
    resultado = full_data["Exited"].value_counts().reset_index()
    resultado.columns = ["Exited", "Cantidad"]
    st.dataframe(resultado)
    # Edad promedio (según estado de abandono):
    st.write("Edad promedio (según estado de abandono):")
    resultado = (
        full_data.groupby("Exited")["Age"]
        .mean()
        .reset_index()
    )
    st.dataframe(resultado)    # ¿Los clientes que tienen tarjeta de crédito son más leales?
    st.write("Tasa de abandono según tenencia de tarjeta de crédito:")
    resultado = (
        pd.crosstab(
            full_data["HasCrCard"],
            full_data["Exited"],
            normalize="index"
        ) * 100
    ).round(2)
    st.dataframe(resultado)
# 2.6. Graficar la distribución de edades según el estado de abandono
elif modulo  == "6.-Graficar la distribución de edades según el estado de abandono":
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.kdeplot(
    data=full_data,
    x="Age",
    hue="Exited",
    fill=True,
    ax=ax
    )
    ax.set_title("Distribución de edades según abandono")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Densidad")
    st.pyplot(fig)
# 2.7. Graficar la distribución de edades según el estado de abandono
elif modulo  == "7.-Selección de variables para análisis":
    st.write("Selección de variables para análisis:")
    categoricas = [
        "Geography",
        "Gender",
        "HasCrCard",
        "IsActiveMember",
        "Exited"
    ]
    numericas = [
        "CreditScore",
        "Balance",
        "EstimatedSalary"
    ]
    cat_sel = st.multiselect(
        "Seleccione 2 variables categóricas",
        categoricas,
        default=["Geography", "Gender"],
        max_selections=2
    )
    num_sel = st.multiselect(
        "Seleccione 2 variables numéricas",
        numericas,
        default=["CreditScore", "Balance"],
        max_selections=2
    )
        # Filtros
    st.header("5. Filtros interactivos")

    Geography = st.multiselect(
        "Filtrar por Geography",
        df["Geography"].unique(),
        default=df["Geography"].unique()
    )
    Gender = st.multiselect(
        "Filtrar por Gender",
        df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    df_filtrado = df[
        (df["Geography"].isin(Geography)) &
        (df["Gender"].isin(Gender))
    ]

    for cat in cat_sel:
        fig = px.histogram(
            df_filtrado,
            x=cat,
            title=f"Distribución de clientes por {cat}"
        )
        st.plotly_chart(fig, use_container_width=True)

