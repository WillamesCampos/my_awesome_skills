# Segurança

Trate segurança como parte do design, não como revisão de última hora. As três frentes abaixo
merecem peso equilibrado — não assuma que uma é mais importante que as outras sem contexto.

## Auth/Authz

- Para a maioria dos projetos pessoais, sessões opacas (cookie + storage no servidor/Redis)
  são mais simples e mais fáceis de revogar do que JWT. Só recomende JWT quando há um motivo
  real (ex.: múltiplos serviços/domínios validando o token sem round-trip ao servidor de auth,
  ou cliente mobile/SPA com necessidade clara de stateless auth).
- Se usar JWT: tokens de vida curta + refresh token, e tenha uma estratégia de revogação
  (allowlist/blocklist) — JWT "stateless puro" sem revogação é uma armadilha comum.
- Não reinvente OAuth/login social — use bibliotecas maduras do ecossistema da linguagem
  (ex.: Authlib/django-allauth em Python, NextAuth/Passport em Node, goth em Go) em vez de
  implementar o fluxo OAuth na mão.
- Separe autenticação (quem é o usuário) de autorização (o que ele pode fazer). Modele
  permissões como dados (roles/policies), não como `if user.email == "admin@..."` espalhado
  pelo código.

## API security / OWASP

Checklist mínimo para qualquer API exposta, mesmo em projeto pessoal:
- Validação de input no boundary (schema validation: Pydantic, Zod, validator do Go) — nunca
  confie em dado vindo do cliente, mesmo que o frontend já valide.
- Rate limiting básico em endpoints públicos e, principalmente, em login/recuperação de senha
  (mitiga brute force e abuse).
- CORS configurado explicitamente para as origens esperadas, não `*` em produção.
- Mensagens de erro não devem vazar detalhes internos (stack trace, query SQL, versão de lib)
  para o cliente — logue o detalhe internamente, devolva algo genérico.
- Para qualquer endpoint que aceita IDs (`/users/123`), confirme que há checagem de
  autorização (o usuário logado pode acessar *esse* recurso específico), não só autenticação.
  Esse é o erro mais comum (IDOR) em APIs feitas rápido.

## Gestão de segredos e dados sensíveis

- Segredos (API keys, credenciais de banco, tokens de LLM) nunca em código ou commitados —
  variáveis de ambiente + `.env` fora do git, ou um secrets manager (AWS Secrets Manager, GCP
  Secret Manager, Doppler, Vault) quando o projeto crescer.
- Dados pessoais (PII) devem ser minimizados: só armazene o que o produto realmente precisa,
  e pense em criptografia em repouso para campos sensíveis (não é preciso criptografar tudo,
  mas senha, dados de pagamento e PII sensível sim).
- Logs nunca devem conter segredos, senhas ou tokens completos — mascare ou trunque.

## Segurança específica de aplicações com IA

Quando o backend integra LLMs/agentes (ver também `ai-integration.md`):
- **Prompt injection**: trate qualquer conteúdo vindo de fora (input do usuário, resultado de
  busca, conteúdo de documento via RAG) como não-confiável quando ele entra no contexto do
  modelo. Não dê ao modelo, por padrão, permissão para executar ações destrutivas/irreversíveis
  só porque um prompt "pediu".
- **Tool-use/agentes**: ferramentas que o agente pode chamar devem ter o menor escopo de
  permissão possível (ex.: uma tool de "buscar pedido" não deveria também conseguir
  deletar pedidos). Trate cada tool exposta como uma superfície de API que precisa de
  autorização própria.
- **Exfiltração de dados**: cuidado ao dar para um agente acesso simultâneo a (a) dados
  sensíveis e (b) uma forma de enviar dados para fora (ex.: chamar uma URL arbitrária, mandar
  email) — essa combinação é o vetor clássico de exfiltração via prompt injection.
- Saída do modelo que vai ser executada como código, query SQL ou comando de sistema precisa
  ser tratada como input não-confiável também, com validação/sandboxing antes de rodar.
