# ADR 001 — corrigir cardinalidade antes de distribuir melhor
Status: adotada no laboratório.

Exigir a granularidade declarada da dimensão antes do inner join. Uma dimensão com mais de uma linha por chave é rejeitada quando o contrato esperado é many-to-one.

Não aplicar dropDuplicates arbitrariamente: pode eliminar registros válidos ou selecionar versões incorretas. Dimensões temporais precisam de predicados de vigência e critérios determinísticos acordados com o negócio.

Salting seletivo distribui a chave quente usando finding_id. A dimensão correspondente é expandida pelos mesmos buckets. O exemplo usa inner join; adaptar para outer joins exige validar nulos, unmatched e multiplicidades.

Trade-off: salting replica parte da dimensão e adiciona manutenção. AQE é preferível quando resolve o plano observado, mas salting continua útil quando a estratégia automática não cobre o gargalo. Broadcast é adequado somente se a dimensão cabe com margem na memória dos executors.
