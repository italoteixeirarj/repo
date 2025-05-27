from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

# Caminho para o Edge WebDriver
caminho_msedgedriver = 'C:\\edgedriver\\msedgedriver.exe'  # ajuste conforme o seu caminho

# Configurações do Edge
options = Options()
options.add_argument("--start-maximized")

service = EdgeService(executable_path=caminho_msedgedriver)
driver = webdriver.Edge(service=service, options=options)

# Número da nota
nota = "3552903"
url = f"https://launchpad.support.sap.com/#/notes/{nota}"
driver.get(url)

print("⚠️ Faça login com seu S-user manualmente no navegador... Aguardando 60 segundos.")
time.sleep(60)

# Exemplo: buscar o título da nota após login
try:
    title = driver.find_element(By.CLASS_NAME, "title").text
    print(f"Título da nota {nota}: {title}")
except Exception as e:
    print("❌ Não foi possível encontrar o título:", e)
