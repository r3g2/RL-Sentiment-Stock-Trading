# Stock Prediction Combining Numerical and Textual Analysis

## Introduction:

This is an AI portfolio manager which uses numerical and textual analysis to predict the best action to increase the value of portfolio in long run. Sentimental Model is creating an moving average of streaming textual data sources such as reddit and twitter. The moving average is then mapped with technical indicator of each stock and ingested into Reinforcement Learning model which give the output what to buy, what to sell and what to hold. The data pipeline of this application uses kafka for migrating the data from one end to other and application uses react for visualization 

## Steps to run the application:

1. Install conda and use environment file to configure the dependency

2.	Install adoptopenjdk-8-hotspot

3. Download Kafka and extract the content:
	```
	curl -O https://archive.apache.org/dist/kafka/1.0.0/kafka_2.11-1.0.0.tgz && tar -xvf kafka_2.11-1.0.0.tgz
	```
4. Run the zookeeper in background:
	```
	bin/zookeeper-server-start.sh config/zookeeper.properties &
	```
5.  Start three broker packages with different broker id and different listener ports

6. Start the topics with three partitions:
	```
	bin/kafka-topics.sh --create --topic text_data --zookeeper localhost:2181 --partitions 3 --replication-factor 2
	bin/kafka-topics.sh --create --topic predictions --zookeeper localhost:2181 --partitions 3 --replication-factor 2
	```
7. Start the text source streams:
	```
	python3 backend/stream_reddit.py text_data <listener-broker-1> <listener-broker-2> <listener-broker-3> -d <today-date> 
	python3 backend/twitter.py text_data <listener-broker-1> <listener-broker-2> <listener-broker-3> -d <today-date>
	```
	Example: ```python3 stream_reddit.py text_data localhost:9092 localhost:9093 localhost:9094 -d "2021-04-29"``` 

8.  Start the backend server:

	```python3 backend/server.py predictions <listener-broker-1> <listener-broker-2> <listener-broker-3> &```

9. Install node packages and start the react server
	
	```
	cd portofolio && npm install
	npm start
	```