# AI Bootcamp Platform — Design Spec

**Date:** 2026-04-15
**Status:** Approved for implementation
**Owner:** LinardsN
**Scope:** Transform the existing CLI-only `workshop/` bootcamp into a production-ready, web-hosted learning platform.

---

## 1. Context

The `workshop/` directory contains a code-complete but untested AI-driven bootcamp platform. Students are meant to learn Claude Code by building a React app called "QA Command Center" over five half-days. Today the bootcamp is a local Python CLI. A hands-on audit found:

- **Platform bugs:** The demo's "struggling student triggers auto-unlock" scenario never fires (Bob's fixture passes S1). Alice's session progression is inconsistent between dashboard and detailed views. Two scoring paths give wildly different numbers (dashboard: 100.0, grade command: 27.5). Prompt-log layout mismatches between the demo's SQLite writes and the analyzer's JSONL reads.
- **Operational gaps:** No `workshop/__init__.py`, no pytest config, Python 3.10+ requirement not enforced at entry (silent `TypeError` on 3.9). Workshop tests not wired into CI. No `./bootcamp doctor` preflight.
- **Missing verification:** AI scoring path via `claude -p` never exercised end-to-end. Atlassian MCP package name unverified. No real-Claude smoke test.
- **Delivery surface:** CLI-only; instructors and students live in terminals. User wants a polished web platform with a Linear/Vercel/Stripe aesthetic and 95% of student journey inside the web UI.

## 2. Goals

1. **Ship a bug-free CLI foundation** (Phase 1) — all tests green, demo correct, ops tooling in place.
2. **Make onboarding one click** (Phase 2) — `.devcontainer/` so students go from link → working environment.
3. **Deliver a professional web platform** (Phase 3) — Astro + React + Supabase + Cloudflare Pages, GitHub OAuth, real-time cohort visibility, full instructor admin, $0 infra cost for the pilot.
4. **Privacy by default** — opt-in leaderboard, private prompts, auditable instructor writes.
5. **Each phase independently shippable.** No throwaway work; Phase 3 reuses all Phase 1 logic unchanged.

## 3. Non-goals

- **No custom in-browser terminal.** GitHub does not allow Codespaces to be iframed (`X-Frame-Options: DENY`). Building xterm.js + ttyd + per-student containers is months of work with real ops cost. Students open their Codespace in a new tab — same pattern as GitHub Classroom.
- **No shared Claude API key / billing proxy.** Students authenticate Claude Code with their own account (`claude /login` via OAuth, free tier or personal Pro subscription). Zero Claude-token cost to the workshop.
- **No real-time chat / forum / comments / video content.** Use Slack/Discord for discussion; curriculum is text + diagrams by design.
- **No mobile admin panel.** Admin is desktop-only.
- **No multi-language UI on day one.** English only for pilot; i18n-ready architecture.
- **No custom workflow builder.** Curriculum is fixed at 10 sessions.
- **Not redesigning curriculum content.** Session guides stay as-is (modulo bug fixes); we render them better.

## 4. System architecture

Four components, each with a clear responsibility boundary:

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUR WEB UI (our domain)                      │
│                 bootcamp.yourdomain.com                         │
│  • Astro + React islands + Tailwind + shadcn/ui                │
│  • Hosted on Cloudflare Pages (free tier, global CDN)          │
│  • All curriculum, dashboards, scoring, admin                   │
└───────────────┬──────────────────────────────┬──────────────────┘
                │ reads/writes                 │ "Open Codespace"
                ▼                              ▼
┌───────────────────────────────┐  ┌──────────────────────────────┐
│   SUPABASE (shared backend)   │  │ GITHUB CODESPACES (per-stu)  │
│ • Postgres (free: 500 MB)     │  │ • Devcontainer auto-boots    │
│ • GitHub OAuth built-in       │  │ • Claude Code CLI installed  │
│ • Row-level security          │  │ • Student runs `claude /login│
│ • Realtime subscriptions      │  │ • VS Code Web terminal       │
│ • Stores: cohorts, profiles,  │  │ • Student's own GH free tier │
│   progress, scores, prompts   │  └──────────────┬───────────────┘
└───────────────▲───────────────┘                 │
                │                                 │ bootcamp CLI runs here
                │ REST after each gate            │
                └─────────────────────────────────┘
                         ┌─────────────────────┐
                         │  bootcamp PYTHON CLI │
                         │ (runs in Codespace)  │
                         │ • gates/scoring      │
                         │ • syncs to Supabase  │
                         └──────────────────────┘
```

