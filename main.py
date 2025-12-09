from Modelo import rf_final, casos_posibles
from Interfaz import pedir_datos_usuario

def main():
    df_user, estilo = pedir_datos_usuario()

    # Mostrar estilo de vida primero
    print("\n🧑 Estilo de vida actual:")
    for k, v in estilo.items():
        print(f"- {k}: {v}")

    # Calcular probabilidades en distintos escenarios
    resultados = casos_posibles(rf_final, df_user)

    print("\n📊 Resultados de riesgo cardiovascular:")

    for _, fila in resultados.iterrows():
        caso = fila["Caso"]
        prob = fila["Probabilidad"] * 100

        # Ajustar textos
        if caso == "No tabaco":
            caso = "Si dejaras de fumar"
        elif caso == "No alcohol":
            caso = "Si dejaras de consumir alcohol"
        elif caso == "Activo":
            caso = "Si fueras físicamente activo"
        elif caso == "Saludable":
            # Mostrar solo si el usuario tiene al menos un hábito negativo
            if df_user["smoke"].iloc[0] == 1 or df_user["alco"].iloc[0] == 1 or df_user["active"].iloc[0] == 0:
                caso = ("Si llevaras un estilo de vida saludable, "
                        "ni fumar, ni alcohol, y siendo activo, tu probabilidad sería")
            else:
                continue  # no mostrar la línea "Saludable" si ya es saludable

        print(f"- {caso}: {prob:.2f}%")

if __name__ == "__main__":
    main()
