from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace
from functools import reduce
from autotec.scrapers import scraper_dani, scraper_neiel, scraper_martin, scraper_belenandrades

data_dani = scraper_dani.ejecutar_extraccion()
data_neiel = scraper_neiel.ejecutar_extraccion()
#data_martin = scraper_martin.ejecutar_extraccion()
#data_belen = scraper_belenandrades.ejecutar_extraccion()

spark = (
    SparkSession.builder
    .appName("IntegradoraBigData")
    .config("spark.mongodb.write.connection.uri", "mongodb+srv://neiel_cortes:neiel0330@cluster0.eo0kyfv.mongodb.net/AutoTec_db?retryWrites=true&w=majority")
    .getOrCreate()
)

df_dani = spark.createDataFrame(data_dani)
df_neiel = spark.createDataFrame(data_neiel)
#df_martin = spark.createDataFrame(data_martin)
#df_belen = spark.createDataFrame(data_belen)

df_final = reduce(lambda a, b: a.unionByName(b, allowMissingColumns=True),
                  [df_dani, df_neiel])

df_limpio = df_final.withColumn(
    "valor_numerico",
    regexp_replace(col("valor"), "[^0-9]", "").cast("double")
)

df_limpio.write \
    .format("mongodb") \
    .mode("append") \
    .option("spark.mongodb.write.connection.uri", "mongodb+srv://neiel_cortes:neiel0330@cluster0.eo0kyfv.mongodb.net/AutoTec_db?retryWrites=true&w=majority") \
    .option("spark.mongodb.write.database", "proyecto_bigdata") \
    .option("spark.mongodb.write.collection", "lista_autos") \
    .save()

print("¡Proceso completado!")