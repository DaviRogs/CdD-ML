import os
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------------------------------------
# 1) Defina o caminho correto para o df_consolidado.csv
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "dados", "df_consolidado.csv")
df = pd.read_csv(csv_path, low_memory=False)

# ------------------------------------------------
# 2) Elimine todas as linhas que tenham NaN
#    em QUALQUER coluna que vamos usar como feature ou target
# ------------------------------------------------
colunas_para_validar = [
    "tipoVoto",
    "siglaUf",
    "id_partido",
    "cod_tipo",
    "numero_proposicao",
    "ano",
    "tema",
    "aprovacao"
]
df = df.dropna(subset=colunas_para_validar)

# ------------------------------------------------
# 3) Converta a coluna tipoVoto para binário (1/0)
# ------------------------------------------------
df["tipoVoto"] = df["tipoVoto"].map({"Sim": 1, "Não": 0})
# (caso haja valores diferentes de “Sim” ou “Não”, eles ficam NaN e já foram descartados pelo dropna acima)

# ------------------------------------------------
# 4) Defina X (features) e y (target) – sem NaNs agora
# ------------------------------------------------
y = df["aprovacao"]

features = [
    "siglaUf",
    "id_partido",
    "cod_tipo",
    "numero_proposicao",
    "ano",
    "tema"
]
X = df[features].copy()

# “tema” é, na prática, uma lista/array de string. Vamos extrair o primeiro tema
# para simplificar em “tema_principal”:
def extrai_primeiro_tema(x):
    try:
        # se x for algo como "['Saúde', 'Educação']", retorna "Saúde"
        return eval(x)[0]
    except Exception:
        return "Outros"

X["tema_principal"] = X["tema"].apply(extrai_primeiro_tema)

# Selecionamos somente as colunas que vamos usar
X_final = X[[
    "siglaUf",
    "id_partido",
    "cod_tipo",
    "ano",
    "tema_principal"
]].copy()

# ------------------------------------------------
# 5) Novamente, garantimos que não haja NENHUM NaN em X_final ou em y
# ------------------------------------------------
mask = X_final.notna().all(axis=1) & y.notna()
X_final = X_final.loc[mask]
y       = y.loc[mask]

# ------------------------------------------------
# 6) Construímos um pipeline que faz o OneHotEncoder
#    nas colunas categóricas e deixa as numéricas “pass through”
# ------------------------------------------------
categorical_features = ["siglaUf", "tema_principal"]
numeric_features     = ["id_partido", "cod_tipo", "ano"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"  # opcional, mas recomendado se as classes estiverem desbalanceadas
    ))
])

# ------------------------------------------------
# 7) Agora sim, vamos rodar o cross_val_score usando o pipeline em vez do RandomForest puro
# ------------------------------------------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(
    pipeline,
    X_final,
    y,
    cv=cv,
    scoring="f1_macro",
    n_jobs=-1
)
print("F1-macro em cada fold:", scores)
print("Média F1-macro:", scores.mean())

# ------------------------------------------------
# 8) Se quiser também avaliar a Matriz de Confusão no conjunto de teste:
# ------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, stratify=y, test_size=0.2, random_state=42
)
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Matriz de Confusão (Test Set)")
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.show()