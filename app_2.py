import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#USO DE LA LIBRERIAS
st.title("Proyecto final UCG")
st.sidebar.title("Parámetros")
st.sidebar.image("Python_logo.png")

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
modulo = st.sidebar.selectbox("Exploración inicial de Datos.. Seleccione:", ["Relación de Clientes Activos versus Clientes que se han ido", "Relación de Años de permanencia laboral versus Clientes que se han ido", "Relación de Número de Productos versus Clientes que se han ido", "Relación de Género del Cliente versus Clientes que se han ido", "Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)", "Graficar la distribución de edades según el estado de abandono"] )

if modulo  == "Relación de Clientes Activos versus Clientes que se han ido":
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
elif modulo  == "Relación de Años de permanencia laboral versus Clientes que se han ido":
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
elif modulo  == "Relación de Número de Productos versus Clientes que se han ido":
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
elif modulo  == "Relación de Género del Cliente versus Clientes que se han ido":
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
elif modulo  == "Cantidad de clientes que permanecen (0) vs. clientes que abandonaron (1)":
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
elif modulo  == "Graficar la distribución de edades según el estado de abandono":
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
