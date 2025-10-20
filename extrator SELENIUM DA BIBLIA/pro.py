from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re
import os
import logging

# Configurar logging detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("salmos_extraction.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def configurar_navegador():
    """Configura e retorna um driver do Chrome com a versão correta do ChromeDriver"""
    try:
        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executa em modo headless
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Usar webdriver-manager para obter a versão correta do ChromeDriver
        logger.info("Configurando ChromeDriver com webdriver-manager...")
        service = Service(ChromeDriverManager().install())
        
        logger.info("Iniciando o navegador Chrome...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Navegador Chrome iniciado com sucesso.")
        
        return driver
    except Exception as e:
        logger.exception(f"Erro ao configurar o navegador: {str(e)}")
        return None

def extrair_introducao():
    """Extrai a introdução do livro de Salmos"""
    url = "https://biblia.paulus.com.br/biblia-pastoral/antigo-testamento/livros-sapienciais/salmos"
    logger.info(f"Acessando página de introdução: {url}")
    
    driver = configurar_navegador()
    if not driver:
        return "Erro ao configurar o navegador"
    
    try:
        logger.info(f"Navegando para {url}...")
        driver.get(url)
        
        # Esperar até que o conteúdo da introdução esteja presente
        logger.info("Aguardando carregamento do conteúdo da introdução...")
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".texto-intro"))
            )
            logger.info("Elemento .texto-intro localizado com sucesso.")
        except Exception as e:
            logger.warning(f"Elemento .texto-intro não encontrado após 15 segundos: {str(e)}")
            # Verificar se a página carregou algo
            page_source = driver.page_source
            if "SALMOS" in page_source:
                logger.info("Página dos Salmos carregada, mas conteúdo específico não encontrado.")
            else:
                logger.error("Página não carregou corretamente. Verifique sua conexão.")
                return "Erro: Página não carregou corretamente"
        
        # Obter o HTML renderizado
        html = driver.page_source
        logger.info(f"HTML obtido com sucesso. Tamanho: {len(html)} caracteres")
        
        # Para debug: salvar o HTML em um arquivo
        with open("debug_introducao.html", "w", encoding="utf-8") as f:
            f.write(html)
        logger.info("HTML da introdução salvo em debug_introducao.html para análise de debug")
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extrair a introdução
        introducao = soup.select_one('.texto-intro')
        
        if introducao:
            logger.info("Introdução encontrada com sucesso.")
            return introducao.get_text(strip=True)
        else:
            logger.warning("Introdução não encontrada. Tentando seletores alternativos...")
            
            # Tentativa alternativa: procurar por qualquer texto que pareça ser introdução
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text()
                if len(text) > 100 and ("salmos" in text.lower() or "livro" in text.lower()):
                    logger.info("Encontrado texto potencialmente relevante como introdução")
                    return text
            
            # Tentativa alternativa: procurar por seções com classe 'container-content'
            container = soup.select_one('.container-content')
            if container:
                logger.info("Encontrado container de conteúdo geral")
                return container.get_text(strip=True, separator='\n')
            
            logger.error("Introdução não encontrada após todas as tentativas")
            return "Introdução não encontrada no site."
            
    except Exception as e:
        logger.exception(f"Erro crítico ao extrair introdução: {str(e)}")
        return f"Erro crítico ao extrair introdução: {str(e)}"
    finally:
        try:
            driver.quit()
            logger.info("Navegador fechado com sucesso.")
        except:
            logger.warning("Não foi possível fechar o navegador (provavelmente não foi iniciado)")

