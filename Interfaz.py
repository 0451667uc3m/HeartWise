import pandas as pd

def pedir_datos_usuario():
    # Función para pedir enteros
    def pedir_int(msg, min_val=None, max_val=None):
        while True:
            valor = input(msg).strip()
            if valor == "":
                print("⚠️ Por favor, completa todos los campos.")
                continue
            try:
                valor = int(valor)
                if min_val is not None and valor < min_val:
                    print("⚠️ Por favor, introduce un valor de campo válido.")
                    continue
                if max_val is not None and valor > max_val:
                    print("⚠️ Por favor, introduce un valor de campo válido.")
                    continue
                return valor
            except ValueError:
                print("⚠️ Por favor, introduce un valor de campo válido.")

    # Función para pedir flotantes
    def pedir_float(msg, min_val=None, max_val=None):
        while True:
            valor = input(msg).strip()
            if valor == "":
                print("⚠️ Por favor, completa todos los campos.")
                continue
            try:
                valor = float(valor)
                if min_val is not None and valor < min_val:
                    print("⚠️ Por favor, introduce un valor de campo válido.")
                    continue
                if max_val is not None and valor > max_val:
                    print("⚠️ Por favor, introduce un valor de campo válido.")
                    continue
                return valor
            except ValueError:
                print("⚠️ Por favor, introduce un valor de campo válido.")

    # Función para pedir Sí/No
    def pedir_yes_no(msg):
        while True:
            respuesta = input(msg).strip().lower()
            if respuesta == "":
                print("⚠️ Por favor, completa todos los campos.")
                continue
            if respuesta in ["sí", "si"]:
                return 1
            elif respuesta in ["no"]:
                return 0
            else:
                print("⚠️ Por favor, introduce un valor de campo válido (Sí/No).")

    print("Por favor, introduce los siguientes datos:")

    edad = pedir_int("Edad (años): ", min_val=1)
    peso = pedir_float("Peso (kg): ", min_val=1)
    altura = pedir_int("Altura (cm): ", min_val=50)
    ap_hi = pedir_int("Presión sistólica (ap_hi): ")
    ap_lo = pedir_int("Presión diastólica (ap_lo): ")
    colesterol = pedir_int("Colesterol (1: normal, 2: por encima, 3: muy por encima): ", min_val=1, max_val=3)
    gluc = pedir_int("Glucosa (1: normal, 2: por encima, 3: muy por encima): ", min_val=1, max_val=3)
    smoke = pedir_yes_no("¿Fumas? (Sí/No): ")
    alco = pedir_yes_no("¿Consumes alcohol? (Sí/No): ")
    active = pedir_yes_no("¿Eres físicamente activo? (Sí/No): ")

    # Calcular IMC
    imc = peso / ((altura / 100) ** 2)

    datos = {
        "age(years)": [edad],
        "weight": [peso],
        "height(cm)": [altura],
        "ap_hi": [ap_hi],
        "ap_lo": [ap_lo],
        "cholesterol": [colesterol],
        "gluc": [gluc],
        "smoke": [smoke],
        "alco": [alco],
        "active": [active],
        "imc": [imc]
    }

    estilo = {
        "Fuma": "Sí" if smoke == 1 else "No",
        "Alcohol": "Sí" if alco == 1 else "No",
        "Activo": "Sí" if active == 1 else "No"
    }

    return pd.DataFrame(datos), estilo
