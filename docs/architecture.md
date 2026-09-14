# Arquitetura e limites
A arquitetura profissional usa SOR (origens de referência) e SPEC (produto especializado), com sete tabelas e persistência diária. Esses nomes são convenções do contexto, não padrões universais.

O laboratório implementa apenas o join crítico entre findings e assets. examples/reference-model.json ilustra sete tabelas e suas granularidades; não afirma reproduzir o schema corporativo.

## Ordem de diagnóstico
1. Confirmar a granularidade desejada do produto.
2. Medir unicidade das chaves de ambos os lados, incluindo datas de vigência.
3. Corrigir joins indevidos e regras que geram multiplicação não desejada.
4. Examinar distribuição de bytes, tempo por task, shuffle e spill.
5. Escolher estratégia de join, paralelismo e particionamento de saída.
6. Validar equivalência e medir novamente.

## Heartbeat, AQE e broadcast
Heartbeat é enviado pelo executor ao driver. O intervalo 60s foi relatado; 600s de timeout no arquivo de exemplo é uma proposta ilustrativa e deve ser muito maior que o intervalo. Aumentar timeout pode tolerar pausas temporárias, mas também retarda detecção de falhas e não resolve OOM/GC.

O fator 3 compara a partição à mediana e opera junto ao limiar absoluto de bytes. O tratamento de skew de AQE atua em operações suportadas no plano; não corrige toda agregação ou lógica de negócio. Em amostras pequenas, o limite padrão pode nunca ser atingido.

Broadcast disponibiliza a relação pequena nos executors para as tasks. Memória desserializada pode exceder tamanho em disco. O laboratório usa uma dimensão minúscula explicitamente; não recomenda elevar um limiar global sem medição.
Fontes: [Spark tuning](https://spark.apache.org/docs/3.5.6/sql-performance-tuning.html), [configuração](https://spark.apache.org/docs/3.5.6/configuration.html).

## Runtime
Glue 4.0 usa Spark 3.3.0 e Python 3.10 com alterações AWS. A CI usa PySpark 3.3.0/Java 11 local por compatibilidade do laboratório e não constitui homologação do runtime gerenciado. [AWS](https://docs.aws.amazon.com/glue/latest/dg/release-notes.html).
