export type PostVisualData = {
  series: string;
  issue: string;
  headline: string;
  supportingText: string;
  nodes: string[];
  footer: string;
  durationSeconds: number;
};

export const DEFAULT_POST_DATA: PostVisualData = {
  series: "BACKEND NOTES",
  issue: "01",
  headline: "Uma query rápida não significa uma request rápida.",
  supportingText:
    "Performance exige medir o caminho inteiro — não apenas abrir o EXPLAIN.",
  nodes: ["QUERY", "SERIALIZER", "PAYLOAD"],
  footer: "MEDIR → COMPARAR → DECIDIR",
  durationSeconds: 10,
};

const requireText = (value: unknown, field: string): string => {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${field} deve ser um texto não vazio`);
  }
  return value.trim();
};

export const parsePostVisualData = (input: unknown): PostVisualData => {
  if (typeof input !== "object" || input === null) {
    throw new Error("post data deve ser um objeto");
  }
  const value = input as Record<string, unknown>;
  const supportingText = requireText(value.supportingText, "supportingText");
  if (supportingText.length > 180) {
    throw new Error("supportingText deve ter no máximo 180 caracteres");
  }
  if (
    !Array.isArray(value.nodes) ||
    value.nodes.length < 2 ||
    value.nodes.length > 4
  ) {
    throw new Error("nodes deve conter entre 2 e 4 itens");
  }
  const nodes = value.nodes.map((node, index) =>
    requireText(node, `nodes[${index}]`),
  );
  if (
    typeof value.durationSeconds !== "number" ||
    value.durationSeconds < 8 ||
    value.durationSeconds > 15
  ) {
    throw new Error("durationSeconds deve estar entre 8 e 15");
  }

  return {
    series: requireText(value.series, "series"),
    issue: requireText(value.issue, "issue"),
    headline: requireText(value.headline, "headline"),
    supportingText,
    nodes,
    footer: requireText(value.footer, "footer"),
    durationSeconds: value.durationSeconds,
  };
};

