import os
from pypdf import PdfReader, PdfWriter

# --- CONFIGURAÇÕES ---

# 1. Defina o caminho completo para o seu arquivo PDF da Bíblia.
#    Use 'r' antes das aspas para evitar problemas com as barras invertidas '\'.
caminho_pdf_original = r"C:\Users\Usuario\Desktop\A\biblia viva\A_BIBLIA_VIVA.pdf"

# 2. Defina o nome da pasta onde os livros serão salvos.
pasta_saida = "Bíblia Viva em Livros (PDFs)"

# 3. Lista dos livros e suas páginas iniciais.
#    Esta lista foi criada a partir dos dados que você forneceu.
livros_biblia = [
    {"nome": "Gênesis", "pagina": 4},
    {"nome": "Êxodo", "pagina": 63},
    {"nome": "Levítico", "pagina": 111},
    {"nome": "Números", "pagina": 148},
    {"nome": "Deuteronômio", "pagina": 191},
    {"nome": "Josué", "pagina": 229},
    {"nome": "Juízes", "pagina": 252},
    {"nome": "Rute", "pagina": 278},
    {"nome": "1º Samuel", "pagina": 282},
    {"nome": "2º Samuel", "pagina": 319},
    {"nome": "1º Reis", "pagina": 350},
    {"nome": "2º Reis", "pagina": 385},
    {"nome": "1º Crônicas", "pagina": 420},
    {"nome": "2º Crônicas", "pagina": 454},
    {"nome": "Esdras", "pagina": 493},
    {"nome": "Neemias", "pagina": 504},
    {"nome": "Ester", "pagina": 520},
    {"nome": "Jó", "pagina": 529},
    {"nome": "Salmos", "pagina": 569},
    {"nome": "Provérbios", "pagina": 667},
    {"nome": "Eclesiastes", "pagina": 703},
    {"nome": "Cântico dos Cânticos", "pagina": 712},
    {"nome": "Isaías", "pagina": 718},
    {"nome": "Jeremias", "pagina": 780},
    {"nome": "Lamentações", "pagina": 848},
    {"nome": "Ezequiel", "pagina": 855},
    {"nome": "Daniel", "pagina": 916},
    {"nome": "Oséias", "pagina": 934},
    {"nome": "Joel", "pagina": 944},
    {"nome": "Amós", "pagina": 948},
    {"nome": "Obadias", "pagina": 956},
    {"nome": "Jonas", "pagina": 958},
    {"nome": "Miquéias", "pagina": 961},
    {"nome": "Naum", "pagina": 967},
    {"nome": "Habacuque", "pagina": 970},
    {"nome": "Sofonias", "pagina": 973},
    {"nome": "Ageu", "pagina": 976},
    {"nome": "Zacarias", "pagina": 978},
    {"nome": "Malaquias", "pagina": 989},
    {"nome": "Mateus", "pagina": 993},
    {"nome": "Marcos", "pagina": 1035},
    {"nome": "Lucas", "pagina": 1062},
    {"nome": "João", "pagina": 1108},
    {"nome": "Atos", "pagina": 1142},
    {"nome": "Romanos", "pagina": 1186},
    {"nome": "1ª Coríntios", "pagina": 1208},
    {"nome": "2ª Coríntios", "pagina": 1231},
    {"nome": "Gálatas", "pagina": 1245},
    {"nome": "Efésios", "pagina": 1253},
    {"nome": "Filipenses", "pagina": 1261},
    {"nome": "Colossenses", "pagina": 1267},
    {"nome": "1ª Tessalonicenses", "pagina": 1272},
    {"nome": "2ª Tessalonicenses", "pagina": 1277},
    {"nome": "1ª Timóteo", "pagina": 1280},
    {"nome": "2ª Timóteo", "pagina": 1286},
    {"nome": "Tito", "pagina": 1290},
    {"nome": "Filemom", "pagina": 1293},
    {"nome": "Hebreus", "pagina": 1295},
    {"nome": "Tiago", "pagina": 1311},
    {"nome": "1ª Pedro", "pagina": 1317},
    {"nome": "2ª Pedro", "pagina": 1323},
    {"nome": "1ª João", "pagina": 1327},
    {"nome": "2ª João", "pagina": 1333},
    {"nome": "3ª João", "pagina": 1334},
    {"nome": "Judas", "pagina": 1335},
    {"nome": "Apocalipse", "pagina": 1337},
]

# --- LÓGICA DO SCRIPT (NÃO PRECISA ALTERAR DAQUI PARA BAIXO) ---

def dividir_biblia():
    """
    Função principal que lê o PDF da Bíblia e o divide em arquivos
    separados para cada livro.
    """
    # Verifica se o arquivo PDF original existe
    if not os.path.exists(caminho_pdf_original):
        print(f"ERRO: O arquivo não foi encontrado em: {caminho_pdf_original}")
        return

    # Cria o caminho completo da pasta de saída
    diretorio_pai = os.path.dirname(caminho_pdf_original)
    caminho_pasta_saida = os.path.join(diretorio_pai, pasta_saida)

    # Cria a pasta de saída se ela não existir
    os.makedirs(caminho_pasta_saida, exist_ok=True)
    print(f"Os arquivos serão salvos em: {caminho_pasta_saida}\n")

    # Abre o arquivo PDF original para leitura
    leitor_pdf = PdfReader(caminho_pdf_original)
    total_paginas_pdf = len(leitor_pdf.pages)

    # Itera sobre a lista de livros para extrair cada um
    for i, livro_info in enumerate(livros_biblia):
        # Cria um novo objeto para escrever o PDF do livro atual
        escritor_pdf = PdfWriter()

        nome_livro = livro_info["nome"]
        # As bibliotecas de PDF contam páginas a partir do 0, então subtraímos 1
        pagina_inicio = livro_info["pagina"] - 1

        # Determina a página final do livro
        # Se for o último livro da lista, vai até o final do PDF
        if i + 1 < len(livros_biblia):
            pagina_fim = livros_biblia[i + 1]["pagina"] - 2 # Página anterior ao início do próximo livro
        else:
            pagina_fim = total_paginas_pdf - 1 # Última página do PDF

        # Validação para garantir que o intervalo de páginas é válido
        if pagina_inicio > pagina_fim:
            print(f"AVISO: Pulando o livro '{nome_livro}' pois o intervalo de páginas é inválido (Início: {pagina_inicio+1}, Fim: {pagina_fim+1}).")
            continue

        print(f"Processando {nome_livro} (Páginas {pagina_inicio + 1} a {pagina_fim + 1})...")

        # Adiciona as páginas do livro ao novo arquivo
        for num_pagina in range(pagina_inicio, pagina_fim + 1):
            escritor_pdf.add_page(leitor_pdf.pages[num_pagina])

        # Cria o nome do arquivo de saída
        # Remove caracteres especiais para nomes de arquivo seguros
        nome_arquivo_seguro = nome_livro.replace('º', '').replace('ª', '').replace(' ', '_').upper()
        nome_arquivo_saida = f"{i + 1}. {nome_arquivo_seguro}_BIBLIA_VIVA.pdf"
        caminho_completo_saida = os.path.join(caminho_pasta_saida, nome_arquivo_saida)

        # Salva o novo arquivo PDF com o livro extraído
        with open(caminho_completo_saida, "wb") as f_out:
            escritor_pdf.write(f_out)

    print("\n--- Processo Concluído! ---")
    print("Todos os livros foram divididos com sucesso.")

# Executa a função principal
if __name__ == "__main__":
    dividir_biblia()