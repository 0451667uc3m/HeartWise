import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Cargar datos
df = pd.read_csv('Datos_limpio1.csv', sep=';')

# Asegurar que las columnas son numéricas
df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
df['height(cm)'] = pd.to_numeric(df['height(cm)'], errors='coerce')

#Añadir nueva variable al dataset  -- INDICE DE MASA CORPORAL
def calc_imc(peso, altura):
    return peso / (altura ** 2)

df['imc'] = df.apply(lambda row: calc_imc(row['weight'], row['height(cm)']/100), axis=1)

#Clases

def clase_imc(imc):
    if imc < 18.5:
        return 0; #por debajo de peso
    elif imc >= 18.5 and imc<25:
        return 1; #peso saludable
    elif imc >= 25 and imc<30:
        return 2; #sobrepeso
    elif imc >=30 and imc<39.9:
        return 3; #obesidad
    elif imc>39.9:
        return 4; #obesidad morbida

df['clase_imc'] = df['imc'].apply(clase_imc)

X = df[["age(years)", "weight", "height(cm)", "ap_hi", "ap_lo",
        "cholesterol", "gluc", "smoke", "alco", "active", "imc"]]
Y = df["cardio"]

# División en train/test
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.20, random_state=4
)

# Modelo Random Forest con hiperparámetros óptimos
rf_final = RandomForestClassifier(
    n_estimators=400,
    min_samples_split=20,
    min_samples_leaf=8,
    max_features='log2',
    max_depth=None,
    class_weight=None,
    n_jobs=-1,
    random_state=4
)

rf_final.fit(X_train, Y_train)

# Columnas de entrada
feature_cols = ["age(years)", "weight", "height(cm)", "ap_hi", "ap_lo",
                "cholesterol", "gluc", "smoke", "alco", "active", "imc"]

def casos_posibles(model, df_user):
    casos = {}

    casos["Real"] = df_user.copy()

    df_no_smoke = df_user.copy()
    df_no_smoke["smoke"] = 0
    casos["No tabaco"] = df_no_smoke

    df_no_alco = df_user.copy()
    df_no_alco["alco"] = 0
    casos["No alcohol"] = df_no_alco

    df_activo = df_user.copy()
    df_activo["active"] = 1
    casos["Activo"] = df_activo

    df_saludable = df_user.copy()
    df_saludable["smoke"] = 0
    df_saludable["alco"] = 0
    df_saludable["active"] = 1
    casos["Saludable (ALC = 0, SMOKE = 0, ACTIVO)"] = df_saludable

    resultados = []

    for caso, df_sc in casos.items():
        proba = model.predict_proba(df_sc[feature_cols])[0, 1]
        resultados.append({"Caso": caso, "Probabilidad": proba})

    df_resultados = pd.DataFrame(resultados)
    return df_resultados