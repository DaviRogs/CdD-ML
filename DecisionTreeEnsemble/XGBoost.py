import pandas as pd
import numpy as np
# import joblib as jb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.utils import class_weight
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from xgboost import XGBClassifier
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_csv('../dados/df_consolidado.csv', dtype={
    'id_votacao': 'str',
    'id_deputado': 'int64',
    'tipoVoto': 'str',
    'siglaUf': 'str',
    'id_partido': 'float64',
    'id_proposicao': 'int64',
    'data': 'str',
    'sigla_orgao': 'str',
    'aprovacao': 'float64',
    'cod_tipo': 'int64',
    'numero_proposicao': 'int64',
    'ano': 'int64',
    'orientacao': 'str',
    'id_autor': 'float64',
    'tema': 'str'
})

# Remover linhas onde qualquer uma das colunas especificadas é NaN
colunas_para_remover_nan = [
    'id_votacao', 'id_deputado', 'tipoVoto', 'siglaUf', 'id_partido',
    'id_proposicao', 'data', 'sigla_orgao', 'aprovacao', 'cod_tipo',
    'numero_proposicao', 'ano', 'orientacao', 'id_autor', 'tema'
]
df = df.dropna(subset=colunas_para_remover_nan)

# Pré-processamento
# Converter voto em variável binária (1 = a favor, 0 = contra/abstenção)
df['voto_favoravel'] = df['tipoVoto'].apply(lambda x: 1 if x == '1.0' else 0)

# Criar variável alvo: aprovação da proposição
# (assumindo que aprovacao=1.0 significa aprovada)
y = df['aprovacao']

# Selecionar features relevantes
features = ['siglaUf', 'id_partido', 'cod_tipo', 'numero_proposicao', 'ano', 'tema']
X = df[features].copy()

# Pré-processamento das features categóricas
# Para temas, vamos extrair os principais temas (primeiro da lista)
X.loc[:, 'tema_principal'] = X['tema'].apply(lambda x: eval(x)[0] if pd.notnull(x) else 'Outros')

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
    X_final, y, test_size=0.2, random_state=42, stratify=y)

# Calcular balanceamento de classes
class_weights = class_weight.compute_sample_weight('balanced', y_train)

# Opção 1: Gradient Boosting do sklearn
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        subsample=0.8
    ))
])

# Opção 2: XGBoost (descomentar para usar)
"""
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        scale_pos_weight=np.sum(y_train == 0) / np.sum(y_train == 1)  # Para dados desbalanceados
    ))
])
"""

# Treinar modelo
pipeline.fit(X_train, y_train, classifier__sample_weight=class_weights)

# Avaliar modelo
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]  # Probabilidades para classe positiva

print(f"Acurácia: {accuracy_score(y_test, y_pred):.2f}")
print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.2f}")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# # Feature importance (para XGBoost ou GradientBoosting)
# try:
#     importances = pipeline.named_steps['classifier'].feature_importances_
#     feature_names = (numeric_features + 
#                     list(pipeline.named_steps['preprocessor']
#                         .named_transformers_['cat']
#                         .get_feature_names_out(categorical_features)))
    
#     importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
#     importance_df = importance_df.sort_values('Importance', ascending=False)
#     print("\nImportância das Features:")
#     print(importance_df.head(20))
# except Exception as e:
#     print("\nNão foi possível extrair importância das features:", str(e))

try:
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
    plt.xlabel('Importância')
    plt.ylabel('Features')
    plt.title('Importância das Features')
    plt.gca().invert_yaxis()  # Inverter o eixo para exibir a feature mais importante no topo
    plt.tight_layout()
    plt.show()
except Exception as e:
    print("\nNão foi possível plotar a importância das features:", str(e))

# Salvar png, caso necessário
# plt.savefig('feature_importance_xgboost.png', dpi=300)

# Salvar o modelo para uso futuro
# jb.dump(pipeline, 'modelo_aprovacao_gb.pkl')