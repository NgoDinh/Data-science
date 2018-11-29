import org.apache.spark.sql.SparkSession
val spark:SparkSession = SparkSession.builder().getOrCreate()
val videoDF = spark.read.format("csv").
  option("header",true).
  option("multiline", "true").
  option("inferSchema", "true").
  load("CAvideos1000.csv").
  withColumn("views",'views.cast("BigInt").as("views")).
  withColumn("likes",'likes.cast("BigInt").as("likes")).
  withColumn("dislikes",'dislikes.cast("BigInt").as("dislikes")).
  withColumn("comment_count",'comment_count.cast("BigInt").as("comment_count")).
  select('video_id,'trending_date,'title,'channel_title, 'likes,'dislikes,'comment_count,'views)

//Q1
val video_group = videoDF.groupBy("channel_title").sum().rdd.collect

//Q2

import org.apache.spark.sql.expressions._
import org.apache.spark.sql.functions._

val dislikes_percentage = videoDF.select("channel_title","views","dislikes","comment_count").groupBy("channel_title").
  agg(sum("dislikes").alias("total_dislikes")).
  withColumn("per_dislikes", col("total_dislikes")/sum("total_dislikes").over())

val comment_percentage = videoDF.select("channel_title","views","dislikes","comment_count").groupBy("channel_title").
  agg(sum("comment_count").alias("total_comment")).
  withColumn("per_comment", col("total_comment")/sum("total_comment").over())

val views_percentage = videoDF.select("channel_title","views","dislikes","comment_count").groupBy("channel_title").
  agg(sum("views").alias("total_views")).
  withColumn("per_views", col("total_views")/sum("total_views").over())
// Vi sao em khong the viet: withColumn("per_views", 100*col("total_views")/sum("total_views").over())
// Lam cach nao em co the extract data trong dataFrame ra nhu mot variance dang Int
//Ngoai cach su dung library, co cach nao khong thay??

//Q3
dislikes_percentage.orderBy(desc("per_dislikes")).show(10)
comment_percentage.orderBy(desc("per_comment")).show(10)
views_percentage.orderBy(desc("per_views")).show(10)
