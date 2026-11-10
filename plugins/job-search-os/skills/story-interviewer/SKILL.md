---
name: story-interviewer
description: Builds the Job Search OS experience library. Use when the user wants to add, tell, record or finish a career story or achievement ("let's add a story", "I want to talk about the X project", "finish my draft stories"), pastes a story transcript or voice-memo text, or on a scheduled Job Search OS story-tidy run. Interviews the user and writes structured entries to the My Experiences database in Notion.
---

# Story interviewer

Turn the user's spoken or written career stories into complete, consistent entries in **My Experiences**. These entries feed every resume, cover letter and interview answer, so accuracy matters more than speed.

## Load settings first
Search Notion for "Job Search OS – Settings", fetch it and parse the JSON block (format: `../job-search-setup/references/settings-and-schema.md`). If it's missing, tell the user to run setup and stop. Use `notion.experiences_data_source`, `owner.preferred_name`, `locale` (currency, spelling) and `writing_rules`. Re-read the database schema at the start, because users add options.

## Pick the mode from what the user says (never ask them to name a mode)

| The user says or does | Mode |
|---|---|
| "let's add a story", names a project, or starts telling a story | **Live interview** |
| Pastes a long transcript or voice-memo text | **Write-up then gaps**: structure it now, then ask only what's missing |
| "finish my draft stories", "any stories need work?" | **Finish drafts** |
| Scheduled or unattended run | **Background tidy**: no questions, leave them in NOTES |

If it's genuinely unclear, ask one short question: "Shall I interview you about this, or just write up what you've given me?"

**Draft entry**: an entry with ACTIONS and OUTCOME empty and raw notes, a transcript or "Source (from resume)" in the page body, or any entry whose NOTES contain "Questions for".

## Style
- **MY ROLE**: "<Role>, <project or theme>", e.g. "Project Lead, Retention Strategy".
- **BACKGROUND**: 2–4 sentences on the organisation, its situation and why it mattered, with scale numbers.
- **CHALLENGE**: 2–3 sentences on the specific problem and its constraints.
- **ACTIONS**: one opening sentence in first person, then 4–6 bullets in the form "• Label: what I did and how". Only the user's own actions.
- **OUTCOME**: 2–4 sentences on results, who endorsed or used the work, and what happened next. Be honest about benefits not yet realised.
- **ATTRIBUTES**: 2–3 first-person sentences on interpersonal traits and how they overcame people-related obstacles.
- **SUMMARY**: one line with the headline number.
- **Numbers**: VALUE ($) in thousands per year in the owner's currency; VALUE (%) as a decimal (0.25 means 25%).
- Use the owner's spelling and currency. Convert other currencies and note the original in NOTES.
- Never invent numbers, names or outcomes. Unknown means blank plus a question. Approximations only when the user gives them.
- Multi-selects (FIRM, PARENT ORG., INDUSTRY, SKILLS): reuse existing options; add new ones only when nothing fits.

## Live interview
1. Let them tell it first; don't interrupt the first telling.
2. Check for duplicates by EMPLOYER and YEAR. If a similar story exists, offer to update it instead of creating a new one.
3. Ask follow-ups **one at a time**, about 6–8 at most, prioritising:
   - hard numbers (value, %, volume, time);
   - their personal part versus the team's;
   - team size and reporting lines;
   - the sharpest constraint or conflict, and how they handled the people side;
   - who endorsed or used the work;
   - what happened afterwards.
   If they "don't know", move on and record it as an open question.
4. Show the draft entry field by field and ask "Anything to correct before I save?"
5. Save it:
   - NO. = current maximum + 1;
   - fill every field that's supported;
   - put any remaining unknowns in NOTES as "Questions for <preferred name>: …".
   Confirm with the entry link.
6. Offer the next story; for a batch, take them one at a time. If setup just imported resumes, start with the most recent or most gap-heavy drafts.

## Write-up then gaps
Structure the pasted text into every field straight away and show it. Ask only the missing questions, one at a time. Save when the user confirms; if they stop early, save what exists with the questions in NOTES.

## Finish drafts
List draft entries in one line each and work through them one at a time: show what's there, ask only the open questions, update the entry, and remove answered questions from NOTES.

## Background tidy (unattended)
For each draft entry:
- structure it using only what the text supports;
- set NO. if it's blank;
- write the questions in NOTES.
Never overwrite fields the user filled in; note any conflicts in NOTES. Report in the run summary how many stories were tidied and how many questions are waiting.
