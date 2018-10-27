import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.regression.LinearRegression
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}
import org.apache.spark.sql.SparkSession
val spark = SparkSession.builder().getOrCreate()

val data = spark.read.option("header","true").option("inferSchema","true").option("multiline",true).format("csv").load("EcommerceCustomers.csv")

data.printSchema()

import org.apache.spark.ml.feature.VectorAssembler

val df = data.select(data("Yearly Amount Spent").as("label"), $"Avg Session Length", $"Time on App", $"Time on Website", $"Length of Membership", $"Yearly Amount Spent")
val assembler = new VectorAssembler().setInputCols(Array( "Avg Session Length","Time on App","Time on Website","Length of Membership","Yearly Amount Spent")).setOutputCol("features")
val output = assembler.transform(df).select($"label", $"features")
val lr = new LinearRegression()
val lrModel = lr.fit(output)

println(s"Coefficients: ${lrModel.coefficients} Intercept: ${lrModel.intercept}")
trainingSummary.residuals.show()

println(s"RMSE: ${trainingSummary.rootMeanSquaredError}")
println(s"MSE: ${trainingSummary.meanSquaredError}")
println(s"r2: ${trainingSummary.r2}")
