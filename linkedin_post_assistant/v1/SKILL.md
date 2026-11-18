---
name: linkedin-post-assistant
description: >
  Transforma aprendizado técnico verificável do usuário em um post conciso para LinkedIn,
  com rastreabilidade, hashtags, pergunta de interação e imagem ou animação Blueprint Signal.
  Use quando o usuário fornecer anotações, exercício, feedback, experimento ou experiência
  autorizada e pedir para criar, revisar ou ilustrar uma publicação técnica. Não use para
  ghostwriting genérico, conteúdo inventado, publicação automática ou afirmações acima das
  evidências fornecidas.
---

# LinkedIn Post Assistant

Crie publicações técnicas úteis sem transformar estudo em autoridade fictícia. Trabalhe em
português brasileiro e mantenha o usuário no controle de cada publicação.

## Antes de escrever

1. Leia o material fornecido e, quando disponível, o contexto técnico autorizado pelo usuário.
2. Leia [references/editorial-policy.md](references/editorial-policy.md) e classifique cada
   afirmação material.
3. Leia [references/author-context.md](references/author-context.md) para calibrar profundidade.
4. Se a entrada estiver incompleta, use [references/input-schema.md](references/input-schema.md)
   para pedir somente os campos que mudam o resultado.
5. Bloqueie conteúdo confidencial. Não invente fatos para completar a narrativa.

## Fluxo obrigatório

1. Proponha um único ângulo sustentado pelas evidências e indique se será educativo,
   exploratório, simulado ou baseado em experiência autorizada.
2. Peça aprovação do ângulo antes de redigir.
3. Após a aprovação, leia [references/writing-style.md](references/writing-style.md) e produza:
   - rascunho do texto;
   - pergunta específica para interação;
   - três a cinco hashtags;
   - roteiro visual coerente com a afirmação principal.
4. Peça aprovação conjunta do texto e do roteiro antes de criar arquivos ou renderizar.
5. Crie o workspace com:

   ```bash
   python3 <skill-dir>/scripts/create_post_workspace.py "Título do post"
   ```

   Use exatamente o caminho absoluto devolvido pelo script.
6. Leia [references/visual-system.md](references/visual-system.md) e, para escolha de
   ferramenta, [references/animation-tools.md](references/animation-tools.md).
7. Copie o template Remotion para `visual/projeto-remotion/`, preencha os arquivos do pacote
   e renderize `output/post.mp4` e `output/capa.png`. Gere GIF somente se solicitado.
8. Leia [references/quality-checklist.md](references/quality-checklist.md) e execute:

   ```bash
   python3 <skill-dir>/scripts/validate_post_package.py <caminho-absoluto-do-post>
   ```

9. Só declare a publicação pronta quando o validador retornar `APROVADO`.

## Limites de autorização

- Não publique, agende, envie mensagens ou apague pacotes.
- Não sobrescreva uma pasta existente.
- Não trate frequência desejada como autorização para criar assunto do nada.
- Não copie frases, identidade, paleta ou assinatura de outro criador.
- Preserve fontes e intermediários quando a renderização falhar e reporte o erro real.
