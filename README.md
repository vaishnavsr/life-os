# Life OS

Claude plugins that run parts of your life on Notion and email. There's one plugin per life area, and each area follows the same pattern:

- **Check**: periodically measure progress against your long-term targets.
- **Change**: adjust course when a check shows you're off track.
- **Concentrate**: the everyday work, where about 80% of the effort goes.

## Plugins

| Plugin | Life area | What it does | Status |
|---|---|---|---|
| [**career-os**](plugins/career-os) | Contributions: career, voluntary work, creations | Experience library from old resumes and story interviews; a researched resume and cover letter for every job you save; an application pipeline that updates itself from your inbox; interview prep and debriefs | Available (v0.4.0) |

More areas (health, home, relationships, learning, wealth, legacy) may follow.

## Install
1. In Claude, open **Settings → Connectors** and connect **Notion** and **Gmail**.
2. In Claude's plugin settings, add the marketplace `vaishnavsr/life-os`, then install the plugins you want (start with **career-os**). In Claude Code, run:

   ```
   /plugin marketplace add vaishnavsr/life-os
   /plugin install career-os@life-os
   ```
3. Start a new chat and say **"set me up"**.

See the [Career OS README](plugins/career-os/README.md) for what setup does, the Claude plan you need, and day-to-day use.

## Credits
Career OS bundles **Interview Coach** by Noam Segal (https://github.com/noamseg/interview-coach-skill) under the MIT licence.

## Safety by design
These plugins never send email, never submit applications or forms on your behalf, and never type or store your passwords. Your data stays in your own Notion; nothing personal lives in this repository.

## Licence
MIT.
