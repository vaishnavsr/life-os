---
name: interview-prep
description: Prepares for and debriefs job interviews using the bundled interview-coach skill, one job at a time. Use when the user says "prep for my Canva interview", "mock interview for the Xero role", "I have an interview tomorrow", "debrief my interview", "how did my interview go", pastes an interview transcript or voice-memo notes, or asks for a thank-you note, salary or negotiation help for a job in their Career OS pipeline.
---

# Interview prep and debrief (Career OS link to the interview coach)

The **interview-coach** skill (Noam Segal's, bundled in this plugin) does the coaching: prep briefs, likely questions, mock interviews, transcript analysis, debriefs, thank-you notes, salary and negotiation. This skill gives it the right material for **one job** and saves its progress back to that job in Notion. Each job's coaching stays separate, so nothing from one employer leaks into another.

## 1. Load settings and find the job
- Search Notion for "Career OS – Settings" (legacy title: "Job Search OS – Settings") and parse its JSON block (format: `../career-setup/references/settings-and-schema.md`). If it's missing, tell the user to run setup and stop.
- Find the job in the Pipeline (`notion.pipeline_data_source`) by the employer or role the user named. If several match, ask which. If none match, offer to create a Pipeline entry first (ROLE, EMPLOYER, URL, STATUS 02 - SUBMITTED or the stage they're at).
- Read the job's fields (JOB DESC., RESPONSIBILITIES, REQS., EMPLOYER DESC., NOTES, STATUS) and its page body, which holds the research brief. Note the attached APP - CV resume as the version they applied with.

## 2. Build this job's coaching file
Work in a fresh folder for this job, e.g. `interview/<employer-slug>/`.
- **Existing coaching**: look for a child page of the job titled "Interview Coaching – <ROLE>". If it exists, fetch it with include_file_urls=true and download its `coaching_state.md` straight away, because the URLs expire in minutes. That file is the coach's memory for this job.
- **First time for this job**: create `coaching_state.md` following `../interview-coach/references/coaching-state-schema.md`, pre-filled from Career OS so the coach doesn't re-ask what's already known:
  - **Profile**: target role from the job; seniority band from the role title and `settings.targets`; interview timeline from NOTES or the calendar; Track "Full System" unless the interview is within 48 hours ("Quick Prep"); feedback directness 4 unless the user has said otherwise.
  - **Resume Analysis**: from the resume they applied with (APP - CV) and the brief.
  - **Storybank**: from **My Experiences** (`notion.experiences_data_source`). Choose the 12–15 stories most relevant to this job's requirements. Use the story's NO. as the ID (S017 for NO. 17), MY ROLE as the title, SKILLS for primary and secondary skill, and BACKGROUND + CHALLENGE as Situation/Task, ACTIONS as Action, OUTCOME + VALUE as Result. Use ATTRIBUTES or a distinctive insight from the story as the Earned Secret, or leave it blank for the coach to develop. Put the Notion link in Notes.
  - **Interview Loops (active)**: one section for this employer, with status and any known round details from NOTES and emails.
  - **JD Analysis**: from the job fields and brief.
  - Leave everything else as empty template sections.
- Give the coach this file only. Never load another job's coaching file into the session.

## 3. Hand over to the interview coach
Invoke the **interview-coach** skill and let it run its own session-start protocol on `coaching_state.md` in the working folder. Route the user's request to the coach's commands:

| User wants | Coach command |
|---|---|
| Prep for an upcoming interview | `prep <employer>` (it also uses `concerns` and `questions`) |
| Interview within 24–48 hours, nerves | `hype` |
| Practise | `mock <format>` or `practice` |
| Same-day recollection, by chat or voice memo | `debrief`. If they pasted voice-memo text, give it to debrief as their recollection. |
| A transcript or recording | `analyze` (the coach's transcript-format guide handles common tools) |
| Thank-you note | `thankyou`. Draft only; the user sends it themselves. |
| Pay talk early in the process | `salary` |
| An offer | `negotiate` |
| Screening questions on an application form | `apply <employer>` |
| Recruiter feedback or an outcome | `feedback` |

Follow the coach's own rules on pacing (one question at a time), evidence and voice.

## 4. Save back to Notion (after each major step and at the end)
- Upload the updated `coaching_state.md` with notion-create-file-upload, then POST it as multipart field `file` to the returned upload_url with the returned headers (curl).
- Create or replace the job's child page "Interview Coaching – <ROLE>" with:
  1. a short plain-language summary at the top: next round and date, the top 3 concerns with counters, the stories to lead with (linked to My Experiences), questions to ask, and the latest scores or debrief takeaways;
  2. the uploaded `coaching_state.md` file;
  3. a dated history line for each session.
- Append one line to the job's NOTES, e.g. `[2026-11-12] Interview prep: mock behavioural, scores Sub 4 / Str 3 …` or `[date] Round 2 debrief: …`.
- Don't change STATUS here; pipeline-status-tracker does that from email. Exception: if the user tells you an outcome directly (e.g. "I got rejected"), update STATUS by the tracker's mapping and note it.

## 5. Feed improvements back to the experience library
If the coach sharpened a story (a better Earned Secret, a clearer result, new numbers) or uncovered a new one, list the changes at the end and ask whether to update My Experiences. Hand new stories to the **story-interviewer** skill. Never overwrite My Experiences fields without the user's yes.

## Rules
- Never send email or messages, and never contact employers or interviewers. Thank-you notes and outreach are drafts only.
- Recording interviews: the user is responsible for consent under their local laws. If they ask, say so in one line and leave it to them.
- Keep each job's coaching file separate; that is the point of this skill.
- Use the owner's spelling and currency from Settings.
