# Changelog

All notable changes to Life OS and its plugins are recorded here. Newest first.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/). Each entry lists what was **Added**, **Changed**, **Removed** or **Fixed**, plus anything existing users need to do under **Upgrade notes**.

To update: in Claude, plugins installed from the `vaishnavsr/life-os` marketplace pick up new versions when the marketplace refreshes. Uploaded `.plugin` files don't update; reinstall from the marketplace instead.

---

## Career OS 0.4.0 (2026-11-11)

### Added
- **Interview prep and debriefs** through a new `interview-prep` skill. Say "prep for my <employer> interview", "mock interview", "debrief my interview", or paste a transcript or voice-memo notes.
  - Works on one job at a time. The coach gets only that job's research and the 12–15 most relevant stories from My Experiences.
  - Saves the coach's `coaching_state.md` and a plain-language summary to an "Interview Coaching – <role>" page under the job in Notion, and adds a dated line to the job's NOTES.
  - Offers story improvements back to My Experiences and never writes them without the user's okay.
- **Interview Coach by Noam Segal**, bundled unmodified under the MIT licence as the `interview-coach` skill (upstream commit `634a8dd`, 29 May 2026). It covers prep, mocks, transcript analysis, debriefs, thank-you notes, salary and negotiation. Its licence and an `UPSTREAM.md` note are included.
- **Calendar events for interviews.** When an email confirms an interview time, `pipeline-status-tracker` adds the interview to the user's own calendar, plus a 45-minute prep slot the day before (evening first, then lunchtime, then the morning of).
  - No attendees and nothing is sent.
  - Reschedules move the events rather than duplicating them, and cancellations remove only the events Career OS created.
  - Emails with only a booking link are flagged instead.
- A setup question about calendar handling, and a `calendar` block in Settings (`interview_and_prep`, `interview_only` or `off`; `prep_minutes`).
- A credits section in both READMEs.

### Changed
- The Career OS README lists six skills and marks interview prep as available under **Change**.

### Upgrade notes
- Reinstall or refresh Career OS. Existing settings keep working, because a missing `calendar` block defaults to `interview_and_prep` when calendar tools are connected. Add `"calendar": {"mode": "off"}` to opt out.

## Career OS 0.3.1 (2026-11-11)

### Fixed
- The Claude app refused to save the plugin ("SKILL.md description cannot contain XML tags"). Removed the angle brackets from the `job-application-drafter` description, and checked every skill's description against the app's rules.

## Life OS / Career OS 0.3.0 (2026-11-11)

### Changed
- **Renamed.** The repository and marketplace are now **Life OS** (`vaishnavsr/life-os`), a catalogue meant to hold one plugin per life area. The plugin `job-search-os` is now **Career OS** (`career-os`). The setup skill `job-search-setup` is now `career-setup`. Install with `career-os@life-os`.
- The settings page is now titled **"Career OS – Settings"**. All skills still find the legacy "Job Search OS – Settings" page.
- New-user workspaces follow the Life OS layout: **A. Check** (Career Check-ins, Aspirations, My Experiences), **B. Change** (Discussions, Networks, Job Pipeline) and **C. Concentrate** (Profession, Voluntary, Creations). Sections not yet automated are created as placeholder pages.
- If a user already has a Check / Change / Concentrate structure, setup builds inside it instead of creating a parallel one.
- New Life OS catalogue README; the Career OS README explains the three parts and the roadmap.

### Added
- Optional Settings IDs for the check-ins database and the Aspirations, Discussions, Networks, Profession, Voluntary and Creations pages.

### Removed
- The `job-search-os` plugin name and `job-search-os` marketplace name (replaced as above).

### Upgrade notes
- Remove the old Job Search OS plugin and install `career-os@life-os`. GitHub redirects the old repo address. Existing Notion data, settings and scheduled tasks keep working.

## Job Search OS 0.2.2 (2026-11-11)

### Changed
- The default schedule is now **one run each weekday** (about 7:37am, Monday to Friday, no weekends). It does the email status check, then drafting, then the story tidy, which keeps inside per-day caps on some plans.

### Added
- A "Which Claude plan do I need?" section in the README (Free versus Pro for on-demand use, automatic runs, Claude in Chrome and usage).

## Job Search OS 0.2.1 (2026-11-11)

### Changed
- Users choose their own schedule during setup: times, days, frequency, which jobs run automatically, or none at all.
- "Change my schedule" updates or pauses existing scheduled tasks instead of creating duplicates. Task IDs are recorded in Settings.

### Fixed
- The Claude Code install commands in the README.

## Job Search OS 0.2.0 (2026-11-10)

### Added
- **Use your own Word resume as the template** (the new default):
  - `analyse_template.py` inspects a user's .docx and flags layouts that can't be refilled reliably (tables, text boxes, columns);
  - `fill_template.py` refills it with new content while keeping fonts, spacing, shading, header and footer;
  - address-block tables in cover letters are supported;
  - hard-coded "1/3"-style page totals become live page counts;
  - empty example paragraphs keep the template's font.
- Template modes in Settings: `own`, `builtin` and `script` (legacy).

### Changed
- Setup asks which look the user wants (their own Word file, a clean standard layout, or a match for their PDF) and shows their original and the result side by side before saving.

## Job Search OS 0.1.0 (2026-11-10)

### Added
- First release, with four skills:
  - `job-search-setup`: builds the Notion workspace (experience library, 13-status job pipeline, templates, settings, how-to page), reads old resumes into draft stories, and creates scheduled runs;
  - `story-interviewer`: live interviews, write-ups of pasted transcripts, finishing draft stories, and background tidy;
  - `job-application-drafter`: job ad capture, company and industry research (regulators by country; optional library databases through the user's own signed-in browser), and a tailored resume and cover letter attached in Notion;
  - `pipeline-status-tracker`: reads email and moves jobs through the pipeline with a logged reason, never sending or deleting anything.
- `build_docs.py`, a clean ATS-friendly resume and cover letter builder (A4 or Letter).
- Country-neutral settings: currency, spelling, page size, age-bias rules, writing rules.
- MIT licence.
