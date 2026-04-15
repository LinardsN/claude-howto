# Session 3: Reusable QA Workflows -- Skills

You have a project with standards. Now you will create reusable workflows that encode QA expertise into skills Claude can invoke automatically. Skills are the building blocks that later sessions will compose into agents (Session 4) and bundle into a plugin (Session 7).

## Learning Objectives

- Create SKILL.md files with YAML frontmatter that enables auto-invocation
- Understand progressive disclosure: metadata, instructions, and bundled resources
- Build skills with supporting files (templates, scripts) for richer functionality
- Use `context: fork` to run skills in an isolated context window
- Verify auto-invocation by describing your need in natural language

## Prerequisites

- Session 2 gate passed (`./bootcamp complete-session 2`)
- CLAUDE.md with QA standards defined
- Test case CRUD feature working

## Schedule

| Time | Activity | Duration |
|------|----------|----------|
| 0:00 | Review skills concept and progressive disclosure | 10 min |
| 0:10 | Create the generate-test-suite skill | 30 min |
| 0:40 | Create the qa-review skill | 20 min |
| 1:00 | Build test suite listing page | 15 min |
| **Total** | | **75 min** |

## The Feature: Skills

> **Reference module**: [03-skills/README.md](../../03-skills/README.md)

Skills are reusable capabilities packaged as SKILL.md files. They go beyond simple slash commands by supporting auto-invocation, progressive disclosure, supporting files, and isolated execution contexts.

### Progressive Disclosure Architecture

Skills load information in stages to manage context efficiently:

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| **Level 1: Metadata** | Always (at startup) | ~100 tokens | `name` and `description` from frontmatter |
| **Level 2: Instructions** | When triggered | Under 5k tokens | SKILL.md body (instructions, constraints) |
| **Level 3: Resources** | As needed | Effectively unlimited | Supporting files (templates, scripts, docs) |

This means you can have dozens of skills without consuming context -- only the metadata is loaded until a skill is invoked.

### SKILL.md Frontmatter

```yaml
---
name: generate-test-suite
description: Generate a comprehensive test suite using ISTQB test design techniques including boundary value analysis, equivalence partitioning, and decision tables
version: 1.0.0
---
```

Key frontmatter fields:

| Field | Purpose |
|-------|---------|
| `name` | Slash command name (`/generate-test-suite`) |
| `description` | Auto-invocation trigger -- Claude matches natural language to this |
| `version` | Semantic version for tracking changes |

### Auto-Invocation

The `description` field is the key to auto-invocation. When you say something like "I need test cases for the authentication module," Claude scans all skill descriptions and invokes the best match. A good description contains the keywords and phrases that naturally appear in requests for that skill.

### Context: Fork

Adding `context: fork` to a skill's behavior causes it to execute in an isolated context window. This prevents the skill's work from polluting your main conversation:

```yaml
---
name: qa-review
description: Review code changes from a QA perspective checking for testability, error handling, edge cases, and security concerns
context: fork
---
```

### Supporting Files

Skills can bundle templates, scripts, and documentation alongside the SKILL.md:

```text
.claude/skills/
  generate-test-suite/
    SKILL.md
    templates/
      test-suite-template.md
      boundary-value-template.md
    scripts/
      analyze-endpoints.sh
```

The SKILL.md instructions can reference these files, and Claude will read them as needed (Level 3 disclosure).

## What You Will Build

### 1. `/generate-test-suite` Skill

A skill that generates comprehensive test suites using ISTQB test design techniques. When invoked, it should:

- Accept a feature or module name as input
- Apply test design techniques: boundary value analysis, equivalence partitioning, decision tables, state transition testing
- Generate test cases following your CLAUDE.md data model (from Session 2)
- Organize test cases by technique and priority
- Output a structured test suite with traceability to requirements

Think about what a QA lead would want when they say "generate a test suite for user authentication." The skill should produce professional-grade test cases, not generic placeholders.

### 2. `/qa-review` Skill

A skill that reviews code from a QA perspective. Unlike a standard code review that focuses on style and patterns, this review focuses on:

- Testability: Is the code structured so it can be tested? Are dependencies injectable?
- Error handling: Are all error paths covered? Do they provide useful feedback?
- Edge cases: What happens with null inputs, empty strings, boundary values?
- Security: Are inputs validated? Is data sanitized? Are there injection risks?
- Observability: Is there logging for debugging test failures?

