# AI tells: what to avoid and why

Contents: 1. Why these patterns exist · 2. Content-level tells (including invented voice) · 3. Sentence and structure tells · 4. Vocabulary · 5. Punctuation and formatting · 6. Chat leftovers · 7. Things that look like tells but aren't

## 1. Why these patterns exist

Language models pick likely next words, so their output drifts toward the most common, most widely applicable phrasing. Specific facts are statistically rare; generic praise and framing are statistically common. The result is text that gets vaguer and more inflated at the same time. Models are also tuned to sound helpful, balanced, and authoritative, which produces hedging, summarizing, and "importance" language. And they penalize repetition, which produces synonym rotation.

Every tell below traces back to one of those. That's why swapping a flagged word for a near-synonym doesn't help: the habit behind it is still there. Fix the habit.

A word list is a smoke alarm, not a cause. A human can use any single item here without trouble. The signal is density and co-occurrence: many of them together, in a piece with no specifics.

## 2. Content-level tells (the strongest)

- **Significance inflation.** Stating that something is important, pivotal, or part of a broader trend instead of saying what it did. Typical shapes: "plays a vital role", "a testament to", "marks a turning point", "reflects the broader shift toward", "leaves a lasting legacy". Replace with the concrete event, number, or consequence, or delete.
- **Superficial analysis tails.** A participle clause bolted on to add meaning: "..., highlighting its importance", "..., ensuring a smooth process", "..., showcasing the team's commitment", "..., contributing to the broader ecosystem". Inanimate things can't highlight or underscore. Cut the clause or write a real sentence about the effect.
- **Promotional tone.** Brochure language for anything with a cultural or commercial angle: "nestled in the heart of", "boasts", "vibrant", "rich tapestry", "stunning", "continues to captivate". Write like a neutral person describing a place or product to a friend.
- **Vague attribution.** "Experts agree", "studies show", "critics argue", "industry reports suggest". Either name the source the user gave you or state the claim as your own.
- **No position.** The piece lists considerations and balances them without choosing. Pick the stance the material supports.
- **Challenges-and-outlook formula.** A late paragraph beginning "Despite its X, Y faces challenges..." and ending with a hopeful forward look. Real pieces end when the points end.
- **Disclaimers aimed at an imagined reader.** "It's important to note", "it's worth remembering", "results may vary", "always consult...", unless the caution is real and specific to this case.
- **Stock people and examples.** The same first names (Sarah, Emily, Michael), a generic "small business owner" or "busy professional", titles on everyone. Use real names from the user or drop the example.
- **Invented quotes that all sound alike.** Every speaker uses the same polished register and echoes the article's own phrasing. Don't invent quotes at all. If the user supplied real ones, keep their roughness.
- **Scene-setting openers.** "Imagine a world where...", "In today's fast-paced world...", "Picture this:". Start with the point.
- **Emotional uplift at the end.** The closing paragraph about hope, journeys, unlocking potential, or what the future holds.

### The category that caught a real post: invented voice

These sentences carry no fact. A model adds them to sound candid, humble, or personable, which is why they stand out most in short text.

- **Invented candor or stance.** "I'd rather say that than wait for a perfect launch." "Honestly, it's been a ride." "I believe in building in the open." The user never said it. Cut it unless they did.
- **Humility and virtue lines.** "It's not perfect, and that's okay." "Progress over perfection." "Learning as I go."
- **Hype with no content.** "Exciting things coming." "Big updates ahead." "Stay tuned." "More to come."
- **Vague placeholders where a fact belongs.** "Still to do: a lot." "Many more features." "And so much more." Name the real next item or stop.
- **Engagement bait.** "What do you think?" "Thoughts?" "Drop a comment." "Follow along." Keep only when the user asked for a call to action.
- **Self-narration of the act of posting.** "Sharing this because...", "Wanted to give an update."

Test each one with the information test in SKILL.md: what fact does it carry?

## 3. Sentence and structure tells

