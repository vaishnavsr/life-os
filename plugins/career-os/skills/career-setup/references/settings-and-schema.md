# Career OS: Notion structure, schemas and settings

Every Career OS skill depends on this file. It defines the Notion workspace that setup creates and the Settings page that every other skill reads.

## Workspace layout

Career OS follows the Life OS pattern: **Check** (periodic measurement), **Change** (adjusting course) and **Concentrate** (everyday work). Setup creates one top-level page laid out in those three sections. Sections marked *(placeholder)* are created as simple pages with a one-line description of what they will hold; later Career OS skills fill them in.

```
Career OS                                   (root page, three callout sections)
├── A. CHECK
│   ├── Career Check-ins                    (database: DATE, STATUS Behind/Risk/Track, RESULTS, ACTIONS) (placeholder)
│   ├── Aspirations                         (page: values, requirements, career direction) (placeholder)
│   └── My Experiences                      (database, the experience library)
├── B. CHANGE
│   ├── Discussions                         (page: performance reviews and one-on-ones) (placeholder)
│   ├── Networks                            (page: people to keep in touch with) (placeholder)
│   └── Job Pipeline                        (database, board view grouped by STATUS)
│       ├── Templates – Resume & Cover Letter  (page: base .docx files, optional build script)
│       └── Career OS – Settings            (page: JSON settings block + plain-language notes)
├── C. CONCENTRATE
│   ├── Profession                          (page: one sub-page per job, with links to document folders) (placeholder)
│   ├── Voluntary                           (page) (placeholder)
│   └── Creations                           (page: drafts and master copies; published work lives on the web) (placeholder)
└── How to use Career OS                    (page: plain-language guide for the user)
```

If the user already has their own life or career structure in Notion (for example a "My Contribs" page with Check, Change and Concentrate sections), build inside it instead: reuse their existing pages and record the IDs in Settings. Never create a parallel structure.

## How skills find the settings

1. Search Notion for the page titled exactly **"Career OS – Settings"**. If it isn't found, also try the legacy title "Job Search OS – Settings". If several pages match, prefer the one under the Job Pipeline or Career OS page.
2. Fetch it and parse the first JSON code block. That object is `settings`.
3. If no page is found, stop and tell the user to say "set up Career OS" first. Never guess IDs.
4. Re-read the Pipeline STATUS options from the data source on every run, because users rename them. Treat the settings `statuses` list as the intended meaning, matched by number prefix (00, 01, …).

## Settings JSON

```json
{
  "version": 1,
  "owner": {
    "name": "Full Name",
    "preferred_name": "Nickname used to sign letters",
    "email": "optional, for matching sent mail",
    "phone": "optional",
    "location": "City, Country",
    "linkedin": "optional URL",
    "website": "optional URL"
  },
  "locale": {
    "country": "AU",
    "currency": "AUD",
    "currency_symbol": "A$",
    "timezone": "Australia/Melbourne",
    "spelling": "Australian English",
    "page_size": "A4",
    "date_format": "D MMM YYYY"
  },
  "notion": {
    "root_page_id": "",
    "settings_page_id": "",
    "experiences_data_source": "collection://…",
    "pipeline_data_source": "collection://…",
    "templates_page_id": "",
    "checkins_data_source": "optional collection://…",
    "aspirations_page_id": "optional",
    "discussions_page_id": "optional",
    "networks_page_id": "optional",
    "profession_page_id": "optional",
    "voluntary_page_id": "optional",
    "creations_page_id": "optional"
  },
  "statuses": [
    "00 - INBOX", "01 - DRAFT", "02 - SUBMITTED", "03 - INT SCREEN", "04 - INT FIT",
    "05 - INT CASE", "06 - INT FINAL", "07 - NEGOTIATION", "08 - ACCEPTED",
    "09 - REJECTED - FIRM", "10 - REJECTED - ME", "11 - ARCHIVED", "12 - EXPIRED"
  ],
  "writing_rules": [
    "Write money in the owner's currency; show converted figures as local currency first with the original in brackets.",
    "Research briefs use full sentences, not bullet fragments.",
    "Resume maximum 2 pages; cover letter 1 page."
  ],
  "age_bias": {
    "state_total_years": "senior_only",
    "early_career_years": false,
    "senior_titles": ["Director", "Head of", "General Manager", "GM", "VP", "Chief", "Executive", "Partner"]
  },
  "targets": {
    "roles": ["e.g. Strategy Manager"],
    "industries": ["e.g. Energy", "Banking"],
    "job_boards": ["e.g. Seek", "LinkedIn"]
  },
  "template": {
    "mode": "own",
    "map": {
      "resume": {"template": "TEMPLATE-Resume.docx (file name on the Templates page)",
                 "prototypes": {"name": 0, "contact": 1, "heading": 2, "body": 3, "label": 5, "bullet": 6,
                                "role_title": 13, "role_intro": 14, "spacer": 19},
                 "keep_contact": true, "name_text": null, "spacer_after_role": true},
      "cover_letter": {"template": "TEMPLATE-Cover_Letter.docx",
                       "prototypes": {"date": 0, "subject": 2, "salutation": 4, "body": 6, "closing": 15,
                                      "signature": 17, "blank": 1, "address_table": 0}}
    },
    "font": "Calibri",
    "accent_hex": "1F3864",
    "notes": "own = the user's Word files refilled with fill_template.py using map; builtin = build_docs.py with font/accent_hex; script = legacy reference script on the Templates page"
  },
  "research": {
    "library_database": {
      "enabled": false,
      "name": "e.g. IBISWorld",
      "access": "e.g. via State Library Victoria: guides.slv.vic.gov.au/az/ibisworld-australia-company-profiles → Access database",
      "requires_browser": true,
      "terms": "personal research only; summarise, never copy reports"
    },
    "extra_sources": []
  },
  "local_folder": {
    "enabled": false,
    "path": "optional folder on the user's computer for copies of finished files"
  },
  "schedule": {
    "default": "weekdays only, once a day at 07:37 (email check, then drafting, then story tidy); no weekend runs",
    "tasks": [{"name": "Career OS daily run", "id": "trig_…", "cron": "CRON_TZ=<timezone> 37 7 * * 1-5"}]
  }
}
```

