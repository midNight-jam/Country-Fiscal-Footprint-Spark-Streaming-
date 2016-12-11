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

allWords = lines.flatMap(lambda line: line.split(","))

words = allWords.map(lambda word:(word,1))
print("word count below")
print(words.count())

wordCount = words.reduceByKey(lambda a,b:a+b)

wordCount.saveAsTextFiles("/home/jayam/PycharmProjects/FirstSpark/output/sparkOutput.txt")

ssc.start()         #start the computation
ssc.awaitTermination()      #wait for computation to terminate
