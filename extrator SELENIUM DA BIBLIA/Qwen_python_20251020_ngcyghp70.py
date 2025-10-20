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
import sys

# Criar pasta de logs se não existir
os.makedirs("logs", exist_ok=True)

# Configurar logging detalhado para salvar na pasta logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/extraction.log"),
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

def limpar_texto(texto):
    """Limpa e formata o texto para resolver problemas de espaçamento"""
    if not texto:
        return texto
    
    # Substituir múltiplos espaços por um único espaço
    texto = re.sub(r'\s+', ' ', texto)
    
    # Garantir espaço após pontuação
    texto = re.sub(r'([,.:;?!])([a-zA-ZÀ-ú])', r'\1 \2', texto)
    
    # Garantir espaço antes de aspas abertas
    texto = re.sub(r'([a-zA-ZÀ-ú])(«)', r'\1 \2', texto)
    
    # Garantir espaço após aspas fechadas
    texto = re.sub(r'(»)([a-zA-ZÀ-ú])', r'\1 \2', texto)
    
    # Remover espaços extras antes de pontuação
    texto = re.sub(r'\s+([,.:;?!»])', r'\1', texto)
    
    # Corrigir casos específicos de palavras grudadas
    texto = re.sub(r'([a-z])([A-Z])', r'\1 \2', texto)
    
    # Remover espaços no início e fim
    texto = texto.strip()
    
    return texto