- **Contrast framing.** "Not only X but also Y", "It's not X, it's Y", "This isn't about X. It's about Y." Fine once in a long piece, a tell when it recurs. Related: strings of negatives ("No fluff. No jargon. Just results.").
- **Rule of three.** Triplets of adjectives, nouns, or clauses for everything: "fast, reliable, and secure". Use the number of items that exist.
- **False ranges.** "From X to Y" where there is no real scale between X and Y ("from startups to sustainability to the future of work"). Just name the things.
- **Elegant variation.** Rotating synonyms for the same referent so no word repeats. People repeat the plain word.
- **Uniform sentence length.** Most sentences within a narrow band of length, with similar clause structure (subject, verb, object, trailing modifier). Real writing has stretches of short and long, and some sentences that are barely sentences.
- **Uniform paragraph shape.** Every paragraph: topic sentence, two support sentences, wrap-up sentence. Vary it. Let a paragraph be one line.
- **Paragraph-ending summaries.** The last sentence of a paragraph restates it or states why it matters. Delete it.
- **Intro-points-conclusion template.** Announce, deliver three points, summarize. Reorder around what the reader needs.
- **Transition crutches.** Sentences opening with "Additionally", "Furthermore", "Moreover", "Notably", "Importantly", "Ultimately", "Overall", "In conclusion", "That said", "With that in mind". If a transition is needed, usually "But", "So", "And", or nothing does it.
- **Over-long, over-complete sentences.** Several dependent clauses stacked, every sentence hedged and balanced. Break some up. Leave some rough.

## 4. Vocabulary

These words are over-represented in model output compared with pre-2022 human writing. Use as a check, not a ban. Expect the list to drift as models change (for instance, "delve" faded in 2025 while others rose).

Verbs: delve, underscore, highlight (figurative), showcase, foster, enhance, leverage, harness, streamline, navigate (figurative), unlock, elevate, empower, align with, garner, facilitate, embark, resonate, bolster.

Adjectives: crucial, pivotal, vital, key (as filler), robust, seamless, vibrant, intricate, multifaceted, nuanced, comprehensive, holistic, meticulous, dynamic, cutting-edge, groundbreaking, transformative, rich, profound, enduring, invaluable.

Nouns and fixed phrases: tapestry, landscape, realm, testament, beacon, journey, interplay, synergy, game-changer, paradigm, cornerstone, "in the realm of", "when it comes to", "a wide range of", "plays a role in", "at the end of the day", "it is worth noting".

Adverbs: notably, importantly, seamlessly, ultimately, significantly, meticulously.

When one of these shows up, ask what the sentence is really claiming. Usually the answer is a plain word or nothing.

## 5. Punctuation and formatting

- **Em dashes.** Models use them for emphasis and in place of commas, colons, and parentheses, far more than most writers. Use rarely. Zero in a piece is normal.
- **Colons and semicolons.** Over-used to set up reveals and balance clauses. Occasional is fine.
- **Curly quotes and apostrophes** mixed with straight ones. Use straight quotes consistently in plain-text output.
- **Hyphens where en dashes belong** in ranges (1990-2000 vs 1990–2000), a small inconsistency models show. Match what the user's own writing does.
- **Bold for emphasis scattered through paragraphs**, and bold key terms on every first mention.
- **Bullets with a bold lead-in and a colon** ("**Scalability:** The system can..."). The signature model list shape. Write a sentence instead.
- **Headers in short pieces**, and Title Case Headings. Use sentence case, and only for pieces long enough to need navigation.
- **Emoji** on headings or bullets.
- **Italicizing every title** or term.
- **Markdown in plain-text contexts** (asterisks, pound signs, backticks) where the user will paste into email or a document.

## 6. Chat leftovers

Remove any text that talks to the user rather than being the piece: "Certainly!", "Here's a...", "I hope this helps", "Let me know if you'd like...", "Would you like me to...", "As an AI...", bracketed placeholders like [Name], leftover "Subject:" lines when it's not an email, and statements about knowledge cutoffs or about what sources don't say.

## 7. Things that look like tells but aren't

Don't "fix" these; they cause false alarms and bad edits.

- **Perfect grammar.** Plenty of human writers, editors especially, write cleanly. Human text usually has more irregularity, but don't manufacture errors.
- **Neutral or formal tone.** Not a tell by itself. A tone matched to the occasion is correct.
- **Long or uncommon words.** Models over-use specific words, not rare words in general. A precise unusual word is more human than a stock one.
- **A single em dash, a single triplet, a single "However".** Density is the signal.
- **Contractions and slang as proof of humanity.** Readers who rely on informality get fooled both ways. Voice should be consistent with the person, not decorated.
- **Salutations and sign-offs in a real letter or email.** Those are genre conventions.
- **Plain colon labels** like "What's done:" and "Next:" in a short post, **hashtags** in the user's usual style, and **slightly informal phrasing** taken from the user's own notes. In a tested case these all survived in a version that read as human, while a persona sentence and a vague placeholder did not.
