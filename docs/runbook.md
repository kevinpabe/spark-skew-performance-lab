# Entrega e handover
- Registrar granularidade, chaves, semântica das sete origens e mapeamento SOR → SPEC.
- Confirmar contagens e regras de cálculo com o consumidor final.
- Guardar configuração de Glue, plano, run_id e métricas sem dados sensíveis.
- Se cardinalidade explodir, suspender promoção e revisar predicados; não ampliar cluster como primeira reação.
- Se houver skew, distinguir bytes desbalanceados de tasks lentas por I/O, GC ou spill.
- Publicar somente após reconciliação e manter versão anterior consumível para recuperação.
- Documentar responsáveis por operação, regras e aceitação, além dos procedimentos de reprocessamento.
