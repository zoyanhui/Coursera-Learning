hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar -input /user/cloudera/input_join2 -output /user/cloudera/output_join2 -file  /home/cloudera/hadoop-assignment-2/join2_mapper.py -mapper 'python join2_mapper.py' -file /home/cloudera/hadoop-assignment-2/join2_reducer.py -reducer 'python join2_reducer.py' -numReduceTasks=1