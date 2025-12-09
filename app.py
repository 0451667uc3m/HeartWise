import streamlit as st
import pandas as pd
from Modelo import rf_final, casos_posibles

# Inicializar estado
if "page" not in st.session_state:
    st.session_state.page = 1

def go_to(page):
    st.session_state.page = page

# Página 1: Inicio de sesión
if st.session_state.page == 1:
    import streamlit as st

    st.title("HeartWise: Predicción de riesgo cardiovascular")
    nombre = st.text_input("Nombre")
    genero = st.radio("Género", ["Mujer", "Hombre"])
    if nombre and genero:
        if st.button("Continuar"):
            st.session_state.nombre = nombre
            st.session_state.genero = genero
            go_to(2)
    else:
        st.info("Por favor, completa todos los campos para continuar.")

# Página 2: Datos de salud
elif st.session_state.page == 2:

    st.header("Datos de salud")
    edad = st.number_input("Edad (años)", min_value=1, max_value=120)
    peso = st.number_input("Peso (kg)", min_value=1.0)
    altura = st.number_input("Altura (cm)", min_value=50)
    ap_hi = st.number_input("Presión sistólica (ap_hi)")
    ap_lo = st.number_input("Presión diastólica (ap_lo)")
    colesterol = st.selectbox("Colesterol", ["Normal", "Alto", "Muy alto"])
    gluc = st.selectbox("Glucosa", ["Normal", "Alto", "Muy alto"])
    smoke = st.radio("¿Fumas?", ["Sí", "No"])
    alco = st.radio("¿Consumes alcohol?", ["Sí", "No"])
    active = st.radio("¿Eres físicamente activo?", ["Sí", "No"])

    if st.button("Calcular mis resultados"):
        if edad and peso and altura and ap_hi and ap_lo:
            imc = peso / ((altura / 100) ** 2)
            df_user = pd.DataFrame({
                "age(years)": [edad],
                "weight": [peso],
                "height(cm)": [altura],
                "ap_hi": [ap_hi],
                "ap_lo": [ap_lo],
                "cholesterol": [ {"Normal":1,"Alto":2,"Muy alto":3}[colesterol] ],
                "gluc": [ {"Normal":1,"Alto":2,"Muy alto":3}[gluc] ],
                "gender": [1 if st.session_state.genero == "Mujer" else 2],
                "smoke": [1 if smoke == "Sí" else 0],
                "alco": [1 if alco == "Sí" else 0],
                "active": [1 if active == "Sí" else 0],
                "imc": [imc]
            })
            st.session_state.df_user = df_user
            go_to(3)
        else:
            st.warning("Por favor, completa todos los campos.")

    if st.button("Volver atrás"):
        go_to(1)

# Página 3: Resultados
elif st.session_state.page == 3:
    st.header("Resultados de riesgo cardiovascular")
    df_user = st.session_state.df_user
    resultados = casos_posibles(rf_final, df_user)

    for _, fila in resultados.iterrows():
        caso = fila["Caso"]
        prob = fila["Probabilidad"] * 100

        # Ajustar mensajes según hábitos actuales
        if caso == "No tabaco" and df_user["smoke"].iloc[0] == 1:
            caso = "Si dejaras de fumar"
        elif caso == "No alcohol" and df_user["alco"].iloc[0] == 1:
            caso = "Si dejaras de consumir alcohol"
        elif caso == "Activo" and df_user["active"].iloc[0] == 0:
            caso = "Si fueras físicamente activo"
        elif caso == "Saludable":
            if df_user["smoke"].iloc[0] == 1 or df_user["alco"].iloc[0] == 1 or df_user["active"].iloc[0] == 0:
                caso = ("Si llevaras un estilo de vida saludable, "
                        "ni fumar, ni alcohol, y siendo activo, tu probabilidad sería")
            else:
                continue

        st.write(f"- {caso}: {prob:.2f}%")

    if st.button("Volver atrás"):
        go_to(2)
    if st.button("Reiniciar"):
        go_to(1)
