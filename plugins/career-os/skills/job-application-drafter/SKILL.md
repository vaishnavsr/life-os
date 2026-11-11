---
name: job-application-drafter
description: Researches saved jobs and drafts a tailored resume and cover letter for each. Use when the user says "process my inbox", "draft my new jobs", "do the <employer> job", pastes a job ad URL asking for an application, or on a scheduled Career OS drafting run. Attaches the files in the Notion Job Pipeline and moves the job to 01 - DRAFT.
---

# Job application drafter

Turn each job the user saved to their Job Pipeline into a researched brief, a tailored resume and a cover letter, ready for them to review and submit.

## Load settings first
Search Notion for the page "Career OS – Settings" (legacy title: "Job Search OS – Settings"), fetch it and parse the JSON block (format: `../career-setup/references/settings-and-schema.md`). If it's missing, tell the user to run setup ("set up Career OS") and stop. Use from it: the owner details, locale (currency, spelling, page size), notion IDs, writing_rules, age_bias, targets, template, research and local_folder. Re-read the Pipeline STATUS options from the data source.

## Standing rules
- Follow every entry in `settings.writing_rules`.
- Money goes in the owner's currency. Show converted figures as local currency first with the original in brackets, and check each experience entry's NOTES for currency caveats.
- **Age bias**: if `age_bias.state_total_years` is "senior_only", state total years of experience only when the job title contains one of `age_bias.senior_titles`. Never put years on the early-career line unless `early_career_years` is true.
- Resume 2 pages maximum; cover letter 1 page.
- Never invent experience, numbers, employers or credentials. Only use what's in My Experiences or the owner profile.
- Never submit an application or contact an employer.

## Steps
1. **Find work.** Query the Pipeline for STATUS = 00 - INBOX unless the user named a job. List them in one line and start. If the user is present and more than 5 are waiting, ask whether to do them all.
2. **Capture the ad.** Prefer job text pasted in the page body. Otherwise fetch the URL with WebFetch. Logged-in sites such as LinkedIn need the browser tools; use them only if available. If you can't get the ad, leave the job in 00 - INBOX, write "Job description needed: paste it into the page" in NOTES, and move on. Fill EMPLOYER, URL, JOB DESC., RESPONSIBILITIES, REQS. and APP. DUE.
3. **Research.** See `references/research-sources.md`. In short:
   - the company's latest annual report, results or investor presentation, or website and news for private firms;
   - the industry regulators and bodies for the user's country;
   - the library database if `research.library_database.enabled` and browser tools are available, through the user's already signed-in session only. Never type a password. If it's unavailable, write "<name> pending" in NOTES.
   Write EMPLOYER DESC. as one paragraph in the owner's currency. Write a full-sentence brief in the page body covering:
   - the company's position and strategy;
   - financials;
   - industry forces;
   - what the role is really for;
   - the three strongest angles for this user.
   Attach useful public files (annual report PDFs) to ADD. INFO.
4. **Pick stories.** Query My Experiences and map the job's requirements to the strongest stories. Prefer recent, quantified and relevant ones. Note in the brief which stories you used.
5. **Draft.** Write the content, then build the files:
   - **own mode** (`template.mode` = "own", the default when the user supplied a Word file): fetch the Templates page with include_file_urls=true. Download the template .docx files straight away, because the URLs expire in minutes. Write `map.json` from `settings.template.map`, setting each `template` path to the downloaded file. Write the content JSON (same format as build_docs.py) and run `scripts/fill_template.py map.json content.json OUT_DIR`. This keeps the user's fonts, spacing, shading and header/footer exactly.
   - **builtin mode** (`template.mode` = "builtin"): write a content JSON and run `scripts/build_docs.py content.json OUT_DIR` (format in the script's docstring), passing `style` from settings (font, accent_hex, page_size) and the owner contact details.
   - **script mode** (legacy): download the template and reference build script from the Templates page, adapt the script's content sections and run it.
   - **Resume content, any mode**:
     - Summary, a 3–4 line positioning statement tailored to the job;
     - Selected impact, 2 bullets with the biggest relevant numbers;
     - Core capabilities, 6–10 phrases echoing the job's language;
     - Professional work history: most recent roles first, 1–4 bullets each, older roles trimmed;
     - Early career, one plain line;
     - Education.
   - **Cover letter**: five short paragraphs:
     1. why this company, now (use the research);
     2. strategy or functional proof with numbers;
     3. execution or operating proof;
     4. one role-specific angle;
     5. close.
     Sign with the owner's preferred name.
   - **Check the result.** Convert each DOCX to PDF with LibreOffice, one file per conversion call, because converting two at once can fail silently. Render the pages with pdftoppm and look at every page. Trim until the resume fits 2 pages and the cover letter 1 page. Check the footer page count reads correctly.
   - **File names**: `<YEAR>-Resume-<Employer>-<Role>-<Initials>` and `<YEAR>-Cover_Letter-<Employer>-<Role>-<Initials>`, each as .docx and .pdf, with underscores instead of spaces.
6. **Attach.** For each file, call notion-create-file-upload, then POST the file as multipart field `file` to the returned upload_url with the returned headers (curl). Set APP - CV (resume PDF and DOCX) and APP - CL (cover letter PDF and DOCX), keeping existing ADD. INFO. files. Set STATUS to 01 - DRAFT.
7. **Deliver.** Notion is the home for the files. If the user is present, also send the PDFs with SendUserFile. If `local_folder.enabled` and the device tools answer, copy the files there too; otherwise skip silently.
8. **Report** in a few full sentences:
   - what was drafted;
   - anything to check (titles, assumptions, currency conversions);
   - jobs waiting on a pasted description or library research.

## Unattended runs
Do steps 1–6 with whatever is reachable, without asking questions. Then send the step 8 summary with SendUserMessage.
