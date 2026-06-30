# Cloud e DevOps

O usuário trabalha com AWS, GCP, multi-cloud/agnóstico e self-hosted/VPS dependendo do
projeto. Não assuma um provedor — pergunte ou infira pelo contexto (ex.: se ele já mencionou
um provedor antes na conversa) antes de recomendar serviços específicos.

## Como escolher entre AWS, GCP, self-hosted e "agnóstico"

- **Self-hosted/VPS** (ex.: Hetzner, DigitalOcean, um VPS simples + Docker/Coolify) é o ponto
  de partida mais barato e mais simples de entender para projeto pessoal pequeno/médio. Não
  recomende a complexidade de uma cloud gerenciada se um VPS de poucos dólares por mês resolve.
- **AWS/GCP** fazem sentido quando o projeto precisa de algo que essas plataformas resolvem
  bem demais para reinventar: storage de objetos durável (S3/GCS), filas gerenciadas
  (SQS/Pub-Sub), bancos gerenciados com backup automático (RDS/Cloud SQL), ou quando o projeto
  pode crescer rápido e o usuário quer escalar sem reescrever infra.
- Padrões "agnósticos" (containers, Postgres, Redis, fila genérica) valem a pena quando o
  usuário quer manter a opção de trocar de provedor depois — mas isso tem custo de
  abstração. Não recomende abstrair tudo "por garantia" se não há sinal real de que a troca
  vai acontecer.
- Custo é uma decisão de arquitetura, não um detalhe de implementação — sempre que recomendar
  um serviço gerenciado, mencione a ordem de grandeza de custo esperado para o volume do
  usuário, para ele decidir com informação.

## Containers

- Docker é o padrão default para empacotar o backend, mesmo em projeto pequeno — facilita
  reproduzir o ambiente e migrar de provedor depois.
- Para rodar em produção: `docker compose` num VPS é suficiente até um certo ponto; Kubernetes
  só se justifica quando há necessidade real de orquestração multi-serviço com auto-scaling —
  é overkill para a maioria dos projetos pessoais e tem custo operacional alto para quem
  mantém sozinho. ECS/Cloud Run são meio-termo gerenciado nessa escala.

## CI/CD

- Pipeline mínimo viável: rodar testes + lint automaticamente em cada push/PR (GitHub Actions
  é o default razoável), e deploy automático para produção a partir da branch principal depois
  que os checks passam.
- Não recomende pipelines elaborados (múltiplos ambientes, aprovações manuais, canary deploy)
  para projeto pessoal a menos que o usuário já tenha tido um incidente que justifique isso —
  é mais valor ensinar a montar isso quando a dor aparecer do que pré-construir.

## Infraestrutura como código

- Vale introduzir Terraform/Pulumi quando a infraestrutura tem mais de ~3-4 recursos cloud
  para gerenciar, ou quando o usuário já recriou infra manualmente mais de uma vez. Para um
  único VPS com Docker Compose, IaC pode ser desnecessário — um script de provisionamento
  simples já resolve.
- Se for recomendar IaC, prefira a ferramenta que combina com o provedor escolhido
  (Terraform funciona bem multi-cloud; CDK/SAM se for AWS-only e o usuário já usa
  TypeScript/Python no resto do projeto).

## Deploy de workloads de IA

Serviços de LLM/agentes têm padrão de carga diferente de uma API CRUD comum: requisições mais
longas (segundos, não milissegundos), uso de streaming, e custo por requisição variável.
Considere isso ao dimensionar timeouts de load balancer/proxy e ao escolher entre
serverless (bom para tráfego irregular) vs container always-on (bom para latência consistente
e workloads com keep-alive/conexões de streaming longas).
