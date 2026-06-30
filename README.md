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

## Instalação

Para instalar uma skill globalmente, copie a pasta da versão desejada para o
diretório de skills do agente, por exemplo:

```bash
cp -r backend_mentor/v1 ~/.claude/skills/backend-mentor
cp -r backend_mentor/v1 ~/.opencode/skills/backend-mentor
cp -r backend_mentor/v1 ~/.codex/skills/backend-mentor
```
