# Ferramenta de Limpeza de Texto Bíblico

Um script Python simples e eficiente para remover números de versículos de arquivos de texto, preservando os títulos dos capítulos.

## 📝 Sobre o Projeto

Este script foi desenvolvido para automatizar a limpeza de arquivos de texto, especificamente textos bíblicos ou documentos estruturados em capítulos e versículos. Ele lê um arquivo `.txt`, remove todos os dígitos numéricos (`0-9`) do conteúdo, o que é útil para limpar a numeração de versículos.

Sua principal característica é a capacidade de identificar e preservar de forma inteligente as linhas que marcam o início de um capítulo (ex: `CAPITULO 1`), garantindo que a estrutura principal do documento não seja perdida no processo.

## ✨ Funcionalidades

-   **Remoção de Dígitos**: Apaga todos os números do corpo do texto.
-   **Preservação de Capítulos**: Mantém intactas as linhas de título de capítulo (ex: `CAPITULO 1`, `CAPITULO 2`, etc.).
-   **Interativo**: O script solicita ao usuário os caminhos dos arquivos de entrada e saída através da linha de comando.
-   **Suporte a UTF-8**: Lida corretamente com acentuação e caracteres especiais da língua portuguesa.
-   **Flexível**: A detecção da palavra "Capitulo" não diferencia maiúsculas de minúsculas, funcionando para "CAPITULO", "Capitulo" ou "capitulo".

## 🔧 Requisitos

-   **Python 3.x**

Nenhuma biblioteca externa é necessária. Todas as ferramentas utilizadas (`re`, `os`) são parte da biblioteca padrão do Python.

## 🚀 Como Usar

1.  **Salve o Script**: Salve o código Python em um arquivo chamado `limpar_texto.py`.

2.  **Abra o Terminal**: Abra um terminal ou prompt de comando (CMD, PowerShell, Terminal, etc.).

3.  **Navegue até a Pasta**: Use o comando `cd` para navegar até o diretório onde você salvou o arquivo `limpar_texto.py`.
    ```bash
    # Exemplo para Windows
    cd C:\Users\SeuNome\Documentos\Scripts

    # Exemplo para macOS/Linux
    cd /home/SeuNome/Documentos/Scripts
    ```

4.  **Execute o Script**: Digite o seguinte comando e pressione Enter:
    ```bash
    python limpar_texto.py
    ```

5.  **Informe os Caminhos**:
    -   O script solicitará o **caminho do arquivo de entrada**. Cole o caminho completo do seu arquivo `.txt` e pressione Enter.
    -   Em seguida, solicitará o **caminho para salvar o novo arquivo**. Cole o caminho completo onde deseja salvar o resultado (use um nome diferente para não sobrescrever o original) e pressione Enter.

6.  **Pronto!** O script processará o arquivo e exibirá uma mensagem de sucesso. Seu novo arquivo de texto, já limpo, estará no local que você especificou.

## 📊 Exemplo de Funcionamento

Considere um arquivo de entrada `livro.txt` com o seguinte conteúdo:

```txt
1º SAMUEL

CAPITULO 1

1 - HAVIA UM HOMEM chamado Elcana, da tribo de Efraim;
2 - Elcana tinha duas mulheres: uma se chamava Ana; o nome da outra era Penina;
11 - Ana fez este voto: "Senhor dos céus, se olhar para o meu sofrimento e responder à minha oração dando-me um filho..."
```

Após executar o script, o arquivo de saída `livro_limpo.txt` terá o seguinte conteúdo:

```txt
º SAMUEL

CAPITULO 1

 - HAVIA UM HOMEM chamado Elcana, da tribo de Efraim;
 - Elcana tinha duas mulheres: uma se chamava Ana; o nome da outra era Penina;
 - Ana fez este voto: "Senhor dos céus, se olhar para o meu sofrimento e responder à minha oração dando-me um filho..."
```

## 📄 Licença

Este projeto é distribuído sob a licença MIT.

---

### Como salvar este arquivo:

1.  Copie todo o texto acima.
2.  Cole em um editor de texto simples (como Bloco de Notas, VS Code, Sublime Text, etc.).
3.  Salve o arquivo com o nome exatamente `README.md` na mesma pasta onde está seu script Python. Plataformas como o GitHub reconhecerão este arquivo automaticamente e o exibirão na página do seu projeto.