def extrair_capitulo(url):
    """Extrai o texto bíblico e comentários de um capítulo específico no formato Markdown"""
    logger.info(f"Iniciando extração do capítulo: {url}")
    
    driver = configurar_navegador()
    if not driver:
        return "Título não encontrado", [], []
    
    try:
        logger.info(f"Acessando {url}...")
        driver.get(url)
        
        # Esperar até que o conteúdo do capítulo esteja presente
        logger.info("Aguardando carregamento do conteúdo do capítulo...")
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".chapter-paragraph"))
            )
            logger.info("Elementos .chapter-paragraph localizados com sucesso.")
        except Exception as e:
            logger.warning(f"Elementos .chapter-paragraph não encontrados após 15 segundos: {str(e)}")
            
            # Verificar se a página carregou algo
            page_source = driver.page_source
            if "SALMOS" in page_source or "Salmo" in page_source:
                logger.info("Página dos Salmos carregada, mas versículos específicos não encontrados.")
            else:
                logger.error("Página não carregou corretamente.")
                return "Título não encontrado", [], []
        
        # Obter o HTML renderizado
        html = driver.page_source
        
        # Para debug: salvar o HTML em um arquivo
        capitulo = re.search(r'/salmos/(\d+)', url)
        cap_num = capitulo.group(1) if capitulo else "erro"
        with open(f"debug_capitulo_{cap_num}.html", "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"HTML do capítulo {cap_num} salvo em debug_capitulo_{cap_num}.html para análise de debug")
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extrair o número do capítulo da URL
        numero_capitulo = re.search(r'/salmos/(\d+)', url)
        capitulo = numero_capitulo.group(1) if numero_capitulo else "Desconhecido"
        logger.info(f"Processando Salmo {capitulo}...")
        
        # 1. Extrair o título do salmo
        titulo_salmo = "Título não encontrado"
        titulo_element = soup.select_one('.container-chapter-title h4')
        if titulo_element:
            titulo_salmo = titulo_element.get_text(strip=True)
            logger.info(f"Título encontrado: {titulo_salmo}")
            # Remover possíveis referências numéricas extras do título
            titulo_salmo = re.sub(r'\[Sl \d+\]', '', titulo_salmo).strip()
        else:
            logger.warning("Título do salmo não encontrado. Tentando seletores alternativos...")
            # Outros seletores possíveis para o título
            titulo_element = soup.select_one('.containerTitle h4')
            if titulo_element:
                titulo_salmo = titulo_element.get_text(strip=True)
                logger.info(f"Título alternativo encontrado: {titulo_salmo}")
            else:
                logger.warning("Nenhum título encontrado para o salmo")
        
        # 2. Extrair o texto bíblico com versículos
        texto_biblico = []
        
        # Baseado no HTML fornecido, os versículos estão em elementos com classe 'chapter-paragraph'
        versiculos = soup.select('.chapter-paragraph')
        logger.info(f"Encontrados {len(versiculos)} elementos com classe 'chapter-paragraph'")
        
        if not versiculos:
            # Tentativa alternativa - procurar por elementos com classe 'texto'
            versiculos = soup.select('.texto')
            logger.info(f"Tentando com classe 'texto': encontrados {len(versiculos)} elementos")
        
        for i, p in enumerate(versiculos):
            # Extrair número do versículo
            num_versiculo = p.select_one('.versicle-number')
            if num_versiculo:
                num = num_versiculo.get_text(strip=True)
                logger.debug(f"Versículo {num} encontrado")
                
                # Obter todo o texto do parágrafo
                texto_completo = p.get_text()
                # Remover o número do início do texto
                texto_versiculo = texto_completo.replace(num, '', 1).strip()
                
                # Limpar texto removendo quebras de linha extras e espaços duplicados
                texto_versiculo = re.sub(r'\s+', ' ', texto_versiculo)
                texto_versiculo = texto_versiculo.replace('«', '«').replace('»', '»')
                
                texto_biblico.append((num, texto_versiculo))
            else:
                logger.debug(f"Elemento {i+1} não contém número de versículo")
        
        if not texto_biblico:
            logger.warning("Nenhum versículo extraído com os seletores padrão. Tentando abordagem alternativa...")
            
            # Abordagem alternativa: procurar por spans com IDs específicos
            versiculos = soup.find_all(id=re.compile(r'^versicle-\d+$'))
            logger.info(f"Encontrados {len(versiculos)} versículos com IDs específicos")
            
            for versiculo in versiculos:
                # Extrair número do ID
                num_match = re.search(r'versicle-(\d+)', versiculo.get('id', ''))
                if num_match:
                    num = num_match.group(1)
                    texto_versiculo = versiculo.get_text(strip=True)
                    texto_biblico.append((num, texto_versiculo))
        
        # 3. Extrair os comentários/notas
        comentarios = []
        
        # Baseado no HTML fornecido, os comentários estão em modais com .modal-body.text-left .notas
        modais = soup.select('.modal-body.text-left .notas')
        logger.info(f"Encontrados {len(modais)} comentários nos modais")
        
        for modal in modais:
            comentario = modal.get_text(strip=True)
            comentarios.append(comentario)
        
        # Se não encontrou nos modais, tentar outra abordagem
        if not comentarios:
            notas = soup.select('.notas')
            logger.info(f"Encontrados {len(notas)} notas com seletor alternativo")
            for nota in notas:
                comentarios.append(nota.get_text(strip=True))
        
        # Verificar se encontramos conteúdo
        if not texto_biblico:
            logger.error(f"Nenhum versículo extraído para o Salmo {capitulo}")
        if not comentarios:
            logger.info(f"Nenhum comentário encontrado para o Salmo {capitulo}")
        
        return titulo_salmo, texto_biblico, comentarios
    
    except Exception as e:
        logger.exception(f"Erro crítico ao processar {url}: {str(e)}")
        return "Título não encontrado", [], []
    finally:
        try:
            driver.quit()
            logger.info(f"Navegador fechado após processar {url}")
        except:
            logger.warning(f"Não foi possível fechar o navegador após processar {url}")

def formatar_markdown_salmos(titulo_salmo, capitulo, texto_biblico, comentarios):
    """Formata o conteúdo do salmo no estilo Markdown desejado"""
    logger.info(f"Formatando Salmo {capitulo}: {titulo_salmo}")
    
    # Formatar título
    markdown = f"## Salmo {capitulo}: {titulo_salmo}\n\n"
    
    # Formatar versículos
    if texto_biblico:
        for num, texto in texto_biblico:
            markdown += f"**{num}** {texto}\n\n"
    else:
        markdown += "⚠️ **Nenhum texto bíblico foi extraído para este salmo.**\n\n"
        logger.warning(f"Nenhum texto bíblico para o Salmo {capitulo}")
    
    # Formatar comentários
    if comentarios:
        markdown += f"### Comentários do Salmo {capitulo}\n\n"
        # Juntar todos os comentários em um único texto
        markdown += " ".join(comentarios) + "\n\n"
    else:
        markdown += f"### Comentários do Salmo {capitulo}\n\n"
        markdown += "Nenhum comentário encontrado para este salmo.\n\n"
        logger.info(f"Nenhum comentário para o Salmo {capitulo}")
    
    # Adicionar separador
    markdown += "---\n\n"
    
    return markdown

def salvar_em_markdown(conteudo, nome_arquivo="Salmos.md"):
    """Salva o conteúdo extraído em um arquivo Markdown"""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    logger.info(f"Conteúdo salvo em {nome_arquivo} ({len(conteudo)} caracteres)")

def main():
    logger.info("Iniciando extração do livro de Salmos em formato Markdown...")
    
    # Preparar o conteúdo do Markdown
    conteudo_md = "# LIVRO DOS SALMOS\n\n"
    
    # Adicionar introdução
    logger.info("Extraindo introdução...")
    introducao = extrair_introducao()
    conteudo_md += "## Introdução\n\n"
    conteudo_md += introducao + "\n\n"
    conteudo_md += "---\n\n"
    
    # Extrair todos os capítulos de 1 a 150
    base_url = "https://biblia.paulus.com.br/biblia-pastoral/antigo-testamento/livros-sapienciais/salmos/"
    
    for capitulo in range(1, 151):
        url = f"{base_url}{capitulo}"
        
        logger.info(f"Processando Salmo {capitulo} ({capitulo}/150)...")
        titulo_salmo, texto_biblico, comentarios = extrair_capitulo(url)
        
        # Formatar e adicionar ao conteúdo do Markdown
        conteudo_md += formatar_markdown_salmos(titulo_salmo, capitulo, texto_biblico, comentarios)
        
        # Pausa para não sobrecarregar o servidor
        time.sleep(2)
        
        logger.info(f"Salmo {capitulo} processado com sucesso.")
    
    # Salvar tudo em um arquivo Markdown
    salvar_em_markdown(conteudo_md)
    logger.info("Processo concluído! Todos os Salmos foram extraídos no formato Markdown.")

if __name__ == "__main__":
    main()