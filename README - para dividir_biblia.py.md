# Divisor de Bíblia em PDF

Este projeto contém um script em Python (`dividir_biblia.py`) projetado para automatizar a divisão de um único arquivo PDF da "Bíblia Viva" em múltiplos arquivos PDF, um para cada livro da Bíblia.

O script organiza os novos arquivos em uma pasta dedicada, nomeando cada um de forma sequencial e descritiva para fácil acesso e organização. Por exemplo: `1. GENESIS_BIBLIA_VIVA.pdf`, `2. EXODO_BIBLIA_VIVA.pdf`, e assim por diante.

## Funcionalidades

-   **Divisão Automática**: Separa um PDF grande em arquivos menores com base em uma lista pré-definida de livros e suas páginas iniciais.
-   **Organização de Arquivos**: Cria uma pasta de saída dedicada para não misturar os arquivos gerados com os originais.
-   **Nomenclatura Padrão**: Renomeia cada arquivo PDF gerado com um número de ordem, o nome do livro em maiúsculas e um sufixo padrão.
-   **Fácil de Configurar**: Requer apenas a definição do caminho do arquivo PDF de origem.
-   **Compatibilidade**: Funciona com a estrutura específica do PDF "A_BIBLIA_VIVA.pdf", mas pode ser adaptado para outras versões ajustando a lista de livros e páginas.

## Requisitos

Para executar o script, você precisará de:

-   **Python 3.x**
-   A biblioteca Python **`pypdf`**

## Instalação

Antes de executar o script, certifique-se de ter a biblioteca `pypdf` instalada. Caso não tenha, instale-a através do pip (gerenciador de pacotes do Python):

```bash
pip install pypdf
```

## Configuração

O script precisa ser configurado com o caminho do seu arquivo PDF. Abra o arquivo `dividir_biblia.py` em um editor de texto e altere a seguinte variável:

1.  **`caminho_pdf_original`**: Altere o valor desta variável para o caminho completo onde o seu arquivo `A_BIBLIA_VIVA.pdf` está localizado.

    ```python
    # Exemplo de configuração:
    caminho_pdf_original = r"C:\Users\Usuario\Desktop\A\biblia viva\A_BIBLIA_VIVA.pdf"
    ```

A lista de livros e suas respectivas páginas iniciais (`livros_biblia`) já está preenchida no script de acordo com a estrutura fornecida. Se o seu PDF tiver uma paginação diferente, você precisará ajustar os números das páginas nesta lista.

## Como Usar

Após a instalação e configuração, siga estes passos para executar o script:

1.  **Abra o terminal** ou o prompt de comando (CMD).
2.  **Navegue até o diretório** onde você salvou o script `dividir_biblia.py` usando o comando `cd`.
    ```bash
    # Exemplo: se você salvou o script na sua Área de Trabalho
    cd Desktop
    ```
3.  **Execute o script** usando o comando `python`:
    ```bash
    python dividir_biblia.py
    ```

O script iniciará o processo e exibirá o progresso no terminal, informando qual livro está sendo processado.

## Como Funciona

A lógica do script é a seguinte:

1.  **Leitura do PDF**: O script abre o arquivo PDF original especificado em `caminho_pdf_original`.
2.  **Cálculo das Páginas**: Ele percorre a lista `livros_biblia`. Para cada livro, ele identifica a página inicial. A página final de um livro é calculada como sendo a página imediatamente anterior ao início do próximo livro. Para o último livro (Apocalipse), ele usa o número total de páginas do PDF como fim.
3.  **Correção de Índice**: As bibliotecas de PDF contam as páginas a partir do índice 0 (a primeira página é `0`, a segunda é `1`, etc.). O script ajusta os números de página para corresponder a essa indexação.
4.  **Criação dos Novos Arquivos**: Para cada livro, um novo objeto PDF é criado em memória. O script copia o intervalo de páginas calculado do PDF original para este novo objeto.
5.  **Salvamento**: O novo PDF, contendo apenas as páginas de um livro, é salvo na pasta de saída com o nome formatado (ex: `66. APOCALIPSE_BIBLIA_VIVA.pdf`).

## Saída Esperada

Ao final da execução, uma nova pasta chamada **`Bíblia Viva em Livros (PDFs)`** será criada dentro do mesmo diretório do seu PDF original. Dentro dela, você encontrará 66 arquivos PDF, cada um correspondendo a um livro da Bíblia.
