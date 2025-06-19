# Librerías
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Parámetros
busqueda = "portatil lenovo thinkpad"
url = "https://www.amazon.com/"
driver.get(url)

# Esperar a que aparezca el cuadro de búsqueda
wait = WebDriverWait(driver, 15)
search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
search_box.send_keys(busqueda)
search_box.send_keys(Keys.RETURN)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # esperar a que carguen nuevos productos
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Esperar resultados
time.sleep(10)

# Rutas relativas (correctas)
titulo = './/h2'
precioWhole = './/span[@class="a-price-whole"]'
precioFraction = './/span[@class="a-price-fraction"]'
precio2 = './/span[@class="a-color-base"]'
descuento = './/span[@class="a-price a-text-price"]//span[@class="a-offscreen"]'
calificacion = './/i//span'
observacion = './/span[@class="a-color-secondary"]'


# Función para extraer texto si existe
def extraer_elemento(elemento, xpath_variable):
    try:
        return elemento.find_element(By.XPATH, xpath_variable).text.strip()
    except:
        return "No disponible"


# Función para extraer el precio
def extraer_precio(elemento, xpath_whole, xpath_fraction, xpath_alternativo):
    try:
        whole = elemento.find_element(By.XPATH, xpath_whole).text.strip().replace(",", "")
        fraction = elemento.find_element(By.XPATH, xpath_fraction).text.strip()
        return f"{whole}.{fraction}"
    except:
        try:
            alt_price = elemento.find_element(By.XPATH, xpath_alternativo).text.strip().split("$")[1]
            return alt_price if alt_price else "No disponible"
        except:
            return "No disponible"


def extraer_descuento(elemento):
    try:
        descuento_elem = elemento.find_element(By.XPATH, ".//span[@class='a-price a-text-price']//span[@class='a-offscreen']")
        return descuento_elem.get_attribute("textContent").strip().split("$")[1]
    except:
        return "No disponible"

def extraer_calificacion(elemento):
    try:
        calificacion_elem = elemento.find_element(By.XPATH, ".//i//span")
        return calificacion_elem.get_attribute("textContent").strip().split(" ")[0]
    except:
        return "No disponible"



# Lista para almacenar resultados
main_products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
try:
    carousel = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-carousel")))
    carousel_products = carousel.find_elements(By.XPATH, './/li[contains(@class,"a-carousel-card")]')
except:
    carousel_products = []

all_products = main_products + carousel_products
datos = []

while True:

    for prod in all_products:
        info = {
            "Título": extraer_elemento(prod, titulo),
            "Precio": extraer_precio(prod, precioWhole, precioFraction, precio2),
            "Descuento": extraer_descuento(prod),
            "Calificación": extraer_calificacion(prod),
            "Observación": extraer_elemento(prod, observacion)
        }
        datos.append(info)
    print("Página procesada")

    # Intentar ir a la siguiente página
    try:
        next_page = driver.find_element(By.XPATH, '//a[contains(@class, "s-pagination-next")]')
        driver.execute_script("arguments[0].click();", next_page)
        time.sleep(7)
    except:
        print("No hay más páginas.")
        break

# Guardar en Excel
df = pd.DataFrame(datos)
df.to_excel("productos_amazon.xlsx", index=False)
print("Datos guardados en productos_amazon.xlsx")



