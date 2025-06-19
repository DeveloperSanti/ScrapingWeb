#librerias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

#configuracion del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Inicia maximizado
options.add_argument("--disable-blink-features=AutomationControlled")

# Crear el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Buscar en Amazon
busqueda = ""
url = "https://www.amazon.com/"
driver.get(url)

# Esperar y buscar el cuadro de búsqueda
time.sleep(2)
search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys(busqueda)
search_box.send_keys(Keys.RETURN)
