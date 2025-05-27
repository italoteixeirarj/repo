from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Caminho para o chromedriver no seu sistema
caminho_chromedriver = '/caminho/para/chromedriver'

# Número da nota SAP
nota = '3552903'

# Iniciar o navegador
service = Service(caminho_chromedriver)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)

# Abrir a nota diretamente
url = f"https://launchpad.support.sap.com/#/notes/{nota}"
driver.get(url)

# Aguardar o login manual (ou automatizar se desejar)
print("Por favor, faça login com seu S-user no navegador... aguardando 60s")
time.sleep(60)

# Exemplo de como localizar o título da nota
try:
    title = driver.find_element(By.CLASS_NAME, "title").text
    print(f"Título da nota {nota}: {title}")
except Exception as e:
    print("Não foi possível capturar o título:", e)

# Mantenha o navegador aberto se quiser inspecionar mais
