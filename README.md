# my_awesome_skills

Coleção pessoal de skills para agentes de IA (Claude Code, OpenCode, Codex e
compatíveis), no formato [SKILL.md](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

## Estrutura

Cada skill vive na sua própria pasta, versionada internamente em subpastas
`v1/`, `v2/`, etc. — cada versão é uma cópia completa e independente da skill
(SKILL.md + recursos), preservando o histórico de versões publicadas:

```
<nome-da-skill>/
└── v1/
    ├── SKILL.md
    └── ... (referências, scripts, assets, se houver)
```

Ao revisar uma skill de forma relevante, crie uma nova pasta de versão
(`v2/`) em vez de sobrescrever a anterior.

## Skills

### `english_tutor`
Conduz sessões de estudo de inglês a partir de um PDF, com exercícios curtos
de fala (respondidos por áudio no chat), feedback estruturado e chunks
(colocações) para praticar.

- Versão atual: `v1`

### `backend_mentor`
Mentor sênior (staff-level) de arquitetura e engenharia backend — orienta
decisões de design de sistemas, escalabilidade, segurança, cloud/DevOps,
observabilidade e integração de IA (LLMs, RAG, agentes, MCP) em projetos
pessoais com Python, Node.js/TypeScript e Go. Estilo didático: lidera com o
raciocínio antes do veredito, nomeia o princípio geral por trás da decisão e
fecha sempre com uma pergunta.

- Versão atual: `v1`
- Domínios de referência: `architecture.md`, `security.md`,
  `cloud-devops.md`, `ai-integration.md`, `observability.md`

### `system_design_generator`
Gera Technical Architecture Documents (TAD) completos a partir de um PRD, com
design modular para startups. Usa uma arquitetura de subagentes em paralelo
(`prd-reader`, `tech-researcher` x5, `tad-writer`) cobrindo stack, infra,
segurança, riscos e alinhamento com o PRD.

- Versão atual: `v1`
- Origem: renomeada a partir da skill `tad-generator` do repositório
  [luongnv89/skills](https://github.com/luongnv89/skills) (MIT, autor Luong
  NGUYEN), instalada via `npx skills`.
- Subagentes: `agents/prd-reader.md`, `agents/tech-researcher.md`,
  `agents/tad-writer.md`
- Referências: `references/tech-stack.md`, `references/tad-template.md`

### `analisador_vagas_tech`
Analisa criticamente vagas de tecnologia para um Backend Engineer Python
sênior (Django, FastAPI, APIs, cloud, microserviços, event-driven, async) em
transição gradual para AI Backend Engineering, e emite um veredito
estratégico sobre aplicar ou não.

- Versão atual: `v1`

## Instalação

Para instalar uma skill globalmente, copie a pasta da versão desejada para o
diretório de skills do agente, por exemplo:

```bash
cp -r backend_mentor/v1 ~/.claude/skills/backend-mentor
cp -r backend_mentor/v1 ~/.opencode/skills/backend-mentor
cp -r backend_mentor/v1 ~/.codex/skills/backend-mentor
```

Ou, para skills instaladas via [`npx skills`](https://skills.sh) (formato
universal), copie para `~/.agents/skills/<nome-da-skill>` — o próprio agente
(Claude Code, Codex, OpenCode) descobre a partir dali:

```bash
cp -r system_design_generator/v1 ~/.agents/skills/system-design-generator
```
