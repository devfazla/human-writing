# Case studies

Real cases where a draft was flagged and the cause was found. Add new ones as they come in. Each is one data point from the user's own testing, with the detector names not recorded, so read them as evidence of direction, not as proof for any specific tool.

## 1. Build-in-public caption: two deleted lines

Request: an Instagram caption saying a website is in development, with the status taken from the user's notes (public site, admin panel and waitlist done; sales funnel next).

First draft, which several detectors scored 70 to 100 percent AI:

> I'm building [site] right now. It's not finished, and I'd rather say that than wait for a perfect launch.
>
> What's done: the public site, an admin panel for managing it, and a waitlist. You put in your name and email, you get a confirmation mail, and we approve people from the admin side.
>
> Still to do: a lot. I'll post as pieces get finished.
>
> [site]
>
> #buildinpublic #webdevelopment #nextjs #developerlife

The user's edit, which every detector then read as human:

> I'm building [site] right now.
>
> What's done: the public site, an admin panel for managing it, and a waitlist. You put in your name and email, you get a confirmation mail, and we approve people from the admin side.
>
> Next: Sales funnel. I'll post as pieces get finished.
>
> [site]
>
> #buildinpublic #webdevelopment #nextjs #developerlife

Only two things changed. The second sentence was deleted, and "Still to do: a lot." was replaced with a specific next item. Everything else, including the hashtags, the colon labels, the comma-spliced "you put in..., you get..." sentence, and the slightly informal "confirmation mail", stayed and read as human.

What was wrong with the deleted lines:

- **Invented stance.** The user never said they'd rather admit it than wait for a perfect launch. The model made up a motive and a philosophy to sound candid. It is also a "I'd rather X than Y" contrast with a stock phrase ("perfect launch"), and "honest build-in-public" confessions are among the most common things a model writes for this kind of request.
- **Vague placeholder.** "A lot" names nothing. The real fact was one specific item.
- **Fails both tests** in SKILL.md: it carried no fact from the user's material, and a generic model given the same prompt would plausibly write it.

What the skill missed the first time: the earlier version of the audit script checked rhythm and word lists and passed both drafts with the same single minor (and false) flag. It had no way to see that a sentence was invented. The `--source` grounding check, the persona and vague-placeholder patterns, and the information test were added because of this case.

What the case does not show: that the surviving text is safe everywhere. It is 45 words. Longer posts have much more surface, and the rest of this skill still applies to them.

Lessons:

1. Look for sentences that exist to sound human or candid. They are the likeliest culprits in short text.
2. Delete first. Specific replacement second. Rewording last.
3. A short post of only the user's facts leaves little for a detector to match.
4. Plain labels ("What's done:", "Next:") and mildly informal wording from the user's own notes are fine.
