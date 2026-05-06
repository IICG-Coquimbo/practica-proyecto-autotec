import os
import re
import time
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- FUNCIONES DE APOYO ---

def limpiar_numero(texto):
    if not texto:
        return 0
    limpio = re.sub(r"[^\d]", "", str(texto))
    return int(limpio) if limpio else 0

def extraer_year(texto):
    match = re.search(r"(20\d{2})", str(texto))
    return int(match.group(1)) if match else 0

def separar_marca_modelo(titulo):
    partes = titulo.split()
    if len(partes) >= 2:
        return partes[0], " ".join(partes[1:])
    return titulo, "No especificado"

def normalizar_combustible(texto):
    texto = texto.lower()
    if "diesel" in texto or "diésel" in texto: return "diesel"
    if "hibrido" in texto or "híbrido" in texto: return "hibrido"
    if "electrico" in texto or "eléctrico" in texto: return "electrico"
    return "gasolina"

def extraer_ciudad(texto):
    # Bruno Fritsch suele listar sucursales o ciudades
    ciudades = ["santiago", "concepcion", "valparaiso", "temuco", "rancagua", "la serena"]
    for c in ciudades:
        if c in texto.lower():
            return c
    return "santiago"

# --- FUNCIÓN PRINCIPAL ---

def ejecutar_extraccion(max_autos=500):
    # 1. Limpieza radical de procesos previos para evitar bloqueos en Docker
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")
    
    # Directorio temporal para que Chrome no choque con otras sesiones
    user_data_dir = tempfile.mkdtemp()
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-allow-origins=*")
    
    # 2. Camuflaje Antidetección (Crucial para Bruno Fritsch)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    autos_extraidos = []
    
    try:
        driver = webdriver.Chrome(options=options)
        # Ocultar la propiedad 'webdriver' de navigator
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        
        print("🌐 Browser de Jocelyn iniciado correctamente.")
        driver.set_page_load_timeout(60)
        driver.get("https://www.brunofritsch.cl/autos-usados")
        
        # Espera inicial generosa para carga dinámica
        time.sleep(10)
        
        links_vistos = set()
        intentos_sin_nuevos = 0

        while len(autos_extraidos) < max_autos and intentos_sin_nuevos < 50:
            # Selector de cuadrícula de Material UI (común en Bruno Fritsch)
            bloques = driver.find_elements(By.CSS_SELECTOR, "div.MuiGrid-item")
            
            puntos_antes = len(autos_extraidos)

            for bloque in bloques:
                if len(autos_extraidos) >= max_autos:
                    break
                
                try:
                    # Validamos que el bloque tenga un link y un precio
                    texto_completo = bloque.text.strip()
                    if "$" not in texto_completo:
                        continue

                    link_elem = bloque.find_element(By.TAG_NAME, "a")
                    link = link_elem.get_attribute("href")
                    
                    if not link or link in links_vistos:
                        continue

                    # Extracción de datos con lógica de respaldo
                    lineas = [l.strip() for l in texto_completo.split("\n") if l.strip()]
                    
                    titulo = lineas[0]
                    marca, modelo = separar_marca_modelo(titulo)
                    
                    # Buscamos el año en todo el texto del bloque
                    year = extraer_year(texto_completo)
                    
                    # Buscamos el precio (la línea que contenga '$')
                    precio_str = next((l for l in lineas if "$" in l), "0")
                    precio = limpiar_numero(precio_str)

                    # Buscamos el kilometraje (la línea que contenga 'km')
                    km_str = next((l for l in lineas if "km" in l.lower()), "0")
                    kilometraje = limpiar_numero(km_str)

                    auto = {
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,
                        "kilometraje": kilometraje,
                        "combustible": normalizar_combustible(texto_completo),
                        "ciudad": extraer_ciudad(texto_completo),
                        "url": link,
                        "precio": precio,
                        "fecha_captura": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": "autotec",
                        "usuario": "jocelyn"
                    }

                    # 3. Validación: Si tiene precio, lo guardamos
                    if auto["precio"] > 0:
                        autos_extraidos.append(auto)
                        links_vistos.add(link)
                        if len(autos_extraidos) % 10 == 0:
                            print(f"✅ {len(autos_extraidos)} autos capturados...")
                except:
                    continue

            # Scroll más agresivo para cargar nuevos elementos
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(3)
            
            if len(autos_extraidos) == puntos_antes:
                intentos_sin_nuevos += 1
            else:
                intentos_sin_nuevos = 0

    except Exception as e:
        print(f"Error fatal en el scraper de Jocelyn: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

    print(f"\n📊 RESULTADO FINAL: {len(autos_extraidos)} autos extraídos.")
    return autos_extraidos