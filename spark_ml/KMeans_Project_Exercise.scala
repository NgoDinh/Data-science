import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.clustering.KMeans

val spark = SparkSession.builder().getOrCreate()
val data = spark.read.option("header", "true").option("inferSchema", "true").option("multiline", "true").format("csv").load("Wholesale customers data.csv")
val feature_data = data.select($"Fresh",$"Milk" ,$"Grocery", $"Frozen", $"Detergents_Paper", $"Delicassen")

import org.apache.spark.ml.feature.VectorAssembler

val assembler = new VectorAssembler().setInputCols(Array("Fresh","Milk" ,"Grocery", "Frozen", "Detergents_Paper", "Delicassen")).setOutputCol("features")
val df = assembler.transform(data)
val kmeans = new KMeans().setK(3).setSeed(1L)
val model = kmeans.fit(df)
val WSSSE = model.computeCost(df)

println(s"Within Set Sum of Squared Errors = $WSSSE")
println("Cluster Centers: ")
model.clusterCenters.foreach(println)