Below the JSON block, add a short plain-language explanation for the user of what each part does and a note that they can edit it.

## My Experiences database

Title property: **MY ROLE**. Property names are in capitals so they match across skills.

| Property | Type | Description (put this in the property description) |
|---|---|---|
| MY ROLE | title | "<Role>, <project or theme>", e.g. "Project Lead, Retention Strategy" |
| NO. | number | Story number, 1, 2, 3… |
| YEAR | number | Year the work finished |
| EMPLOYER | text | Who paid you (the employer or consulting firm) |
| FIRM | multi_select | The client or site where the work happened |
| PARENT ORG. | multi_select | Parent group of the firm |
| INDUSTRY | multi_select | Industry of the firm |
| LOCATION | text | City and country |
| SUMMARY | text | One-line summary of the whole story with the headline number |
| BACKGROUND | text | Organisation, situation and why the work mattered |
| CHALLENGE | text | The specific problem and its constraints |
| ACTIONS | text | What you personally did, opening sentence plus labelled bullets |
| OUTCOME | text | Results, endorsements and what happened next |
| ATTRIBUTES | text | Interpersonal traits used to overcome people-related obstacles |
| VALUE ($) | number (currency format of the owner, in thousands per year) | Total benefit delivered ($K p.a.) |
| VALUE (%) | number (percent) | % improvement |
| SKILLS | multi_select | Seed options: Strategy, Business Case, Commercial Modelling, Pricing, Operating Model, Transformation, Project Management, Stakeholder Management, Customer Experience Design, Product Development, Sales, Business Development, Operations, Dashboards, Research, Due Diligence, Valuation, Negotiation, Facilitation, Mentoring, Technology, Software Development, Regulation, Procurement |
| DIRECT REPORTS (#) | number | Roles that reported directly to you |
| LATERAL RELATIONS (#) | number | Distinct people you had to work with to achieve the outcome |
| REPORTING TO (#) | number | Number of leaders you reported to |
| NOTES | text | Currency caveats, "Questions for <name>: …", source resume |

## Job Pipeline database

Title property: **ROLE**, written as "<Employer>, <Role>".

| Property | Type | Notes |
|---|---|---|
| ROLE | title | "<Employer>, <Role>" |
| EMPLOYER | text | |
| STATUS | select | The 13 options in the settings `statuses` list, in order. 00 grey, 01 green, 02 pink, 03–06 blue/grey/orange, 07 yellow, 08 red, 09 brown, 10 green, 11 orange, 12 purple. |
| URL | url | Job ad link. Use the property name "URL", written `userDefined:URL` in tool calls. |
| APP. DUE | date | Closing date |
| EMPLOYER DESC. | text | One paragraph on the employer, in the owner's currency |
| JOB DESC. | text | Summary of the role |
| RESPONSIBILITIES | text | |
| REQS. | text | Requirements |
| NOTES | text | Status history lines, "IBISWorld pending", "Job description needed" |
| APP - CV | files | Resume PDF + DOCX |
| APP - CL | files | Cover letter PDF + DOCX |
| APP - OTHER | files | Selection criteria responses etc. |
| ADD. INFO. | files | Research files (annual reports, results) |

Create a board view grouped by STATUS, sorted by STATUS ascending.

## Status meanings

| Status | Meaning | Who sets it |
|---|---|---|
| 00 - INBOX | Saved by the user, waiting for drafting | User (phone share sheet or manually) |
| 01 - DRAFT | Research, resume and cover letter attached; ready for review | job-application-drafter |
| 02 - SUBMITTED | Applied | User, or pipeline-status-tracker from a confirmation email |
| 03 - INT SCREEN | Recruiter/HR screening | pipeline-status-tracker |
| 04 - INT FIT | Hiring manager / behavioural interview | pipeline-status-tracker |
| 05 - INT CASE | Case study, assessment, presentation | pipeline-status-tracker |
| 06 - INT FINAL | Final round / executive panel | pipeline-status-tracker |
| 07 - NEGOTIATION | Offer, salary, references | pipeline-status-tracker |
| 08 - ACCEPTED | Offer accepted | User only |
| 09 - REJECTED - FIRM | Employer said no | pipeline-status-tracker |
| 10 - REJECTED - ME | User withdrew or declined | pipeline-status-tracker (from sent mail) or user |
| 11 - ARCHIVED | Kept for reference | User |
| 12 - EXPIRED | Closed without applying | User (tracker may suggest) |
