📊 Análise de Custos de Frete no E-commerce
🔎 Sobre o Projeto
Este projeto tem como objetivo analisar e identificar os principais fatores que impactam o custo de frete no e-commerce, com foco na rentabilidade da operação.
A análise considera como referência uma meta de 5% do valor da Nota Fiscal para custo de frete. Os dados analisados compreendem o período de Janeiro a Maio de 2026.

🎯 Objetivo
Identificar padrões e variáveis que contribuem para o aumento do custo logístico, respondendo perguntas como:

Quais regiões possuem maior custo de envio?
Qual o impacto das transportadoras?
Como campanhas promocionais influenciam o frete?
Qual o efeito de cupons (especialmente frete grátis) na rentabilidade?


⚙️ Tecnologias Utilizadas

Python (Pandas / NumPy) → ETL e tratamento de dados
Power BI → Visualização e construção do dashboard
DAX (Data Analysis Expressions) → Criação de métricas e indicadores
Power Query (M Language) → Tratamento, modelagem e anonimização dos dados
Parquet → Armazenamento eficiente de dados


🧱 Estrutura do Projeto
📁 projeto/
│
├── 📁 data/
│   ├── fretes/
│   └── notas/
│
├── 📁 output/
│   └── df_final_total_.parquet
│
├── ANALISE_ECOMMERCE - Anonimizado.py
└── Analise de custo - Ecommerce 2026 - Anonimizado.pdf


⚠️ Observação: As bases de dados originais não foram incluídas por questões de confidencialidade.


🔄 Pipeline de Dados (ETL)
O processamento foi dividido em duas camadas:

🐍 Camada 1 — Python (ETL)
1. Extração

Leitura de múltiplos arquivos Excel de:

Fretes
Notas fiscais




2. Transformação
Principais etapas aplicadas:

Padronização de colunas
Conversão de tipos numéricos
Cruzamento entre pedidos e notas fiscais
Cálculo de métricas

💰 Valor da Nota Fiscal
Pythondf_total["VALOR_NF"] = df_total["NUM_NFE"].map(mapa_valores)Mostrar mais linhas
🚚 Custo de Frete
Pythonmapa_custo_frete = df_filtrado.groupby("CHAVE_DE_ACESSO_NFE")["VALOR_CT_E"].sum()Mostrar mais linhas
📈 Percentual de Frete
Pythondf_total["PERC_FRETE"] = df_total["CUSTO_FRETE"] / df_total["VALOR_NF"]Mostrar mais linhas
🏷️ Classificação de Frete

BAIXO ≤ 4%
OK entre 4% e 5%
ALTO > 5%

Pythondf_total.loc[df_total["PERC_FRETE"] > 0.05, "CLASSIFICACAO_FRETE"] = "ALTO"Mostrar mais linhas

3. Carga

Exportação para .parquet para consumo no Power BI


📊 Camada 2 — Power BI
🔄 Power Query (M)

Tratamento complementar dos dados
Padronização de campos
Modelagem das tabelas
Aplicação de regras de anonimização


📐 DAX (Data Analysis Expressions)
Utilizado para criação de indicadores e análises como:

Percentual médio de frete
Comparação com a meta (5%)
Análises por região e transportadora
Impacto de campanhas promocionais
Avaliação de cupons e frete grátis


📊 Principais Resultados
✅ Indicadores Gerais

Média custo de frete: R$18,31
Ticket médio: R$228,16
Percentual médio de frete: 7,05% (acima da meta)


💰 Impacto Financeiro
A análise identificou um impacto financeiro relevante:

📉 Aproximadamente R$114 mil de custo excedente
comparando o custo real de frete com o cenário ideal considerando a meta de 5%.

📌 Esse valor representa uma oportunidade direta de ganho de eficiência e melhoria de margem na operação.

🌎 Insights por Região

Estados com maior percentual de frete:

GO: 11,79%
RS: 10,82%
BA: 10,27%



📌 Regiões com menor volume apresentam maior custo logístico — evidenciando efeito de escala.

🚛 Transportadoras

Diferença relevante entre transportadoras:

Transportadora A: 10,59%
Transportadora B: 8,42%




🎟️ Impacto de Cupons

Fretes com cupom apresentam custo elevado
Frete grátis impacta significativamente a rentabilidade
Campanhas acumuladas ampliam o custo logístico


💡 Principais Insights

O custo de frete está diretamente ligado à escala operacional
Frete grátis é um dos principais drivers de aumento de custo
Campanhas promocionais impactam diretamente a margem
Existem oportunidades claras de otimização por:

Região
Transportadora
Tipo de campanha




🚀 Recomendações

Revisar política de frete grátis
Direcionar campanhas para regiões mais eficientes
Evitar acúmulo de incentivos comerciais
Monitorar performance por transportadora
Implementar regras baseadas em margem


📎 Dashboard
O dashboard completo pode ser visualizado no arquivo:
Analise de custo - Ecommerce 2026 - Anonimizado.pdf


🔐 Dados
Os dados utilizados neste projeto foram anonimizados e não estão disponíveis neste repositório por questões de confidencialidade.
O processo de anonimização foi aplicado tanto:

No pipeline em Python
Quanto na camada de modelagem no Power BI (Power Query)

O objetivo desta publicação é demonstrar:

Técnicas de ETL com Python
Modelagem e transformação de dados
Criação de métricas com DAX
Análise orientada a negócio
Construção de dashboards


👨‍💼 Autor
Ruan de Lima Massad Cheluje
Analista de Logística
