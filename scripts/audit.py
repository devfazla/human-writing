#!/usr/bin/env python3
"""
audit.py - surface-pattern audit for a prose draft.

Usage:
    python3 audit.py draft.txt --source material.txt
    python3 audit.py draft.txt --json
    cat draft.txt | python3 audit.py -

--source FILE (repeatable) is the most important option. Put everything the user
told you (their messages, facts, pasted docs) in that file. The audit then flags
every sentence whose content words appear nowhere in it. Those sentences are
usually invented stance, filler, or generic framing, which is the strongest
machine tell in short posts.

What it does: counts the surface habits that make text read as machine-written
(flat sentence rhythm, stock words and phrases, triplets, contrast framing,
-ing tails, paragraph-end summaries, em dash density, formatting habits,
stock names, chat leftovers) and prints where they are.

What it does NOT do: predict any detector's score. Thresholds below are rough
heuristics chosen by this skill's author. Treat the report as a list of places
to look, then fix the underlying idea, not just the flagged word.
"""
import argparse
import json
import re
import statistics
import sys

# ---------------------------------------------------------------- vocab lists

STOCK_WORDS = [
    "delve", "delves", "delving", "tapestry", "testament", "beacon", "realm",
    "landscape", "multifaceted", "nuanced", "intricate", "intricacies",
    "pivotal", "crucial", "vital", "robust", "seamless", "seamlessly",
    "vibrant", "holistic", "comprehensive", "meticulous", "meticulously",
    "transformative", "groundbreaking", "cutting-edge", "invaluable",
    "underscore", "underscores", "underscoring", "showcase", "showcases",
    "showcasing", "foster", "fosters", "fostering", "enhance", "enhances",
    "enhancing", "leverage", "leverages", "leveraging", "harness", "harnessing",
    "streamline", "streamlines", "elevate", "elevates", "empower", "empowers",
    "unlock", "unlocks", "facilitate", "facilitates", "bolster", "bolsters",
    "garner", "garnered", "embark", "resonate", "resonates", "interplay",
    "synergy", "paradigm", "cornerstone", "game-changer", "notably",
    "importantly", "ultimately", "journey", "navigate", "navigating",
]

STOCK_PHRASES = [
    r"it(?:'s| is) (?:important|crucial|essential|worth) (?:to )?(?:note|noting|remember|mention|mentioning)",
    r"in today'?s (?:\w+[- ]){0,3}(?:world|landscape|era|age|market|environment)",
    r"in the (?:ever-)?(?:evolving|changing) (?:\w+ )?(?:world|landscape)",
    r"plays? an? (?:\w+ )?(?:vital|crucial|key|pivotal|significant|important|essential) role",
    r"a testament to",
    r"(?:rich|vibrant) tapestry",
    r"in the realm of",
    r"when it comes to",
    r"at the end of the day",
    r"in (?:conclusion|summary)\b",
    r"to (?:sum up|summarize|summarise)\b",
    r"i hope this helps",
    r"let me know if",
    r"let'?s dive",
    r"dive (?:in|into|deeper)",
    r"stands? as (?:a|an)\b",
    r"serves? as (?:a|an)\b",
    r"shed(?:s|ding)? light on",
    r"paves? the way",
    r"nestled",
    r"in the heart of",
    r"a wide (?:range|variety|array) of",
    r"the world of",
    r"(?:continues|continue) to (?:captivate|thrive|evolve|inspire)",
    r"lasting (?:legacy|impact)",
    r"it goes without saying",
    r"needless to say",
    r"in an? (?:increasingly )?(?:fast-paced|digital|interconnected) (?:world|age)",
    r"the (?:future|power|art|importance) of\b",
    r"(?:rich|diverse) (?:heritage|history|culture)",
    r"unlock(?:s|ing)? (?:the )?(?:full )?(?:potential|power)",
    r"take(?:s)? (?:it|things) to the next level",
]

TRANSITION_OPENERS = [
    "additionally", "furthermore", "moreover", "notably", "importantly",
    "ultimately", "overall", "in conclusion", "in summary", "in addition",
    "consequently", "indeed", "essentially", "that said", "with that in mind",
    "it is worth noting", "it's worth noting",
]

