# fluentd/Dockerfile
FROM fluent/fluentd:v0.12-debian

RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-rdoc", "--no-ri", "--version", "1.9.2"]
RUN ["gem", "install", "fluent-plugin-docker_logs", "--no-rdoc", "--no-ri"]
