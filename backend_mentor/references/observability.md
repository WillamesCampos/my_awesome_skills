# Observabilidade e monitoria

Mantenha-se agnóstico de ferramenta por padrão: ensine o conceito e sugira ferramentas
conforme o contexto do projeto (self-hosted, AWS, GCP), em vez de empurrar sempre a mesma
stack — ver `cloud-devops.md` para a decisão de provedor.

## Os três pilares (e por onde começar)

Para um projeto pessoal, a ordem de prioridade costuma ser:
1. **Logs estruturados** — o mais barato de implementar e o que resolve a maior parte do
   debugging do dia a dia. Logue em JSON (não texto livre), com campos consistentes
   (timestamp, nível, request_id, contexto relevante). Um `request_id`/`trace_id` propagado
   por toda a requisição é o que transforma "logs soltos" em "consigo seguir essa requisição
   do início ao fim".
2. **Métricas** — entram quando o usuário precisa responder "está lento? está dando erro
   mais que o normal?" sem ler log por log. Comece com o básico: taxa de erro, latência
   (p50/p95/p99), e throughput por endpoint. Não precisa instrumentar tudo — comece pelos
   endpoints/jobs mais críticos.
3. **Tracing distribuído** — só vale a pena quando há múltiplos serviços/chamadas externas
   compondo uma requisição (ex.: API → fila → worker → chamada de LLM → banco) e fica difícil
   saber onde o tempo/erro está sendo gasto só com logs. Para um monolito simples, tracing é
   frequentemente prematuro.

## Ferramentas por contexto

- **Self-hosted/VPS**: stack open-source costuma ser a escolha natural — Prometheus +
  Grafana para métricas, Loki para logs, e OpenTelemetry como padrão de instrumentação que
  não amarra o código a um vendor específico.
- **AWS**: CloudWatch (logs + métricas) é o caminho de menor atrito por já vir integrado;
  considere uma ferramenta gerenciada de erros (ex.: Sentry) à parte, porque o agrupamento e
  triagem de exceptions do CloudWatch é fraco comparado a ferramentas dedicadas.
- **GCP**: Cloud Logging + Cloud Monitoring, mesmo raciocínio do CloudWatch.
- Em qualquer caso, instrumentar com **OpenTelemetry** desde o início é uma boa prática
  agnóstica — permite trocar o backend de observabilidade (self-hosted ↔ gerenciado) sem
  reescrever a instrumentação do código.
- Sentry (ou equivalente) para rastreamento de exceções vale a pena cedo em qualquer stack —
  é barato de configurar e dá visibilidade imediata de erros em produção que passariam
  despercebidos em log puro.

## Alertas

- Alerte só no que exige ação humana imediata (taxa de erro disparou, serviço fora do ar,
  fila travada) — alertar demais (ex.: todo erro 4xx) treina o usuário a ignorar alertas, o
  que é pior do que não ter alerta nenhum.
- Para projeto pessoal mantido por uma pessoa só, prefira poucos alertas de alta confiança
  (ex.: via Slack/Telegram/email) a um painel sofisticado de on-call que ninguém vai olhar.

## Observabilidade específica de IA

Para backends com LLM/agentes, registre também: tokens consumidos e custo estimado por
chamada, qual modelo/versão foi usado, e o resultado de cada tool call em fluxos de agente.
Isso é o que permite responder "por que esse mês o gasto de IA subiu" ou "por que o agente
tomou essa decisão" depois do fato — sem isso, debugar comportamento de agente vira
adivinhação.
