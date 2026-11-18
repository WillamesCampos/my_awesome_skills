# Checklist de qualidade

O script valida os artefatos determinísticos. O agente também deve concluir as revisões
editorial e técnica antes de executar o script.

## Integridade editorial

- Cada afirmação material tem classe, fonte e redação publicada em `rastreabilidade.yaml`.
- Experiência relatada, simulação e aprendizado estão claramente diferenciados.
- Não há métrica, incidente, ferramenta ou resultado inventado.
- Detalhes confidenciais foram removidos e registrados sem reproduzi-los.
- A versão final foi aprovada pelo usuário.

## Precisão técnica

- Código, SQL, terminologia e trade-offs foram revisados.
- Informação externa atual usa fonte oficial ou primária registrada.
- Pendências não aparecem como conclusão verificada.
- O texto permanece dentro do nível sustentado pelo material da sessão.

## Visual

- Capa e vídeo têm 1080×1350.
- O vídeo dura entre 8 e 15 segundos e usa 30 fps.
- A capa comunica a ideia sem depender do vídeo.
- Texto não está cortado e permanece legível em escala de feed.
- Cor não é o único meio de transmitir informação.
- O movimento acompanha o raciocínio e não é puramente decorativo.

## Pacote

Preencha fontes, texto final, roteiro e rastreabilidade. Renderize MP4 e PNG. O GIF é opcional.
Execute `validate_post_package.py` e reporte todos os erros quando o estado for `PENDENTE`.
Nunca crie ou declare um marcador falso de aprovação.
