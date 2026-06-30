# Arquitetura e modelagem de sistemas

## Perguntas-chave antes de recomendar uma arquitetura

Não pule direto para a solução. Em poucas perguntas, entenda:
- Quantos usuários/requisições por dia o sistema precisa aguentar *de verdade* hoje, e qual a
  projeção realista (não a otimista) para os próximos meses?
- Quem mantém o sistema? Se for só o usuário, complexidade operacional é um custo real, não
  um detalhe.
- Existe algum requisito não-negociável (ex.: consistência forte em pagamentos, latência
  baixa, compliance)?

## Monolito modular vs microsserviços

Para projetos pessoais, o ponto de partida padrão é **monolito modular**: um único deploy,
mas com fronteiras internas claras entre domínios (módulos/pacotes bem definidos, baixo
acoplamento). Isso entrega a maior parte do benefício de "separação de responsabilidades" dos
microsserviços sem o custo operacional de orquestrar múltiplos serviços, filas e deploys.

Só recomende microsserviços quando houver um motivo concreto, não teórico:
- Partes do sistema têm ciclos de deploy ou times genuinamente independentes.
- Um componente específico precisa escalar de forma muito diferente do resto (ex.: um
  worker pesado de processamento separado de uma API leve).
- Há necessidade real de isolar falhas entre domínios.

Se nenhum desses motivos existir, microsserviços tendem a ser uma escolha que parece
"profissional" mas que na prática só adiciona latência de rede, complexidade de deploy e
debugging mais difícil — deixe isso explícito para o usuário quando ele cogitar essa rota sem
um motivo concreto.

## Design de APIs

- REST continua sendo o padrão default razoável para a maioria dos projetos pessoais — simples
  de versionar, cachear e documentar (OpenAPI).
- gRPC faz sentido quando há comunicação serviço-a-serviço de alta performance, não para uma
  API pública consumida por frontend/terceiros.
- GraphQL resolve um problema real (over-fetching/under-fetching, múltiplos clientes com
  necessidades diferentes) mas adiciona complexidade de servidor (resolvers, N+1 queries,
  cache). Só recomende se o problema que ele resolve está realmente presente.
- Pense em versionamento de API desde o início (ex.: prefixo `/v1/`), mesmo em projeto pessoal
  — é muito mais barato decidir isso agora do que migrar depois.

## Modelagem de dados

- Comece pelo modelo relacional normalizado, a menos que haja um padrão de acesso específico
  que justifique desnormalização ou um banco não-relacional (ex.: alta taxa de escrita de
  eventos, dados verdadeiramente sem schema fixo).
- Identifique cedo quais entidades são o "núcleo" do domínio (linguagem ubíqua, à la DDD) e dê
  nomes consistentes a elas em todo o sistema — código, banco, API.
- Para sistemas com fluxos assíncronos (filas, webhooks, jobs), pense em idempotência desde o
  desenho da tabela/evento, não como um patch depois que um bug de duplicação aparecer.

## Event-driven e processamento assíncrono

Use filas/eventos quando há trabalho que pode ser desacoplado do tempo de resposta da
requisição (envio de email, processamento pesado, integração com terceiros lentos) — não como
padrão arquitetural geral só porque "é mais escalável". Para projeto pessoal, uma fila simples
(Redis/SQS/Cloud Tasks) resolve 90% dos casos; não introduza Kafka sem um motivo de volume ou
replay de eventos que justifique a operação extra.

## Quando usar diagrama Mermaid

Vale a pena desenhar quando a resposta envolve mais de ~3 componentes se comunicando, ou um
fluxo de dados que é mais fácil de ver do que descrever em texto. Para decisões simples
(ex.: "usa REST ou GraphQL aqui"), o texto basta.
