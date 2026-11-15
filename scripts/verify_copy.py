# -*- coding: utf-8 -*-
"""Real-material-copy 硬闸校验器（确定性，零模型调用）。

对每一屏/段文案，对照它引用的「真实素材（发现自搜索、带 url/source）」做事实红线 +
结构闸门检查。失败即硬闸未过，需带审计提示重改；仍不过则整段剔除（绝不带编造出厂）。

本校验器与文案类型无关：短视频口播、小红书、电商详情、公众号、广告语都按「文本块列表」
处理，每个块即一屏/一段。

用法：
    python verify_copy.py input.json
    cat input.json | python verify_copy.py -

输入 JSON 结构：
    {
      "material": [ {"id": 1, "text": "原始观点/真实素材原文", "url": "...", "source": "..."}, ... ],
      "script":   [ {"no": 1, "ids": [1,3], "text": "这一屏/段文案"}, ... ]
    }
    ids 缺省或非法时回落到「全部素材」的并集（仅用于数字/数词 grounding 兜底）。

输出 JSON：
    {"pass": bool, "screens": [ {"no":int,"ok":bool,"hard_reason":str,
                                 "soft_reason":str} ], "failed": [...]}
"""
import json
import re
import sys

# ---- 数字 grounding ----
def _nums(t):
    return sorted(re.findall(r"\d+(?:\.\d+)?", str(t or "")))

# ---- 中文数词组合（单字「一」太常见，只认带量词的） ----
_CN_UNIT_RE = re.compile(
    r"[零一二两三四五六七八九十百千]+(?:\s*)"
    r"(?:厘米|公分|毫米|米|分钟|小时|年|月|天|块|元|成|倍|次|层|度|折|D|d|%)")

def _cn_num_units(t):
    return set(m.group(0) for m in _CN_UNIT_RE.finditer(str(t or "")))

# ---- 说满＝把留余地改成打包票（属编造） ----
_ABSOLUTE_RE = re.compile(
    r"怎么用都|怎么都|永远|绝对|保证|一定不|都不会|百分百|完全不|万无一失|"
    r"再也不|随便用|随便怎么|不带变形|从不")

def _absolutes(t):
    return set(m.group(0) for m in _ABSOLUTE_RE.finditer(str(t or "")))

# ---- 开场/收尾结构闸门 ----
_OPENERS_BAD = ("再说", "还有", "另外", "那么", "其实", "简单来说", "接下来",
                "其次", "而且", "并且", "此外", "话说回来", "换言之", "总的说",
                "之一", "话说")
_END_FILLER_RE = re.compile(
    r"(按.{0,4}需求|自己的需求|总之.{0,2}要|要注意|希望对大家|有所帮助|"
    r"按需(选|挑|买|挑)|根据.{0,4}需求|看(自己|个人)?.{0,4}需求|合适(的)?(自己|你).{0,3})")

def _open_bad(t):
    s = str(t or "")
    return any(s.startswith(w) or s[:2] == w for w in _OPENERS_BAD)

def _end_filler(t):
    return bool(_END_FILLER_RE.search(str(t or "")))

# ---- 占位符 / 整句照搬 ----
_PLACEHOLDER_RE = re.compile(r"【|】|待补|\[")
def _has_placeholder(t):
    return bool(_PLACEHOLDER_RE.search(str(t or "")))


def verify_screen(text, cited_srcs, idx, n):
    """返回 (ok, hard_reason, soft_reason)。"""
    t = str(text or "").strip()
    cited_text = " ".join(str(s.get("text") or "") for s in cited_srcs)
    base_nums = sorted(_nums(cited_text))
    base_cn = set()
    base_abs = set()
    for s in cited_srcs:
        base_cn |= _cn_num_units(s.get("text", ""))
        base_abs |= _absolutes(s.get("text", ""))

    # 事实红线
    num_new = [x for x in _nums(t) if x not in set(base_nums)]
    cn_new = _cn_num_units(t) - base_cn
    added_abs = _absolutes(t) - base_abs
    verbatim = bool(cited_srcs) and t in [str(s.get("text") or "") for s in cited_srcs]
    clean_ok = (not _has_placeholder(t)) and (not verbatim) and bool(t)
    # 长度只砍离谱膨胀：真实爆款范例注入后，一屏常把一件事讲透，不能压太紧。
    maxlen = max(180, (max((len(str(s.get("text") or "")) for s in cited_srcs), default=20)) * 6.0)
    len_ok = (len(t) <= maxlen) and (len(t) >= 6)

    is_open, is_end = (idx == 0), (idx == n - 1)
    open_bad = bool(is_open and _open_bad(t))
    end_bad = bool(is_end and (_open_bad(t) or _end_filler(t)))

    ok = bool(not num_new and not cn_new and not added_abs and clean_ok
              and len_ok and not open_bad and not end_bad and t)
    hard_reason = ""
    if not ok:
        bits = []
        if num_new:
            bits.append("新增数字%s" % "/".join(num_new))
        if cn_new:
            bits.append("新增中文数词%s" % "/".join(sorted(cn_new)))
        if added_abs:
            bits.append("说满%s" % "/".join(sorted(added_abs)))
        if not clean_ok:
            bits.append("含占位符或整句照搬")
        if not len_ok:
            bits.append("长度超标(>%d)" % int(maxlen))
        if open_bad:
            bits.append("开场承接词起头")
        if end_bad:
            bits.append("收尾空话(未呼应开头痛点)" if _end_filler(t) else "收尾承接词起头")
        hard_reason = "；".join(bits)

    # 软指标（仅触发定向重改，不剔除）
    soft = []
    _BOOKISH = ("进行", "具有", "从而", "此外", "综上", "需要注意的是", "值得注意",
                "建议优先", "可有效", "应当", "较为", "予以", "即可", "综上所述",
                "首先", "其次", "因此", "相对而言")
    bookish = [w for w in _BOOKISH if w in t]
    if bookish:
        soft.append("偏书面%s" % "/".join(bookish[:3]))
    if is_open and not re.search(r"(你|我|咱|这|那|为什么|咋|别|误区|错|糟|坑|"
                                 r"踩|纠结|头疼|水太深|上当|中招)", t):
        soft.append("开场偏弱(缺场景/痛点cue)")
    if is_end and not re.search(r"(所以|总之|说到底|记住|关键|别|选|看|说白|最该|"
                                r"宁可|不如|这才是|认准)", t):
        soft.append("收尾偏弱")
    soft_reason = "；".join(soft)
    return ok, hard_reason, soft_reason


def main():
    src = None
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], encoding="utf-8") as f:
            src = f.read()
    else:
        src = sys.stdin.read()
    data = json.loads(src)
    material = data.get("material") or []
    script = data.get("script") or []
    mat_by_id = {int(m.get("id")): m for m in material
                 if str(m.get("id", "")).isdigit()}

    out_screens = []
    failed = []
    n = len(script)
    for idx, sc in enumerate(script):
        t = sc.get("text", "")
        ids = sc.get("ids") or []
        cited = [mat_by_id[i] for i in ids if i in mat_by_id]
        if not cited:  # 兜底：本片全部素材并集（仅用于 grounding）
            cited = list(material)
        ok, hard, soft = verify_screen(t, cited, idx, n)
        rec = {"no": sc.get("no", idx + 1), "ok": ok,
               "hard_reason": hard, "soft_reason": soft}
        out_screens.append(rec)
        if not ok:
            failed.append(rec)
    result = {"pass": len(failed) == 0, "screens": out_screens,
              "failed": [f["no"] for f in failed]}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
