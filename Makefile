.PHONY: start_consumer
start_consumer:
	docker exec -it flink-jobmanager ./bin/flink run -py /opt/flink/usrlib/consumer.py
