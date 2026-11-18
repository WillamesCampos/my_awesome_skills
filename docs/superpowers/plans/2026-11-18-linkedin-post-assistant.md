# LinkedIn Post Assistant Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a versioned, cross-agent skill that turns verified technical learning into a concise LinkedIn post plus a locally rendered Blueprint Signal cover and MP4 package.

**Architecture:** A concise `SKILL.md` orchestrates evidence review, human approval, writing, rendering, and package validation. Conditional guidance lives in focused references; deterministic Python scripts create and validate post workspaces; a reusable Remotion/TypeScript template renders visual assets from per-post JSON data.

**Tech Stack:** Agent Skills (`SKILL.md`), Markdown/YAML, Python 3 standard library, Node.js, React, TypeScript, Remotion, FFmpeg/ffprobe when available, Git.

## Global Constraints

- Store the complete skill at `linkedin_post_assistant/v1/`, matching this repository's internal versioning convention.
- Use Brazilian Portuguese for generated posts and interaction with the author.
- Never invent benchmarks, metrics, incidents, experience, tools used, or production outcomes.
- Never expose employers, clients, private systems, endpoints, source code, secrets, or unauthorized incidents.
- Do not publish or schedule posts; every post requires manual invocation and human approval before rendering.
- Create each post under `/home/willames/Documents/Posts/<safe-title>/` without overwriting an existing directory.
- Render `output/post.mp4` and `output/capa.png` at 1080×1350; `output/post.gif` is optional.
- Use Remotion as the default renderer; document Motion Canvas, Jitter, and Canva only as optional alternatives.
- Do not commit the confidential technical assessment or generated personal post workspaces.

---

### Task 1: Skill entrypoint and sanitized editorial references

**Files:**
- Create: `linkedin_post_assistant/v1/SKILL.md`
- Create: `linkedin_post_assistant/v1/references/editorial-policy.md`
- Create: `linkedin_post_assistant/v1/references/writing-style.md`
- Create: `linkedin_post_assistant/v1/references/author-context.md`
- Create: `linkedin_post_assistant/v1/references/input-schema.md`

**Interfaces:**
- Consumes: user-supplied study notes, exercises, feedback, experiments, or authorized professional experience.
- Produces: an approved editorial angle, `brief.yaml`, draft copy, final copy, and traceability fields consumed by Tasks 2–4.

- [ ] **Step 1: Create the entrypoint with discriminating activation rules**

Write frontmatter with `name: linkedin-post-assistant` and a description that triggers for transforming the author's verified technical learning into LinkedIn copy plus visual media. Explicitly exclude generic ghostwriting, invented thought leadership, auto-publishing, and content above the author's evidence level.

The workflow must require this sequence:

```text
read supplied evidence
→ classify every material claim
→ propose one angle
→ obtain author approval
→ write copy and visual script
→ obtain author approval
→ create post workspace
→ render
→ validate package
```

- [ ] **Step 2: Write the evidence policy**

Define these exact claim classes in `editorial-policy.md`:

```yaml
claim_classes:
  - professional_experience_reported
  - knowledge_demonstrated
  - learning_in_progress
  - simulated_example
  - unverified_information
  - confidential_or_prohibited
```

Require exploratory framing for `learning_in_progress`, verification or removal for `unverified_information`, and blocking/anonymization for `confidential_or_prohibited`.

- [ ] **Step 3: Write the copy contract**

Define a flexible post shape in `writing-style.md`: short hook, authentic learning context, brief technical reasoning, compact example, trade-off, specific audience question, and 3–5 hashtags. Require first person, concise Brazilian Portuguese, one angle per post, and no imitation of Nikki Siapno's wording or identity.

- [ ] **Step 4: Add sanitized author context**

Record only publication-relevant context: senior Python backend background; current learning focus on Django ORM, PostgreSQL performance, requirement-led architecture, distributed systems, reliability, and applied AI; differentiated evidence maturity. Do not include employer/client names, raw evaluation scores, compensation, or private incidents.

- [ ] **Step 5: Define the per-session input schema**

Use this complete YAML shape in `input-schema.md`:

