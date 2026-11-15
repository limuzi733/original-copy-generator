---
name: original-copy-generator
display_name: 原创文案生成器
display_name_en: Original Copy Generator
version: 1.0.0
description: "先全网搜证、再把关键词扩成多视角，挖出你自己都没意识到的痛点；当不同来源说法打架时，它把冲突亮出来让你拍板，绝不替你赌技术立场。每句文案可溯源到出处，受控换说法保原创、能过平台查重；一份真料同源出短视频口播、种草笔记、电商详情等多种文体。关键词入口，不预置任何行业模板。"
description_zh: "先全网搜证、再把关键词扩成多视角，挖出你自己都没意识到的痛点；当不同来源说法打架时，它把冲突亮出来让你拍板，绝不替你赌技术立场。每句文案可溯源到出处，受控换说法保原创、能过平台查重；一份真料同源出短视频口播、种草笔记、电商详情等多种文体。关键词入口，不预置任何行业模板。"
description_en: "Takes one keyword, searches the web for real viewpoints with sources, expands it into multiple angles, surfaces conflicting claims and lets the user decide the technical stance, then writes traceable non-derivative copy with controlled paraphrase; one source pack yields short-video scripts, social notes, product pages and long-form articles. No industry templates."
agent_created: true
---

# 原创文案生成器 — 搜证发现式文案引擎

## Overview

Generate **genuinely original (passes platform duplicate-detection)**, non-derivative copy for **any industry** by **discovering** real
material at runtime — not by requiring the user to hand it over. The skill takes a
**keyword/topic**, expands it into multiple angles, searches the web (and optionally a
same-domain viral video) to collect real viewpoints **with sources**, fuses them into a
main line, then rewrites into the requested copy type with controlled variation to beat
plagiarism detectors.

This is the opposite of a "knowledge base": nothing is pre-stored, no industry
templates, no hardcoded examples. Material is found live; structure is learned from
discovered exemplars; facts are traced to discovered sources. The only thing the user
must supply is a **keyword** (and, optionally, the copy type they want).

## When To Use

- A user gives a keyword, product, brand, or industry and wants original copy.
- Copy type is flexible: 短视频口播 (default), 小红书笔记, 电商详情页, 公众号文章,
  广告语 / Slogan, etc.
- Goal: non-derivative copy that won't trip platform duplicate-content detection.

## When NOT To Use

- When the user wants the model to invent facts / numbers / cases. Never — every claim
  must trace to a discovered source OR the user's resolved real material.
- When search returns nothing real for the keyword (can't fabricate from empty). Tell
  the user and ask for a clearer / broader keyword.
- **When public sources conflict AND the user declines to resolve them.** Do NOT pick a
  side and write. State the conflict openly and stop, or write only the non-contested
  parts clearly labeled "publicly disputed." Never gamble a technical stance the user
  hasn't endorsed — that is how copy gets a business into trouble (wrong install
  guidance, peer call-outs).

## Core Principles (load-bearing)

1. **Discovery over knowledge base.** Material is found live via search; the user only
   supplies a keyword. Do NOT ask the user to "provide real material first" — that is
   the exact anti-pattern this skill was built to escape.
2. **Expand before you search — this is the fix for narrow material.** A single keyword
   returns a single pain point. AI MUST expand it into multiple angles (failure modes,
   user scenarios, comparisons, selection criteria, common misconceptions) so the
   collected material is BROAD, not one-dimensional. A user who "doesn't know their pain
   points" is exactly why the engine must discover them.
3. **Every claim is sourced.** Each viewpoint carries a `url` / `source`. The copy never
   states a fact the sources don't support. This is the no-fabrication floor.
4. **Controlled rephrasing, not copying — this is what makes the copy genuinely original and pass platform checks.** Fuse sources into a NEW text with a single through-line; controlled rephrasing (never verbatim synonym-swapping) yields low n-gram overlap that defeats duplicate-detection. The output is original, not a reordered clone of one source.
5. **Exemplar teaches structure, never content.** A discovered or uploaded viral video
   is read for rhythm / opening / closure / sentence length only — never for its nouns,
   numbers, or cases.
6. **Search finds the landscape; real material takes the position.** Web search reveals
   what's publicly claimed — **including where sources contradict each other on basic
   facts.** The copy must not gamble on a technical stance the user hasn't endorsed.
   After search, surface the conflicts and ask the user to resolve them with their real
   product facts / on-site experience. This is the gate, but it is *informed by
   discovery* — not a blank "give me material" wall at Step 1. The user's answers become
   the defensible position; everything else from search is landscape/context, not the
   stance.

## Workflow — the 7 steps (discovery chain)