**Component responsibilities:**
| Component | Owns | Does not own |
|---|---|---|
| Web UI (Astro) | Rendering curriculum, dashboards, admin forms | Sandboxing, running Claude, storing student files |
| Supabase | Canonical state (profiles, scores, progress, logs), auth, authz (RLS), realtime events | Gate validation logic, AI scoring |
| Codespaces (GitHub) | Sandboxing, file persistence per student, terminal, editor | Curriculum rendering, cohort state |
| Python CLI (`workshop/`) | Gate validation, local scoring, AI-scoring calls, syncing to Supabase | UI, auth, multi-tenant state |

**Key design decisions and why:**
- **Single source of truth is Supabase** (not JSON-in-git, not per-student SQLite). This is required because instructor admin writes (register student, force-unlock, re-grade) from the web UI need a writable backend.
- **Local SQLite stays** in each Codespace as the CLI's scratch store. The CLI writes there first (for offline-resilience), then POSTs to Supabase. If Supabase is down, the CLI still works; it retries on next action.
- **Astro static, React islands only where interactive.** Guides render as static HTML (fastest possible). Dashboards, forms, charts are React islands. Zero client JS on content pages.

## 5. Phased rollout

Each phase is independently shippable and tested with real users before the next begins.

### Phase 1 — Fix the CLI platform (week 1)

Ships a bug-free, tested, documented local CLI. Pilot-testable without any web UI.

**Code fixes:**
1. Add `workshop/__init__.py` to make `workshop` a real package
2. Add `pyproject.toml` at repo root with `[tool.pytest.ini_options] pythonpath = ["."]` so `pytest` works without env vars
3. Add `workshop/requirements-dev.txt` (pytest, ruff, mypy, bandit)
4. Python version guard at `bootcamp` entry point — bail with clear message on < 3.10
5. **Demo fix: Bob's S1 must actually fail.** Remove `.claude/skills/new-tc/SKILL.md` from his fixture so he misses a critical gate. Verify auto-unlock fires at attempt 5 with 20% penalty recorded.
6. **Fix Alice's progression.** The demo's `current-session` file hack doesn't cleanly register S2/S3 completions. Refactor `complete-session` to accept an explicit `--session` override for scripted demos, or fix the demo to use it correctly.
7. **Unify scoring paths.** Today `status --detailed` and `grade ... --no-ai` disagree. The dashboard averages pre-stored per-session scores; `grade` re-runs analyzers. Pick one source of truth: scores are recomputed on `complete-session` and stored; dashboard and `grade` both read stored values.
8. **Fix prompt-log layout.** Demo writes to `prompt_logs` SQLite table; analyzer reads JSONL files from `~/.claude-bootcamp/logs/{student}/session-{N}/prompts.jsonl`. Decide on one format (JSONL on disk, matching what real hooks write), and make demo use it.
9. Verify Atlassian MCP package name via `npm view <pkg>`. Update `INSTRUCTOR-GUIDE.md` and session 5 references with the correct name.
10. Add `./bootcamp doctor` preflight: checks Python version, Claude CLI present, node present, git configured, Codespaces quota (if env indicates Codespaces), Supabase reachable (if configured).

**Tests:**
11. All 45 existing tests must still pass
12. Add tests for: auto-unlock trigger, scoring consistency (dashboard vs grade), JSONL prompt-log round-trip, doctor command
13. Wire workshop tests into `.github/workflows/test.yml`

**Docs:**
14. Write `workshop/PILOT-RUNBOOK.md` — minute-by-minute checklist for running a 2-3 person local pilot

**Exit criteria:** `./demo.sh` runs clean, Bob triggers auto-unlock, all scores consistent, CI green including workshop tests, pilot runbook reviewed.

### Phase 2 — Codespaces-ready (week 2)

Ships a one-click setup. No web UI yet — still CLI-driven from inside the Codespace.