This skill should use `context: fork` so the review happens in isolation.

### 3. Test Suite Listing Page

A React page that displays test suites with:

- Suite name, creation date, and associated feature/module
- Status badges (pass/fail/pending/in-progress)
- Count of test cases per suite
- Link or navigation to view individual test cases within a suite

This builds on the test case CRUD from Session 2 by adding the concept of a test suite as a container for related test cases.

## Requirements

### Must-Have (Gate Checks)

- [ ] At least 2 SKILL.md files exist in `.claude/skills/` with valid YAML frontmatter
- [ ] Both skills have a `name` field in frontmatter
- [ ] Both skills have a `description` field in frontmatter (required for auto-invocation)
- [ ] SKILL.md body contains meaningful instructions (not just frontmatter)
- [ ] Test suite listing page exists as a React component
- [ ] Test suite page renders without errors

### Should-Have (Bonus Points)

- [ ] A skill includes supporting template files in a `templates/` subdirectory
- [ ] Auto-invocation works: typing a natural language request triggers the appropriate skill
- [ ] Skills reference ISTQB test design techniques by name
- [ ] `/qa-review` skill uses `context: fork` for isolated execution
- [ ] Test suite page displays status badges (pass/fail/pending)
- [ ] Skills reference the CLAUDE.md standards from Session 2

## Rules

1. **Skills must be QA-domain-specific.** Do not create generic coding skills like "refactor code" or "add comments." Every skill should solve a QA engineering problem.

2. **The description field must enable auto-invocation.** Write descriptions as natural language sentences containing the keywords someone would naturally use when requesting that capability.

3. **Skills must reference your standards.** Your `/generate-test-suite` skill should produce test cases that follow the data model you defined in CLAUDE.md (Session 2). If your standards say severity levels are "critical, major, minor, trivial," the generated test suite must use those exact levels.

4. **Build the skills before the page.** Create and test both skills first, then build the React page. The page should work with the test suite structure your skills generate.

## Hints (Not Solutions)

### Building the Generate-Test-Suite Skill

- Think about what input the skill needs. A feature name is the minimum. But what about the type of testing (functional, integration, security)? What about the depth of coverage?
- ISTQB test design techniques are well-defined. Your skill instructions should describe when to apply each technique: boundary value analysis for input ranges, equivalence partitioning for input classes, decision tables for complex business logic.
- Consider including a test suite template as a supporting file. The template gives Claude a concrete structure to fill in, which produces more consistent output.

### Building the QA-Review Skill

- A QA review is different from a code review. Focus on what a QA engineer cares about: "Can I test this? What would break this? What is not handled?"
- Using `context: fork` means this skill runs in its own context. Describe clearly in the SKILL.md body what files to analyze and what format the review should take.
- Think about the output format. A QA review might produce findings categorized by risk level (high, medium, low) with specific recommendations.

### Building the Test Suite Page

- Ask Claude to create the data model for test suites, then the API routes, then the React page. Reference your CLAUDE.md conventions.
- Test suites are containers for test cases. The data model needs a relationship between suites and the test cases from Session 2.
- Status badges are a common UI pattern. Think about what statuses a test suite goes through: draft, ready, in-progress, passed, failed.

### Testing Auto-Invocation

- After creating your skills, try invoking them with natural language instead of the slash command. Say something like "I need a test suite for the login feature" or "review the test case API code from a QA perspective."
- If auto-invocation does not trigger, revisit your `description` field. It may not contain the keywords Claude needs to match.

## Verification

Before running `./bootcamp complete-session 3`, verify:

1. **Skills exist**: Check `.claude/skills/` for at least 2 directories with SKILL.md files
2. **Frontmatter is valid**: Each SKILL.md has `name` and `description` in the YAML frontmatter
3. **Slash commands appear**: Type `/` in Claude Code REPL and confirm your skills are listed
4. **Auto-invocation works**: Try a natural language request and see if the right skill triggers
5. **Test suite page renders**: Navigate to the test suite page in your browser
6. **Integration with Session 2**: Generated test suites use the data model and severity levels from your CLAUDE.md

```bash
./bootcamp complete-session 3
```

## What Comes Next

In Session 4, you will create specialized subagents that use these skills. Your test-writer agent will invoke `/generate-test-suite`, and your bug-triager agent will use domain knowledge from your skills. The agents add a layer of specialization on top of the reusable skills you built here.
