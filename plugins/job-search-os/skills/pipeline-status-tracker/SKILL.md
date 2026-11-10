---
name: pipeline-status-tracker
description: Keeps the Job Search OS pipeline in step with the user's email. Use when the user says "check my email for job updates", "update my pipeline", "any news on my applications?", or on a scheduled Job Search OS email run. Reads application confirmations, interview invites, offers, rejections and withdrawals, then updates job statuses in Notion.
---

# Pipeline status tracker

Keep the Job Pipeline in Notion in step with the user's email. This skill is read-only on email and writes only to the Pipeline.

## Load settings first
Search Notion for "Job Search OS – Settings", fetch it and parse the JSON block (format: `../job-search-setup/references/settings-and-schema.md`). If it's missing, tell the user to run setup and stop. Use `notion.pipeline_data_source`, `statuses`, `owner.email` and `locale.timezone`. Re-read the STATUS options from the data source every run, and match statuses by their number prefix.

If no email tools are connected, say so in one line and stop.

## Hard limits
- Never send, reply to, forward, label, archive or delete email.
- Never delete or archive Notion entries.
- Never set 08 (Accepted). Accepting is the user's decision; flag offers instead.
- Never move an entry out of a closed status (08 to 12) unless an email clearly reopens it. Flag any reopened entry.
- Ignore job alerts, newsletters and marketing ("jobs you may like"). They never create entries.

## Steps
1. **Load the Pipeline.** Get every row's ROLE, EMPLOYER, STATUS and NOTES.
2. **Search email.** Use the last 3 days by default; the overlap is deliberate. On request, use the period the user names. Run several focused searches:
   - confirmations: "thank you for applying", "application received", "we have received your application";
   - interviews: interview, "phone screen", "next stage", assessment, "case study", presentation, "final round", panel, invitation;
   - outcomes: unfortunately, "not progressing", "other candidates", unsuccessful, "position has been filled", offer, "reference check";
   - the user's own sent mail for withdrawals: withdraw, "no longer wish", "accepted another".
   Open each candidate thread and read it; don't classify from snippets.
3. **Match** each email to a row by employer, sender domain, role title or job reference. Recruitment-agency emails often name the client only in the body. If there's no confident match, don't guess; list it under "Couldn't match".
4. **Classify and update** using this mapping:

   | Email says | Set STATUS to |
   |---|---|
   | Application received or confirmed | 02 (only if the row is at 00 or 01) |
   | Recruiter or HR screening | 03 |
   | Hiring-manager, behavioural or fit interview | 04 |
   | Case study, assessment, presentation or work sample | 05 |
   | Final round, executive or panel | 06 |
   | Offer, salary discussion or references | 07 |
   | Rejection at any stage | 09 |
   | The user's own email withdrawing | 10 |

   - Move forward only through 02 to 07; never backwards. Rejection and withdrawal can apply from any open status.
   - If an email is ambiguous, leave the status and flag it.
   - For each change, append to NOTES: `[YYYY-MM-DD] STATUS 02 → 03 from email "<subject>" (<sender>).` Check NOTES for the same subject first, so re-runs don't duplicate work.
5. **Create missing entries.** When a confirmation or interview email refers to a job with no row, create one with:
   - ROLE as "<Employer>, <Role>", plus EMPLOYER;
   - the URL, if the email has one;
   - the STATUS the email shows;
   - NOTES naming the source email.
6. **Interviews.** Report interview dates and times in the summary. If calendar tools exist and the user is present, offer to add them; don't add them on unattended runs.
7. **Stale check.** Weekly, or when asked, list rows at 02 for more than 45 days with no email activity. Suggest 09 or 12, but only suggest; the user decides.
8. **Summarise** in full sentences:
   - status changes with reasons;
   - new entries;
   - upcoming interviews;
   - flagged items: ambiguous, couldn't match, reopened, or an offer awaiting the user's decision.
   If nothing changed, say so in one line. On unattended runs, send the summary with SendUserMessage.
