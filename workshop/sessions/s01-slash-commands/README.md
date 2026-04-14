# Session 1: First Contact -- Slash Commands

Your first hands-on session with Claude Code. You will explore the CLI, discover built-in commands, scaffold a full-stack project from nothing, and create your first custom slash commands -- all without writing a single line of code manually.

## Learning Objectives

- Navigate the Claude Code CLI and understand its interactive REPL
- Explore built-in slash commands (`/help`, `/status`, `/model`, `/cost`, `/compact`)
- Scaffold a full-stack Express + React (Vite) project using only Claude Code prompts
- Create custom slash commands via SKILL.md files with YAML frontmatter
- Understand how slash commands fit into the broader Claude Code feature set

## Prerequisites

- Claude Code CLI installed and authenticated (`claude --version` returns a version)
- Node.js 18+ and npm installed (`node --version`)
- Git configured with a GitHub account (`git config --global user.name`)
- Bootcamp setup completed (`./bootcamp setup`)

## Schedule

| Time | Activity | Duration |
|------|----------|----------|
| 0:00 | Explore built-in slash commands | 15 min |
| 0:15 | Scaffold the QA Command Center project | 30 min |
| 0:45 | Create custom slash commands | 30 min |
| **Total** | | **75 min** |

## The Feature: Slash Commands

> **Reference module**: [01-slash-commands/README.md](../../01-slash-commands/README.md)

Slash commands are shortcuts you type in the Claude Code REPL to control behavior, get information, or trigger workflows. They come in several varieties:

### Built-in Commands

Claude Code ships with 60+ built-in commands. Some essentials for this session:

| Command | What It Does |
|---------|--------------|
| `/help` | Shows available commands and usage guidance |
| `/status` | Displays current model, account, and session info |
| `/model` | Switch between models (use left/right arrows for effort level) |
| `/cost` | Shows token usage and cost for the current session |
| `/compact` | Compresses conversation history to free up context space |
| `/init` | Initializes a CLAUDE.md file (you will use this heavily in Session 2) |
| `/skills` | Lists all available skills/custom commands |

Type `/` in the REPL and start typing to filter the full list. Spend the first 15 minutes discovering what is available.

### Custom Slash Commands via SKILL.md

You create custom commands by placing `SKILL.md` files in `.claude/skills/`. Each file needs YAML frontmatter at the top:

```yaml
---
name: my-command
description: What this command does (used for auto-invocation matching)
---
```

The body of the file contains the instructions Claude follows when the command is invoked. You invoke it by typing `/my-command` in the REPL, or Claude may auto-invoke it when your natural language matches the description.

Key points about SKILL.md files:

- The `name` field becomes the `/command-name` in the REPL
- The `description` field enables auto-invocation -- Claude matches your natural language to this description
- The body contains instructions, constraints, and templates that guide Claude's behavior
- Skills can reference supporting files (templates, scripts) in their directory

## What You Will Build

### 1. QA Command Center -- Project Scaffold

A full-stack web application that you will build across all 10 sessions:

- **Backend**: Express.js server with a health check endpoint
- **Frontend**: React app via Vite with a landing page
- **Project structure**: `package.json` with scripts, `server/` and `client/` directories
- **Landing page**: A branded welcome page for "QA Command Center" with your name and TestDevLab branding

This is a monorepo structure where `npm run dev` starts both the Express server and the Vite dev server concurrently.

### 2. Custom Slash Commands

Two QA-focused custom commands that you will use throughout the bootcamp:

- **`/new-test-case`** -- Generates a structured test case following QA best practices. Think about what fields a professional test case needs: title, preconditions, test steps, expected results, severity classification, and more.

- **`/bug-report`** -- Generates a structured bug report. Consider the standard defect report fields: summary, environment, reproduction steps, actual vs expected behavior, severity, priority, attachments.

## Requirements

### Must-Have (Gate Checks)

These are validated automatically when you run `./bootcamp complete-session 1`:

- [ ] `package.json` exists in the project root with `express` and `react` as dependencies
- [ ] A `server/` directory exists with at least one `.js` or `.ts` file
- [ ] A `client/` directory exists with React source files
- [ ] `npm run dev` starts the application without errors
- [ ] At least 1 SKILL.md file exists in `.claude/skills/` with valid YAML frontmatter
- [ ] The landing page is accessible in a browser when the dev server is running

### Should-Have (Bonus Points)

These earn additional points but are not required to pass the gate:

- [ ] 2 custom SKILL.md files (`/new-test-case` and `/bug-report`)
- [ ] Landing page includes TestDevLab branding (logo, colors, or name)
- [ ] Landing page displays the project name "QA Command Center"
- [ ] Both custom commands produce structured, QA-domain-specific output when invoked
- [ ] `npm run dev` uses `concurrently` to start both server and client

## Rules

1. **Use Claude Code for everything.** Do not manually create files, write code, or edit configurations. Every file in your project should be generated by Claude Code.

2. **Explore before you create.** Spend the first 15 minutes trying at least 3 different built-in slash commands. Understand what tools are already available before building custom ones.

3. **Think in QA terms.** You are a QA engineer building tools for QA engineers. Your slash commands should reflect QA domain knowledge -- ISTQB terminology, standard test case structures, professional defect reporting formats.

4. **One thing at a time.** Ask Claude to scaffold the project first. Get it running. Then move on to creating custom commands. Do not try to do everything in a single prompt.

## Hints (Not Solutions)

These hints guide your thinking without giving you the exact prompts to use.

### Scaffolding the Project

- Describe the tech stack you want (Express backend, React frontend with Vite, monorepo structure). Be specific about how you want the dev scripts to work.
- Think about what a QA Command Center landing page should communicate. What would a QA engineer want to see when they first open the app?
- If the scaffold does not start cleanly, describe the error to Claude and ask it to fix the issue. Iterative refinement is a core skill.

### Creating Custom Commands

- Before creating `/new-test-case`, think about what fields a professional test case includes. Reference ISTQB standards: test case ID, title, preconditions, test steps (action + expected result per step), postconditions, priority, severity, test type (functional, non-functional, regression).
- For `/bug-report`, consider the defect lifecycle. A good bug report needs environment details, reproduction steps that someone else can follow, severity vs priority distinction, and attachment placeholders.
- The `description` field in your SKILL.md frontmatter matters. Write it so that when you later say "I need to create a test case for the login feature," Claude knows to invoke your skill automatically.

### Common Pitfalls

- If `npm run dev` fails, check that all dependencies are installed (`npm install`). Ask Claude to diagnose the issue.
- If your custom command does not appear when you type `/`, verify the file is in `.claude/skills/` (not `.claude/commands/`, though that also works) and has valid YAML frontmatter with `---` delimiters.
- Vite and Express need to run on different ports. Make sure the scaffold configures this correctly.

## Verification

Before running `./bootcamp complete-session 1`, verify these yourself:

1. **Server runs**: Execute `npm run dev` and confirm no errors in the terminal
2. **Landing page loads**: Open the browser URL shown in the terminal output and see your landing page
3. **Custom command exists**: Type `/` in Claude Code REPL and verify your custom command appears in the list
4. **Custom command works**: Invoke your command (e.g., `/new-test-case`) and confirm it produces structured QA output
5. **Project structure**: Verify `server/` and `client/` directories exist with source files

When you are confident everything works:

```bash
./bootcamp complete-session 1
```

## What Comes Next

In Session 2, you will teach Claude your QA standards by creating a CLAUDE.md file. The project you just scaffolded becomes the foundation for everything you build in the remaining 9 sessions. The custom commands you created here will be referenced by skills (Session 3) and bundled into a plugin (Session 7).
