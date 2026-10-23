---
name: human-writing
description: Write or rewrite prose so it reads like a specific person wrote it, not a language model. Use this skill whenever the user asks Claude to write, draft, rewrite, edit, or polish text that a person will send, post, publish, or submit (emails, essays, articles, blog posts, social media posts for Instagram, Facebook, LinkedIn or Hashnode, bios, cover letters, captions, messages, speeches, product copy, reports), and especially when they say "make it sound human", "less AI", "humanize this", "sound natural", "don't sound like ChatGPT", "pass AI detection", or paste a draft that reads stiff, padded, or machine-made. Also use it when the user wants their own writing voice matched. Skip it for code, data files, translations that must stay literal, and casual chat replies.
---

# Human writing

The goal is prose that sounds like one particular person with something to say. That is also what makes text hard to flag. AI detectors, and the human editors who spot machine text, are reacting to the same thing: writing that is generic in content and default in structure. So the fix happens before and during drafting, not in a cosmetic pass afterward.

Read `references/ai-tells.md` once per session before your first draft. It lists the specific words, constructions, and formatting habits to avoid, and why. If the piece is for a platform (Instagram, Facebook, LinkedIn, Hashnode or another blog), also read `references/platforms.md`. Read `references/case-studies.md` when a draft keeps getting flagged. Read `references/detectors.md` only if the user asks how detection works or whether this will beat a given detector.

## What this skill can and can't promise

No writing method guarantees a detector score. Detectors are probabilistic, disagree with each other, and get updated. What this skill does is remove the real signals they measure (uniform rhythm, predictable word choice, stock phrases, templated structure) and, more importantly, put real specifics into the text. If the user asks for a guarantee, say that plainly in one sentence and move on.

## Workflow

### 1. Get the raw material

Human writing is specific, and specifics come from the user. Before drafting, check what you have: who it's for, what it's for, the user's actual facts, opinions, names, numbers, examples, and ideally a sample of their own writing.

If the material is thin and the piece needs more, ask for two or three concrete details in one short message. If you can reasonably write without them, write, and note at the end in one line what a real detail would improve.

If the user links a document, read it. Facts from their own docs (stack, numbers, steps, names) are the best source of specifics, far better than anything you could add.

Save everything the user told you, plus any doc contents you fetched, into a file such as `material.txt`. Step 5 checks the draft against it.

Never invent the user's personal experiences, credentials, quotes, statistics, or named sources to add texture. Fake specifics are worse than generic ones. Texture comes from precise wording of what is true, plus the user's own details.

### 2. Decide the point

Before writing, settle in one sentence what the piece is actually saying and what stance it takes. Most machine-sounding text is a topic with no position: it surveys, balances, and hedges. Pick the position the material supports and write from it. Mention the counterargument only if a real reader would raise it.

### 3. Match the person and the register

If the user gave a writing sample, copy its habits: sentence length, contractions, punctuation, how it opens and closes, how formal it is. Match their variety of English too (British, American, Indian, Australian spelling and idiom). Defaulting to US English when the user writes otherwise is a tell.

With no sample, write the way a thoughtful person speaks to the intended reader. A cover letter is plainer than a blog post, which is plainer than an academic essay, but none of them should sound like a brochure.

### 4. Draft in one pass

Two tests apply to every sentence. They matter more than any word list, because the most recognizable machine text is not a bad word, it is a sentence the model produced out of nothing.

**The information test.** Name the fact from the user's material that this sentence carries. If you can't, cut it. This removes invented stance and feeling ("I'd rather say that than wait for a perfect launch"), humility and virtue lines, hype, motives the user never stated, and vague placeholders ("still to do: a lot"). A model adds these to sound human; they are the exact lines detectors and readers pick up. If a sentence does carry a fact, fine. If it only comments on the facts, it goes.

**The default-completion test.** Imagine a generic model given this request with none of the user's material. Would this sentence plausibly appear in its answer? If yes, it matches what detectors have seen thousands of times, and many tools are trained on or compared against exactly that kind of output. Cut it, or replace it with something only this person's material could produce (a real stack, number, step, name).

**Short posts: write less.** For anything under about 100 words (an Instagram caption, a short Facebook post, a tweet), every extra sentence is extra surface to be flagged. Facts, one line on what comes next, the link. No hook, no stance, no reflection, no call to engage, no closing slogan. A short post made only of facts the user gave has almost nothing for a detector to latch onto. Concrete labels like "What's done:" and "Next:" are fine; people write that way.

Then draft in one pass, using these habits:

**Say the specific thing.** Name the object, the number, the place, the person. Replace "a significant impact on the industry" with what happened. If you can't say what happened, cut the sentence.

**State facts; don't narrate their importance.** Don't tell the reader something "highlights", "underscores", "serves as a testament", or "reflects broader trends". If the fact matters, the reader sees it. Don't tack an "-ing" clause on the end of a sentence to add significance ("..., ensuring a seamless experience").

**Let the rhythm be uneven for real reasons.** Some sentences are three words. Some run long because the thought has a turn in it, with an aside or a second clause. Don't alternate short and long on a schedule; that is its own pattern. Paragraphs vary too: one line is fine, so is a fat one. Starting a sentence with "And" or "But" is fine. Fragments are fine when they land.

