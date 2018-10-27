import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.log4j._

Logger.getLogger("org").setLevel(Level.ERROR)
val spark = SparkSession.builder().getOrCreate()
val data = spark.read.option("header", "true").option("inferSchema", "true").option("multiline",true).format("csv").load("advertising.csv")
data.printSchema()
val df = data.select(data("Clicked on Ad").as("label"),$"Daily Time Spent on Site",$"Age",$"Area Income",$"Daily Internet Usage",$"Timestamp",$"Male")
val df1 = df.withColumn("Hour", hour(df("Timestamp")))

import org.apache.spark.ml.feature.{VectorAssembler,StringIndexer,VectorIndexer,OneHotEncoder}
import org.apache.spark.ml.linalg.Vectors

val assembler = new VectorAssembler().setInputCols(Array("Daily Time Spent on Site", "Age", "Area Income","Daily Internet Usage","Hour")).setOutputCol("features")
val Array(training, test) = df1.randomSplit(Array(0.7, 0.3), seed = 12345)

import org.apache.spark.ml.Pipeline
val lr = new LogisticRegression()
val pipeline = new Pipeline().setStages(Array(assembler, lr))
val model = pipeline.fit(training)
val results = model.transform(test)

import org.apache.spark.mllib.evaluation.MulticlassMetrics

val predictionAndLabels = results.select($"prediction",$"label").as[(Double, Double)].rdd
val metrics = new MulticlassMetrics(predictionAndLabels)
println(metrics.confusionMatrix)