15. `.devcontainer/devcontainer.json` with:
    - Base image: `mcr.microsoft.com/devcontainers/python:3.12`
    - Features: `node:20`, `git`, `github-cli`
    - `postCreateCommand`: install Claude Code (`curl ... | sh`), create venv, install workshop deps
    - `customizations.vscode.extensions`: Python, ESLint, Prettier
16. `.devcontainer/post-create.sh`: verifies Claude Code installed, runs `pytest workshop/tests/ -q` as smoke
17. `README.md` update: "Open in Codespaces" button at top, with clear first-run instructions (`claude /login` → `./bootcamp setup`)
18. Local verification: `devcontainer up` from devcontainer CLI builds successfully
19. CI: add devcontainer-build job using `devcontainers/ci@v0.3`

**Exit criteria:** A person with a fresh GitHub account can: click "Open in Codespaces" → wait for boot (~2 min) → run `claude /login` → run `./bootcamp setup` → start Session 1 — with zero manual install.

### Phase 3 — Web UI (weeks 3-6)

Ships the polished learning platform. See sections 6–11 for full detail.

**Exit criteria:** Five pilot students complete at least S1-S3 via the web UI. No data-loss or auth bugs. Instructor admin operations work. Lighthouse scores > 90.

## 6. Data model

All schema lives in `supabase/migrations/*.sql`, version-controlled.

```sql
-- Cohorts: a group of students moving through the bootcamp together
create table cohorts (
  id text primary key,                        -- 'testdevlab-2026-q2'
  name text not null,
  registration_open boolean default true,
  deadline timestamptz,
  created_at timestamptz default now()
);

-- Profiles: both students AND instructors
create table profiles (
  id uuid primary key references auth.users on delete cascade,
  github_username text unique not null,
  display_name text not null,
  email text,
  role text not null default 'student'
    check (role in ('student','instructor','admin')),
  cohort_id text references cohorts,
  avatar_url text,
  leaderboard_opt_in boolean default false,   -- privacy default
  created_at timestamptz default now()
);

-- Session progress: one row per (student, session)
create table session_progress (
  student_id uuid references profiles on delete cascade,
  session_number int check (session_number between 1 and 10),
  started_at timestamptz,
  completed_at timestamptz,
  gate_passed boolean default false,
  gate_details jsonb,                         -- full CheckResult list
  attempt_count int default 0,
  auto_unlocked boolean default false,
  primary key (student_id, session_number)
);

-- Scores: one row per (student, session)
create table scores (
  student_id uuid references profiles on delete cascade,
  session_number int check (session_number between 1 and 10),
  prompt_quality real,
  efficiency real,
  deliverable_quality real,
  standards_compliance real,
  total real,
  ai_feedback text,                           -- AI-generated feedback excerpt
  scored_at timestamptz default now(),
  primary key (student_id, session_number)
);

-- Prompt logs: captured by hooks inside each Codespace
create table prompt_logs (
  id bigserial primary key,
  student_id uuid references profiles on delete cascade,
  session_number int,
  event_type text check (event_type in ('prompt','response')),
  content text,
  logged_at timestamptz default now()
);
create index on prompt_logs (student_id, session_number);

-- Instructor notes on students
create table instructor_notes (
  id bigserial primary key,
  student_id uuid references profiles on delete cascade,
  instructor_id uuid references profiles,
  note text,
  created_at timestamptz default now()
);

-- Auto-unlock events (auditable)
create table unlock_events (
  id bigserial primary key,
  student_id uuid references profiles on delete cascade,
  session_number int,
  reason text check (reason in ('auto_after_5_attempts','instructor_override')),
  penalty_percent int default 0,
  triggered_by uuid references profiles,      -- null if auto
  created_at timestamptz default now()
);

-- Audit log: every write from instructor UI
create table audit_log (
  id bigserial primary key,
  actor_id uuid references profiles,
  action text not null,                       -- 'register_student', 'unlock_session', 'view_prompts', etc.
  target_id uuid,
  details jsonb,
  created_at timestamptz default now()
);
```

**Migrations approach:** Every schema change is a new file in `supabase/migrations/` with a timestamp prefix, applied via `supabase db push`. Seed data for local dev in `supabase/seed.sql`.

## 7. Authentication & authorization

### Auth flow

