# Arquitetura de trabalho Runner v2

O Runner é um consumidor de backlog, não uma fila autônoma divergente. O estado efetivo da task deriva de overrides do Orquestrador e receipt publicado. Preparação paralela usa workers isolados; integração/commit/push permanecem seriais. Queue vazia local não autoriza parada.
