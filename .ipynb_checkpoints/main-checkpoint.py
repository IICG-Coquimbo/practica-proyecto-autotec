from pyspark.sql import SparkSession
from autotec.scrapers import scraper_dani, scraper_neiel, scraper_martin, scraper_belenandrades, scraper_javiera, scraper_jocelyn, scraper_luz, scraper_martin2

data_dani = scraper_dani.ejecutar_extraccion()
print("scraper DANI completado!")
data_neiel = scraper_neiel.ejecutar_extraccion()
print("scraper NEIEL completado!")
data_martin = scraper_martin.ejecutar_extraccion()
print("scraper MARTIN completado!")
data_belen = scraper_belenandrades.ejecutar_extraccion()
print("scraper BELEN completado!")
data_javi = scraper_javiera.ejecutar_extraccion()
print("scraper JAVI completado!")
data_jocy = scraper_jocelyn.ejecutar_extraccion()
print("scraper JOCY completado!")
data_luz = scraper_luz.ejecutar_extraccion()
print("scraper LUZ completado!")
data_martin2 = scraper_martin2.ejecutar_extraccion()
print("scraper MARTIN2 completado!")

spark = (
    SparkSession.builder
    .appName("IntegradoraBigData")
    .config("spark.mongodb.write.connection.uri", "mongodb+srv://neiel_cortes:neiel0330@cluster0.eo0kyfv.mongodb.net/AutoTec_db?retryWrites=true&w=majority")
    .getOrCreate()
)

df_dani = spark.createDataFrame(data_dani)
df_neiel = spark.createDataFrame(data_neiel)
df_martin = spark.createDataFrame(data_martin)
df_belen = spark.createDataFrame(data_belen)
df_javi = spark.createDataFrame(data_javi)
df_jocy = spark.createDataFrame(data_jocy)
df_luz = spark.createDataFrame(data_luz)
df_martin2 = spark.createDataFrame(data_martin2)

df_final = (
    df_neiel
    .unionByName(df_dani, allowMissingColumns=True)
    .unionByName(df_martin, allowMissingColumns=True)
    .unionByName(df_belen, allowMissingColumns=True)
    .unionByName(df_javi, allowMissingColumns=True)
    .unionByName(df_jocy, allowMissingColumns=True)
    .unionByName(df_luz, allowMissingColumns=True)
    .unionByName(df_martin2, allowMissingColumns=True)

)

df_final.write \
    .format("mongodb") \
    .mode("append") \
    .option("spark.mongodb.write.connection.uri", "mongodb+srv://neiel_cortes:neiel0330@cluster0.eo0kyfv.mongodb.net/AutoTec_db?retryWrites=true&w=majority") \
    .option("spark.mongodb.write.database", "proyecto_bigdata") \
    .option("spark.mongodb.write.collection", "lista_autos") \
    .save()

print("¡Proceso completado!")