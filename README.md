# human-writing

An agent skill that makes AI-drafted prose read like a specific person wrote it, not a language model. Built for emails, essays, social posts (Instagram, Facebook, LinkedIn, Hashnode), bios, cover letters, and product copy.

The approach is not a synonym spinner. Detectors and human editors flag text that is generic in content and default in structure, so the fix happens before and during drafting: take a position, use only the user's real facts, and cut every sentence that doesn't carry one.

## Contents

```
SKILL.md                    the skill: workflow, drafting rules, audit step
references/ai-tells.md      words, constructions, and formatting habits to avoid, and why
references/platforms.md     per-platform shapes (Instagram, Facebook, LinkedIn, Hashnode)
references/case-studies.md  a real before/after: flagged at 70% to 100% human by deleting two lines
references/detectors.md     how detectors actually work, read only when asked
scripts/audit.py            static audit: flags ungrounded sentences, rhythm, stock phrases, tells
evals/evals.json            three test prompts with expected outputs
```

## How it works

1. Collect the user's real material (facts, numbers, names, a writing sample). No invented specifics, ever.
2. Decide the point of the piece in one sentence.
3. Draft in one pass under two tests per sentence: does it carry a fact from the material, and would a generic model have produced it anyway?
4. Audit with the script:

   ```bash
   python3 scripts/audit.py draft.txt --source material.txt
   ```

   `--source` lists every sentence whose content words appear nowhere in the user's material. That is how invented stance and filler get caught. Thresholds are heuristics, not detector scores.
5. One revision pass, then stop. Repeated "make it more human" rounds add new machine habits.

## What it doesn't promise

No writing method guarantees a detector score. Detectors are probabilistic, disagree with each other, and get updated. This skill removes the signals they measure and puts real specifics into the text. It explicitly bans cheap tricks (invisible characters, look-alike Unicode, planted typos) because they damage the text for readers and detectors learn them quickly.

## Installing

Drop the folder into your agent's skills directory (e.g. `~/.claude/skills/` for Claude Code, or the equivalent for your agent). The skill activates on requests like "make it sound human", "less AI", or "don't sound like ChatGPT".
