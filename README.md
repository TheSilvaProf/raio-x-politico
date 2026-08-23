# raio-x-politico
Projeto para consultar dados públicos e históricos de políticos

🕵️‍♂️ Raio-X Político: Análise CEAP 2026

Este projeto realiza o processamento e análise de dados da Cota para Exercício
da Atividade Parlamentar (CEAP) da Câmara dos Deputados. Utilizando uma
arquitetura baseada em containers e scripts de ETL em Python, o sistema
consolida quase 100 mil registros para identificar padrões de gastos públicos.

📊 Números Atuais (Dez/2025 - Ago/2026)

  - Total de Despesas Processadas: R$ 113.369.371,73
  - Volume de Registros: 92.986 despesas vinculadas.
  - Cobertura Parlamentar: 509 dos 513 deputados analisados.

🔍 Principais Insights

1. Onde está o dinheiro? (Top 5 Categorias)

| Categoria de Gasto                      | Total Acumulado  |
| :-------------------------------------- | :--------------- |
| **Divulgação da Atividade Parlamentar** | R$ 46.707.406,74 |
| **Locação de Veículos Automotores**     | R$ 24.335.707,38 |
| **Manutenção de Escritórios de Apoio**  | R$ 18.675.125,46 |
| **Combustíveis e Lubrificantes**        | R$ 14.497.347,81 |
| **Hospedagem**                          | R$ 3.023.139,60  |

2. Maiores Recebedores (Top 5 Fornecedores)

O Facebook lidera o ranking, evidenciando o foco massivo em marketing digital e
impulsionamento, seguido por empresas de logística e frotas.

1.  Facebook Serviços Online do Brasil: R$ 2.054.670,00
2.  PANTANAL VEÍCULOS LTDA: R$ 1.288.177,64
3.  NOVACAR LOCADORA DE VEICULOS: R$ 834.280,80
4.  SUPREMA MOBILIDADE LTDA: R$ 763.281,00
5.  HPE AUTOMOTORES DO BRASIL: R$ 508.097,82

3. Deputados com Maior Volume de Gastos

| Deputado            | Partido      | UF | Total Gasto   |
| :------------------ | :----------- | :- | :------------ |
| **Carlos Veras**    | PT           | PE | R$ 439.309,09 |
| **Robinson Faria**  | PP           | RN | R$ 411.834,94 |
| **Átila Lins**      | PSD          | AM | R$ 391.828,29 |
| **Geraldo Resende** | UNIÃO        | MS | R$ 391.768,40 |
| **Albuquerque**     | REPUBLICANOS | RR | R$ 386.380,91 |

🛠️ Stack Tecnológica

  - Linguagem: Python 3.11
  - Bibliotecas: Pandas (ETL), SQLAlchemy (ORM), Requests.
  - Banco de Dados: PostgreSQL 15 (Dockerizada).
  - Sistema Operacional: Kali Linux.

🛡️ Qualidade e Transparência de Dados

  - Relacionamento: Vinculação via id_camara (unificação de dados da API e do
    CSV oficial).
  - Tratamento de Exceções: 1.238 registros (0.23% do valor total) apresentaram
    data nula no arquivo oficial e foram catalogados para auditoria separada.
  - Deputados sem gastos no período: Amom Mandel, Nivaldo Albuquerque, Priscila
    Costa e Roseana Sarney.

✅ O que fazer agora para publicar:













