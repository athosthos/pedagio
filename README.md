# 🚗 Calculadora de Pedágios

Um aplicativo web simples e eficiente criado para automatizar a extração e a soma de cobranças de pedágio a partir de extratos bancários em PDF. 

Criado para poupar o tempo de ler o extrato linha por linha todo mês, o app identifica os pedágios, soma os valores e gera um detalhamento pronto para o Excel.

## ✨ Funcionalidades

* **Leitura de PDF:** Lê diretamente o arquivo do extrato bancário.
* **Busca Inteligente:** Aceita múltiplas palavras-chave (ex: `PASSAGEM PEDAGIO, SEM PARAR, VELOE`).
* **Cálculo Automático:** Encontra o valor exato na linha da cobrança, ignora o sinal negativo de saídas da conta e soma o total.
* **Tabela Interativa:** Exibe um detalhamento na tela com a linha do extrato e o valor de cada passagem.
* **Exportação para Excel:** Botão para baixar a tabela em `.csv` já formatado para o padrão brasileiro (separador por ponto e vírgula, decimais com vírgula e acentuação corrigida).

## 🛠️ Tecnologias Utilizadas

* **[Python](https://www.python.org/):** Linguagem principal.
* **[Streamlit](https://streamlit.io/):** Para a criação da interface web e deploy.
* **[pdfplumber](https://github.com/jsvine/pdfplumber):** Para extração precisa de texto de arquivos PDF.
* **[Pandas](https://pandas.pydata.org/):** Para manipulação dos dados e exportação da tabela.
* **Regex (`re`):** Expressões regulares para encontrar o padrão financeiro no texto.

## 🚀 Como rodar o projeto localmente

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd SEU_REPOSITORIO
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```