```yaml
date: YYYY-MM-DD
topic: ""
concepts_studied: []
answers_or_artifacts: []
feedback_received: []
case_type: "simulated | personal_experiment | authorized_real_experience"
demonstrated_points: []
learning_gaps: []
verified_corrections: []
verified_quantitative_results: []
do_not_disclose: []
suggested_angle: ""
editorial_state: "exploratory | ready_for_review | approved"
```

- [ ] **Step 6: Validate the files manually**

Run:

```bash
rg -n 'invent|confiden|approval|Remotion|linkedin-post-assistant' linkedin_post_assistant/v1
```

Expected: evidence safeguards, approval gates, renderer choice, and skill name are all found.

- [ ] **Step 7: Commit the editorial core**

```bash
git add linkedin_post_assistant/v1/SKILL.md linkedin_post_assistant/v1/references
git commit -m "feat: add LinkedIn post assistant editorial workflow"
```

### Task 2: Deterministic post workspace creation

**Files:**
- Create: `linkedin_post_assistant/v1/scripts/create_post_workspace.py`
- Create: `linkedin_post_assistant/v1/tests/test_create_post_workspace.py`
- Modify: `linkedin_post_assistant/v1/SKILL.md`

**Interfaces:**
- Consumes: `create_post_workspace.py TITLE [--date YYYY-MM-DD] [--root PATH]`.
- Produces: the absolute new workspace path on stdout and the approved package directory tree.

- [ ] **Step 1: Write failing workspace tests**

Cover slug normalization and collision safety with `unittest`:

```python
def test_slugifies_accents_and_punctuation(self):
    self.assertEqual(slugify("Por que EXPLAIN não basta?"), "por-que-explain-nao-basta")

def test_existing_title_uses_date_without_overwrite(self):
    first = create_workspace("N+1 no Django", self.root, date(2026, 11, 18))
    marker = first / "keep.txt"
    marker.write_text("preserve", encoding="utf-8")
    second = create_workspace("N+1 no Django", self.root, date(2026, 11, 18))
    self.assertNotEqual(first, second)
    self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")
```

- [ ] **Step 2: Run tests and confirm failure**

Run:

```bash
python3 -m unittest linkedin_post_assistant/v1/tests/test_create_post_workspace.py -v
```

Expected: FAIL because `create_post_workspace.py` does not exist.

- [ ] **Step 3: Implement workspace creation**

Implement `slugify(title: str) -> str` with Unicode NFKD normalization, ASCII conversion, lowercase hyphen separation, and rejection of an empty result. Implement `create_workspace(title: str, root: Path, run_date: date) -> Path` using `Path.mkdir(exist_ok=False)`. On collision, try `<slug>-YYYY-MM-DD`, then `<slug>-YYYY-MM-DD-2`, incrementing until unused.

Create exactly:

```text
brief.yaml
fontes/material-estudado.md
fontes/referencias.md
texto/rascunho.md
texto/versao-final.md
visual/roteiro.md
visual/assets/
visual/projeto-remotion/
output/
rastreabilidade.yaml
```

Initialize text files with descriptive headings and YAML files with valid empty schemas. Never copy the confidential assessment.

- [ ] **Step 4: Run workspace tests**

Run the command from Step 2.

Expected: all tests PASS.

- [ ] **Step 5: Link the script from the entrypoint**

Document the exact invocation:

```bash
python3 <skill-dir>/scripts/create_post_workspace.py "Título do post"
```

State that the returned path, rather than a guessed path, must be used for subsequent writes.

- [ ] **Step 6: Commit the workspace creator**

```bash
git add linkedin_post_assistant/v1/scripts linkedin_post_assistant/v1/tests linkedin_post_assistant/v1/SKILL.md
git commit -m "feat: add collision-safe post workspace creation"
```

### Task 3: Blueprint Signal Remotion template

**Files:**
- Create: `linkedin_post_assistant/v1/assets/remotion-template/package.json`
- Create: `linkedin_post_assistant/v1/assets/remotion-template/tsconfig.json`
- Create: `linkedin_post_assistant/v1/assets/remotion-template/src/index.ts`
- Create: `linkedin_post_assistant/v1/assets/remotion-template/src/Root.tsx`
- Create: `linkedin_post_assistant/v1/assets/remotion-template/src/BlueprintSignal.tsx`
- Create: `linkedin_post_assistant/v1/assets/remotion-template/src/schema.ts`
- Create: `linkedin_post_assistant/v1/assets/remotion-template/public/post-data.example.json`
- Create: `linkedin_post_assistant/v1/references/visual-system.md`
- Create: `linkedin_post_assistant/v1/references/animation-tools.md`