OPENER_CLICHES = [
    r"^in today'?s", r"^in the (?:ever|ever-)", r"^imagine\b", r"^picture this",
    r"^in a world", r"^have you ever", r"^when it comes to", r"^whether you'?re",
    r"^in an? (?:increasingly|rapidly)", r"^welcome to", r"^are you (?:looking|ready)",
]

CLOSER_MARKERS = [
    r"\bin conclusion\b", r"\bin summary\b", r"\boverall\b", r"\bultimately\b",
    r"\bthe future (?:of|is|looks|holds)\b", r"\bremember\b.*\bjourney\b",
    r"\bjourney\b", r"\bpotential\b", r"\bbright(?:er)? future\b",
    r"\bhere'?s to\b", r"\blet me know\b", r"\bi hope\b", r"\bfeel free\b",
]

SUMMARY_MARKERS = re.compile(
    r"\b(?:ultimately|overall|in short|in essence|"
    r"this (?:shows|highlights|demonstrates|underscores|ensures|means|reflects)|"
    r"which (?:highlights|underscores|shows|demonstrates|reflects)|"
    r"(?:highlights|underscores|demonstrates) (?:the|its|their)|"
    r"(?:important|significan(?:t|ce)|crucial|vital|essential)\b)",
    re.I,
)

ING_TAIL = re.compile(
    r",\s+(?:\w+ly\s+)?(?:highlighting|underscoring|emphasi[sz]ing|ensuring|"
    r"showcasing|reflecting|contributing|fostering|enabling|allowing|"
    r"demonstrating|illustrating|reinforcing|cementing|solidifying|paving|"
    r"positioning|setting the stage|making it (?:easier|possible|simple))\b",
    re.I,
)

CONTRAST_PATTERNS = [
    re.compile(r"\bnot (?:only|just|merely|simply)\b[^.?!\n]{0,90}?\b(?:but|it'?s|it is)\b", re.I),
    re.compile(r"\b(?:it'?s|it is|this is|that'?s|this isn'?t|it isn'?t|isn'?t) (?:not )?(?:just |only |merely )?(?:about )?[^.?!\n]{1,60}[,;:—–-]\s*(?:it'?s|it is|but|rather)\b", re.I),
    re.compile(r"\bnot (?:a|an|about|just)\b[^.?!\n]*[.?!]\s+(?:It'?s|It is|This is|That'?s|Instead)\b", re.I),
    re.compile(r"\b(?:no|not) [^.?!\n]{1,30}[.]\s+(?:No|Not) [^.?!\n]{1,30}[.]\s+(?:Just|No|Not)\b"),
]

TRIPLET = re.compile(
    r"\b(?:[A-Za-z'-]+(?: [A-Za-z'-]+){0,2}), (?:[A-Za-z'-]+(?: [A-Za-z'-]+){0,2}),? (?:and|or) (?:[A-Za-z'-]+(?: [A-Za-z'-]+){0,2})\b"
)

STOCK_NAMES = re.compile(r"\b(?:Sarah|Emily|Jessica|Michael|Chen|Dr\.|Prof\.|Professor)\b")

SPEECH_ALT = re.compile(
    r"\b(?:notes|explains|emphasi[sz]es|highlights|remarks|asserts|points out|observes|underscores|stresses)\b", re.I
)
SPEECH_PLAIN = re.compile(r"\b(?:says|said)\b", re.I)

CHAT_LEFTOVERS = re.compile(
    r"(?:^|\n)\s*(?:certainly|sure|absolutely|of course)[!,.]|"
    r"(?:^|\n)\s*here(?:'s| is) (?:a|an|the|your)\b|"
    r"\bi hope this (?:helps|finds)|\blet me know if\b|\bwould you like me to\b|"
    r"\bas an ai\b|\bfeel free to\b|\[[A-Z][A-Za-z ]{2,25}\]",
    re.I,
)

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]"
)

