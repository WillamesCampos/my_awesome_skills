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

const requireBoundedText = (
  value: unknown,
  field: string,
  maxLength: number,
): string => {
  const text = requireText(value, field);
  if (text.length > maxLength) {
    throw new Error(`${field} deve ter no máximo ${maxLength} caracteres`);
  }
  return text;
};

export const parsePostVisualData = (input: unknown): PostVisualData => {
  if (typeof input !== "object" || input === null) {
    throw new Error("post data deve ser um objeto");
  }
  const value = input as Record<string, unknown>;
  const supportingText = requireBoundedText(
    value.supportingText,
    "supportingText",
    180,
  );
  if (
    !Array.isArray(value.nodes) ||
    value.nodes.length < 2 ||
    value.nodes.length > 4
  ) {
    throw new Error("nodes deve conter entre 2 e 4 itens");
  }
  const nodes = value.nodes.map((node, index) =>
    requireBoundedText(node, `nodes[${index}]`, 24),
  );
  if (
    typeof value.durationSeconds !== "number" ||
    value.durationSeconds < 8 ||
    value.durationSeconds > 15
  ) {
    throw new Error("durationSeconds deve estar entre 8 e 15");
  }

  return {
    series: requireBoundedText(value.series, "series", 24),
    issue: requireBoundedText(value.issue, "issue", 8),
    headline: requireBoundedText(value.headline, "headline", 90),
    supportingText,
    nodes,
    footer: requireBoundedText(value.footer, "footer", 48),
    durationSeconds: value.durationSeconds,
  };
};
