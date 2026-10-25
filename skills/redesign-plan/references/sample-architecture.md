# OVERVIEW
**Name:** Scraper Pipeline

**Summary:** Two scheduled batch jobs on a single EC2 instance. Each step selects the PostgreSQL rows that need work, does the work, and records the result, so any step can be re-run safely. Scraping keeps snapshots of relevant pages. Extraction turns snapshots into *mentions* of entities, then resolves mentions into the canonical venues, activities, and occurrences that the website reads.

# TECHNOLOGIES
- **AWS EC2:** One instance. Cron runs the CLI jobs.
- **AWS S3:** Page snapshots (visible text) and images.
- **AWS RDS (PostgreSQL):** All other state. Also serves as the work queue; there is no separate queue service.
- **Terraform:** All AWS resources, plus the instance's crontab.
- **Python:** All application code.
- **SQL:** Schema migrations and queries. No ORM.
- **AWS Nova:** High-volume model calls. Micro classifies relevance; Lite (multimodal) extracts entities from text and images.
- **Claude:** Low-volume model calls. Discovers sites via its web search tool; judges ambiguous entity matches.

No technologies added beyond the feature doc.

# DATA MODEL
The website reads `venue`, `activity`, and `occurrence`. All other tables are internal.

- `site`: A discovered site. Relevance verdict, poll interval, `next_poll_at`.
- `page`: A relevant page. URL, current fingerprint, fingerprint at last extraction, S3 snapshot key.
- `venue_mention`, `activity_mention`: One reference to an entity, as extracted from one page. Extracted fields, plus FK to the resolved entity.
- `venue`, `activity`: Canonical entities. `activity.kind` is `class` or `event`; `activity.recurrence` is an iCalendar RRULE, or null for one-time events.
- `occurrence`: One dated instance of an activity.
- `schema_migration`: Migration files already applied.

# CODE FLOWS
```
discover (weekly):  discover_sites ─► classify_site ─► site

update (hourly):    crawl_sites ─► page + S3 snapshot
                    ─► extract_mentions ─► venue_mention / activity_mention
                    ─► resolve_mentions ─► venue / activity
                    ─► expand_occurrences ─► occurrence
```

## Discover (`cli discover`, weekly)
1. `discover_sites()` asks Claude, with web search, for dance-related sites in each configured region.
2. `classify_site()` has Nova Micro judge each new site from its homepage text. Rejected sites are kept so they aren't re-checked.

## Update (`cli update`, hourly)
Four steps, in order. Each acts only on rows that need it.
1. **Poll.** For each relevant site past its `next_poll_at`, `crawl_sites()` fetches the site's pages, fingerprints them with `fingerprint()`, classifies new ones with `classify_page()`, and saves changed relevant pages with `store_snapshot()`. `next_poll_at()` schedules the site's next poll.
2. **Extract.** For each page whose fingerprint changed since its last extraction, `extract_mentions()` sends the snapshot's text and images to Nova Lite. `parse_rows()` validates and normalizes the output into mentions, which replace that page's previous mentions.
3. **Resolve.** `resolve_mentions()` links each unlinked mention to an existing entity, or creates one. `merge_entity()` recomputes each affected entity from all of its mentions. Entities left with no mentions are retired.
4. **Expand.** `expand_occurrences()` regenerates `occurrence` rows for changed activities and extends all activities' occurrences to eight weeks out.

# DIRECTORY STRUCTURE
```
scraper-pipeline/
├── infra/                    Terraform: EC2, RDS, S3, IAM, crontab
├── migrations/               0001_initial.sql, 0002_….sql; forward-only
├── src/scraper_pipeline/
│   ├── cli.py                Entry points: discover, update, migrate
│   ├── db.py                 connect(), run_migrations()
│   ├── llm.py                ask_nova(), ask_claude()
│   ├── models.py             One dataclass per table
│   ├── prompts/              One text file per LLM prompt
│   ├── scraping/
│   │   ├── discover.py       discover_sites(), classify_site()
│   │   ├── crawl.py          crawl_sites(), classify_page(), fingerprint()
│   │   ├── snapshot.py       store_snapshot(), load_snapshot()
│   │   └── schedule.py       next_poll_at()
│   └── extraction/
│       ├── extract.py        extract_mentions(), parse_rows()
│       ├── resolve.py        resolve_mentions(), merge_entity()
│       └── occurrences.py    expand_occurrences()
└── tests/                    Mirrors src/; runs against a local PostgreSQL
```

# COMPONENTS
Components call each other only through the functions listed under "Exposes"; everything else is internal. Pipeline steps also hand off work through tables, so each component lists what it writes. Every column has exactly one writer. The website is outside this system; it depends only on the tables Entities writes.

