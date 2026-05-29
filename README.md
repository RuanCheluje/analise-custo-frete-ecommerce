# Análise de Custos de Frete no E-commerce

Projeto de análise de dados focado na redução de custos logísticos, identificando oportunidades que podem gerar economia de aproximadamente R$114 mil.

---

## Problema de Negócio

O custo de frete no e-commerce frequentemente ultrapassa a meta estabelecida, impactando diretamente a rentabilidade da operação.

Este projeto busca identificar os principais drivers desse custo elevado e propor ações para otimização logística.

---

## Sobre o Projeto

Este projeto tem como objetivo analisar e identificar os principais fatores que impactam o custo de frete no e-commerce.

A análise considera como referência uma meta de **5% do valor da Nota Fiscal** para custo de frete.

Os dados analisados compreendem o período de **Janeiro a Maio de 2026**.

---

## Objetivo

Identificar padrões e variáveis que contribuem para o aumento do custo logístico:

- Quais regiões possuem maior custo de envio?  
- Qual o impacto das transportadoras?  
- Como campanhas promocionais influenciam o frete?  
- Qual o efeito de cupons (especialmente frete grátis) no custo logístico?  

---

## Tecnologias Utilizadas

- **Python (Pandas / NumPy)** → ETL e tratamento de dados  
- **Power BI** → Visualização e construção do dashboard  
- **DAX (Data Analysis Expressions)** → Criação de métricas e indicadores  
- **Power Query (M Language)** → Tratamento, modelagem e anonimização dos dados  
- **Parquet** → Armazenamento eficiente  

---

## Estrutura do Projeto

```bash
📁 projeto/
├── 📁 data/
│   ├── fretes/
│   └── notas/
├── 📁 output/
│   └── df_final_total_.parquet
├── etl_frete_ecommerce.py
└── dashboard_frete_ecommerce.pdf
````

OBS: As bases de dados originais não foram incluídas por questões de confidencialidade.


Pipeline de Dados (ETL)

O processamento foi dividido em duas camadas:

- Camada 1 — Python (ETL)

Extração:

Leitura de múltiplos arquivos Excel de:

- Fretes
- Notas fiscais

Transformação:

Principais etapas aplicadas:

- Padronização de colunas
- Conversão de tipos numéricos
- Cruzamento entre pedidos e notas fiscais
- Cálculo de métricas
  
- Valor da Nota Fiscal:
```python
df_total["VALOR_NF"] = df_total["NUM_NFE"].map(mapa_valores)
```

- Custo de Frete:
```python
mapa_custo_frete = df_filtrado.groupby("CHAVE_DE_ACESSO_NFE")["VALOR_CT_E"].sum()
```

- Percentual de Frete:

```python
df_total["PERC_FRETE"] = df_total["CUSTO_FRETE"] / df_total["VALOR_NF"]
```

- Classificação de Frete:

- **BAIXO** ≤ 4%
- **OK** entre 4% e 5%
- **ALTO** > 5%

```python
df_total.loc[df_total["PERC_FRETE"] > 0.05, "CLASSIFICACAO_FRETE"] = "ALTO"
```

Carga:

- Exportação para formato `.parquet` para consumo no Power BI

- Camada 2 — Power BI

- Power Query (M):

- Tratamento complementar dos dados
- Padronização de campos
- Modelagem das tabelas
- Aplicação de regras de anonimização

- DAX (Data Analysis Expressions):

Utilizado para construção de métricas e análises como:

- Percentual médio de frete
- Comparação com a meta (5%)
- Análises por região e transportadora
- Impacto de campanhas promocionais
- Avaliação de cupons e frete grátis



- Dashboard:

O dashboard completo pode ser visualizado no arquivo:

```
dashboard_frete_ecommerce.pdf
```



- Principais Resultados:

  
- Indicadores Gerais (Página 1):
  
- Média custo de frete: **R$18,31**
- Ticket médio: **R$228,16**
- Percentual médio de frete: **7,05% (acima da meta)**
- Média custo frete meta: **R$11,40** (5% do ticket médio)
- Fretes acima da meta: 59,15%



- Insights por Região (Página 2):
Estados com maior percentual de frete:

- GO: 11,79%
- RS: 10,82%
- BA: 10,27%

- Regiões com menor volume apresentam maior custo logístico, evidenciando o impacto da escala operacional. Região Sudeste concentra o maior volune de vendas e evidencia um percentual de frete mais baixo em relação as demais regiões do país.



- Transportadoras (Página 2):

Diferença relevante entre transportadoras:

- Transportadora A: 10,59%
- Transportadora B: 8,42%

- A quantidade de fretes emitidos por cada transportador são praticamente a mesma, porém, observa-se um percentual de custo médio diferente.



- Impacto de Cupons dos Fretes de Custo Alto (Página 3 e 4):

- Fretes com cupom apresentam custo elevado
- Frete grátis impacta significativamente a rentabilidade
- Campanhas acumuladas ampliam o custo logístico



 - Principais Insights:

- O custo de frete está diretamente ligado à **escala operacional**
- **Frete grátis** é um dos principais drivers de aumento de custo
- Campanhas promocionais impactam diretamente a margem
- Existem oportunidades claras de otimização por:
  - Região
  - Transportadora
  - Tipo de campanha



- Recomendações:

- Revisar política de frete grátis
- Direcionar campanhas para regiões mais eficientes
- Evitar acúmulo de incentivos comerciais
- Monitorar performance por transportadora
- Implementar regras baseadas em margem




- Dados:

Os dados utilizados neste projeto foram **anonimizados** e **não estão disponíveis neste repositório** por questões de confidencialidade.

O processo de anonimização foi aplicado tanto:

- No pipeline em **Python**
- Quanto na camada de modelagem no **Power BI (Power Query)**

O objetivo desta publicação é demonstrar:

- Técnicas de ETL com Python
- Modelagem e transformação de dados
- Criação de métricas com DAX
- Análise orientada a negócio
- Construção de dashboards

- Conclusão:

Este projeto demonstra a importância da análise de dados aplicada à logística, evidenciando como decisões estratégicas podem impactar diretamente a rentabilidade do e-commerce.

- Autor:

**Ruan de Lima Massad Cheluje**  
Analista de Logística