PERSONA_PATTERNS = [
    r"\bI'?d rather\b[^.?!\n]{0,70}\bthan\b",
    r"\brather (?:say|be|tell|admit)\b",
    r"\bperfect (?:launch|time|moment|product|version)\b",
    r"\bprogress over perfection\b",
    r"\bI'?m (?:so |really |incredibly |truly |beyond |super )?(?:excited|thrilled|humbled|proud|grateful|passionate|stoked)\b",
    r"\b(?:excited|thrilled|proud|happy|delighted) to (?:share|announce|introduce|say|finally)\b",
    r"\bstay tuned\b", r"\bmore to come\b", r"\bwatch this space\b", r"\bbig things\b",
    r"\bexciting (?:updates|things|news|features|times)\b",
    r"\bthe truth is\b", r"\bhere'?s the (?:thing|truth|reality)\b",
    r"\blet'?s be (?:real|honest)\b", r"\bnot gonna lie\b", r"\bbuckle up\b",
    r"\bno fluff\b", r"\bnothing fancy\b", r"\bjust getting started\b",
    r"\bone (?:step|commit|line of code|feature) at a time\b",
    r"\bI believe (?:in|that)\b", r"\bI truly\b",
    r"\bgame[- ]?chang\w*\b",
    r"\bbuilding something\b", r"\bsomething (?:special|big|great|amazing)\b",
]

VAGUE_PLACEHOLDERS = [
    r"\ba lot\b", r"\blots? of\b", r"\btons of\b", r"\bplenty (?:of|more)\b",
    r"\bso much (?:more|to)\b", r"\bmuch more\b", r"\bmany (?:things|features|more)\b",
    r"\bvarious\b", r"\bnumerous\b", r"\ba number of\b", r"\bseveral (?:things|features|more)\b",
    r"\band more\b", r"\band so much more\b", r"\bsome (?:exciting|new|cool)\b",
]

ENGAGEMENT_BAIT = [
    r"\bwhat do you think\b", r"\bwhat'?s your (?:take|experience|favorite|thoughts?)\b",
    r"\bthoughts\?", r"\bagree\?", r"\bdrop a comment\b", r"\blet me know (?:in the comments|what you think|your thoughts)\b",
    r"\bfollow (?:along|for more|me)\b", r"\blink in bio\b", r"\btag (?:a|someone)\b",
    r"\bwould love to hear\b", r"\bI'?d love to hear\b", r"\bshare (?:this|your)\b.*\b(?:with|below)\b",
    r"\bsmash\b.*\blike\b", r"\bcomment below\b",
]

STOPWORDS = set("""
a about above after again all also am an and any are as at be because been before being below between both
but by can could did do does doing down during each few for from further had has have having he her here hers
him his how i if in into is it its itself just let like me more most my myself no nor not now of off on once
only or other our ours out over own same she should so some such than that the their them then there these
they this those through to too under until up us very was we were what when where which while who whom why
will with would you your yours yourself it's i'm i'll i've i'd you're we're we'll we've that's there's here's
what's don't doesn't didn't isn't aren't won't can't couldn't wouldn't shouldn't one get got make made going
go goes still next thing things way really right even much many every
""".split())

