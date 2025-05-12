### 📄 README — Mini Trabalho 4: Preparação e Tratamento dos Dados

#### 🎯 Objetivo

O foco desta etapa foi preparar os dados coletados anteriormente para aplicação de algoritmos de aprendizado de máquina. A equipe realizou a limpeza dos dados, tratou valores ausentes, codificou variáveis categóricas e aplicou transformações iniciais visando uma estrutura compatível com os requisitos da modelagem.

---

#### 📦 Dados utilizados

Todos os dados utilizados foram obtidos via **API pública da Câmara dos Deputados** e correspondem exclusivamente à **56ª legislatura (2019–2022)**. Foram tratados os seguintes arquivos `.csv`, organizados por ano:

* `deputados_legislatura_56.csv`
* `partidos.csv`
* `proposicoes_YYYY.csv`
* `votacoes_proposicoes_YYYY.csv`
* `votos_individuais_proposicoes_raw_YYYY.1.csv`
* `votos_individuais_proposicoes_raw_YYYY.2.csv`
* `autores_proposicoes_YYYY.csv`
* `temas_proposicoes_YYYY.csv`
* `orientacoes_proposicoes_YYYY.csv`

(`YYYY` variando entre 2019 e 2022)

---

#### 🧼 Etapas de Tratamento Realizadas

1. **Leitura e verificação dos arquivos**

   * Verificações automáticas para ignorar arquivos ausentes.
   * Leitura padronizada dos dados com uso de `pandas`.

2. **Padronização de colunas e estrutura**

   * Renomeação de colunas (ex: `id` → `id_proposicao`, `sigla` → `sigla_partido`, etc).
   * Remoção de colunas com URIs/URLs desnecessárias.

3. **Unificação de arquivos**

   * Arquivos divididos (como votos `.1` e `.2`) foram concatenados em um único `DataFrame`.

4. **Codificação de variáveis categóricas**

   * A variável `tipoVoto` foi convertida para formato binário:
     `Sim` → `1`, `Não` → `0`.
   * Os demais atributos categóricos foram renomeados e padronizados, com vistas à codificação futura.

5. **Eliminação de redundâncias e colunas irrelevantes**

   * Expansões de campos JSON foram reduzidas à apenas colunas essenciais.
   * Informações duplicadas ou desnecessárias (ex: nome completo do deputado onde já existe `id_deputado`) foram removidas.

6. **Salvamento em pasta `processed/`**

   * Os arquivos tratados foram organizados com consistência para uso posterior na modelagem.

---

#### ✅ Resultados

Ao final desta etapa, os dados estão **padronizados, limpos e codificados** para aplicação em modelos de ML. As transformações garantem que todos os conjuntos compartilhem chaves comuns (`id_deputado`, `id_proposicao`, `id_votacao`) e estejam prontos para unificação futura.

---

#### 🧠 Mini Trabalho 5 — Próximos Passos

A próxima fase terá como objetivo **testar e comparar diferentes algoritmos de aprendizado de máquina**, avaliando seu desempenho e aderência ao problema definido.

As atividades incluem:

* Precisamos unificar os dataframes obtidos em um único.
* Unificação final do dataset com base nas chaves comuns.
* Aplicação de algoritmos de classificação supervisionada.
* Avaliação com métricas apropriadas (ex: accuracy, precision, recall, f1-score).
* Comparação crítica dos resultados e escolha dos modelos mais promissores.

