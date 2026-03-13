import streamlit as st
import pdfplumber
import re
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Calculadora de Pedágio", page_icon="🚗")

# Definindo um título e uma explicação do app
st.title("🚗 Calculadora de Pedágios")
st.write("Anexe o extrato em PDF, defina as palavras-chave (separadas por vírgula) e descubra o valor total.")

# Criando um input do tipo PDF
uploaded_file = st.file_uploader("Selecione o PDF do extrato", type="pdf")

# Criando um input de palavras-chaves
palavras_chave_input = st.text_input("Quais palavras devemos procurar? (Separe por vírgula)", value="PASSAGEM PEDAGIO")

# Se o input de PDF e palavras-chaves estiver preenchido
if uploaded_file is not None and palavras_chave_input:
    if st.button("Calcular Total", type="primary"): # Se o botão calcular for clicado
        
        total_pedagio = 0.0 # Setando o valor de pedágio como zero
        padrao_valor = r'(-?\d{1,3}(?:\.\d{3})*,\d{2})' # Vai servir para procurar um valor com um sinal negativo no início, seguido por 1 a 3 números
        lista_passagens = [] # Criando a lista de passagens
        
        # Separa as palavras-chaves do input pelo delimitador de virgula, remove os espaços nas extremidades e transforma em minúsculo
        lista_palavras_chave = [palavra.strip().lower() for palavra in palavras_chave_input.split(',')] 

        # Criando um ícone de carregamento
        with st.spinner('Lendo o PDF e calculando...'):
            try:
                with pdfplumber.open(uploaded_file) as pdf: # Abre o PDF
                    for pagina in pdf.pages: # Para cada página no PDF
                        texto = pagina.extract_text() # Extrai todo o texto e guarda na variável "texto"
                        
                        if texto: # Se existir um texto
                            linhas = texto.split('\n') # Separa o texto em quebras de linha e guarda no array "linhas"
                            for linha in linhas: # Para cada linha do array "linhas"
                                linha_minuscula = linha.lower() # Transforma tudo em minúsculo
                                
                                # Primeira pega cada palavra do array de palavras-chaves
                                # Depois verifica se a palavra-chave está na linha
                                if any(palavra in linha_minuscula for palavra in lista_palavras_chave if palavra):
                                    
                                    # Se encontrar a palavra chave, ele vai procurar o valor padrão (numero negativo com 1 a 3 numeros) na linha 
                                    valores_encontrados = re.findall(padrao_valor, linha)
                                    
                                    # Se tiver 2 ou mais pedágios, ele realiza o cálculo
                                    if len(valores_encontrados) >= 2:
                                        valor_str = valores_encontrados[-2] # Pega a penultima coluna do pdf, que é onde está o valor do pedágio
                                        valor_formatado = valor_str.replace('.', '').replace(',', '.') # Troca as virgulas pelos pontos e os pontos pelas virgulas
                                        valor_float = abs(float(valor_formatado)) # Transforma em float e remove o sinal negativo
                                        
                                        total_pedagio += valor_float # Soma na variável de "total_pedagio"
                                        
                                        # Cria um dicionário com a linha do extrato que possui a cobrança do pedágio e o valor do pedágio
                                        lista_passagens.append({
                                            "Linha do Extrato": linha.strip(),
                                            "Valor (R$)": valor_float
                                        })
                
                # Se existir uma lista de passagens no pedágio
                if lista_passagens:
                    st.success("Pronto! Cálculo finalizado.") # Mostra esse texto na tela
                    st.metric(label="Valor total", value=f"R$ {total_pedagio:.2f}") # Mostra o valor total do pedágio
                    
                    st.divider() # Linha horizontal na tela
                    
                    st.write("### Detalhamento das passagens:") # Mostra esse texto na tela
                    df = pd.DataFrame(lista_passagens) # Cria um dataframe com o dicionário criado anteriormente
                    st.dataframe(df, use_container_width=True) # Mostra o dataframe na tela
                    
                    # Cria um arquivo CDV a partir do dataframe criado anteriormente
                    # Define apenas duas colunas, o delimitador e o valor defimal
                    csv = df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
                    # Botão de download
                    st.download_button(
                        label="📥 Baixar Tabela para o Excel", # Rótulo do botão
                        data=csv, # O que será baixado
                        file_name='pedagios_detalhados.csv', # Nome do arquivo
                        mime='text/csv', # Evita abrir como uma imagem e baixa o arquivo
                    )
                
                # Se nenhuma palavra-chave for encontrada
                else:
                    st.warning("Nenhuma cobrança encontrada. Verifique se as palavras-chave estão corretas.")

            # Se ocorrer algum erro em relação ao PDF
            except Exception as e:
                st.error(f"Ocorreu um erro ao ler o arquivo: {e}")