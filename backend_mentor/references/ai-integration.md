# Integração de IA em backend

## LangChain/LangGraph vs API direta do LLM

Não recomende um framework por padrão — pergunte-se (ou pergunte ao usuário) se ele resolve um
problema real:
- **API direta do provedor** (ex.: SDK da Anthropic/OpenAI, chamada HTTP simples) é a escolha
  certa quando o fluxo é relativamente simples: um prompt, talvez algumas tools, sem muitos
  passos condicionais. Mais fácil de debugar, menos camadas de abstração, menos dependência de
  versão de framework.
- **LangChain** ajuda quando há muita integração padronizada a montar rápido (loaders de
  documento, integrações com vector DBs variados, chains comuns) e o usuário aceita a
  abstração em troca de velocidade.
- **LangGraph** vale a pena quando o fluxo é genuinamente um grafo de estados — múltiplos
  passos com ramificação, loops (ex.: agente que tenta, avalia, tenta de novo), ou múltiplos
  agentes coordenados. Para um fluxo linear simples (prompt → resposta, ou prompt → 1 tool →
  resposta), LangGraph é complexidade desnecessária.
- Para o usuário ainda calibrando seu nível nesse domínio: comece recomendando a API direta
  para ele entender o que está de fato acontecendo (mensagens, tokens, tool calls) antes de
  introduzir um framework que esconde esses detalhes.

## RAG e bancos vetoriais

- RAG só resolve o problema de "o modelo não sabe sobre X" quando X é conhecimento privado,
  específico ou que muda com frequência. Se o conhecimento é geral e estável, considere se
  realmente precisa de RAG ou se um prompt bem escrito (ou fine-tuning, raramente) resolveria
  melhor.
- Chunking é a parte que mais afeta qualidade na prática: comece com chunks por
  seção/parágrafo lógico (não por tamanho fixo arbitrário) e com overlap pequeno entre chunks
  para não cortar contexto importante no meio.
- Escolha de vector DB: para projeto pessoal, pgvector (extensão do Postgres que ele já deve
  estar usando) costuma ser a escolha mais simples — evita operar um banco extra. Bancos
  vetoriais dedicados (Qdrant, Pinecone, Weaviate) valem a pena quando o volume de vetores ou
  a necessidade de filtros/performance de busca crescem além do que pgvector aguenta bem.
- Sempre pense em uma estratégia de avaliação (mesmo que informal: um conjunto de
  perguntas/respostas esperadas) para saber se mudanças no pipeline de RAG melhoraram ou
  pioraram a qualidade — sem isso, iteração vira tentativa e erro às cegas.

## Agentes, tool-use e MCP

- Defina o escopo de cada tool de forma mínima e específica (ver também `security.md`) — isso
  também melhora a qualidade do agente, porque tools muito genéricas confundem o modelo sobre
  quando usá-las.
- MCP (Model Context Protocol) faz sentido quando o usuário quer expor ferramentas/dados de
  forma reutilizável entre múltiplos agentes/clientes, ou consumir servidores MCP já prontos
  (ex.: GitHub, bancos de dados). Para uma tool única usada só dentro do próprio backend, uma
  function/tool definida diretamente no código do agente é mais simples do que montar um
  servidor MCP.
- Para agentes com múltiplos passos, pense desde o início em: limite de iterações (evitar
  loop infinito de custo), logging de cada passo (essencial para debugar por que o agente fez
  o que fez) e um caminho de fallback quando o agente não conseguir resolver — não deixe o
  usuário final preso numa conversa que nunca conclui.

## Custo e latência

LLMs introduzem uma variável que APIs tradicionais não têm: custo por chamada e latência
não-trivial (especialmente com múltiplos passos de agente ou RAG com re-ranking). Ao desenhar
o backend, pense em: cache de respostas quando a pergunta se repete, streaming para melhorar
percepção de latência, e um limite de gasto/observabilidade de custo desde o início (ver
`observability.md`) — é fácil um agente em loop gerar uma conta inesperada.
