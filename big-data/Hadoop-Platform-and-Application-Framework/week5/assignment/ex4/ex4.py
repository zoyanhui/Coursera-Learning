# read from hdfs
show_views_file = sc.textFile("input/join2_gennum?.txt")
show_views_file.take(2)

def split_show_views(line):
    [show, views] = line.strip().split(",")
    return (show, views)

show_views = show_views_file.map(slit_show_views)


show_channel_file = sc.textFile("input/join2_genchan?.txt")

def split_show_channel(line):
    [show,channel] = line.strip().split(",")
    return (show, channel)

show_channel = show_channel_file.map(split_show_channel)

joined_dataset = show_channel.join(show_views)

def extract_channel_views(show_views_channel): 
    channel, views = show_views_channel[1][0], show_views_channel[1][1] 
    return (channel, views)

channel_views = joined_dataset.map(extract_channel_views)

def some_function(a, b):
    some_result = int(a) + int(b)
    return some_result

channel_views.reduceByKey(some_function).collect()