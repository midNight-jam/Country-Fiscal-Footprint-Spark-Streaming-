from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# StreamingContext is the main entry point
#  to all streaming functionality

# Create a local StreamingContext
# with two working thread and batch interval of 1 second
sc = SparkContext("local[2]","NetWordCount")
ssc = StreamingContext(sc,1)

topic  = "connect-test"
kvs = KafkaUtils.createStream(ssc,"localhost:2181","spark-streaming-consumer",{topic:1})
lines = kvs.map(lambda x:x[1])

allWords = lines.flatMap(lambda line: line.split(" "))

words = allWords.map(lambda word:(word,1))

wordCount = words.reduceByKey(lambda a,b:a+b)

wordCount.pprint()


# # Create a DStream that will connect to hostname:port,
# # like localhost:9999
# lines = ssc.socketTextStream("localhost",9999)
#
# # Split each line into words, commas because reading csv line
# words  = lines.flatMap(lambda line:line.split(","))
#
# pairs = words.map(lambda word:(word,1))
# wordCounts = pairs.reduceByKey(lambda x,y:x+y)
# print("Priting the word coubt from input nt ")
# wordCounts.pprint()
# print("Processing ends")

ssc.start()         #start the computation
ssc.awaitTermination()      #wait for computation to terminate