def extrair_conteudo(url):
    """Extrai conteúdo da página, seja introdução ou capítulo"""
    logger.info(f"Acessando: {url}")
    
    driver = configurar_navegador()
    if not driver:
        return "Erro ao configurar o navegador", [], []
    
    try:
        logger.info(f"Navegando para {url}...")
        driver.get(url)
        
        # Esperar até que o conteúdo esteja presente
        logger.info("Aguardando carregamento do conteúdo...")
        try:
            # Primeiro tenta encontrar elementos de capítulo
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".chapter-paragraph, .texto-intro"))
            )
            logger.info("Conteúdo encontrado com sucesso.")
        except Exception as e:
            logger.warning(f"Conteúdo não encontrado após 15 segundos: {str(e)}")
            return "Erro: Conteúdo não encontrado", [], []
        
        # Obter o HTML renderizado
        html = driver.page_source
        
        # Para debug: salvar o HTML em um arquivo
        livro = re.search(r'/livros-sapienciais/([^/]+)', url)
        livro_nome = livro.group(1) if livro else "desconhecido"
        
        capitulo = re.search(r'/salmos/(\d+)', url)
        cap_num = capitulo.group(1) if capitulo else "introducao"
        
        os.makedirs(f"logs/debug", exist_ok=True)
        with open(f"logs/debug/{livro_nome}_{cap_num}.html", "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"HTML salvo em logs/debug/{livro_nome}_{cap_num}.html para análise de debug")
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Verificar se é uma página de introdução (URL sem número de capítulo)
        is_introducao = not bool(re.search(r'/\d+$', url))
        
        # 1. Extrair título
        titulo = "Título não encontrado"
        if is_introducao:
            titulo_element = soup.select_one('.title-content')
            if titulo_element:
                titulo = titulo_element.get_text(strip=True)
        else:
            titulo_element = soup.select_one('.container-chapter-title h4, .containerTitle h4')
            if titulo_element:
                titulo = titulo_element.get_text(strip=True)
                # Limpar título de referências numéricas
                titulo = re.sub(r'\[.*?\]', '', titulo).strip()
        
        logger.info(f"Título identificado: {titulo}")
        
        # 2. Extrair texto principal
        texto_principal = []
        
        if is_introducao:
            # Página de introdução
            intro_element = soup.select_one('.texto-intro')
            if intro_element:
                texto = limpar_texto(intro_element.get_text())
                texto_principal.append(("INTRODUCAO", texto))
            else:
                # Tentativa alternativa para introdução
                container = soup.select_one('.sub-intro-ca, .container-content')
                if container:
                    texto = limpar_texto(container.get_text())
                    texto_principal.append(("INTRODUCAO", texto))
        else:
            # Página de capítulo
            versiculos = soup.select('.chapter-paragraph')
            
            if not versiculos:
                versiculos = soup.select('.texto')
            
            for p in versiculos:
                # Extrair número do versículo
                num_versiculo = p.select_one('.versicle-number')
                if num_versiculo:
                    num = num_versiculo.get_text(strip=True)
                    
                    # Obter todo o texto do parágrafo
                    texto_completo = p.get_text()
                    # Remover o número do início do texto
                    texto_versiculo = texto_completo.replace(num, '', 1).strip()
                    
                    # Limpar texto
                    texto_versiculo = limpar_texto(texto_versiculo)
                    
                    texto_principal.append((num, texto_versiculo))
                else:
                    # Se não tem número de versículo, mas é um parágrafo relevante
                    texto = limpar_texto(p.get_text())
                    if len(texto) > 20:  # Evitar textos muito curtos
                        texto_principal.append(("SEM_NUM", texto))
        
        # 3. Extrair comentários
        comentarios = []
        modais = soup.select('.modal-body.text-left .notas, .notas')
        
        for modal in modais:
            comentario = limpar_texto(modal.get_text())
            comentarios.append(comentario)
        
        return titulo, texto_principal, comentarios
    
    except Exception as e:
        logger.exception(f"Erro ao processar {url}: {str(e)}")
        return "Erro ao processar página", [], []
    finally:
        try:
            driver.quit()
            logger.info("Navegador fechado com sucesso.")
        except:
            logger.warning("Não foi possível fechar o navegador")

def formatar_markdown(titulo, url, texto_principal, comentarios, is_introducao=False):
    """Formata o conteúdo no estilo Markdown desejado"""
    logger.info(f"Formatando conteúdo: {titulo}")
    
    # Extrair nome do livro e capítulo da URL
    livro_match = re.search(r'/livros-sapienciais/([^/]+)', url)
    livro_nome = livro_match.group(1).capitalize() if livro_match else "Livro"
    
    capitulo_match = re.search(r'/(\d+)$', url)
    capitulo = capitulo_match.group(1) if capitulo_match else "Introdução"
    
    # Formatar título
    if is_introducao:
        markdown = f"## Introdução do Livro de {livro_nome}\n\n"
    else:
        markdown = f"## {titulo}\n\n"
    
    # Formatar texto principal
    if texto_principal:
        for num, texto in texto_principal:
            if num == "INTRODUCAO":
                markdown += f"{texto}\n\n"
            elif num == "SEM_NUM":
                markdown += f"{texto}\n\n"
            else:
                markdown += f"**{num}** {texto}\n\n"
    else:
        markdown += "⚠️ **Nenhum texto foi extraído desta página.**\n\n"
        logger.warning("Nenhum texto extraído")
    
    # Formatar comentários
    if comentarios:
        if is_introducao:
            markdown += f"### Comentários da Introdução\n\n"
        else:
            markdown += f"### Comentários do Capítulo {capitulo}\n\n"
        markdown += " ".join(comentarios) + "\n\n"
    
    # Adicionar separador
    markdown += "---\n\n"
    
    return markdown

def obter_proximo_link(driver, url_atual):
    """Obtém o link da próxima página usando o botão 'próximo'"""
    try:
        # Verificar se é uma página de introdução
        is_introducao = not bool(re.search(r'/\d+$', url_atual))
        
        if is_introducao:
            # Na página de introdução, o próximo link é o capítulo 1
            livro_match = re.search(r'/livros-sapienciais/([^/]+)', url_atual)
            livro_nome = livro_match.group(1) if livro_match else ""
            
            if livro_nome:
                return f"{url_atual.rstrip('/')}/1"
            return None
        
        # Para páginas de capítulo, usar o botão "próximo"
        try:
            # Esperar até que o botão de próximo esteja presente
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#btn-next, a.fa-chevron-right"))
            )
            proximo_link = next_button.get_attribute("href")
            return proximo_link
        except Exception as e:
            logger.warning(f"Não foi possível encontrar o botão 'próximo': {str(e)}")
            return None
            
    except Exception as e:
        logger.exception(f"Erro ao obter próximo link: {str(e)}")
        return None

