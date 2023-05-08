from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Configuração do Microsoft Edge Driver
edge_options = webdriver.EdgeOptions()
edge_options.binary_location = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
edge_driver = 'C:/path/to/msedgedriver.exe'  # Substitua pelo caminho para o seu executável do Edge Driver
edge_options.add_argument('--disable-logging')
driver = webdriver.Edge(executable_path=edge_driver, options=edge_options)

# Configuração dos sites de streaming
sites = {
    'twitch': 'https://www.twitch.tv/',
    'youtube': 'https://www.youtube.com/',
    'nimo': 'https://www.nimo.tv/',
    'mercadolivre': 'https://lista.mercadolivre.com.br/',
}

# Função para extrair informações do site
def extract_info(site, search_term):
    url = sites[site] + search_term
    driver.get(url)
    if site == 'mercadolivre':
    # Encontrar os elementos com informações do produto
        items = WebDriverWait(driver, 2000).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ui-search-layout__item')))
        results = []
        for item in items:
            try:
                name = item.find_element(By.CSS_SELECTOR, '.ui-search-item__title').text
            except NoSuchElementException:
                name = ""
            try:
                price = item.find_element(By.CSS_SELECTOR, '.price-tag-fraction').text
            except NoSuchElementException:
                price = ""
            try:
                seller_rating = item.find_element(By.CSS_SELECTOR, '.ui-search-reviews__rating').text
            except NoSuchElementException:
                seller_rating = ""
            results.append((name, price, seller_rating))
            # Ordenar os resultados por preço
            if len(results) >= 10:  # adiciona condição de parada
                break
        results = sorted(results, key=lambda x: float(x[1].replace('R$', '').replace('.', '').replace(',', '.')) if x[1] else float('inf'))
        return results
    elif site == 'twitch':
        # Aqui você pode usar o Selenium para encontrar e extrair informações do site
        # e retorná-las como uma string ou uma lista
        return 'resultado_da_busca'

# Loop para permitir que o usuário escolha o site e o termo de busca
while True:
    site = input('Digite o site de streaming que deseja buscar (twitch, youtube, nimo, mercadolivre): ')
    if site in sites:
        break
    print('Site inválido! Tente novamente.')
    
search_term = input('Digite o termo de busca: ')

# Extrai as informações do site e imprime o resultado
result = extract_info(site, search_term)
if site == 'mercadolivre':
    print('Data:', search_term)
    print('Resultado:')
    for name, price, seller_rating in result:
        print(f'{name} - {price} - {seller_rating}')
else:
    print('Data:', search_term)
    print('Resultado:', result)

# Encerra o driver
driver.quit()
