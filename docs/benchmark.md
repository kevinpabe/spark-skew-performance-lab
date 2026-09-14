# Protocolo de benchmark
Nenhum resultado de performance produtiva foi publicado como medido.

Executar cada estratégia em processo novo, mesma entrada/seed, mesma configuração e mesma máquina. Fazer aquecimento separado e pelo menos três medições, alternando a ordem. Documentar cache, runtime e recursos. A demo mede join + agregação local e imprime o plano executado; não mede ingestão S3, qualidade completa e escrita SPEC.

A fixture default é pequena. Não se espera que salting/AQE ganhem do baseline em qualquer tamanho; overhead pode dominar. A equivalência compara o multiconjunto completo com assertCountEqual em uma fixture de 400 linhas, preservando valores e duplicidades. collect é restrito ao teste pequeno; não deve ser aplicado à origem produtiva.

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

## Compatibilidade observada no primeiro CI
O PySpark 3.3.0 não expôs functions.pmod no wrapper Python; o laboratório usa a expressão SQL pmod com número inteiro validado. A primeira combinação exceptAll(...).count() também falhou internamente durante o teste. A comparação de multiconjunto foi mantida, usando assertCountEqual sobre a fixture pequena, sem depender desse plano de execução.
[Execução que identificou as incompatibilidades](https://github.com/kevinpabe/spark-skew-performance-lab/actions/runs/34881658589).
