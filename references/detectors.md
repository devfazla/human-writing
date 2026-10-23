# How detection works and what the evidence says

Read this only when the user asks how detectors work, whether this skill will beat a particular tool, or why a draft still gets flagged. It's background for giving honest answers, not a checklist for drafting.

## The three kinds of detector

1. **Perplexity and burstiness scoring.** A reference language model measures how predictable each word is (perplexity) and how much that predictability varies from sentence to sentence (burstiness). Machine text tends to be predictable and uniform. Early GPTZero and open-source tools like Binoculars and Fast-DetectGPT work this way. Rewording the text to be less predictable defeats them fairly easily.
2. **Trained classifiers.** A model trained on large sets of labeled human and AI text, which learns whatever separates them: vocabulary distributions, syntax, paragraph shape, punctuation habits. Pangram, current GPTZero, Turnitin, and Originality.ai are mostly this, often blended with the statistical signals. These are much harder to beat with surface edits because they learn the underlying patterns, and vendors retrain against known evasion tools.
3. **Human experts.** Not a product, but relevant: editors and heavy LLM users spot machine text well.

## What the research found

The most useful recent study is Russell, Karpinska and Iyyer (2025, ACL), which compared expert human readers with commercial and open-source detectors on 300 articles, including paraphrased and "humanized" machine text.

- Readers who use LLMs for writing every week or day were highly accurate. A majority vote of five misclassified 1 of 300 articles. Readers without that experience performed near chance, while feeling confident.
- Sentence-level paraphrasing badly hurt perplexity-based detectors (Binoculars and Fast-DetectGPT dropped sharply) but did not fool the expert readers.
- A prompt-based humanizer built from the experts' own list of tells hurt GPTZero and the open-source tools a lot (humanized text: GPTZero around 47% detected, Binoculars around 7%), while Pangram still caught about 90 to 97% and the expert majority caught all of it. This is a snapshot from early 2025 models and tools; expect it to have moved.
- The clues experts cited, by how often they mentioned them: vocabulary (53%), sentence structure (36%), grammar and punctuation (25%), originality (24%), unnatural quotes (22%), clarity and padding (20%).
- Lessons about humanizing: asking a model to "make it sound more human" after the fact worked like paraphrasing. Many rounds of step-by-step edits added more machine traits, not fewer. What worked best was generating the text in one pass with the tell-list in view, because many of the biggest tells come from the original generation, not from surface wording.
- Tells that survived even the best humanizer: titles on every named person, default first names, quotes always in the same position and format, descriptive speech verbs ("notes", "explains") where humans keep writing "says", and low originality.

## Detection by similarity to known model output

Krishna et al. (NeurIPS 2023) showed that a model provider who stores what its model generates can catch even heavily paraphrased text by retrieving semantically similar stored generations: 80 to 97 percent of paraphrases detected at about 1 percent false positives, in their experiments. This only works for the provider that holds the database, so a third-party detector generally can't do it. But classifiers trained on very large sets of model output learn a softer version of the same thing: text that is what a model would say by default for that kind of request looks familiar to them. That is why the default-completion test in SKILL.md matters. A sentence that any generic model would have written for the prompt is the easiest kind to match, however it's worded.

Which of a given user's detectors work this way isn't knowable from outside. Treat it as a reason to put the user's own facts in, not as a claim about a specific tool.

## Short text

Very short posts give detectors little to work with, and tools disagree widely on them. A short post made only of the user's concrete facts leaves the least to match. The reverse also holds: one or two generic "voice" sentences can dominate the verdict. See `case-studies.md` (case 1).

## Other commonly reported limits

These come from secondary sources and vendor explainers, so treat them as general tendencies:

- Detectors output probabilities, not facts, and the same text can score differently across tools.
- Short passages (under roughly 200 words) are unreliable either way.
- Formulaic, simple, or very formal human writing, including writing by non-native English speakers, is flagged more often than it should be. A high score is not proof.
- Heavily edited text is harder for every detector.

## What this means for the skill

- Cosmetic tricks (synonym swaps, shuffled sentences, planted typos, odd Unicode) beat the weakest detectors and nothing else. Don't use them.
- The durable approach is the one in SKILL.md: start from real material, take a position, write specifically in one pass, match the person's voice, then do one audit pass. That addresses the same signals expert readers and trained classifiers use.
- Be honest with the user: this lowers the machine-like signals and raises quality, it does not guarantee a result on any specific tool.

## Sources

- Russell, Karpinska, Iyyer. "People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text." ACL 2025. arXiv:2501.15654.
- Krishna, Song, Karpinska, Wieting, Iyyer. "Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense." NeurIPS 2023. arXiv:2303.13408.
- Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup field guide), which catalogs patterns observed across thousands of machine-generated submissions and itself warns that no single sign is proof.
- Kobak et al. 2025, Science Advances, on LLM-favored vocabulary in biomedical papers; Juzek and Ward 2025 on why models over-use words like "delve".
- Vendor explainers on perplexity, burstiness, and classifier detection (GPTZero, Pangram and others), used for the general mechanism only.
