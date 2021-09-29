# cpu-ram-alert

1. docker-compose up
2. cd client
3. docker build -t alert-client .
4. docker run --net cpu-ram-alarm_default alert-client
