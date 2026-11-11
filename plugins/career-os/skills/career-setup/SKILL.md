---
name: career-setup
description: Sets up Career OS for a new user from nothing, and changes it later. Use when the user says "set me up", "set up Career OS", "install Career OS", "install my job search system", "start my job search", "change my schedule", "change my Career OS settings", or when another Career OS skill can't find the "Career OS – Settings" page. Creates the Notion workspace and databases, reads the user's existing resumes into an experience library, builds a resume template, and schedules the background runs.
---

# Career OS setup

Take a new user from "I have a Claude account, a Notion account and an email account" to a working job-search system in one guided session. Keep everything in plain language. The user should never see database IDs, JSON or file paths unless they ask.

Read `references/settings-and-schema.md` (in this skill's folder) before starting. It defines the exact workspace, database schemas, statuses and Settings JSON that every other Career OS skill depends on.

Create a task list for the user with these stages, and tick them off as you go.

## Stage 0: Check what's already there
- Search Notion for "Career OS – Settings" (or the legacy "Job Search OS – Settings"). If it exists, this user is already set up: offer to repair missing pieces or change preferences, rather than creating a duplicate workspace.
- Check the connectors:
  - **Notion** is required. If no Notion tools are available, tell the user to connect Notion in Claude's Settings → Connectors (give Claude access to the whole workspace, or at least a page it can build under), then stop.
  - **Email** is needed for automatic status tracking. Gmail is supported. If no email tools are present, carry on and say status tracking will start once they connect it.
  - **Scheduling tools** decide whether background runs are possible. Check with ToolSearch for scheduled-task tools.
  - **Browser tools** (Claude in Chrome) are optional, used for logged-in job sites and library databases.

## Stage 1: Preferences (AskUserQuestion, at most 4 questions per round; then free-text follow-ups)
Ask (spread over two rounds if needed):
1. **Where are they job hunting?** This sets country, currency, spelling, page size (A4 or US Letter) and default job boards. Offer the common options; infer timezone from location, or confirm it.
2. **What level of roles?** E.g. graduate/junior, manager, senior manager/director, executive. This sets the age-bias rule. For manager level and below, never state total years of experience and list early-career roles without years. For clearly senior roles, years of experience may be used.
3. **Target roles and industries.** Free text; this drives research sources and story selection.
4. **Calendar**: when an interview invite arrives, should Claude add the interview and a 45-minute prep slot the day before, the interview only, or leave the calendar alone? Events go on their own calendar with no invitations. Only ask if calendar tools are connected; otherwise record "off" and mention they can connect Google Calendar later.
5. **Library or paid research databases?** E.g. IBISWorld through a state library, or a university database. Optional. Record how they access it (always through their own signed-in browser session; never store their password).
Then collect owner details for the resume header: name, preferred name for signing letters, phone, city, LinkedIn, website. Read these from their resume in Stage 3 where possible and only ask for what's missing.

## Stage 2: Build the Notion workspace
- Ask where to put it: under a page they name, or as a new top-level page. If they don't mind, create it as a top-level private page.
- Also check whether the user already has a life or career structure (e.g. a "My Contribs" page, or Check / Change / Concentrate sections). If so, offer to build inside it and reuse their pages.
- Otherwise create the **Career OS** page with three callout sections (A. CHECK, B. CHANGE, C. CONCENTRATE), exactly as in the workspace layout in the reference. In order:
  1. the **My Experiences** database (under Check), using the schema exactly, including property descriptions and seed SKILLS options, with VALUE ($) in their currency where Notion supports it;
  2. the **Job Pipeline** database (under Change) with the 13 statuses in order and a board view grouped by STATUS;
  3. under the Job Pipeline page, "Templates – Resume & Cover Letter" and "Career OS – Settings";
  4. the **Career Check-ins** database (DATE, STATUS: Behind / Risk / Track, RESULTS, ACTIONS) and the placeholder pages Aspirations, Discussions, Networks, Profession, Voluntary and Creations, each with a one-line description of what it will hold;
  5. "How to use Career OS".
  Use the Notion create-database tool's own description for the exact schema syntax. Fetch each database after creating it to confirm its properties and get its collection:// URL.
- Write the Settings JSON with every ID filled in, followed by a plain-language explanation. Re-fetch it and check the JSON parses.
- Write the "How to use" page using the user guide in `references/user-guide.md`, personalised with their job boards and schedule.

## Stage 3: Read their existing resumes
- Ask for 1–3 recent resumes, uploaded to the chat (PDF or Word), or a link to a Notion or Drive file if those connectors exist. LinkedIn profile text pasted in also works.
- Extract:
  - **Owner profile**: contact details, education, certifications, and the full role timeline (title, employer, location, dates).
  - **Achievement stories**: each bullet or group of bullets that describes a distinct piece of work becomes one candidate story.
- Deduplicate across resumes. The same achievement often appears with different wording; keep the most specific version and merge numbers.
- Create one **My Experiences** entry per story:
  - Fill MY ROLE, NO., YEAR, EMPLOYER, FIRM, INDUSTRY and LOCATION, and SUMMARY where the resume supports it.
  - Put the original resume wording in the page body under "Source (from resume)".
  - Draft BACKGROUND, CHALLENGE, ACTIONS and OUTCOME only from what the resume says. Leave anything unsupported blank.
  - Write "Questions for <preferred name>: …" in NOTES listing what's missing (value, team size, their personal part, outcome, the people side).
  - Convert currencies to theirs and note the original in NOTES.
- Tell the user how many stories you found and how many questions are waiting. Never invent numbers.

## Stage 4: Their resume template (their look, not ours)
Everyone has their own layout preference, so default to the user's own.
1. Ask: "Do you have a resume layout you like? If so, upload it as a Word file (.docx), plus a cover letter if you have one." Offer three choices:
   - **Use my own Word resume** (recommended whenever they have a .docx they like);
   - **Use a clean standard layout** (the builtin builder);
   - **Match the look of my PDF**: builtin, styled with the PDF's font and accent colour. PDFs can't be edited reliably.
2. **Own template**:
   - Run `../job-application-drafter/scripts/analyse_template.py their.docx`. If it warns about tables used for the main layout, text boxes or multiple columns, explain in plain words that this layout can't be refilled reliably. Offer either a builtin layout styled to match, or ask whether they have a simpler single-column version. A small table used only for an address block is fine; use `address_table`.
   - Choose one example paragraph for each kind: name, contact, heading, body, label, bullet, role_title, role_intro, and spacer if there is one. Use `doc.paragraphs` indices from the analysis; tables don't count in that numbering. Write the map in the format in `fill_template.py`'s docstring.
   - Test it on their real content: build a full resume from their profile and stories with `fill_template.py`. Render both their original and the result to images and compare them side by side. Fix the map until headings, dates, bullets, fonts and the footer match. The script turns hard-coded "1/3"-style page totals into live page counts.
   - **Cover letter**: if they uploaded one, map it the same way (date, address or address_table, subject, salutation, body, closing, signature, blank). If not, reuse the resume file as letterhead: set the cover_letter template to the resume file with name, contact and body prototypes from it; other kinds fall back to body.
   - Upload the template .docx files to the Templates page. Save `template.mode = "own"` and the full map, with each `template` path replaced by the Notion file name, under `template.map` in Settings.
3. **Builtin or PDF look**: build a sample with `../job-application-drafter/scripts/build_docs.py`, using their page size and, where possible, their old resume's font and accent colour. Show it, adjust the fonts, colours, section names and order they ask for, and save `template.mode = "builtin"` with the style.
4. Always show the final sample resume and cover letter as PDFs and get a thumbs-up before moving on.

## Stage 5: Background runs (the user chooses)
Ask how hands-off they want to be, then create exactly what they pick. If scheduled-task tools are missing, skip to the last bullet.
- **Offer the default as a starting point**: one scheduled task, once a day on weekdays only (Monday to Friday, nothing on weekends), at about 7:37am in their timezone. Each run does all three jobs in order:
  1. the email status check (pipeline-status-tracker);
  2. drafting everything in the Inbox (job-application-drafter);
  3. tidying draft stories (story-interviewer, background-tidy mode).
  That's five runs a week, which fits within plan limits on scheduled runs.
- **Let them change any part**:
  - the time;
  - the days (e.g. adding weekends);
  - frequency, e.g. a separate email check two or three times a day. The minimum interval is usually hourly, and some plans cap scheduled runs per day, so warn if their choice could exceed that;
  - which jobs run automatically, e.g. email tracking only, with drafting on demand;
  - no schedule at all.
- **Create the tasks**:
  - use minutes off the hour (e.g. :07, :41, :23), and run in the cloud unless their library database or local folder needs their computer;
  - write each prompt as a standalone instruction that names the skill to invoke and states the hard limits (never send email, never submit applications, never type passwords), ending with a SendUserMessage summary;
  - tell them which approval setting each task got and, if runs will ask for approval, that they can switch the task to automatic approval in its settings.
- **Record the schedule in Settings**, including each task's ID, so it can be changed later.
- **Later changes** ("change my schedule", "run drafting once a day", "pause the email check"): list the existing scheduled tasks and update or pause the matching ones. Never create duplicates. Then update the schedule in Settings.
- **If no scheduling tools exist**, explain that everything works on demand ("process my inbox", "check my email for job updates").

## Stage 6: Show them how to use it, then start
Explain in a few short lines:
- **Saving a job on the phone**: in the Seek, LinkedIn or Indeed app, tap Share, then Notion, choose the Job Pipeline database, and set STATUS to "00 - INBOX". For LinkedIn, also paste the job description into the page.
- **What happens next**: drafts appear in Notion at the next run, and statuses update from email on their own.
- **Adding stories**: say "let's add a story" any time, or drop a voice-memo transcript into My Experiences.
Then offer to start the first story interview right away, beginning with the story that has the biggest gaps or the most recent role. When they agree, invoke the story-interviewer skill.

## Rules
- Never type, store or ask for passwords. Library and job-site access always goes through the user's own signed-in browser session.
- Never send email or submit applications on the user's behalf.
- Don't create a second workspace if one exists; repair the existing one instead.
- Keep the conversation non-technical. Describe what is being set up, not how.
