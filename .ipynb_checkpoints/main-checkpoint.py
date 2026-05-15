from pyspark.sql import SparkSession
<<<<<<< HEAD
from autotec.scrapers import scraper_dani, scraper_neiel
from pyspark.sql.functions import col, regexp_replace

# 1. prueba scrappers neiel dani
data_dani = scraper_dani.ejecutar_extraccion()
data_neiel = scraper_neiel.ejecutar_extraccion()

# 2. Iniciamos Spark
spark = (
    SparkSession.builder
    .appName("IntegradoraBigData")
    .config("spark.mongodb.output.uri", "mongodb+srv://neiel_cortes:neiel0330@cluster0.eo0kyfv.mongodb.net/AutoTec_db?retryWrites=true&w=majority")
    .getOrCreate()
)

# 3. Spark convierte las listas en un solo DataFrame unificado
df_dani = spark.createDataFrame(data_dani)
df_neiel = spark.createDataFrame(data_neiel)

df_final = df_neiel.union(df_dani)
print(f"DataFrame final: {df_final.count()} registros")
# 4. Acción de Spark: limpieza y transformación
df_limpio = df_final.withColumn(
    "valor_numerico",
    regexp_replace(col("valor"), "[^0-9]", "").cast("float")
)

# 5. Spark guarda todo de un solo golpe en MongoDB
print("Guardando en MongoDB...")
df_limpio.write \
    .format("mongodb") \
    .mode("append") \
    .option("database", "autotec_db") \
    .option("collection", "productos_unificados") \
    .save()

print("¡Proceso completado!")
=======
from autotec.scrapers import scraper_dani, scraper_neiel, scraper_martin, scraper_belenandrades1,scraper_belenandrades2, scraper_belenandrades3, scraper_belenandrades4, scraper_javiera, scraper_jocelyn, scraper_luz, scraper_martin2

# Configuración de Spark (Mantenlo fuera de las funciones para no recrear la sesión)
spark = (
    SparkSession.builder
    .appName("AutoTec_Batch_Processing")
    .config("spark.mongodb.write.connection.uri", "mongodb+srv://neiel_cortes:neiel0330@cluster0.eo0kyfv.mongodb.net/AutoTec_db")
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") # Asegúrate de tener el conector
    .getOrCreate()
)

def procesar_y_guardar(lista_scrapers):
    """Ejecuta scrapers y realiza un UPSERT en MongoDB para evitar duplicados"""
    for nombre, funcion in lista_scrapers:
        print(f"\n🚀 Procesando: {nombre}")
        try:
            datos = funcion()
            if datos and len(datos) > 0:
                # 1. Aseguramos que cada dato tenga un campo _id (opcional pero recomendado)
                # O podemos decirle a Spark qué campo usar como llave.
                df = spark.createDataFrame(datos)
                
                # 2. Configuración de UPSERT
                df.write \
                    .format("mongodb") \
                    .mode("append") \
                    .option("database", "proyecto_bigdata") \
                    .option("collection", "lista_autos") \
                    .option("operationType", "update") \
                    .option("upsertDocument", "true") \
                    .option("shardKey", '{"url": 1}') \
                    .save()
                
                print(f"✅ {nombre}: {len(datos)} registros procesados (actualizados/insertados) en MongoDB.")
            else:
                print(f"⚠️ {nombre}: No se obtuvieron datos.")
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
# --- DEFINICIÓN DE TANDAS ---

# Tanda 1
grupo_1 = [
    ("Dani", scraper_dani.ejecutar_extraccion),
    ("Neiel", scraper_neiel.ejecutar_extraccion),
    ("Martin", scraper_martin.ejecutar_extraccion),
    ("Belen1", scraper_belenandrades1.ejecutar_extraccion),
    ("Belen2", scraper_belenandrades2.ejecutar_extraccion),
    ("Belen3", scraper_belenandrades3.ejecutar_extraccion)
]

# Tanda 2
grupo_2 = [
    ("Luz", scraper_luz.ejecutar_extraccion),
    ("Martin2", scraper_martin2.ejecutar_extraccion),
    ("Belen4", scraper_belenandrades4.ejecutar_extraccion),
    ("Jocelyn", scraper_jocelyn.ejecutar_extraccion),
    ("Javiera", scraper_javiera.ejecutar_extraccion)
]

# --- EJECUCIÓN ---
# Puedes comentar una línea para ejecutar solo la otra
#print("Iniciando Tanda 1...")
#procesar_y_guardar(grupo_1)

print("Iniciando Tanda 2...")
procesar_y_guardar(grupo_2)

print("\n¡Proceso de carga parcial completado!")
>>>>>>> 89b3dfa679dc7db574f723f294f580a3f8ecf079