**Interfaces:**
- Consumes: JSON `{series, issue, headline, supportingText, nodes[], footer, durationSeconds}`.
- Produces: Remotion compositions `BlueprintSignalVideo` and `BlueprintSignalCover`, both 1080×1350.

- [ ] **Step 1: Define and test the data parser**

In `schema.ts`, export `PostVisualData`, `DEFAULT_POST_DATA`, and `parsePostVisualData(input: unknown): PostVisualData`. Reject empty headlines, fewer than two or more than four nodes, supporting text over 180 characters, and durations outside 8–15 seconds.

Add a minimal Node assertion script exposed as `npm run test:schema` that checks valid example parsing and rejection of an empty headline.

- [ ] **Step 2: Confirm the schema test fails before implementation**

Run:

```bash
cd linkedin_post_assistant/v1/assets/remotion-template
npm install
npm run test:schema
```

Expected: FAIL until the parser is implemented.

- [ ] **Step 3: Implement Blueprint Signal compositions**

Use a light blue background, deep navy text, blue accent, a 24-pixel engineering grid, sans-serif title, monospace labels, 80-pixel safe margins, and a horizontal or wrapped node flow. Animate with `interpolate()` and `spring()` so the headline, nodes, arrows, supporting text, and footer enter sequentially. Keep information independent of color and use no external images.

The cover composition must render the final, fully visible state. The video must use 30 fps and derive duration from `durationSeconds`.

- [ ] **Step 4: Add render scripts**

Expose these package scripts:

```json
{
  "render:video": "remotion render src/index.ts BlueprintSignalVideo output/post.mp4 --props=public/post-data.json",
  "render:cover": "remotion still src/index.ts BlueprintSignalCover output/capa.png --props=public/post-data.json",
  "test:schema": "tsx src/schema.test.ts"
}
```

- [ ] **Step 5: Document tool routing**

In `animation-tools.md`, make Remotion the default. Route to Motion Canvas only for complex vector/algorithm sequencing. Describe Canva and Jitter as manual optional fallbacks with plan-dependent export limits. Include official links and require current license/plan checks before relying on paid features.

- [ ] **Step 6: Render and inspect representative outputs**

Run:

```bash
npm run test:schema
cp public/post-data.example.json public/post-data.json
npm run render:video
npm run render:cover
ffprobe -v error -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of json output/post.mp4
```

Expected: schema tests PASS; MP4 and PNG exist; video reports 1080×1350, 30 fps, and 8–15 seconds.

- [ ] **Step 7: Commit the visual template**

Do not commit `node_modules`, temporary `public/post-data.json`, or generated output.

```bash
git add linkedin_post_assistant/v1/assets linkedin_post_assistant/v1/references
git commit -m "feat: add Blueprint Signal Remotion template"
```

### Task 4: Package validation and quality contract

**Files:**
- Create: `linkedin_post_assistant/v1/scripts/validate_post_package.py`
- Create: `linkedin_post_assistant/v1/tests/test_validate_post_package.py`
- Create: `linkedin_post_assistant/v1/references/quality-checklist.md`
- Modify: `linkedin_post_assistant/v1/SKILL.md`

**Interfaces:**
- Consumes: `validate_post_package.py /absolute/path/to/post`.
- Produces: JSON `{status: "APROVADO"|"PENDENTE", checks: [...], errors: [...]}` and exit code 0 only for `APROVADO`.

- [ ] **Step 1: Write failing validator tests**

Test that a missing final post, missing traceability, missing cover, or missing MP4 returns `PENDENTE`; test that GIF is optional. Mock `subprocess.run` for ffprobe metadata and assert rejection of dimensions other than 1080×1350 or duration outside 8–15 seconds.

- [ ] **Step 2: Confirm validator tests fail**

Run:

