# -*- coding: utf-8 -*-

import re
import os

def remover_numeros_exceto_capitulos(caminho_entrada, caminho_saida):
    """
    Lê um arquivo de texto, remove todos os dígitos numéricos,
    mas preserva as linhas que contêm 'CAPITULO [número]'.
    
    Argumentos:
    caminho_entrada (str): O caminho para o arquivo de texto original.
    caminho_saida (str): O caminho para salvar o novo arquivo processado.
    """
    # Verifica se o caminho de saída é um diretório, para evitar erros
    if os.path.isdir(caminho_saida):
        print(f"Erro: O caminho de saída '{caminho_saida}' é um diretório. Por favor, forneça um nome de arquivo completo.")
        return

    try:
        # Abre o arquivo de entrada para leitura e o de saída para escrita.
        # 'with' garante que os arquivos sejam fechados automaticamente.
        # 'encoding='utf-8'' é importante para lidar com acentos e caracteres especiais.
        with open(caminho_entrada, 'r', encoding='utf-8') as arquivo_entrada, \
             open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:

            for linha in arquivo_entrada:
                # Usamos uma expressão regular para verificar se a linha é um cabeçalho de capítulo.
                # re.search() procura pelo padrão em qualquer lugar da string.
                # r'CAPITULO \d+' significa: a palavra "CAPITULO", seguida por um espaço, 
                # seguida por um ou mais dígitos (\d+).
                # re.IGNORECASE faz a busca não diferenciar maiúsculas de minúsculas (funciona para "CAPITULO", "Capitulo", etc.).
                if re.search(r'CAPITULO \d+', linha, re.IGNORECASE):
                    # Se for uma linha de capítulo, escreve-a no novo arquivo sem alterações.
                    arquivo_saida.write(linha)
                else:
                    # Se não for uma linha de capítulo, removemos todos os dígitos.
                    # re.sub() substitui todas as ocorrências de um padrão.
                    # '\d' é o padrão para qualquer dígito numérico (0-9).
                    # '' é a string de substituição (ou seja, nada).
                    linha_sem_numeros = re.sub(r'\d', '', linha)
                    arquivo_saida.write(linha_sem_numeros)
        
        print("\nArquivo processado com sucesso!")
        print(f"O novo arquivo foi salvo em: {os.path.abspath(caminho_saida)}")

    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada '{caminho_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- Parte principal do Script ---
# O código dentro deste 'if' só roda quando o script é executado diretamente.
if __name__ == "__main__":
    print("--- Ferramenta para Remover Números de Texto Bíblico ---")
    print("Este script remove os números dos versículos, mas mantém os dos capítulos.\n")

    # Pede ao usuário o caminho do arquivo de entrada
    caminho_arquivo_entrada = input("Digite o caminho completo do arquivo de texto para processar: ")

    # Pede ao usuário o caminho para salvar o novo arquivo
    caminho_arquivo_saida = input("Digite o caminho completo para salvar o novo arquivo: ")

    # Chama a função principal para executar a lógica
    remover_numeros_exceto_capitulos(caminho_arquivo_entrada, caminho_arquivo_saida)