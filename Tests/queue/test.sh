docker-compose up -d
docker-compose exec broker kafka-topics \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic topic_input
docker-compose exec broker kafka-topics \
  --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic topic_output
docker-compose run -d queue python src/consumer.py
docker-compose run queue python \
  -m pytest tests/integration/ \
  -vv \
  --cov=src \
  --cov-report=term-missing
docker-compose stop


# docker-compose up -d
# docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic topic_input
# docker-compose exec broker kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic topic_output
# docker-compose run -d queue python src/consumer.py
# docker-compose run queue python -m pytest tests/integration/ -vv --cov=src --cov-report=term-missing
# docker-compose stop