def main():
    logger.info("Iniciando extrator de textos bíblicos")
    
    # Obter inputs do usuário
    nome_arquivo = input("Digite o nome do arquivo de saída (sem extensão): ").strip()
    if not nome_arquivo:
        nome_arquivo = "Biblia"
    
    link_inicio = input("Digite o link de início: ").strip()
    link_fim = input("Digite o link de fim: ").strip()
    
    if not link_inicio or not link_fim:
        logger.error("Links de início e fim são obrigatórios")
        sys.exit(1)
    
    # Validar se os links são da Bíblia Paulus
    if "biblia.paulus.com.br" not in link_inicio or "biblia.paulus.com.br" not in link_fim:
        logger.error("Os links devem ser do site biblia.paulus.com.br")
        sys.exit(1)
    
    # Preparar o conteúdo do Markdown
    conteudo_md = f"# {nome_arquivo}\n\n"
    
    # Verificar se é uma página de introdução
    is_introducao_inicio = not bool(re.search(r'/\d+$', link_inicio))
    
    # Extrair conteúdo inicial
    logger.info(f"Extraindo conteúdo inicial de: {link_inicio}")
    
    # Configurar navegador para verificar o link de início
    driver = configurar_navegador()
    if not driver:
        logger.error("Não foi possível configurar o navegador")
        sys.exit(1)
    
    try:
        driver.get(link_inicio)
        # Extrair conteúdo da página inicial
        titulo, texto_principal, comentarios = extrair_conteudo(link_inicio)
        
        # Formatar e adicionar ao conteúdo do Markdown
        conteudo_md += formatar_markdown(titulo, link_inicio, texto_principal, comentarios, is_introducao_inicio)
        
        # Se for uma página de introdução, começar pelo capítulo 1
        if is_introducao_inicio:
            livro_match = re.search(r'/livros-sapienciais/([^/]+)', link_inicio)
            livro_nome = livro_match.group(1) if livro_match else ""
            
            if livro_nome:
                capitulo_atual = f"{link_inicio.rstrip('/')}/1"
            else:
                logger.error("Não foi possível determinar o livro a partir do link de início")
                sys.exit(1)
        else:
            capitulo_atual = link_inicio
    
        # Navegar até o link de fim
        logger.info(f"Iniciando navegação até: {link_fim}")
        
        while capitulo_atual != link_fim:
            # Obter próximo link
            driver.get(capitulo_atual)
            proximo_link = obter_proximo_link(driver, capitulo_atual)
            
            if not proximo_link:
                logger.error("Não foi possível encontrar o próximo link")
                break
                
            logger.info(f"Processando: {proximo_link}")
            
            # Extrair conteúdo
            titulo, texto_principal, comentarios = extrair_conteudo(proximo_link)
            
            # Verificar se chegou ao link de fim
            if proximo_link == link_fim:
                # Extrair conteúdo do link de fim
                titulo, texto_principal, comentarios = extrair_conteudo(link_fim)
                conteudo_md += formatar_markdown(titulo, link_fim, texto_principal, comentarios)
                break
            
            # Formatar e adicionar ao conteúdo do Markdown
            conteudo_md += formatar_markdown(titulo, proximo_link, texto_principal, comentarios)
            
            # Atualizar capitulo_atual
            capitulo_atual = proximo_link
            
            # Pausa para não sobrecarregar o servidor
            time.sleep(2)
    
    finally:
        try:
            driver.quit()
            logger.info("Navegador fechado com sucesso.")
        except:
            logger.warning("Não foi possível fechar o navegador")
    
    # Salvar tudo em um arquivo Markdown
    nome_arquivo_final = f"{nome_arquivo}.md"
    with open(nome_arquivo_final, 'w', encoding='utf-8') as f:
        f.write(conteudo_md)
    
    logger.info(f"Processo concluído! Conteúdo salvo em {nome_arquivo_final}")

if __name__ == "__main__":
    main()