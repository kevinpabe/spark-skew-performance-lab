# Protocolo de benchmark
Nenhum resultado de performance produtiva foi publicado como medido.

Executar cada estratégia em processo novo, mesma entrada/seed, mesma configuração e mesma máquina. Fazer aquecimento separado e pelo menos três medições, alternando a ordem. Documentar cache, runtime e recursos. A demo mede join + agregação local e imprime o plano executado; não mede ingestão S3, qualidade completa e escrita SPEC.

A fixture default é pequena. Não se espera que salting/AQE ganhem do baseline em qualquer tamanho; overhead pode dominar. O relatório de equivalência usa exceptAll nos dois sentidos em amostra pequena, preservando duplicidades.

| Campo a preencher | Fonte |
|---|---|
| Commit e configuração | Git e argumentos |
| Linhas/bytes por entrada | Manifesto e métricas |
| Contagens pós-join | Métricas dos estágios |
| Duração e variação entre execuções | Saída da demo ou job |
| Shuffle read/write e spill | Spark UI/event logs |
| Tasks p50/p95/max | Spark UI/event logs |
| Estratégia final efetivamente usada | Plano físico final |
| Saída correta | Reconciliação e testes |

Roadmap: leitura/gravação Parquet, dataset maior, event logs persistidos, métricas de shuffle e execução em Glue isolado. Testes de CI demonstram correção funcional em pequena escala; não validam SLA.
