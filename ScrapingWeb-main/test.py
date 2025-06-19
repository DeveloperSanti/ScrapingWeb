#librerias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

#configuracion del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") # Inicia maximizado
options.add_argument("--disable-blink-features=AutomationControlled")

# Crear el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Buscar en Amazon
busqueda = "portatil lenovo thinkpad"
url = "https://www.amazon.com/"
driver.get(url)
time.sleep(5)

#buscar el cuadro de búsqueda

search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys(busqueda)
search_box.send_keys(Keys.RETURN)
time.sleep(5)



#rutas
titulo='//div[@class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style"]//a//h2'
precioWhole='//span[@class="a-price-whole"]'
precioFraction='//span[@class="a-price-fraction"]'
descuento='//div[@class="a-section aok-inline-block"]//span[@class="a-price a-text-price"]//span[@class="a-offscreen"]'
calificacion='//div[@class="a-row a-size-small"]//span//a//i//span'
observacion='//div[@class="a-row a-spacing-micro"]//span//a//span//span[@class="a-color-secondary"]'
precio2='//div[@class="a-row a-size-base a-color-secondary"]//span[@class="a-color-base"]'
#numero = float(texto.split("$")[1])




# Lista para almacenar los datos
resultados = []

# Extraer productos
productos = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
for prod in productos:
    try:
        titulo = prod.find_element(By.XPATH, './/h2/a/span').text.strip()
    except:
        titulo = "No disponible"

    try:
        precio = prod.find_element(By.XPATH, './/span[@class="a-price-whole"]').text.strip()
        precio += prod.find_element(By.XPATH, './/span[@class="a-price-fraction"]').text.strip()
    except:
        precio = "No disponible"

    try:
        patrocinado = prod.find_element(By.XPATH, '//div[@class="a-row a-spacing-micro"]//span//a//span//span')
        es_patrocinado = "Sí"
    except:
        es_patrocinado = "No"

    resultados.append({
        "Título": titulo,
        "Precio": precio,
        "¿Patrocinado?": es_patrocinado
    })

# Cerrar navegador
driver.quit()

# Guardar en Excel
df = pd.DataFrame(resultados)
df.to_excel("resultados_amazon.xlsx", index=False)
print("Datos guardados")



#Crear los metodos para guardar la informaciíon extraida de dicha pagina web en un archivo excel, tengo las rutas guardadas en variables, es decir que debo pasar como xpath la variable. precioWhole y precioFraction se deben sumar y precio2 es otra forma de extraer el precio, entonces ese metodo debe buscar de la primer forma que es con las 2 davriables que se suman, la segundo forma es con la variable precio2 y validar si no tiene precio que tambien es una posibilidad