Mini Trabalho 7 — Apresentação e Documentação da Solução de Aprendizado de Máquina
Equipe:
Andre Ricardo Meyer de Melo - 231011097

Luiz Felipe Bessa Santos - 231011687

Tiago Antunes Balieiro - 231011838

Wesley Pedrosa dos Santos - 180029240

Objetivo
O objetivo proposto foi a previsão de aprovação de proposições legislativas. O projeto tem como base os dados consolidados sobre votações, proposições, temas e partidos, além das diversas características dos deputados e das proposições. A seguinte documentação ve inclui os seguintes pontos principais:

Como o projeto atende aos objetivos inicialmente propostos.

Descrição da metodologia utilizada.

Modelos de aprendizado de máquina selecionados.

Resultados obtidos e análise crítica.


Como o projetoo atende aos objetivos inicialmente propostos
Atráves do modelo treinado, podemos aplicá-lo em uma nova base de dados para prever o resultado de uma proposição, sendo necessário apenas os dados públicos e divulgados da proposição.
Como não era um dos objetivos iniciais e também por questões de tempo, não foi criada uma interface gráfica para a utilização do modelo.

Metodologia Utilizada
A metodologia aplicada no projeto se baseia no processo iterativo de aprendizado de máquina, onde primeiramente foi feita a análise exploratória dos dados, seguido do pré-processamento e divisão em conjunto de treino e teste. Os passos principais incluem:

1. Pré-processamento dos Dados
Tratamento de valores ausentes: Substituição dos valores faltantes por valores médios, moda ou imputação com técnicas adequadas.

Codificação de variáveis categóricas: Utilização de técnicas como One-Hot Encoding para variáveis como siglaUf, tema, entre outras.

Balanceamento de classes: A classe alvo estava desbalanceada, então utilizamos técnicas como class_weight para balancear os dados.

Normalização e Escalonamento: Alguns modelos como KNN e SVM exigem dados normalizados, então utilizamos técnicas como MinMaxScaler.

2. Modelos de Aprendizado de Máquina Selecionados
A seguir, apresentamos os modelos de aprendizado de máquina que foram utilizados para prever a aprovação das proposições legislativas:

Decision Tree: Um modelo simples e interpretável para fornecer uma visão clara de como as decisões são tomadas.

Random Forest: Um ensemble de árvores de decisão que melhora a precisão ao combinar múltiplas árvores.

K-Nearest Neighbors (KNN): Um modelo simples que pode ser eficaz em alguns contextos, mas requer boa normalização dos dados.

Support Vector Machine (SVM): Um modelo robusto, ideal para separar classes em espaços de alta dimensionalidade.

XGBoost: Um modelo baseado em Gradient Boosting, altamente eficaz em problemas com dados desbalanceados e grande complexidade.

3. Avaliação dos Modelos
Os modelos foram avaliados com base nas seguintes métricas:

Acurácia

Precisão

Recall

F1-Score

AUC-ROC (para o modelo XGBoost)

As métricas foram calculadas utilizando a função classification_report da biblioteca sklearn.

Resultados Obtidos
Modelo	Acurácia	F1-Score (Classe 1)	Observações
Random Forest	0.77	~0.75	Melhor desempenho geral
Decision Tree	0.66	~0.61	Boa interpretabilidade
K-Nearest Neighbors	0.62	~0.60	Requer normalizaçãol
Support Vector Machine	0.66	~0.61	Mais lento para treinar
XGBoost	0.76	~0.67

Esses valores apresentados são aproximados e podem variar de acordo com ajustes adicionais de hiperparâmetros.

Análise Crítica
Árvores de Decisão e Random Forest: Apresentaram resultados robustos, com o Random Forest se destacando como o melhor modelo. Seu desempenho foi consistente em termos de acurácia e F1-Score, além de fornecer interpretabilidade.

XGBoost: Este modelo demonstrou grande potencial, especialmente em datasets desbalanceados. A métrica AUC-ROC foi superior, o que sugere que este modelo tem mais capacidade de discriminar as classes, sendo um bom candidato para otimizações futuras.

KNN e SVM: Ambos modelos exigem um maior tempo de treinamento, com o KNN sendo altamente dependente de normalização. O desempenho foi razoável, mas inferior ao dos outros modelos.

Balanceamento de classes e Codificação: O balanceamento adequado das classes e a codificação das variáveis foram fatores cruciais para alcançar um bom desempenho. Ajustes nessas etapas podem impactar significativamente os resultados.

Justificativa para o Modelo Selecionado
Os modelo Random Forest foi escolhido para a continuidade do projeto, uma vez que mostrou ótimo desempenho nas métricas de avaliação, especialmente em relação à acurácia e F1-Score.

Random Forest é uma boa escolha devido à sua robustez e facilidade de uso, além de ser mais eficiente para conjuntos de dados grandes.

Esse modelo apresenta bom equilíbrio entre performance e tempo de treinamento e é o utilizado para o modelo final.

Estrutura da Documentação

Mini Trabalho 7 - Grupo 09/
    ├── ajusteHiperparametrosRandomForest.py  # Arquivo com o código utilizado para otimizar o modelo escolhido
    ├── Comparativo_Modelos_Completo.ipynb  # Arquivo com o código de comparativo dos modelos, e com as técnicas utilizadas e especificadas na documentação
    ├── README.txt
