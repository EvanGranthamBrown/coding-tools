# OVERVIEW
**Name:** Scraper Pipeline

**Description:** Searches the web for dance studios, scrapes their websites, and extracts information about classes, venues, and events.

**Purpose:** Supports a website where users can search for upcoming dance activities near them.

# TECHNOLOGIES
- Infrastructure
    - AWS EC2
    - AWS S3
    - AWS RDS
    - Terraform
- Languages
    - Python
    - SQL
- Storage
    - PostgreSQL
- AI Models
    - AWS Nova
    - Claude

# DUTIES

## Scraping
Functionality:
- Search the web for websites that might have information about dance classes, venues, or events.
- Confirm or reject relevance for each site found.
- For sites confirmed relevant, scrape the website and store the relevant content.
- Poll those sites for updates and store relevant updated content.

Complications:
- 3f9a1c7: Images contain important information not found in text.
- a7d20e4: Sites automatically inject timestamps into their HTML, causing false positives in change detection.
- c58b93f: Storing all pages and images from all sites wastes space and pushes storage costs over budget.
- c58b93f: Sites update daily, but polling all sites daily would push costs over budget.

## Extraction
Functionality:
- Ingest website content captured by scraping.
- Extract dance entities (classes, venues, events) in standardized format.
- Clean entity data and write it to the database.

Complications:
- 3f9a1c7: Images contain important information not found in text.
- 0e6d4a9: Sites contain multiple references to the same entity.
- 0e6d4a9: Multiple references to the same entity may have conflicting information.
- 0e6d4a9: Sites describe repeating events ("Bronze class every Tuesday at 7:15 PM") without specifying individual instances.
- 9b1f7c3: Extraction pushes LLM token costs over budget due to verbosity of JSON format.
- e4c28a6: The same entity is referenced on multiple websites.
- 5d8e0b2: Development can require schema changes to the live database.