### Step 1 — Keyword entry
Accept a keyword/topic. Also confirm (or default) the **copy type** (短视频口播 default).
Optionally accept an uploaded same-domain viral video transcript as an exemplar.

### Step 2 — AI expands the keyword (critical step)
Run the EXPAND prompt (`references/prompts.md`). From the one keyword, produce 3–6
**complementary search-query groups spanning DIFFERENT angles** — not synonyms of the
same phrase. This deliberately surfaces pain points / viewpoints the user never stated,
which is the root fix for narrow material. Example angles for a product keyword:
failure modes, real-use scenarios, head-to-head comparisons, selection criteria,
misconceptions / pitfalls, "who should NOT buy".

### Step 3 — Full web search (discovery)
For each query group, run a real web search (the agent's WebSearch tool, or 博查 /
Tavily if API keys are configured). Collect real snippets/results; for each capture
`text` + `url` + `source`. Aim for 12–20 distinct **sourced** viewpoints. If a query
returns nothing, drop it and keep searching the others. If ALL return nothing, stop and
tell the user.

### Step 4 — Surface conflicts, then resolve with the user's real material (THE GATE)
After search, run the CONFLICT prompt (`references/prompts.md`) over the collected sourced
viewpoints. Flag every place where public sources **contradict each other on a basic fact**
(different sealing mechanism, compatible pipes, bury-ability, failure cause, lifespan
numbers, etc.).

Then present those conflicts to the user and ask them to resolve each with their **real
material** — their actual product facts, on-site experience, or installation reality. This
is the gate, but it is *informed by discovery*: you are not demanding "give me material
blindly," you are showing the user exactly where the public record disagrees and asking
"which is true for YOUR product?" The user's answers become the defensible position the copy
takes; everything else from search is landscape/context, not the stance.

If the user declines to resolve a conflict, do NOT pick a side and write. State the conflict
openly and stop, or write only the non-contested parts clearly labeled "publicly disputed."
Never gamble a technical stance the user hasn't endorsed.

**Do NOT block at Step 1 for "no material."** The gate lives HERE, after discovery has shown
what's at stake. A bare keyword with no conflicts found can proceed (Step 5+); a keyword
whose sources fight each other must be resolved before any copy is written.

### Step 5 — Organize viewpoints
Run EXTRACT + DEDUP over BOTH the searched viewpoints AND the user's resolved real material.
Each viewpoint: `{id, text, topic, quote, url, source}` (user material gets `source:
"owner"`). Drop clickbait titles, calls to follow/like, ads, pure slogans (rules in
prompts.md). Merge semantic repeats, keeping the most informative variant + merged sources.

### Step 6 — Fuse main line
Run PLAN: group the sourced viewpoints + resolved material into episodes / sections by angle.
Episode/section count is decided by material, never preset. Each angle needs enough real
points; if thin, state what's missing (don't invent to fill). Multiple distinct sources per
angle; the user's resolved position is authoritative where sources conflict.

### Step 7 — Generate copy (multi-type, same source)
Run STRUCTURE + REWRITE for the requested copy type. Short-video uses a screen skeleton;
other types use their own format (see copy-type notes in prompts.md). **Multiple copy types
share the SAME resolved material** — e.g. a 短视频口播 and a 公众号推文 are derived from one
source, different genres, never relaxing the no-fabrication line for the longer form. Fuse
into one through-line; controlled rephrasing; tag each paragraph/screen with cited `ids` for
traceability. Use the exemplar (if any) for rhythm only.

### Step 8 — Hard gates + audit + deliver
Run `scripts/verify_copy.py` (no new numbers, no absoluteness words, no placeholders,
opening/closing gates, length). Run AUDIT: every claim in the copy must trace to a source
`url` OR the user's resolved material. Rewrite failed parts; drop what can't be grounded.
Deliver the copy **plus a source list (urls + owner-resolved positions)** so the owner can
self-check — do NOT surface raw exemplar transcripts.

## Resources

- `references/prompts.md` — the exact system prompts for every step (EXPAND / EXTRACT /
  DEDUP / PLAN / STRUCTURE / REWRITE / AUDIT / NAME). Load when performing that step.
- `references/fact_gates.md` — the deterministic hard-gate rules (mirrored in the script).
- `scripts/verify_copy.py` — runnable JSON checker enforcing the hard gates. Usage:
  `python verify_copy.py input.json` where `input.json` =
  `{"material":[{id,text,url,source,...}], "script":[{no,ids,text}]}`. Works on any copy
  type (treat each block as one screen/paragraph).
- `assets/reference_example.txt` — a generic, industry-neutral example of a "full spoken
  transcript" structure sample. Format reference only; never a factual source.
