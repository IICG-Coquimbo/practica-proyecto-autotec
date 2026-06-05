<<<<<<< HEAD
#Contenedor A

import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from autotec.scrapers import   scraper_dani, scraper_neiel, scraper_martin, scraper_belenandrades1, scraper_belenandrades3, scraper_belenandrades4, scraper_javiera, scraper_jocelyn, scraper_luz, scraper_martin2, scraper_belenandrades5
# scraper_dani, scraper_neiel, scraper_martin, scraper_belenandrades1, scraper_belenandrades3, scraper_belenandrades4, scraper_javiera, scraper_jocelyn, #scraper_luz, scraper_martin2, scraper_belenandrades5

# Configuración de Spark (Mantenlo fuera de las funciones para no recrear la sesión)

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
spark = (
    SparkSession.builder
    .appName("AutoTec_Batch_Processing")
    .config("spark.mongodb.write.connection.uri", MONGO_URI)
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1")
=======
from pyspark.sql import SparkSession
from autotec.scrapers import scraper_dani, scraper_neiel, scraper_martin, scraper_belenandrades1,scraper_belenandrades2, scraper_belenandrades3, scraper_belenandrades4, scraper_javiera, scraper_jocelyn, scraper_luz, scraper_martin2, scraper_martin3, scraper_belenandrades5

# Configuración de Spark (Mantenlo fuera de las funciones para no recrear la sesión)
spark = (
    SparkSession.builder
    .appName("AutoTec_Batch_Processing")
    .config("spark.mongodb.write.connection.uri", "mongodb+srv://neiel_cortes:neiel0330@cluster0.eo0kyfv.mongodb.net/AutoTec_db")
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") # Asegúrate de tener el conector
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
    .getOrCreate()
)

def procesar_y_guardar(lista_scrapers):
    """Ejecuta scrapers y realiza un UPSERT en MongoDB para evitar duplicados"""
    for nombre, funcion in lista_scrapers:
        print(f"\n🚀 Procesando: {nombre}")
        try:
            datos = funcion()
            if datos and len(datos) > 0:
<<<<<<< HEAD
=======
                # 1. Aseguramos que cada dato tenga un campo _id (opcional pero recomendado)
                # O podemos decirle a Spark qué campo usar como llave.
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
                df = spark.createDataFrame(datos)
                
                # 2. Configuración de UPSERT
                # 2. Configuración de UPSERT
                df.write \
                    .format("mongodb") \
                    .mode("append") \
                    .option("database", "proyecto_bigdata") \
<<<<<<< HEAD
                    .option("collection", "bd_autos") \
=======
                    .option("collection", "lista_autos") \
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
                    .option("operationType", "update") \
                    .option("upsertDocument", "true") \
                    .option("idFieldList", "url") \
                    .save()
                
                print(f"✅ {nombre}: {len(datos)} registros procesados (actualizados/insertados) en MongoDB.")
            else:
                print(f"⚠️ {nombre}: No se obtuvieron datos.")
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
# --- DEFINICIÓN DE TANDAS ---

# Tanda 1
grupo_1 = [
<<<<<<< HEAD
   ("Dani", scraper_dani.ejecutar_extraccion),
    ("Neiel", scraper_neiel.ejecutar_extraccion),
    ("Martin", scraper_martin.ejecutar_extraccion),
    ("Belen1", scraper_belenandrades1.ejecutar_extraccion),
=======
    ("Dani", scraper_dani.ejecutar_extraccion),
    ("Neiel", scraper_neiel.ejecutar_extraccion),
    ("Martin", scraper_martin.ejecutar_extraccion),
    ("Belen1", scraper_belenandrades1.ejecutar_extraccion),
    ("Belen2", scraper_belenandrades2.ejecutar_extraccion),
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
    ("Belen3", scraper_belenandrades3.ejecutar_extraccion)
]

# Tanda 2
<<<<<<< HEAD
#grupo_2 = [
#    ("Luz", scraper_luz.ejecutar_extraccion),
#    ("Martin2", scraper_martin2.ejecutar_extraccion),
#    ("Belen4", scraper_belenandrades4.ejecutar_extraccion),
#    ("Jocelyn", scraper_jocelyn.ejecutar_extraccion),
#    ("Javiera", scraper_javiera.ejecutar_extraccion),
#    ("Belen5", scraper_belenandrades5.ejecutar_extraccion)

#]

# --- EJECUCIÓN ---
# Puedes comentar una línea para ejecutar solo la otra
print("Iniciando Tanda 1...")
procesar_y_guardar(grupo_1)

#print("Iniciando Tanda 2...")
#procesar_y_guardar(grupo_2)
print("\n¡Proceso de carga parcial completado!")
spark.stop()
=======
grupo_2 = [
    ("Luz", scraper_luz.ejecutar_extraccion),
    ("Martin2", scraper_martin2.ejecutar_extraccion),
    ("Belen4", scraper_belenandrades4.ejecutar_extraccion),
    ("Jocelyn", scraper_jocelyn.ejecutar_extraccion),
    ("Martin3", scraper_martin3.ejecutar_extraccion),
    ("Javiera", scraper_javiera.ejecutar_extraccion),
    ("Belen5", scraper_belenandrades5.ejecutar_extraccion)

]

# --- EJECUCIÓN ---

print("Iniciando Tanda 1...")
procesar_y_guardar(grupo_1)

print("Iniciando Tanda 2...")
procesar_y_guardar(grupo_2)

print("\n¡Proceso de carga parcial completado!")
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
