# 📦 Mini Trabalho 6 – Otimização e Ajuste Fino dos Modelos de Machine Learning

## 🎯 Objetivo

Este mini trabalho teve como foco a **otimização e ajuste fino dos modelos de aprendizado de máquina** utilizados para prever a aprovação de proposições legislativas na Câmara dos Deputados.

Foram aplicadas técnicas de ajuste de hiperparâmetros com validação cruzada para **maximizar a performance** dos modelos (Random Forest e XGBoost), reduzindo overfitting e melhorando a capacidade de generalização.

---

## 👥 Equipe e Responsabilidades

| Integrante         | Responsabilidade                                                                 |
|--------------------|----------------------------------------------------------------------------------|
| Pessoa 1           | Otimização do modelo **Random Forest** com GridSearchCV e validação cruzada     |
| Pessoa 2           | Otimização do modelo **XGBoost** com RandomizedSearchCV e ajuste de parâmetros   |
| Pessoa 3           | Implementação de validação cruzada + análise de erros e métricas de avaliação    |
| Pessoa 4           | Organização final dos notebooks, arquivos e documentação (`README.txt`)          |

---

## 🧪 Modelos Otimizados

### ✅ Random Forest (Pessoa 1)

- Utilizou `RandomizedSearchCV` com validação cruzada (5-fold) para ajustar os hiperparâmetros:
  - `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features`
- Aplicou `class_weight=balanced` para corrigir desbalanceamento da classe alvo.
- Métrica de avaliação principal: **F1-score**
- Resultados:
  - **Melhor F1-score na validação cruzada**: ~0.95
  - **Importância das features** plotada com `seaborn`
- Modelo final salvo como: `random_forest_otimizado.joblib`

- Resultados:
  - Melhor F1-score para a classe "1" (aprovada)
  - Gráfico de validação para `max_depth` incluído

---

### ✅ XGBoost (Pessoa 2)

- Ajustou os hiperparâmetros com `RandomizedSearchCV` e `StratifiedKFold`:
  - `learning_rate`, `n_estimators`, `max_depth`, `subsample`, `colsample_bytree`, `gamma`, `min_child_weight`
- Configuração extra:
  - `use_label_encoder=False`
  - `eval_metric='logloss'`
- Métricas analisadas: **Acurácia**, **F1-score**, **AUC-ROC**
- Resultados:
  - **Melhoria significativa de desempenho após tuning**
  - **Feature importance** visualizada e interpretada
- Modelo pronto para exportação via `joblib`

- Observações:
  - Otimização com 20 combinações e 5 folds: total de 100 treinamentos
  - Monitoramento com `verbose` e suporte a `tqdm` se necessário
  - Redução de warnings e melhora na performance geral
  - AUC e F1 melhoraram em comparação ao modelo anterior

---

### ✅ Validação Cruzada e Análise de Erros (Pessoa 3)

- Aplicou `cross_val_score` com `f1_macro` e `StratifiedKFold` (5-fold)
- Utilizou `RandomForestClassifier` como baseline
- Análises realizadas:
  - Distribuição de scores entre as folds com `boxplot`
  - Matriz de confusão com `seaborn.heatmap`
  - Identificação de **erros comuns**, como proposições previstas como rejeitadas mas que foram aprovadas
- Insights relevantes para próximas iterações dos modelos


## 📂 Estrutura da Entrega

📁 modelos_otimizados/
    ├── random_forest_otimizado.pkl
    ├── xgboost_otimizado.pkl

📁 resultados/
    ├── matriz_confusao_rf.png
    ├── matriz_confusao_xgb.png
    ├── grafico_importancia_rf.png
    ├── grafico_validacao_xgb.png

📁 notebooks/
    ├── otimizacao_random_forest.ipynb
    ├── otimizacao_xgboost.ipynb
    ├── validacao_cruzada_analise_erros.ipynb

📄 README.txt


## 🛠️ Como Executar

1. Certifique-se de ter as bibliotecas instaladas:
   - `scikit-learn`, `xgboost`, `matplotlib`, `seaborn`, `pandas`, `numpy`

2. Abra os notebooks em `/notebooks/` e execute célula por célula.

3. Para carregar os modelos otimizados:
```python
import joblib
modelo_rf = joblib.load('modelos_otimizados/random_forest_otimizado.pkl')
modelo_xgb = joblib.load('modelos_otimizados/xgboost_otimizado.pkl')


Conclusão
Os modelos otimizados apresentaram melhorias significativas nas métricas de avaliação.

A escolha criteriosa dos hiperparâmetros e o uso da validação cruzada aumentaram a robustez das previsões.

As análises de erro e importância das features trouxeram insights valiosos para futuras melhorias.