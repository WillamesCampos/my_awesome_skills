# Política editorial e evidências

## Classes de afirmação

```yaml
claim_classes:
  - professional_experience_reported
  - knowledge_demonstrated
  - learning_in_progress
  - simulated_example
  - unverified_information
  - confidential_or_prohibited
```

- `professional_experience_reported`: pode contextualizar a publicação, mas não autoriza
  revelar empresa, cliente, sistema ou incidente.
- `knowledge_demonstrated`: pode sustentar uma explicação direta dentro do escopo demonstrado.
- `learning_in_progress`: use postura exploratória, como “ao estudar” ou “ainda quero testar”.
- `simulated_example`: identifique explicitamente como cenário simulado ou ilustrativo.
- `unverified_information`: verifique em fonte primária, remova ou apresente como pergunta.
- `confidential_or_prohibited`: bloqueie; só prossiga com versão anonimizada aprovada.

## Regras inegociáveis

Nunca invente benchmark, métrica, incidente, volume, resultado, ferramenta usada ou experiência.
Não converta uma resposta correta isolada em alegação de domínio completo. Não exponha nomes,
endpoints internos, código privado, segredos, clientes ou detalhes identificáveis de produção.

Separe no registro de rastreabilidade:

```yaml
claims:
  - statement: ""
    class: "knowledge_demonstrated"
    source: ""
    verified: false
    publication_wording: ""
pending_verification: []
removed_confidential_details: []
```

Se a afirmação depender de informação externa atual, use documentação oficial ou fonte
primária e guarde o link em `fontes/referencias.md`.

## Decisão editorial

- Evidência suficiente: proponha um ângulo e aguarde aprovação.
- Evidência parcial: proponha diário de aprendizagem ou post exploratório.
- Evidência ausente: pare e peça o material necessário.
- Risco de confidencialidade: mostre apenas a versão anonimizada antes de continuar.

