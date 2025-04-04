import openai
import pandas as pd

# Função para ler a chave da API de um arquivo txt
def ler_chave_api(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as f:
            print("Lendo chave da API...")
            return f.read().strip()
    except Exception as e:
        print("Erro ao ler chave da API", e)
        return None

# Indique o caminho do arquivo openai_api_key.txt
caminho_arquivo = 'C:/caminho-do-arquivo/apikey-openai.txt'
openai.api_key = ler_chave_api(caminho_arquivo)

if openai.api_key is None:
    print("Erro: chave da API com problemas")
else:
    print("Chave da API lida com sucesso!")
    
    try:
        # Função para categorizar frases
        def categorizar_frase(frase):
            categorias = """
            Categoria 1: "Questões relacionadas a categoria 1.",
            Categoria 2: "Questões sobre categoria 2.",
            Categoria n: "Questões sobre a categoria n.",
            Outros: "Outras questões."
            """
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You will be provided with input text from a customer. Classify the intent into one of these categories:\n{categorias}\n\nOnly output the category name, without any additional text."},
                    {"role": "user", "content": frase}
                ],
                max_tokens=50
            )
            categoria = response.choices[0].message['content'].strip()
            print(f"Categoria: {categoria}")
            return categoria

        # Ler a planilha
        print("Lendo planilha...")
        df = pd.read_excel('C:/caminho-do-arquivo/planilha.xlsx')
        print("Planilha lida com sucesso.")

        # Categorizar frases
        print("Categorizando...")
        df['categoria'] = df['input'].apply(categorizar_frase)
        print("Categorização feita com sucesso!")

        # Exportar
        print("Exportando planilha...")
        df.to_excel('C:/caminho-do-arquivo/planilhacategorizada.xlsx', index=False)
        print("Planilha categorizada e exportada com sucesso!")
    except Exception as e:
        print("Erro:", e)
