# Plausibilidade de capacidade
Classificação: cálculo de cenário, não benchmark produtivo.

## Premissas
500.000.000 registros na maior origem; Glue 4.0; 30 workers G.2X; duração estimada de 2 a 3 horas. O autor ainda precisa confirmar workers e duração em registros de execução.

G.2X corresponde a 2 DPUs, 8 vCPUs e 32 GB de memória por worker. Para 30 workers: 60 DPUs, 240 vCPUs e 960 GB nominais. Recursos efetivos das tasks são inferiores ao total nominal devido a driver, overhead e configuração de executors.
Fonte: [AWS, propriedades do job](https://docs.aws.amazon.com/glue/latest/dg/add-job.html).

| Duração assumida | DPU-h com capacidade constante | Vazão equivalente de entrada |
|---|---:|---:|
| 2 horas | 120 | 69.444 registros/s |
| 3 horas | 180 | 46.296 registros/s |

Vazão equivalente é linhas de entrada divididas pelo tempo total; não é throughput medido de I/O ou shuffle. Auto Scaling e cobrança efetiva exigem métricas reais do job.

## Sensibilidade ao tamanho da linha
| Bytes lógicos por registro, hipotéticos | Volume da origem de 500 milhões |
|---|---:|
| 200 | 100 GB decimais |
| 1.000 | 500 GB decimais |
| 2.000 | 1 TB decimal |

Parquet comprimido, representação em memória e shuffle podem ter tamanhos muito diferentes. Esses valores não foram medidos no caso profissional. As outras seis tabelas e operações intermediárias adicionam custo.

## Um trilhão de linhas
Um inner equijoin produz, por chave, n_esquerda × n_direita linhas. Somar esses produtos estima cardinalidade. Por exemplo, 500 milhões de ocorrências de uma chave combinadas com 2.000 correspondências resultariam em um trilhão de linhas (exemplo aritmético, não diagnóstico do job real).

Corrigir predicados, granularidade e vigência pode reduzir a cardinalidade para o domínio esperado. Salting redistribui trabalho e não corrige multiplicação lógica. Uma queda de cardinalidade também não comprova sozinha que a regra de negócio ficou correta.

## Conclusão condicionada
2–3 horas é um cenário tecnicamente possível. Não há evidência suficiente para afirmar que seja esperado, eficiente ou reproduzível. Obter: volume lido/escrito em bytes, contagens por estágio, tipos/cardinalidades dos joins, plano físico, shuffle, spill, tempo p50/p95/max das tasks, workers efetivos e duração por execução.

Sem região e preço vigente, manter custo como DPU-h. Custo de Glue = DPU-h faturadas × preço regional aplicável, além de S3, catálogo e outros serviços.
