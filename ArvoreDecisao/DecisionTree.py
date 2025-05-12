import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Carregar os dados
df = pd.read_csv('../dados/df_consolidado.csv')

# Pré-processamento
# Converter voto em variável binária (1 = a favor, 0 = contra/abstenção)
df['voto_favoravel'] = df['tipoVoto'].apply(lambda x: 1 if x == 1.0 else 0)

# Criar variável alvo: aprovação da proposição
# (assumindo que aprovacao=1.0 significa aprovada)
y = df['aprovacao']

# Selecionar features relevantes
features = ['siglaUf', 'id_partido', 'cod_tipo', 'numero_proposicao', 'ano', 'tema']
X = df[features]

# Pré-processamento das features categóricas
# Para temas, vamos extrair os principais temas (primeiro da lista)
X['tema_principal'] = X['tema'].apply(lambda x: eval(x)[0] if pd.notnull(x) else 'Outros')

# Selecionar colunas finais para o modelo
final_features = ['siglaUf', 'id_partido', 'cod_tipo', 'ano', 'tema_principal']
X_final = X[final_features]

# Codificar variáveis categóricas
categorical_features = ['siglaUf', 'tema_principal']
numeric_features = ['id_partido', 'cod_tipo', 'ano']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Dividir dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42)

# Criar pipeline com pré-processamento e modelo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', DecisionTreeClassifier(
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    ))
])

# Treinar modelo
pipeline.fit(X_train, y_train)

# Avaliar modelo
y_pred = pipeline.predict(X_test)
print(f"Acurácia: {accuracy_score(y_test, y_pred):.2f}")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# Salvar modelo para uso futuro
joblib.dump(pipeline, 'modelo_aprovacao_proposicao.pkl')