**Student:** GitHub OAuth via Supabase Auth.
1. Click "Sign in with GitHub" → Supabase redirects to GitHub OAuth
2. GitHub returns token → Supabase creates `auth.users` row
3. Trigger on `auth.users` inserts auto-creates matching `profiles` row with `role='student'`, `leaderboard_opt_in=false`
4. Onboarding wizard populates `cohort_id`, `display_name`

**Instructor:** Same GitHub OAuth. Role is promoted manually by an admin via SQL or admin panel. First admin is bootstrapped from `INITIAL_ADMIN_GH_USERNAME` env var in a one-shot Supabase function.

**CLI (inside Codespace):** Pair-token flow.
1. Student runs `./bootcamp setup` inside the Codespace
2. CLI prints a one-time pair code (e.g., `A3F7-2K9M`) and a URL: `https://bootcamp.yourdomain.com/settings/cli-pair?code=A3F7-2K9M`
3. Student opens that URL in their browser (they're already logged in there via GitHub OAuth) and clicks "Authorize"
4. Cloudflare Worker endpoint validates the code, mints a Supabase JWT scoped to that student's `auth.uid()`, and makes it retrievable by the CLI
5. CLI polls the endpoint every 2s for ~60s until the token is available; writes it to `~/.claude-bootcamp/.supabase-token` with mode 0600
6. RLS enforces that the JWT can only read/write rows belonging to that `auth.uid()`

Token TTL 30 days; refresh token stored alongside. If expired, CLI re-runs the pair flow.

### Row-level security (RLS)

RLS is enabled on every table. Full policy definitions live in `supabase/migrations/*.sql`; summary:

**profiles:**
- `select`: self, OR `leaderboard_opt_in = true`, OR requesting user is `instructor`/`admin`
- `update`: self only (for `display_name`, `leaderboard_opt_in`), OR admin for role changes
- `insert`: only via auth.users trigger; not user-insertable

**session_progress, scores:**
- `select`: self, OR `(target student's leaderboard_opt_in AND current user authenticated)` for aggregates, OR instructor/admin
- `insert/update`: self (via CLI JWT), OR instructor/admin (for force-unlock, re-grade) — logged to audit

**prompt_logs:**
- `select`: self, OR instructor/admin (triggers `audit_log` entry via Postgres trigger)
- `insert`: self only

**unlock_events, audit_log:**
- `select`: admin only (audit_log), OR self for own unlock_events
- `insert`: handled by triggers and instructor actions

**Privacy guarantees:**
- Prompts are never visible to other students — period, regardless of opt-in
- Leaderboard shows only `leaderboard_opt_in = true` profiles with name/score
- Instructors viewing prompts creates an audit entry
- Students have a self-service "delete my data" action that cascades via `on delete cascade` + a Supabase function call

## 8. Web UI — information architecture

### Route map

```
PUBLIC (no auth required)
  /                              Landing page
  /curriculum                    All 10 sessions overview
  /curriculum/[n]                Individual session guide (read-only for recruitment)
  /leaderboard                   Opt-in students only
  /about                         How the bootcamp works, how it's graded

AUTH
  /sign-in                       GitHub OAuth kickoff
  /auth/callback                 OAuth callback handler

STUDENT (auth, role=student)
  /dashboard                     Home: next session, progress, recent scores
  /dashboard/onboarding          First-time wizard (5 steps)
  /sessions/[n]                  Student view of a session: guide + requirements + Open Codespace
  /sessions/[n]/score            Score breakdown + AI feedback + share card
  /progress                      Full heatmap + charts
  /achievements                  Badges earned/locked
  /settings                      Privacy toggle, delete data, notification prefs

INSTRUCTOR / ADMIN (auth, role in ['instructor','admin'])
  /admin                         Cohort health overview, alerts
  /admin/cohorts                 List + create cohorts
  /admin/cohorts/[id]            Roster, bulk actions
  /admin/cohorts/[id]/register   Add students (form + CSV import)
  /admin/students/[id]           Drill-down: progress, scores, prompts, notes
  /admin/students/[id]/prompts   Prompt log viewer (logs audit entry on view)
  /admin/actions/unlock          Force-unlock flow with penalty selector
  /admin/actions/regrade         Re-grade session
  /admin/export                  CSV/HTML/PDF exports
  /admin/audit-log               Who did what, when
```

### Component library

Built on shadcn/ui primitives (copy-in, we own the source):

**Primitives used:** Button, Card, Dialog, Sheet, Toast, Tabs, Table, Form, Input, Select, Command, Tooltip, Avatar, Skeleton, Dropdown, Separator

**Custom components:**
- `<SessionCard variant="compact|default|featured">` — used on landing, curriculum, dashboard
- `<ScoreBreakdown scores={...}>` — animated 4-bar score visualization
- `<ProgressTimeline sessions={...}>` — horizontal 10-session tracker with states
- `<AchievementBadge earned={bool}>` — with tooltip for unlock criteria
- `<CodeBlock language={} code={}>` — syntax-highlighted, copy-to-clipboard
- `<RequirementsList items={...}>` — checked/unchecked with progressive reveal
- `<LeaderboardRow rank name score grade trend>` — rank display
- `<CohortHealthGrid students={...}>` — instructor's at-a-glance status
- `<AlertBanner severity={} action={}>` — "Bob is stuck" nudges
- `<CommandPalette>` — ⌘K global nav
- `<ShareCard>` — dynamic OG image endpoint for win moments

### Key flows

**Flow 1: Student first-time login (onboarding)**
1. `/` → "Start Bootcamp" → `/sign-in` → GitHub OAuth
2. Returns to `/dashboard/onboarding` (5 steps)
3. Step 1: Welcome + cohort code entry (or auto-assigned)
4. Step 2: Leaderboard opt-in toggle (default OFF, explain trade-offs)
5. Step 3: Open Codespace button → new tab → waits for devcontainer boot
6. Step 4: "Run `./bootcamp setup` in terminal" — polls Supabase for heartbeat POST from CLI
7. Step 5: Done → auto-navigate to `/dashboard`

**Flow 2: Session completion**
1. `/sessions/3` → student reads guide + requirements
2. "Open Codespace" → new tab
3. Student prompts Claude, builds deliverables
4. Runs `./bootcamp complete-session 3` in Codespace terminal
5. CLI runs gate locally → POSTs to Supabase → prints pretty summary
6. Supabase realtime pushes update → web UI's `/sessions/3` tab
7. Requirements animate to checked state, "Session 3 Complete!" overlay
8. Auto-navigate to `/sessions/3/score` after 2s
9. Score bars reveal with AI feedback + share card + "Next: Session 4" CTA

**Flow 3: Instructor intervention**
1. `/admin` shows alert: "Bob stuck on S2 (3 attempts, 2h)"
2. Click → `/admin/students/bob`
3. Review scores, activity timeline; "View prompts" requires justification (logs audit)
4. Add note via `<InstructorNoteForm>` → stored in `instructor_notes`
5. Optional: "Send hint" → picks from session's hint library → in-app notification to Bob
6. Optional: "Force unlock" → modal with penalty selector (default 20%, configurable 0-50%)
7. Action logged in `audit_log` with instructor identity

## 9. Visual design system

**Typography:**
- Display: **Fraunces** (editorial serif; hero headings only)
- Body: **Inter** (14-15px base, optimized tracking, system fallback)
- Mono: **JetBrains Mono** (code blocks, stats, identity accent)
- Modular scale 1.25 ratio; max 3 fonts total

**Color:**
- Dark mode first: `bg-[#0a0a0b]`, `text-[#fafafa]`
- Light mode: `bg-[#faf9f7]` warm off-white, charcoal text
- Single accent: **electric indigo** `#5b5bf8` for primary actions
- Semantic: desaturated success/warning/error (no eye-bleed)
- WCAG AA contrast everywhere; verified in CI via axe-core

**Motion:**
- Framer Motion for meaningful transitions
- Score bars: 1200ms ease-out, staggered 100ms
- Session completion: 3-stage celebration (checkmark 400ms → score fill 1200ms → subtle confetti once)
- Page transitions: View Transitions API where supported
- **`prefers-reduced-motion`: everything becomes instant**

**Layout:**
- 8-point grid system
- Max content width: 768px for reading (guides), 1280px for dashboards
- Generous whitespace (no filled-to-brim feeling)
- Sticky TOC sidebars on long guides
- Mobile: guides fully readable; dashboards use card stack; admin is desktop-only

**Polish details:**
- ⌘K command palette: search sessions, jump pages, toggle theme
- Keyboard shortcuts: `g d` → dashboard, `j/k` → next/prev session, `?` → help
- Empty states: illustrated + actionable
- Loading states: skeleton screens matching final layout (not spinners)
- Error states: conversational tone, clear retry action
- OG images: dynamic per-session, per-win
- Lucide icons throughout (no mixed icon sets)

## 10. Tech stack

### Frontend
| Choice | Why |
|---|---|
| **Astro 4+** | Static-first, markdown-native (renders session guides natively), React islands for interactivity only, top Lighthouse scores |
| **React 18** | Islands only (dashboards, forms, charts) |
| **TypeScript strict** | Non-negotiable for shared-state app |
| **Tailwind CSS + shadcn/ui** | Atomic styling + accessible primitives we own (copy-in pattern) |
| **Framer Motion** | Meaningful animations; reduced-motion aware |
| **Recharts** | Score charts, progress heatmaps |
| **Lucide icons** | Consistent, clean icon set |
| **@supabase/ssr + @supabase/supabase-js** | Auth helpers, realtime client |

**Rejected alternatives (recorded for future reference):**
- Next.js: Astro's island architecture better fits static-heavy content
- Vue/Svelte: ecosystem maturity favors React (shadcn/ui, auth libs)
- Material UI / Chakra: too heavy, too opinionated, hard to achieve distinctive look
- CSS-in-JS: Tailwind is better at this scale

### Backend
| Choice | Why |
|---|---|
| **Supabase Cloud** (Postgres + Auth + Realtime + Storage) | One platform covers DB, GitHub OAuth, RLS, realtime; free tier generous (500MB, 50k MAU) |
| **Cloudflare Workers** (thin server layer) | For endpoints beyond PostgREST (AI scoring orchestration, CSV import, Codespace deep-link generation); free, edge-deployed |

### CLI (Python, additive changes only)
- New module: `workshop/platform/supabase_sync.py` — called from `complete-session`
- **Offline queue:** If Supabase unreachable, pending syncs are written as JSON rows to `~/.claude-bootcamp/sync-queue/`. A new `./bootcamp sync` command flushes the queue when back online. The CLI's local SQLite remains authoritative for offline work; Supabase is the shared mirror.
- Auth token stored in `~/.claude-bootcamp/.supabase-token` (mode 0600)

### Package manager
**pnpm** for the web project (`web/package.json`). Chosen for disk efficiency and strict peer-dep resolution. Repo root stays Python-only; the web project is self-contained.

## 11. Repository layout after all phases

```
claude-howto/
├── .devcontainer/                     # Phase 2
│   ├── devcontainer.json
│   └── post-create.sh
├── .github/workflows/
│   ├── test.yml                       # expanded: Python + markdown + web + devcontainer
│   ├── web-deploy.yml                 # new: Cloudflare Pages deploy
│   └── version-watcher.yml            # existing
├── docs/superpowers/specs/
│   └── 2026-04-15-ai-bootcamp-platform-design.md   # THIS FILE
├── supabase/                          # Phase 3
│   ├── migrations/                    # SQL migrations, version-controlled
│   ├── seed.sql                       # Dev seed (Alice/Bob/Carol)
│   └── config.toml
├── web/                               # Phase 3: Astro site
│   ├── src/
│   │   ├── pages/                     # Astro routes
│   │   ├── components/                # Astro + React islands
│   │   ├── lib/                       # Supabase client, auth helpers, utils
│   │   ├── content/                   # Collections config (sources workshop/sessions/)
│   │   └── styles/
│   ├── public/
│   ├── astro.config.mjs
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
├── workshop/                          # existing, Phase 1 fixes
│   ├── __init__.py                    # new
│   ├── PILOT-RUNBOOK.md               # new
│   ├── platform/supabase_sync.py      # new
│   ├── pyproject.toml                 # new at workshop root for tests
│   └── ...existing...
├── pyproject.toml                     # new at repo root (pytest config)
└── ...existing files...
```

## 12. Deployment

| Piece | Service | How | Cost |
|---|---|---|---|
| Web UI (Astro static) | Cloudflare Pages | Auto-deploy on push to main | Free |
| Serverless endpoints | Cloudflare Workers | Via Pages `functions/` directory | Free (100k req/day) |
| Postgres + Auth + Realtime | Supabase Cloud | `supabase db push` for migrations | Free (500MB, 50k MAU) |
| Codespaces | GitHub | Per-student free tier | Free to workshop, free to students |
| Domain | Cloudflare DNS | Apex + subdomain for staging | $10/yr if custom; else `*.pages.dev` free |

**Total pilot infra cost: $0. Full 500-student cost: ~$25/mo** (Supabase Pro when free-tier MAU crossed).

**Environments:**
- **Local dev:** `supabase start` (Docker) + `pnpm dev` (Astro). Everything works without cloud signups.
- **Staging:** Cloudflare Pages preview branch + separate staging Supabase project. Auto-deploy on PR.
- **Production:** main branch → prod Supabase project → prod Cloudflare Pages project.

**Secrets management:** Cloudflare Pages env vars for public keys (`PUBLIC_SUPABASE_URL`, `PUBLIC_SUPABASE_ANON_KEY`). Cloudflare Workers secrets for service-role keys (`SUPABASE_SERVICE_ROLE_KEY`, `ANTHROPIC_API_KEY`). No secrets in repo.

## 13. Testing strategy

**Phase 1 (CLI):**
- `pytest workshop/tests/` — expand from 45 to ~80 tests, covering new auto-unlock + scoring-consistency + JSONL round-trip cases
- `./demo.sh` exit-0 enforced in CI
- Manual smoke test checklist in `PILOT-RUNBOOK.md` (requires real Claude auth; documented, not automated)

**Phase 2 (Devcontainer):**
- `devcontainers/ci@v0.3` builds the container in GitHub Actions
- `post-create.sh` runs pytest smoke inside
- Claude Code binary presence check

**Phase 3 (Web UI):**
- **Vitest** for utility/logic unit tests
- **Testing Library** for critical component tests (auth, score breakdown, forms)
- **Playwright** E2E for: sign-in, view dashboard, admin register student, complete-session sync, score reveal
- **Playwright screenshot diffs** for canonical pages (landing, dashboard, session guide, score, admin)
- **axe-core** in Playwright — must pass WCAG AA
- **Lighthouse CI** budgets: LCP < 1.5s, CLS < 0.1, TBT < 200ms

**Local dev loop:**
```bash
supabase start                  # local Postgres in Docker
cd web && pnpm dev              # Astro dev server
pytest workshop/tests/          # CLI tests
cd web && pnpm test:e2e         # Playwright
cd web && pnpm lint && pnpm type-check
```

## 14. CI/CD pipeline

**`.github/workflows/test.yml` (on PR and push to main):**
1. **Python job:** ruff → mypy → pytest → `./demo.sh` exit 0
2. **Markdown job:** markdownlint → cross-refs → mermaid → links
3. **Web job:** pnpm lint → type-check → vitest → build → Playwright → axe
4. **Devcontainer job:** build verification via `devcontainers/ci@v0.3`

**`.github/workflows/web-deploy.yml` (on push to main):**
1. Require `test.yml` green
2. Install Supabase CLI via `supabase/setup-cli@v1`
3. `supabase db push --linked` — apply migrations to production DB (uses `SUPABASE_ACCESS_TOKEN` secret)
4. Cloudflare Pages auto-deploys the `web/` build output via its GitHub integration (no explicit step needed once connected)

**All merges blocked by CI.** No flaky tests allowed in main.

## 15. Rollout plan

| Week | Activity | Gate |
|---|---|---|
| 1 | Phase 1 implementation + 2-person local pilot | All tests green, pilot feedback collected |
| 2 | Phase 2 (devcontainer) + same 2 pilots retry via Codespaces | Codespaces boot < 3min, pilot completes S1 |
| 3-5 | Phase 3 build (Astro, Supabase, all routes, admin, polish) | Local dev feature-complete |
| 5 | **User performs 20-min account setup** (Supabase cloud, GitHub OAuth App, Cloudflare Pages, domain) | Prod environment live |
| 5-6 | 5-student pilot through full web UI | Zero data loss, zero auth bugs, Lighthouse > 90 |
| Post-pilot | Evaluate before opening to 500 | Decision gate |

**No full 500-engineer launch until pilot feedback is positive and any issues are patched.**

## 16. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Codespaces free-tier exhaustion | Student can't code | Monitor usage per student; document fallback to local install |
| Supabase free-tier MAU exceeded at scale | Auth breaks | Budget alerts at 80% of limit; upgrade to Pro ($25/mo) pre-emptively before 500-student launch |
| Student's `claude /login` rate-limits | Can't complete session | Document Pro/Max subscription option; bootcamp still works on free tier for moderate use |
| GitHub OAuth outage | No one can log in | Graceful degradation: show "log in failed, try again shortly"; CLI still works against local data |
| Real-time subscription failures | Session completion doesn't auto-advance UI | Fallback: poll every 15s; manual "refresh" button always available |
| Web UI bugs discovered post-launch | Cohort disruption | Staging environment catches most; rapid rollback via Cloudflare Pages; CLI path always works |
| Privacy regression (student prompts leaked) | Legal/HR | RLS policy tests in CI; axe-core for accessibility; manual security review pre-launch |

## 17. Success metrics (for pilot evaluation)

- **Completion rate:** ≥ 80% of pilot students complete at least S1-S5
- **Net-promoter:** Post-pilot NPS ≥ 7/10
- **Zero data loss:** No lost scores, no lost progress
- **Zero privacy incidents:** No student sees another's prompts
- **Ops burden:** < 1 hour/week instructor time during pilot
- **Performance:** Lighthouse ≥ 90 on all major pages; LCP < 1.5s

## 18. Open questions deferred to implementation

These are intentionally not decided in this spec; choose during implementation:

- Exact color tokens for semantic states (wait for design palette work)
- Specific achievement badge criteria and visual design (defer to after core pages are up)
- Final icon set for empty-state illustrations (consider commissioning 5 illustrations vs using an open set like unDraw)
- Email notifications via Supabase functions (out of pilot scope; revisit post-pilot)

---

## Appendix A — Known bugs being fixed in Phase 1 (from audit)

1. Missing `workshop/__init__.py` — tests require `PYTHONPATH=.` workaround
2. No pytest config — `pytest` from repo root fails
3. No Python-version enforcement — silent `TypeError` on 3.9
4. `demo.sh` Bob scenario — passes S1 instead of failing; auto-unlock never fires
5. Alice progression inconsistency — dashboard shows completed sessions, detailed view shows "Not Started"
6. Two scoring paths disagree — dashboard: 100.0, grade: 27.5 for same student
7. Prompt-log format mismatch — demo writes SQLite, analyzer reads JSONL
8. Atlassian MCP package name unverified
9. Workshop tests not in CI
10. No `./bootcamp doctor` preflight

## Appendix B — Files to be created (summary)

**Phase 1:**
- `workshop/__init__.py`
- `pyproject.toml` (repo root, pytest config)
- `workshop/requirements-dev.txt`
- `workshop/platform/doctor.py`
- `workshop/PILOT-RUNBOOK.md`
- Fixes to: `workshop/demo.sh`, `workshop/platform/cli.py`, `workshop/platform/database.py`, `workshop/scoring/scorer.py`, `workshop/scoring/prompt_analyzer.py`, `workshop/hooks/*.sh`, `workshop/INSTRUCTOR-GUIDE.md`

**Phase 2:**
- `.devcontainer/devcontainer.json`
- `.devcontainer/post-create.sh`
- README.md updates

**Phase 3:**
- `supabase/migrations/0001_init.sql` (schema + RLS)
- `supabase/migrations/0002_triggers.sql` (audit triggers)
- `supabase/seed.sql`
- `supabase/config.toml`
- `web/` — full Astro project (~30 route files, ~25 components, config, tests)
- `.github/workflows/web-deploy.yml`
- `workshop/platform/supabase_sync.py`

## Appendix C — User tasks required at deploy time (20 min total)

1. **Create Supabase cloud project** (supabase.com → New Project → copy URL + anon + service-role keys)
2. **Create GitHub OAuth App** (github.com/settings/developers → New OAuth App → copy client ID + secret)
3. **Connect Cloudflare Pages to the GitHub repo** (pages.cloudflare.com → Connect repo → set env vars)
4. **(Optional) Configure custom domain** on Cloudflare DNS
