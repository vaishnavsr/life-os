# Career OS

Part of **Life OS**. Career OS runs your career on Claude, Notion and email.

Save a job from your phone, and Claude researches the company, drafts a tailored resume and cover letter, and files them in Notion. Your application statuses update themselves from your inbox, and your experience library grows through short story interviews.

## What you need
- A **Claude** account. Free works when you ask; automatic runs need Pro or higher (see "Which Claude plan do I need?" below).
- A **Notion** account (the free plan is fine).
- A **Gmail** account, used for automatic status tracking.
- Optional: **Google Calendar**, so interviews and prep slots are added for you.

## Which Claude plan do I need?

| | Free | Pro or higher |
|---|---|---|
| Setup, story interviews, drafting and email checks **when you ask** | Yes | Yes |
| Connecting Notion and Gmail | Yes | Yes |
| **Automatic** weekday runs (scheduled tasks) | No | Yes |
| Library databases (e.g. IBISWorld) and LinkedIn ads through Claude in Chrome | No | Yes |
| Enough usage for regular applications | Tight: researching and drafting is heavy, so expect one or two applications before you hit the usage limit and have to wait for it to reset | Comfortable |

**Suggestion:** start on Free to try setup and draft a couple of applications by asking. Upgrade to Pro when you want it to run by itself every weekday. Pro plans may also cap how many scheduled runs start per day. The default schedule of one run each weekday stays well inside that.

## Install (5 minutes)
1. In Claude, open **Settings → Connectors** and connect **Notion** (give it access to your workspace) and **Gmail**.
2. Add the plugin. In Claude's plugin settings, add the marketplace `vaishnavsr/life-os` (https://github.com/vaishnavsr/life-os) and install **career-os**. Alternatively, upload the `.plugin` file you were sent. In Claude Code, run:

   ```
   /plugin marketplace add vaishnavsr/life-os
   /plugin install career-os@life-os
   ```
3. Start a new chat and say **"set me up"**.

Claude will then:
- ask a few questions: where you're job hunting, your level, and your target roles and industries;
- build your Notion workspace, with an experience library, a job pipeline board, templates, settings and a how-to page;
- read 1–3 of your old resumes and turn every achievement into a draft story;
- use your own Word resume as the template (or a clean standard layout if you prefer) and show you a sample;
- set up background runs on a schedule you choose. The default is once a day on weekdays only (email check, then drafting, then story tidy) and nothing on weekends. Change any of it, then or later, by saying "change my schedule";
- start interviewing you about your stories to fill in the gaps.

## Day to day
- **Found a job?** In the Seek, LinkedIn or Indeed app, tap **Share → Notion**, choose Job Pipeline and set STATUS to **00 - INBOX**. For LinkedIn, also paste the description into the page.
- **Drafts appear** in Notion at the next run, with status **01 - DRAFT**. Review them, ask for tweaks, then apply yourself.
- **Statuses update** from your email: screening, interviews, case studies, offers and rejections.
- **Add stories** any time by saying "let's add a story", or by pasting a voice-memo transcript.

## How Career OS is organised: Check, Change, Concentrate
Life OS splits every life area into three parts. Spend about 80% of your effort on **Concentrate**, the everyday work, and about 20% on **Check** and **Change**.

| Part | What it's for | In Career OS | Status |
|---|---|---|---|
| **Check** | Periodic measurement against whole-of-career targets | Aspirations (your why, values and requirements), Achievements (experience library), career check-ins | Achievements available; aspirations and check-ins coming |
| **Change** | Adjusting course when a check shows you're off track | Discussions (reviews and one-on-ones), Networks, Job Pipeline, Interviews | Job Pipeline and interview prep available; networks and discussions coming |
| **Concentrate** | The everyday work | Profession, Voluntary, Creations | Achievement log coming |

## Skills in this plugin

| Skill | What it does |
|---|---|
| career-setup | One-time setup from nothing; also changes settings and your schedule |
| story-interviewer | Interviews you and writes structured stories (background, challenge, actions, outcome) |
| job-application-drafter | Research, resume and cover letter for every job in the Inbox |
| pipeline-status-tracker | Reads email, moves jobs through the pipeline, and adds interviews and prep slots to your calendar |
| interview-prep | Prepares you for and debriefs each interview, one job at a time, using the interview coach and your own stories |
| interview-coach | Noam Segal's Interview Coach, bundled with credit (see below) |

## Interview prep and debriefs
Say "prep for my Canva interview", "mock interview for the Xero role" or "debrief my interview". Claude gives the interview coach only that job's research and your most relevant stories. It saves the coaching progress to an "Interview Coaching" page under that job in Notion, so each job's prep stays separate. For debriefs, chat with Claude, paste a voice-memo transcript, or paste a meeting transcript. Improvements to your stories are offered back to My Experiences, never written without your okay.

## Credits
The interview coaching is **Interview Coach** by Noam Segal (https://github.com/noamseg/interview-coach-skill), included unmodified under the MIT licence. See `skills/interview-coach/LICENSE` and `UPSTREAM.md`.

## Safety by design
- Claude never sends email, never submits applications, and never types or stores your passwords.
- Library databases (like IBISWorld through a state library) are used only through your own signed-in browser session.
- Every automatic status change is logged in the job's notes with the email that caused it.

## Licence
MIT.