```bash
python3 -m unittest linkedin_post_assistant/v1/tests/test_validate_post_package.py -v
```

Expected: FAIL because the validator module does not exist.

- [ ] **Step 3: Implement deterministic validation**

Require non-empty `brief.yaml`, `fontes/material-estudado.md`, `texto/versao-final.md`, `visual/roteiro.md`, `output/post.mp4`, `output/capa.png`, and `rastreabilidade.yaml`. Parse PNG dimensions with the standard library. Use `ffprobe` JSON when available; report a clear pending check when absent rather than claiming video validation succeeded.

- [ ] **Step 4: Run validator tests**

Run the command from Step 2.

Expected: all tests PASS.

- [ ] **Step 5: Document the final quality gate**

Require editorial integrity, technical accuracy, visual checks, and package completeness. The agent must report `PENDENTE` with exact causes on any failed check and may never create a false success marker.

- [ ] **Step 6: Commit validation**

```bash
git add linkedin_post_assistant/v1/scripts linkedin_post_assistant/v1/tests linkedin_post_assistant/v1/references/quality-checklist.md linkedin_post_assistant/v1/SKILL.md
git commit -m "feat: validate LinkedIn post packages"
```

### Task 5: Repository integration, skill validation, and remote delivery

**Files:**
- Modify: `README.md`
- Create: `linkedin_post_assistant/v1/agents/openai.yaml`
- Create: `linkedin_post_assistant/v1/.gitignore`

**Interfaces:**
- Consumes: the complete skill from Tasks 1–4.
- Produces: discoverable repository documentation, valid Codex UI metadata, a clean Git history, and a pushed `origin/main`.

- [ ] **Step 1: Add repository documentation**

Add a `linkedin_post_assistant` section to `README.md` describing verified-learning input, copy plus Blueprint Signal media output, manual approval, Remotion default, and `v1`. Add installation examples for Claude Code, OpenCode, Codex, and `~/.agents/skills` using the folder name `linkedin-post-assistant`.

- [ ] **Step 2: Add Codex metadata**

Create `agents/openai.yaml` with:

```yaml
interface:
  display_name: "LinkedIn Post Assistant"
  short_description: "Transforme aprendizado técnico verificado em post e animação."
  default_prompt: "Use $linkedin-post-assistant para transformar este aprendizado técnico em um post rastreável com visual Blueprint Signal."
```

- [ ] **Step 3: Ignore generated dependencies and media**

Ignore `node_modules/`, `output/`, `public/post-data.json`, and local render caches inside the template while preserving the checked-in example JSON.

- [ ] **Step 4: Run all tests and skill validation**

Run:

```bash
python3 -m unittest discover -s linkedin_post_assistant/v1/tests -v
python3 /home/willames/.codex/skills/.system/skill-creator/scripts/quick_validate.py linkedin_post_assistant/v1
cd linkedin_post_assistant/v1/assets/remotion-template
npm install
npm run test:schema
npm run render:video
npm run render:cover
```

Expected: Python tests PASS, skill validation succeeds, schema tests PASS, and both media files render.

- [ ] **Step 5: Perform a clean-package smoke test**

Create a workspace under a temporary directory, populate it with non-confidential simulated N+1 learning material, copy the template, render video and cover, run the package validator, and expect `APROVADO`. Remove only the temporary test directory after recording the results.

- [ ] **Step 6: Review diff and commit integration**

```bash
git diff --check
git status --short
git add README.md linkedin_post_assistant/v1/agents linkedin_post_assistant/v1/.gitignore docs/superpowers/plans/2026-11-18-linkedin-post-assistant.md
git commit -m "docs: publish LinkedIn post assistant skill"
```

- [ ] **Step 7: Sync and push**

```bash
git fetch origin
git rebase origin/main
git push origin main
```

Expected: push succeeds and `origin/main` points to the final commit.

- [ ] **Step 8: Verify remote delivery**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Expected: clean working tree, local HEAD equals remote main, and final report includes links to:

```text
https://github.com/WillamesCampos/my_awesome_skills/tree/main/linkedin_post_assistant/v1
https://github.com/WillamesCampos/my_awesome_skills/blob/main/README.md
```
