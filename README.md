def guardar_en_dataframe(productos):
    df = pd.DataFrame(productos)
    df["precio_actual"] = df["precio_actual"].str.replace(r'[^\d.]', '', regex=True)  # Eliminar símbolos
    df["precio_actual"] = pd.to_numeric(df["precio_actual"], errors="coerce")#convertimos la columna "precio_actual" a numerico
    df["precio_actual"] = np.where(df["precio_actual"] >= 50, df["precio_actual"].round(), df["precio_actual"])# Aplicar redondeo solo a los valores >= 50
 
    df["precio_anterior"] = df["precio_anterior"].str.replace(r'[^\d.]', '', regex=True)  # Eliminar símbolos
    df["precio_anterior"] = pd.to_numeric(df["precio_anterior"], errors="coerce")  # Convertir a float
    df["precio_anterior"] = df["precio_anterior"].fillna(df["precio_actual"])
    # Reemplazar NaN en "precio_anterior" con "precio_actual"
 
    df = df[df["nombre"].str.contains("iPhone", na=False)]
    df = df.sort_values(by='precio_actual', ascending=False) #Ordena los precios de mayor a menor
 
    return df


    # Librerías
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")

busqueda = input('Ingresa una busqueda: ')

# Abrir navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Parámetros
url = "https://www.amazon.com/"
driver.get(url)

# Esperando cuadro de búsqueda
wait = WebDriverWait(driver, 15)
search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
search_box.send_keys(busqueda)
search_box.send_keys(Keys.RETURN)

def extraer_resultados_busqueda(driver):
    try:
        # Extraigo el texto de la página de resultados de búsqueda
        result_text = driver.find_element(By.XPATH, "//span[contains(text(),'resultados para')]").text
        print("Texto extraído:", result_text)

        # Convertimos el texto extraído a un número
        match = re.search(r'(\d+)\s+a\s+(\d+)', result_text)
        if match:
            numero_deseado = int(match.group(2))
            print(result_text)
        else:
            numero_deseado = 0
        return numero_deseado
    except Exception as e:
        print(f"Error al extraer resultados de búsqueda: {e}")
        return 0

def extraer_cantidad_paginas(driver):
    try:
        paginas = driver.find_elements(By.XPATH, "//*[contains(@class,'s-pagination-item') and not(contains(@class,'dots'))]")

        num_paginas = [int(i.text) for i in paginas if i.text.isdigit()]

        total_pages = max(num_paginas, default=1)

        print("Total páginas:", total_pages)
        return total_pages
    except Exception as e:
        print(f"Error al extraer la cantidad de páginas: {e}")
        return 1

# Rutas XPATH
titulo = './/h2'
precioWhole = './/span[@class="a-price-whole"]'
precioFraction = './/span[@class="a-price-fraction"]'
precio2 = ".//div[@class='a-section a-spacing-none a-spacing-top-mini']//div[@class='a-row a-size-base a-color-secondary']//span[@class='a-color-base']"
calificacion = (
    ".//div[@class='a-row a-size-small']//span//a//i//span | .//div[@class='a-icon-row']//a//i//span"
)
observacion = ".//div[@class='a-row a-spacing-micro']//span//a//span[@class='a-color-secondary']"
xpath_titulos = (
    ".//div[@class='a-section a-spacing-none a-spacing-top-small s-title-instructions-style']//a//h2"
    " | .//div[@class='a-section a-spacing-none puis-padding-right-small s-title-instructions-style']//a//h2"
    " | .//div[@class='a-section a-spacing-none puis-padding-right-small s-title-instructions-style faceout-product-title']//a//h2"
    " | .//div[@class='p13n-sc-uncoverable-faceout']//div//div//a//span//div"
    " | .//div[@class='a-box-inner a-padding-none']//div[@class='a-row']//span[@class='a-color-base sp_short_strip_title']"
    " | .//*[@id='dynamic-bb']/div/div/div[1]"
)

# Funcion principal
def extraer_elemento(elemento, xpath_variable):
    try:
        return elemento.find_element(By.XPATH, xpath_variable).text
    except:
        return "General"



def extraer_nombre(item):
    try:
        nombre = item.find_element(By.XPATH, xpath_titulos).text
        return nombre[:35]
    except:
        return "no disponible"


def extraer_precio(elemento):
    try:
        whole = elemento.find_element(By.XPATH, precioWhole).text.strip().replace(",", "")
        fraction = elemento.find_element(By.XPATH, precioFraction).text.strip()
        precio_actual = f"{whole}.{fraction}"
        return precio_actual
    except:
        try:
            alt_price = elemento.find_element(By.XPATH, precio2).text.strip().split("$")[1]
            return alt_price if alt_price else "N/A"
        except:
            return "N/A"


def extraer_precio_full(elemento):
    try:
        precio_full = elemento.find_element(By.XPATH,
                                               ".//span[@class='a-price a-text-price']//span[@class='a-offscreen']")
        precio_full = precio_full.get_attribute("textContent").strip().split("$")[1]
    except:
        precio_full = "N/A"
    return precio_full

def extraer_descuento(precio_full, precio_actual):
    try:
        precio_actual = float(precio_actual) if precio_actual != "N/A" else 0
        precio_full = float(precio_full) if precio_full != "N/A" else 0
        descuento = precio_full - precio_actual
    
        if descuento < 0:
            descuento = 0
    except:
        return "N/A"
    
    return descuento
        
    

def extraer_calificacion(elemento):
    try:
        calificacion_elem = elemento.find_element(By.XPATH, calificacion)
        return calificacion_elem.get_attribute("textContent").strip().split(" ")[0]
    except:
        return "N/A"


# Lista final de resultados
datos = []

while True:
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))

    main_products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
    try:
        carousel = driver.find_element(By.CLASS_NAME, "a-carousel")
        carousel_products = carousel.find_elements(By.XPATH, './/li[contains(@class,"a-carousel-card")]')
    except:
        carousel_products = []

    all_products = main_products + carousel_products

    for prod in all_products:

        info = {
            "Título": extraer_nombre(prod),
            "Precio_actual": extraer_precio(prod),
            "Pecio_full": extraer_precio_full(prod),
            "Descuento": extraer_descuento(extraer_precio_full(prod), extraer_precio(prod)),
            "Calificación": extraer_calificacion(prod),
            "Observación": extraer_elemento(prod, observacion)
        }
        datos.append(info)

    print("Página procesada")
    # Pasar a la siguiente página
    try:
        next_page = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                           '//a[contains(@class, "s-pagination-next") and not(contains(@class, "s-pagination-disabled"))]')))
        driver.execute_script("arguments[0].click();", next_page)
    except:
        print("No hay más páginas.")
        break

# Guardar en Excel
df = pd.DataFrame(datos)
df.to_excel("productos_amazon.xlsx", index=False)
print("Datos guardados en productos_amazon.xlsx")