**Use plain words and repeat them.** Write "said" five times if five people spoke. Don't rotate synonyms to avoid repetition ("the protagonist", "the central figure", "the lead"). Choose the ordinary word over the impressive one.

**Don't reach for threes or contrasts by reflex.** One example, two, or four is fine. "Not just X, but Y" and "It's not X, it's Y" are rare tools, not defaults. Lists should have as many items as there actually are.

**Start with the thing.** No scene-setting opener, no restating the prompt, no "In today's fast-paced world", no announcing what the piece will cover.

**Stop when you're done.** No closing summary, no "Overall" or "In conclusion", no uplifting last line about the future, no offer to help further. End on the last real point.

**No disclaimers or filler.** Cut "it's important to note", "it's worth mentioning", "may vary", and vague authorities ("experts say", "studies show") unless you name the source and the user supplied it.

**Keep punctuation ordinary.** Periods and commas do most of the work. Em dashes are rare (none is fine). Colons and semicolons are occasional. Use straight quotes and apostrophes. Use parentheses for a real aside.

**Write prose.** No bullets, bold lead-ins, headers, or emojis unless the format needs them (a recipe, a README, a slide). In longer pieces that do need headers, use sentence case, not Title Case.

**Let informality come from the voice, not from sprinkles.** Contractions are right when the person would use them. Don't scatter "honestly", "just", "actually", or slang as costume. Uniformly casual text is as detectable as uniformly formal text.

**Don't fake mistakes.** No planted typos or broken grammar. Natural looseness that matches the person's voice is fine; manufactured errors are not.

**Avoid stock names and examples.** Machine text over-uses certain first names (Sarah, Emily), stock personas, and academic titles ("Dr.", "Prof.") on every person. Use the user's real names or leave the example out.

### 5. Audit once, then fix the ideas

Save the draft to a file and run:

```bash
python3 scripts/audit.py draft.txt --source material.txt
```

(Path is relative to this skill's folder.) The `--source` flag is the important one: it lists every sentence whose content words appear nowhere in the user's material, which is how invented stance and filler get caught. The rest of the report covers sentence-length variation, stock phrases, persona and hype lines, vague placeholders, engagement bait, em dash and triplet density, "-ing" tails, contrast constructions, paragraph-end summaries, formatting habits, and stock names. Thresholds are rough heuristics from this skill's author, not detector scores. Use the report to find what to look at.

A grounding flag on a sentence that only rephrases a fact the user gave you (for example, "finished" where they wrote "complete") is fine. A flag on a feeling, a motive, a claim, or a commitment the user never made is not. Fix those, including small drifts like turning "I'll post" into "I'll write about".

Delete before you reword. If a flagged sentence doesn't carry a fact, remove it. Rewording an empty sentence keeps the emptiness. Otherwise fix flagged spots by rewriting the idea, not swapping the word. Replacing "crucial" with "essential" in a sentence that only exists to say something is important leaves the problem untouched. Cut the sentence or replace it with a fact.

Do one revision pass, then stop. Repeated rounds of "make it more human" add new machine habits and flatten the voice. If the audit is still noisy after one pass, the usual cause is missing material (step 1), not missing polish.

### 6. Deliver

Give the text. No "Here's a more natural version" and no explanation of what you changed unless asked. If a real detail was missing and would help, add one short line after the piece saying which.

## When the user reports detector results

Ask which sentences or sections the tool highlighted, and which tool, if it shows them. Check those against the two tests first. Fix by deleting, then by replacing with a real detail from the material. Change one thing at a time so you can tell what worked. A real example is in `references/case-studies.md`: two deleted lines took a post from flagged at 70 to 100 percent to read as human. Don't claim a draft will pass; say what you changed and why, and ask them to rerun it.

## Rewriting text the user already has

When the user pastes AI-sounding text, don't paraphrase it sentence by sentence. Paraphrase keeps the skeleton, and the skeleton (order, paragraph shapes, the intro-three-points-conclusion template) is much of what gets caught. Instead:

1. List the actual claims and facts in the text, in your own notes.
2. Drop anything that was only filler: significance statements, restated points, hedges, the summary.
3. Rebuild from the list with a new order that serves the reader, in the user's register.
4. Check every claim in the original survived and nothing new was added.

Expect the result to be shorter, often by a quarter to a half.

## One announcement, several platforms

Write each version from the facts, not by adapting a master draft. Four versions with the same skeleton and shared phrases are a pattern in themselves. Each platform gets its own shape and its own selection of facts (see `references/platforms.md`).

## Things not to do

Don't use invisible characters, look-alike Unicode letters, random typos, or synonym-spinner tricks. They damage the text for real readers, trained detectors learn them quickly, and none of it is writing. If the text is specific, plainly worded, and has a point of view, you don't need them.

## Examples

**Generic (avoid):**
"Our new coffee subscription offers a seamless way to enjoy freshly roasted beans, ensuring you never run out. Whether you're a casual drinker or a dedicated enthusiast, there's something for everyone."

**Specific (aim for):**
"We roast on Tuesdays and ship Wednesday, so the bag on your counter is usually less than a week off the roaster. Pick a size, pick how often. Skip a month from your account whenever you like."

**Padded opener (avoid):**
"In today's competitive job market, having a strong network is more important than ever. In this post, we'll explore three key strategies."

**Starts with the thing (aim for):**
"Most of my jobs came from people I'd already worked with, not from applications. Here's what I did to keep those people around."
