# Bible Tracker - Acompanhamento de Leitura da Bíblia

## 📖 Sobre o Projeto

O **Bible Tracker** é uma aplicação web completa e interativa, projetada para ajudar usuários a acompanhar seu progresso de leitura da Bíblia de forma organizada e pessoal. Construído com HTML, CSS (TailwindCSS) e JavaScript puro, ele utiliza o IndexedDB do navegador para armazenar todos os dados localmente, garantindo privacidade e um funcionamento rápido e offline.

Este projeto vai além de um simples checklist, oferecendo ferramentas para reflexão, anotações e uma visualização detalhada do seu avanço.

-----

## ✨ Funcionalidades Principais

O aplicativo é dividido em seções, cada uma com funcionalidades específicas para enriquecer sua jornada de leitura:

### **Painel de Controle (Dashboard)**

  - **Progresso Geral:** Uma barra de progresso visual que mostra a porcentagem total de leitura da Bíblia completa.
  - **Progresso por Testamento:** Gráficos detalhados que exibem seu avanço separadamente para o Antigo e o Novo Testamento.
  - **Visualização Consolidada:** Uma seção opcional para ver todas as suas anotações e comentários de todos os livros em um único feed, ordenado por data.
  - **Gerenciamento de Dados:**
      - **Backup (Download):** Exporte todo o seu progresso (capítulos lidos, comentários, anotações e datas marcadas) para um único arquivo `JSON`.
      - **Restauração (Upload):** Importe um arquivo de backup `JSON` para restaurar seus dados, ideal para trocar de navegador ou computador.

### **Leitura por Livro**

  - **Navegação Completa:** Acesso a todos os 66 livros da Bíblia, organizados por testamento, através de um menu lateral.
  - **Marcação de Capítulos:** Marque e desmarque capítulos como lidos com um simples clique.
  - **Marcar/Desmarcar Todos:** Botões de ação rápida para marcar ou desmarcar todos os capítulos de um livro de uma só vez.
  - **Comentários por Capítulo:**
      - Adicione comentários detalhados para capítulos específicos.
      - Faça anotações gerais para o livro sem especificar um capítulo.
      - Visualize todos os comentários de um livro em um único painel, organizados por capítulo.
      - Edite e exclua seus comentários a qualquer momento.
      - Cada comentário registra a data e a hora em que foi salvo.

### **Calendário de Leitura**

  - **Visualização Mensal e Anual:** Alterne entre uma visão detalhada do mês atual e uma visão geral do ano inteiro.
  - **Marcação Automática:** Os dias em que você marca um capítulo como lido são automaticamente destacados no calendário.
  - **Marcação Manual e Interativa:**
      - Clique em qualquer dia para marcá-lo ou desmarcá-lo manualmente, ideal para registrar dias de estudo ou reflexão.
      - A marcação manual tem prioridade, permitindo desmarcar um dia mesmo que uma leitura tenha sido registrada nele, garantindo controle total ao usuário.
  - **Navegação Intuitiva:** Navegue facilmente entre meses e anos.

### **Anotações Gerais**

  - **Diário de Reflexões:** Uma seção dedicada para anotações, orações ou reflexões que não pertencem a um livro ou capítulo específico.
  - **CRUD Completo:** Crie, leia, **edite** e exclua suas anotações.
  - **Registro de Data e Hora:** Cada anotação salva automaticamente a data e a hora, permitindo uma organização cronológica.

-----

## 🚀 Como Utilizar

1.  **Download:** Baixe o arquivo `bible_tracker.html`.
2.  **Abrir no Navegador:** Abra o arquivo `bible_tracker.html` em qualquer navegador de internet moderno (Google Chrome, Mozilla Firefox, Microsoft Edge, etc.).
3.  **Pronto\!** A aplicação funcionará localmente no seu navegador. Não é necessária nenhuma instalação adicional ou conexão com a internet após o primeiro carregamento.

Todo o seu progresso é salvo automaticamente no banco de dados interno do navegador (IndexedDB).

-----

## 🛠️ Tecnologias Utilizadas

  - **HTML5:** Estrutura semântica da aplicação.
  - **CSS3 com TailwindCSS:** Estilização moderna e responsiva para uma interface limpa e agradável.
  - **JavaScript (ES6+):** Lógica principal da aplicação, manipulação do DOM e interatividade.
  - **IndexedDB:** Banco de dados NoSQL do lado do cliente, usado para armazenar de forma persistente e segura todos os dados do usuário diretamente no navegador.
  - **Font Awesome:** Biblioteca de ícones para uma melhor experiência visual.