- **Database** (`db.py`, `models.py`, `migrations/`): Schema, connections, and row types.
    - Exposes: `connect() -> Connection`, `run_migrations(conn)`, one dataclass per table
    - Writes: `schema_migration`
- **LLM** (`llm.py`, `prompts/`): All model calls. Loads prompts by name; handles retries and rate limits.
    - Exposes: `ask_nova(prompt_name, *, model, text, images) -> str`, `ask_claude(prompt_name, *, text, web_search) -> str`
- **Discovery** (`scraping/discover.py`): Finds candidate sites and judges their relevance.
    - Exposes: `discover_sites(conn, regions)`
    - Writes: new `site` rows and their relevance verdicts
    - Uses: Database, LLM
- **Crawler** (`scraping/crawl.py`, `snapshot.py`, `schedule.py`): Polls relevant sites that are due and snapshots changed pages.
    - Exposes: `crawl_sites(conn)`; `load_snapshot(page) -> Snapshot`, which returns a page's visible text and images
    - Writes: `site` poll interval and `next_poll_at`; `page` rows, except fingerprint at last extraction; S3 snapshots and images
    - Uses: Database, LLM
- **Extraction** (`extraction/extract.py`): Turns changed pages into mentions.
    - Exposes: `extract_mentions(conn)`
    - Writes: `venue_mention` and `activity_mention` rows, except their entity FKs; `page` fingerprint at last extraction
    - Uses: Database, LLM, Crawler (`load_snapshot()`)
- **Entities** (`extraction/resolve.py`, `extraction/occurrences.py`): Turns mentions into the tables the website reads.
    - Exposes: `resolve_mentions(conn)`, `expand_occurrences(conn)`
    - Writes: `venue`, `activity`, `occurrence`; entity FKs on mention rows
    - Uses: Database, LLM
- **CLI** (`cli.py`): Entry points. Runs the steps in order; each step function selects its own rows.
    - Exposes: `cli discover`, `cli update`, `cli migrate`
    - Uses: Database, Discovery, Crawler, Extraction, Entities
- **Infrastructure** (`infra/`): AWS resources and the crontab.
    - Exposes: crontab entries for `cli discover` (weekly) and `cli update` (hourly); environment variables `DATABASE_URL`, `SNAPSHOT_BUCKET`, `ANTHROPIC_API_KEY`, `NOVA_API_KEY`

# COMPLICATIONS
- **3f9a1c7: Images carry information not in the text.** Snapshots include the images on relevant pages. Extraction sends text and images together to Nova Lite, which is multimodal.
- **a7d20e4: Injected timestamps cause false change detection.** `fingerprint()` hashes visible text and image URLs (minus query strings), not raw HTML, so timestamps in markup, scripts, or cache-busting URLs don't register as changes.
- **c58b93f: Storing every page and image is over budget.** Only relevant pages are stored, as visible text rather than HTML, and only their latest version. Images are stored once per content hash, so shared logos and banners aren't duplicated.
- **c58b93f: Polling every site daily is over budget.** Each site has its own poll interval: halved when a poll finds changes, doubled when it doesn't, clamped to 1–28 days. Routine polls fetch only the site's known relevant pages; a full crawl for new pages runs monthly.
- **0e6d4a9: A site references the same entity several times.** Extraction outputs mentions, not entities. Resolution links all mentions of one entity to a single row.
- **0e6d4a9: References conflict.** `merge_entity()` recomputes each entity field by field from all its mentions; the most recently changed source page wins. Because entities are always derived from mentions, re-running the merge is safe, and rule changes apply retroactively.
- **0e6d4a9: Recurring activities have no listed instances.** Nova outputs a recurrence rule rather than dates. `expand_occurrences()` turns rules into dated `occurrence` rows.
- **9b1f7c3: JSON output is too token-expensive.** Extraction prompts request tab-separated rows with a fixed column order per entity type, so field names never appear in the output.
- **e4c28a6: Several sites reference the same entity.** Resolution spans all sites. `resolve_mentions()` matches venues by normalized address, and activities by venue, weekday, start time, and normalized name. Mentions with close but inexact candidates go to Claude for a same-or-different judgment.
- **5d8e0b2: Schema changes on a live database.** Each change is a numbered, forward-only SQL file. `cli migrate` applies pending files in order, one transaction each, and records them in `schema_migration`; every deploy runs it first. Breaking changes are split into expand and contract migrations across two deploys.

# USER REVIEW ITEMS
- The roadmap says studio owners will be able to create accounts on the website and edit their own listings, but it doesn't say how this will be integrated with automatic scraping. I assumed this would be handled at a later stage and kept it out of scope for the pipeline.
- Nothing indicates how the system should access Claude and Nova. I chose to connect through their developer APIs (api.anthropic.com, api.nova.amazon.com) rather than using AWS Bedrock.