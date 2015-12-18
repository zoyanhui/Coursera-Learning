 # Start pyspark
```
 java.lang.NoClassDefFoundError: org/apache/spark/sql/types/AtomicType

 PYSPARK_DRIVER_PYTHON=ipython pyspark --packages com.databricks:spark-csv_2.10:1.2.0
```


# create schema
```
from pyspark.sql.types import *

schema = StructType([
StructField("business_id", StringType(), True),
StructField("cool", IntegerType(), True),
StructField("date", StringType(), True),
StructField("funny", IntegerType(), True),
StructField("id", StringType(), True),
StructField("stars", IntegerType(), True),
StructField("text", StringType(), True),
StructField("type", StringType(), True),
StructField("useful", IntegerType(), True),
StructField("user_id", StringType(), True),
StructField("name", StringType(), True),
StructField("full_address", StringType(), True),
StructField("latitude", DoubleType(), True),
StructField("longitude", DoubleType(), True),
StructField("neighborhoods", StringType(), True),
StructField("open", StringType(), True),
StructField("review_count", IntegerType(), True),
StructField("state", StringType(), True),
])
```

# load csv data
```
yelp_df = sqlCtx.load(source='com.databricks.spark.csv',
header = 'true',
schema = schema,
path = 'file:///usr/lib/hue/apps/search/examples/collections/solr_configs_yelp_demo/index_data.csv')
```

# Q1
```
yelp_df.agg({"cool":"mean"}).collect()
```

# Q2
```
yelp_df.filter("review_count>=10").groupBy("stars").avg("cool").filter("stars=4").show()
```
# Q3
```
yelp_df.filter("review_count>=10").filter("open='True'").groupBy("stars").avg("cool").filter("stars=5").show()
```


# Q4
```
import pyspark.sql.functions as F

yelp_df.filter("review_count>=10").filter("open='True'").groupBy("state").agg(yelp_df.state,F.sum(yelp_df.review_count).alias("reviewcount")).orderBy(F.desc("reviewcount")).show(5)
```

# Q5
```
yelp_df.groupBy("business_id").count().orderBy(F.desc("count")).show(1)
```