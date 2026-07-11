---
name: html-to-email
description: Use when the user provides an HTML file and wants it converted into email-client-safe HTML that renders correctly across Outlook (desktop/mobile), Gmail, Apple Mail, and Yahoo — e.g. "make this email safe", "convert to email HTML", "email-compatible HTML", "make this safe to paste into Outlook", or the HTML needs tables, CSS inlining (premailer), dark mode, or Outlook conditionals. Also use when the user mentions mjml, Litmus, or Email on Acid workflows.
---

# HTML to Email Converter

Convert a source HTML file into email-client-safe HTML, outputting a new file.

If the user mentions copying or pasting into Outlook, treat that as a separate rendering target from normal sent-email HTML and apply the Outlook paste-safe rules in the reference.

## Process

1. Read the source HTML file.
2. Read [references/email-html-rules.md](references/email-html-rules.md) for the full compatibility ruleset (layout, CSS, dark mode, Outlook conditionals, images, typography, links, gotchas by client).
3. Analyze the source HTML and identify what needs transformation:
   - Layout method (`flexbox`/`grid`/`div` → tables)
   - CSS location (external or `<style>` → inline)
   - Unsupported properties to remove or replace
   - Images missing attributes
   - Missing email boilerplate (DOCTYPE, meta tags, MSO conditionals)
   - Whether the target is standard email rendering or Outlook copy/paste
4. Transform the HTML applying the rules from the reference.
5. Verify the output against [eval/checklist.md](eval/checklist.md). For the critical spacer-row failure (white banded rows in Outlook paste), compare against `examples/good-spacer-row.html` and `examples/bad-spacer-row.html`.
6. Write the output to `{original-name}-email.html` in the same directory.
