# Check data
Examples in this section rely on the table stored in Hive during the previous module on Hive.

Check that the data are available

Start PySpark, check if this is working by running a simple query on the customer table:
```
sqlCtx.sql("SELECT customer_fname, customer_lname FROM customers").limit(2).collect()
```
The result should be:
```
[Row(customer_fname=u'Richard', customer_lname=u'Hernandez'),
 Row(customer_fname=u'Mary', customer_lname=u'Barrett')]
```
Insert data from the Cloudera Quickstart

ONLY if the previous step fails, you need to follow again the instructions on the Cloudera Quickstart to import data into Hive.

open browser inside the Cloudera VM
Click on the Getting started icon on the bookmarks bar, last item on the right
Click on "Start Tutorial"
Execute the commands in Tutorial 1 and Tutorial 2
Finally verify that the tables have been created in Hue

# Quizs
## Q1
```
sqlCtx.sql("SELECT count(*) from orders where order_status='SUSPECTED_FRAUD'").limit(2).collect()
```

## Q2
```
import pyspark.sql.functions as F
sqlCtx.sql("SELECT order_item_order_id, sum(order_item_subtotal) as total from order_items group by order_item_order_id").orderBy(F.desc("total")).limit(5).collect()
```

## Q3
*table orders*
[Row(order_id=1, order_date=1374735600000, order_customer_id=11599, order_status=u'CLOSED'),
Row(order_id=2, order_date=1374735600000, order_customer_id=256, order_status=u'PENDING_PAYMENT')]
*table order_items*
[Row(order_item_id=1, order_item_order_id=1, order_item_product_id=957, order_item_quantity=1, order_item_subtotal=299.98001098632812, order_item_product_price=299.98001098632812),
Row(order_item_id=2, order_item_order_id=2, order_item_product_id=1073, order_item_quantity=1, order_item_subtotal=199.99000549316406, order_item_product_price=199.99000549316406)]

```
order_items = sqlCtx.sql("SELECT * from order_items")
temp_order_items = sqlCtx.createDataFrame(order_items.rdd, order_items.schema)
temp_order_items.registerTempTable("temp_order_items")
orders = sqlCtx.sql("SELECT * from orders")
temp_orders = sqlCtx.createDataFrame(orders.rdd, orders.schema)
temp_orders.registerTempTable("temp_orders")

temp_join=sqlCtx.sql("SELECT O.order_id, O.order_status, O.order_customer_id, I.order_item_id, I.order_item_product_id, I.order_item_quantity, I.order_item_subtotal, I.order_item_product_price FROM temp_orders as O inner join temp_order_items as I on O.order_id=I.order_item_order_id").cache()
temp_join.groupBy("order_status").avg("order_item_product_price").filter("order_status='COMPLETE'").show()
```

## Q4
# temp_join=sqlCtx.sql("SELECT O.order_id, O.order_customer_id, O.order_status, I.order_item_subtotal FROM temp_orders as O inner join temp_order_items as I on O.order_id=I.order_item_order_id WHERE order_status='COMPLETE'")
temp_join.filter("order_status='COMPLETE'").groupBy("order_customer_id").agg(temp_join.order_customer_id,F.sum(temp_join.order_item_subtotal).alias("total")).orderBy(F.desc("total")).show(3)

## Q5
temp_join.filter("order_status!='COMPLETE'").groupBy("order_status").agg(temp_join.order_status,F.sum(temp_join.order_item_subtotal).alias("total")).orderBy(F.desc("total")).show(3)



