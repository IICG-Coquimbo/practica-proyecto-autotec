from pyspark.sql import SparkSession
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