hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -input /user/cloudera/input -output /user/cloudera/output_new -file /home/cloudera/hadoop-assignment-1/wordcount_mapper.py -mapper 'python wordcount_mapper.py' -file /home/cloudera/hadoop-assignment-1/wordcount_reducer.py -reducer 'python wordcount_reducer.py'

