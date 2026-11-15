# Fact Gates — Hard Rules

These are the deterministic gates enforced by `scripts/verify_copy.py` and mirrored here for
quick reference. They are the no-fabrication floor plus the anti-plagiarism structure gates.
A block that fails a hard gate is rewritten (with audit hints) and re-checked; blocks that
still fail are dropped, never shipped with fabrication.

> Material here = **discovered, sourced viewpoints** collected via web search in Step 3–4 of
> the workflow (each carries a `url` / `source`). The skill never requires the user to supply
> material up front; it discovers it. Every claim in the copy must trace to one of these
> sources.

## Fact red line (anti-fabrication)
- **No new numbers.** Every digit/decimal in a block must appear in the cited material's
  union. Numbers keep their exact written form — no convert, no rephrase.
- **No new Chinese number-units.** Combinations like 十公分 / 五分钟 / 1.2米 / 25厘米 absent
  from cited material fail.
- **No "saying it full".** Absoluteness words (怎么用都 / 永远 / 绝对 / 保证 / 一定不 / 百分百 /
  万无一失 / 随便用 / 从不) absent from cited material fail — they turn a qualified claim into a
  guarantee (a form of fabrication).
- **No placeholders / verbatim.** 【】, 待补, [ ], or copying a source sentence verbatim fail.
- **Hedges preserved.** Material's "可能/相对/需要…/别只…" must not be dropped.
- **Sourced or dropped.** Any concrete claim in the copy that no cited source `url` supports
  fails the audit (Step 7).

## Structure gates (anti-plagiarism / readability)
- **Opening must not start with a connector.** 再说 / 还有 / 另外 / 那么 / 其实 / 简单来说 /
  接下来 / 其次 / 而且 / 并且 / 此外 / 话说回来 / 换言之 / 总的说 / 之一 at the head of the
  opening block fail (signals a listing-break, not an independent hook).
- **Closing must not be filler.** Patterns like 按.{0,4}需求 / 自己的需求 / 总之.{0,2}要 / 要注意 /
  希望对大家 / 按需(选|挑|买) / 根据.{0,4}需求 fail (doesn't catch the opening pain/conflict).
- **Length guard (anti-bloat only).** block length ≤ max(180, longest cited point ×6) and ≥6
  chars. This only trims离谱膨胀; good blocks that expand one scene/action are NOT
  penalized. Real anti-fabrication is the fact red line + the LLM audit, not character count.

## Soft indicators (trigger one targeted rephrase, never drop)
- **Bookish words** (进行 / 具有 / 从而 / 此外 / 综上 / 需要注意的是 / 建议优先 / 应当 / 较为 /
  予以 / 首先 / 其次 / 因此…) → one rephrase pass.
- **Opening too weak** (no scene/pain cue: 你/我/这/那/为什么/别/误区/错/坑/糟…) → one rephrase
  pass.
- **Closing too weak** (no 所以/关键/别/选/看/说白/最该… cue) → one rephrase pass.
- **Hedge lost** in a block vs its cited material → one rephrase pass.

## What is NOT a problem
- Rephrasing, splitting, reordering, fusing material's existing elements.
- Copy longer / more spoken than material.
- Teaching the reader a verification action using only material's existing
  objects/attributes (turn it over / heft it / compare two / pull / pinch) — this is
  expression, not fabrication.

## Output contract (verify_copy.py)
`verify_copy.py` returns, per block: `ok` (bool), `hard_reason` (if failed), and per-block
`ids`/cited material. Aggregate: `pass` (all blocks ok) or list of failed blocks with
reasons. Re-run after each rewrite until `pass` or drop. Works on any copy type (treat each
text block as one screen/paragraph).