# ------------------------------------------------------------------ helpers


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_markdown(text):
    t = re.sub(r"```.*?```", " ", text, flags=re.S)
    t = re.sub(r"^\s{0,3}#{1,6}\s+", "", t, flags=re.M)
    t = re.sub(r"^\s*(?:[-*+•]|\d+[.)])\s+", "", t, flags=re.M)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"__(.+?)__", r"\1", t)
    t = re.sub(r"(?<!\w)[*_](.+?)[*_](?!\w)", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t


def drop_noise_lines(text):
    """Remove hashtag-only and URL/domain-only lines so they don't count as sentences."""
    keep = []
    for line in text.split("\n"):
        st = line.strip()
        if re.fullmatch(r"(?:#\w+\s*)+", st):
            continue
        if re.fullmatch(r"(?:https?://\S+|(?:www\.)?[\w-]+(?:\.[\w-]+)+(?:/\S*)?)", st):
            continue
        keep.append(line)
    return "\n".join(keep)


def stem(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"'s$", "", w)
    for suf in ("ingly", "ing", "edly", "ed", "ly", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def content_stems(text):
    out = []
    for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", text):
        lw = w.lower().replace("’", "'")
        if lw in STOPWORDS or len(lw) < 3:
            continue
        out.append(stem(lw))
    return out


def ungrounded_sentences(sentences, source_text):
    """Sentences whose content words never appear in the user's own material."""
    vocab = set(content_stems(source_text))
    # allow compound/domain tokens in source to ground their parts
    vocab |= {stem(x) for x in re.findall(r"[A-Za-z]{3,}", source_text.lower())}
    found = []
    for s_ in sentences:
        cs = content_stems(s_)
        if len(cs) < 2:
            continue
        overlap = [c for c in cs if c in vocab]
        ratio = len(overlap) / len(cs)
        # mostly new words (or all new): the sentence is not carrying the user's facts
        if not overlap or (len(cs) >= 3 and ratio < 0.34):
            novel = sorted({c for c in cs if c not in vocab})
            found.append((s_, novel))
    return found


def split_paragraphs(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return paras


def split_sentences(text):
    flat = re.sub(r"\s+", " ", text).strip()
    if not flat:
        return []
    # protect common abbreviations
    protected = re.sub(
        r"\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|e\.g|i\.e|No|Inc|Ltd|Co)\.",
        lambda m: m.group(0).replace(".", "<DOT>"),
        flat,
    )
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])", protected)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def words(text):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text)


def snippet(text, start, width=70):
    s = max(0, start - 20)
    e = min(len(text), start + width)
    return ("…" if s else "") + re.sub(r"\s+", " ", text[s:e]).strip() + ("…" if e < len(text) else "")


def per_k(count, n_words):
    return round(1000.0 * count / n_words, 1) if n_words else 0.0


# ------------------------------------------------------------------- audit


def audit(raw, source_text=""):
    flags = []  # (severity, message)
    report = {}

    body = strip_markdown(drop_noise_lines(raw))
    n_words = len(words(body))
    paras = split_paragraphs(body)
    sents = split_sentences(body)
    lens = [len(words(s)) for s in sents if words(s)]
    report["words"] = n_words
    report["sentences"] = len(lens)
    report["paragraphs"] = len(paras)

    # --- rhythm
    rhythm = {}
    if len(lens) >= 8:
        mean = statistics.mean(lens)
        sd = statistics.pstdev(lens)
        cv = sd / mean if mean else 0
        band = sum(1 for L in lens if abs(L - mean) <= 0.25 * mean) / len(lens)
        rhythm = {
            "mean_len": round(mean, 1),
            "sd": round(sd, 1),
            "cv": round(cv, 2),
            "share_within_25pct_of_mean": round(band, 2),
            "shortest": min(lens),
            "longest": max(lens),
            "sentences_5_words_or_fewer": sum(1 for L in lens if L <= 5),
            "sentences_30_words_or_more": sum(1 for L in lens if L >= 30),
        }
        if cv < 0.45:
            flags.append(("high", f"Sentence rhythm is flat (variation {cv:.2f}; roughly 0.5-0.8 is typical of varied prose)."))
        elif cv < 0.55:
            flags.append(("low", f"Sentence rhythm is a bit even (variation {cv:.2f})."))
        if band > 0.5:
            flags.append(("med", f"{band:.0%} of sentences sit within 25% of the average length."))
        if mean > 24:
            flags.append(("low", f"Average sentence is long ({mean:.0f} words). Break a few up."))
        if rhythm["sentences_5_words_or_fewer"] == 0 and n_words > 250:
            flags.append(("low", "No very short sentences. A fragment or a five-word sentence somewhere would be natural."))
    else:
        rhythm = {"note": "fewer than 8 sentences; rhythm stats skipped"}
    report["rhythm"] = rhythm

    if len(paras) >= 4:
        plens = [len(words(p)) for p in paras]
        pcv = statistics.pstdev(plens) / statistics.mean(plens) if statistics.mean(plens) else 0
        report["paragraph_length_variation"] = round(pcv, 2)
        if pcv < 0.2:
            flags.append(("med", f"Paragraphs are all about the same size (variation {pcv:.2f}). Let one be a line, let one run."))
        elif pcv < 0.3:
            flags.append(("low", f"Paragraphs are fairly uniform in size (variation {pcv:.2f})."))

    # --- punctuation
    em = raw.count("—") + raw.count(" -- ")
    semi = raw.count(";")
    colon = len(re.findall(r":\s", body))
    punct = {"em_dashes": em, "per_1000_words": per_k(em, n_words), "semicolons": semi, "colons": colon}
    report["punctuation"] = punct
    if em >= 2 and per_k(em, n_words) > 3:
        flags.append(("high", f"{em} em dashes ({per_k(em, n_words)} per 1000 words). Use commas, periods, or parentheses."))
    elif em >= 1 and n_words < 150:
        flags.append(("low", "Em dash in a very short piece."))
    if semi >= 3 and per_k(semi, n_words) > 3:
        flags.append(("low", f"{semi} semicolons; check they earn their place."))

    # --- stock words
    word_hits = {}
    lower = body.lower()
    for w in STOCK_WORDS:
        c = len(re.findall(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", lower))
        if c:
            word_hits[w] = c
    total_wh = sum(word_hits.values())
    report["stock_words"] = {"hits": word_hits, "per_1000_words": per_k(total_wh, n_words)}
    if total_wh:
        sev = "high" if per_k(total_wh, n_words) > 6 or total_wh >= 5 else "med" if total_wh >= 2 else "low"
        flags.append((sev, "Stock words: " + ", ".join(f"{w}×{c}" if c > 1 else w for w, c in word_hits.items()) + ". Ask what the sentence really claims."))

    # --- stock phrases
    phrase_hits = []
    for pat in STOCK_PHRASES:
        for m in re.finditer(pat, body, flags=re.I):
            phrase_hits.append(snippet(body, m.start()))
    report["stock_phrases"] = phrase_hits
    if phrase_hits:
        sev = "high" if len(phrase_hits) >= 3 else "med"
        flags.append((sev, f"{len(phrase_hits)} stock phrase(s): " + " | ".join(phrase_hits[:4])))

    # --- transition openers
    trans = []
    for s in sents:
        sl = s.lower().lstrip("\"'(")
        for t in TRANSITION_OPENERS:
            if sl.startswith(t):
                trans.append(s[:60])
                break
    report["transition_openers"] = trans
    if len(trans) >= 2 or (trans and n_words < 300):
        flags.append(("med", f"{len(trans)} sentence(s) open with a transition crutch: " + " | ".join(trans[:4])))
    elif trans:
        flags.append(("low", "One transition-crutch opener: " + trans[0]))

    # --- contrast framing
    contrasts = []
    for pat in CONTRAST_PATTERNS:
        for m in pat.finditer(body):
            contrasts.append(snippet(body, m.start(), 90))
    seen, uniq = set(), []
    for c in contrasts:
        k = c[:40]
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    report["contrast_framing"] = uniq
    if len(uniq) >= 2:
        flags.append(("high", f"{len(uniq)} 'not X, it's Y' style constructions: " + " | ".join(uniq[:3])))
    elif uniq:
        flags.append(("low", "One 'not X, it's Y' construction: " + uniq[0]))

    # --- triplets
    trips = [snippet(body, m.start(), 60) for m in TRIPLET.finditer(body)]
    report["triplets"] = {"count": len(trips), "per_1000_words": per_k(len(trips), n_words)}
    if len(trips) >= 3 and per_k(len(trips), n_words) > 5:
        flags.append(("med", f"{len(trips)} three-item lists ({per_k(len(trips), n_words)} per 1000 words). Are there really three each time? " + " | ".join(trips[:3])))

    # --- -ing tails
    tails = [snippet(body, m.start(), 70) for m in ING_TAIL.finditer(body)]
    report["ing_tails"] = tails
    if len(tails) >= 2:
        flags.append(("high", f"{len(tails)} '-ing' significance tails: " + " | ".join(tails[:3])))
    elif tails:
        flags.append(("low", "One '-ing' significance tail: " + tails[0]))

    # --- paragraph-end summaries
    summ = []
    for p in paras:
        ps = split_sentences(p)
        if len(ps) >= 3 and SUMMARY_MARKERS.search(ps[-1]):
            summ.append(ps[-1][:90])
    report["paragraph_end_summaries"] = summ
    if len(summ) >= 2:
        flags.append(("med", f"{len(summ)} paragraphs end on a significance or summary sentence: " + " | ".join(summ[:3])))

    # --- opener / closer
    first = sents[0].lower() if sents else ""
    opener_hit = any(re.search(p, first) for p in OPENER_CLICHES)
    last_para = paras[-1].lower() if paras else ""
    closer_hit = [p for p in CLOSER_MARKERS if re.search(p, last_para)]
    report["opener_cliche"] = opener_hit
    report["closer_markers"] = closer_hit
    if opener_hit:
        flags.append(("high", "Opens with a stock opener. Start with the point."))
    if closer_hit and len(paras) >= 3:
        flags.append(("med", "Final paragraph has summary/uplift markers. End on the last real point."))

    # --- speech verbs
    alt = len(SPEECH_ALT.findall(body))
    plain = len(SPEECH_PLAIN.findall(body))
    report["speech_verbs"] = {"plain_says_said": plain, "descriptive_alternatives": alt}
    if alt >= 3 and alt > plain * 2:
        flags.append(("low", f"Speech verbs rotate ({alt} descriptive vs {plain} says/said). People mostly repeat 'says'."))

    # --- stock names
    names = sorted(set(STOCK_NAMES.findall(body)))
    report["stock_names"] = names
    if names:
        flags.append(("low", "Default names/titles present: " + ", ".join(names) + ". Use the user's real names or drop the example."))

    # --- chat leftovers
    left = [snippet(raw, m.start(), 60) for m in CHAT_LEFTOVERS.finditer(raw)]
    report["chat_leftovers"] = left
    if left:
        flags.append(("high", "Text addressed to the user or placeholder left in: " + " | ".join(left[:3])))

    # --- formatting
    bullets = len(re.findall(r"^\s*(?:[-*+•]|\d+[.)])\s+", raw, flags=re.M))
    bold_spans = len(re.findall(r"\*\*[^*\n]+\*\*", raw))
    bold_lead = len(re.findall(r"^\s*(?:[-*+•]|\d+[.)])\s+\*\*[^*\n]+?(?::\*\*|\*\*\s*[:\-–—])", raw, flags=re.M))
    headers = re.findall(r"^\s{0,3}#{1,6}\s+(.+)$", raw, flags=re.M)
    title_case = 0
    for h in headers:
        ws = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", h) if len(w) > 3]
        if len(ws) >= 3 and sum(1 for w in ws if w[0].isupper()) / len(ws) >= 0.75:
            title_case += 1
    emojis = len(EMOJI.findall(raw))
    curly = len(re.findall(r"[\u2018\u2019\u201c\u201d]", raw))
    straight = len(re.findall(r"[\"']", raw))
    fmt = {
        "bullets": bullets, "bold_spans": bold_spans, "bold_lead_in_bullets": bold_lead,
        "headers": len(headers), "title_case_headers": title_case,
        "emojis": emojis, "curly_quotes": curly, "straight_quotes": straight,
    }
    report["formatting"] = fmt
    if bold_lead:
        flags.append(("high", f"{bold_lead} bullet(s) with a bold lead-in. Write sentences."))
    if bullets >= 4 and n_words < 400:
        flags.append(("med", f"{bullets} bullets in a short piece. Prose is usually better."))
    if bold_spans >= 3:
        flags.append(("med", f"{bold_spans} bolded phrases. Remove most or all."))
    if headers and n_words < 500:
        flags.append(("low", "Headers in a short piece."))
    if title_case:
        flags.append(("low", f"{title_case} Title Case header(s). Use sentence case."))
    if emojis:
        flags.append(("med", f"{emojis} emoji."))
    if curly and straight:
        flags.append(("low", "Mixed curly and straight quotes."))
    elif curly:
        flags.append(("low", "Curly quotes present; use straight quotes if this is going into plain text."))

    # --- invented voice / persona lines
    persona, last_pos = [], []
    hits = sorted((m.start(), pat) for pat in PERSONA_PATTERNS for m in re.finditer(pat, body, flags=re.I))
    for pos, _pat in hits:
        if any(abs(pos - q) < 70 for q in last_pos):
            continue
        last_pos.append(pos)
        persona.append(snippet(body, pos, 80))
    report["persona_lines"] = persona
    if persona:
        sev = "high" if (n_words < 150 or len(persona) >= 2) else "med"
        flags.append((sev, f"{len(persona)} persona/hype line(s). Did the user actually say this? " + " | ".join(persona[:3])))

    vague = []
    for pat in VAGUE_PLACEHOLDERS:
        for m in re.finditer(pat, body, flags=re.I):
            vague.append(snippet(body, m.start(), 50))
    report["vague_placeholders"] = vague
    if vague:
        flags.append(("high" if n_words < 150 else "med", f"{len(vague)} vague placeholder(s). Name the real thing or cut it: " + " | ".join(vague[:3])))

    bait = []
    for pat in ENGAGEMENT_BAIT:
        for m in re.finditer(pat, body, flags=re.I):
            bait.append(snippet(body, m.start(), 60))
    report["engagement_bait"] = bait
    if bait:
        flags.append(("med", f"{len(bait)} engagement-bait phrase(s): " + " | ".join(bait[:3]) + ". Only keep if the user asked for a call to action."))

    hashtags = re.findall(r"(?<!\w)#[A-Za-z]\w+", raw)
    report["hashtags"] = len(hashtags)
    if len(hashtags) > 10:
        flags.append(("med", f"{len(hashtags)} hashtags. Large hashtag blocks are a machine habit; 3 to 5 is typical."))
    elif len(hashtags) > 6:
        flags.append(("low", f"{len(hashtags)} hashtags; consider trimming."))

    emoji_lines = len(re.findall(r"^\s*(?:" + EMOJI.pattern + r")", raw, flags=re.M))
    report["emoji_led_lines"] = emoji_lines
    if emoji_lines >= 2:
        flags.append(("med", f"{emoji_lines} lines start with an emoji."))

    if len(paras) >= 6:
        one_liners = sum(1 for p in paras if len(split_sentences(p)) == 1)
        share = one_liners / len(paras)
        report["one_sentence_paragraph_share"] = round(share, 2)
        if share >= 0.7:
            flags.append(("med", f"{share:.0%} of paragraphs are a single sentence (the stacked one-liner look). Merge some."))

    # --- grounding against the user's own material
    if source_text.strip():
        pool = [x for x in sents if not re.fullmatch(r"[#\s\w-]*", x) or len(x.split()) > 2]
        ung = ungrounded_sentences(pool, source_text)
        report["ungrounded_sentences"] = [{"sentence": a, "novel_words": b} for a, b in ung]
        for a, b in ung:
            sev = "high" if n_words < 150 else "med"
            flags.append((sev, f"Not in the user's material: \"{a[:110]}\" (new words: {', '.join(b[:6])}). Is this a fact they gave you, or something you made up to sound human? Cut it or replace it with a real detail."))
    else:
        report["ungrounded_sentences"] = None
        if n_words < 200:
            flags.append(("low", "No --source given. For short posts the grounding check is the best test here: run again with --source material.txt."))

    # --- contractions (info only)
    contr = len(re.findall(r"\b\w+(?:'|’)(?:s|t|re|ve|ll|d|m)\b", body))
    report["contractions"] = contr

    report["flags"] = [{"severity": s, "message": m} for s, m in flags]
    return report


def print_report(r):
    print(f"Words {r['words']} · sentences {r['sentences']} · paragraphs {r['paragraphs']}")
    rh = r["rhythm"]
    if "cv" in rh:
        print(
            f"Rhythm: mean {rh['mean_len']} words, variation {rh['cv']}, "
            f"{int(rh['share_within_25pct_of_mean'] * 100)}% near the mean, "
            f"shortest {rh['shortest']}, longest {rh['longest']}"
        )
    else:
        print("Rhythm: " + rh.get("note", ""))
    print(f"Em dashes {r['punctuation']['em_dashes']} · contractions {r['contractions']}")
    if r["words"] < 100:
        print("Short text: rhythm stats don't apply. Grounding, persona lines and vague placeholders are the checks that matter.")
    print()
    order = {"high": 0, "med": 1, "low": 2}
    fl = sorted(r["flags"], key=lambda f: order[f["severity"]])
    if not fl:
        print("No flags. (That is not a guarantee. Read it aloud once.)")
        return
    label = {"high": "LOOK AT", "med": "CHECK", "low": "MINOR"}
    for f in fl:
        print(f"[{label[f['severity']]}] {f['message']}")
    print()
    n_high = sum(1 for f in fl if f["severity"] == "high")
    print(f"{len(fl)} flag(s), {n_high} high. Fix by rewriting the idea, not by swapping the word. One revision pass, then stop.")


def main():
    ap = argparse.ArgumentParser(description="Surface-pattern audit for prose drafts.")
    ap.add_argument("path", help="text file, or - for stdin")
    ap.add_argument("--json", action="store_true", help="print full report as JSON")
    ap.add_argument("--source", action="append", default=[], help="file with the user's own material (repeatable)")
    args = ap.parse_args()
    text = read_text(args.path)
    if not text.strip():
        print("Empty input.")
        return
    source_text = "\n".join(read_text(p) for p in args.source)
    r = audit(text, source_text)
    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print_report(r)


if __name__ == "__main__":
    main()
