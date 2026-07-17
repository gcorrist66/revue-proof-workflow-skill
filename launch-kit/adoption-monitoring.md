# Adoption monitoring without product telemetry

revüe does not phone home. The bundled validation layer uses local files and requires no network or
credentials. That is a trust advantage, but it means there is no exact cross-platform active-user
count.

Use a small scorecard of observable signals and label each one honestly.

## What each metric means

| Metric | Where | What it measures | What it does **not** prove |
| --- | --- | --- | --- |
| Unique cloners | GitHub Traffic | Distinct clients that cloned in GitHub's rolling 14-day window | People, successful installs, or continued use |
| Total clones | GitHub Traffic | Clone events in the rolling window | Unique users; automation may contribute |
| Stars | GitHub | People/accounts that bookmarked publicly | Active use |
| Forks | GitHub | Public forks | Production adoption |
| Release downloads | GitHub Releases | Downloads of attached installer assets | Marketplace installs or successful executions |
| Referring sites | GitHub Traffic | Domains sending repository visitors | Conversion or continued use |
| Directory installs | Anthropic directory | Installs reported by Anthropic, if exposed after approval | Cross-runtime use outside Anthropic |
| Product Hunt votes/comments | Product Hunt dashboard | Launch interest and discussion | Installs or retained users |
| Post analytics | LinkedIn/X/Dev.to/Hashnode | Reach, clicks, saves, and discussion | Product use |
| Self-reported use | Issues, discussions, consulting leads | Named use cases with context | Total population |

## Weekly GitHub commands

Run while authenticated with GitHub CLI:

```bash
gh api repos/gcorrist66/revue-proof-workflow-skill/traffic/clones
gh api repos/gcorrist66/revue-proof-workflow-skill/traffic/views
gh api repos/gcorrist66/revue-proof-workflow-skill/traffic/popular/referrers
gh api repos/gcorrist66/revue-proof-workflow-skill/traffic/popular/paths
gh api repos/gcorrist66/revue-proof-workflow-skill \
  --jq '{stars:.stargazers_count,forks:.forks_count,watchers:.subscribers_count,open_issues:.open_issues_count}'
gh api repos/gcorrist66/revue-proof-workflow-skill/releases \
  --jq '[.[] | {tag:.tag_name,assets:[.assets[]|{name,downloads:.download_count}]}]'
```

GitHub exposes traffic for only a rolling 14-day window. Capture it weekly so the history is not lost.

## Baseline — 2026-07-17, before coordinated launch

| Signal | Baseline |
| --- | ---: |
| Unique cloners, rolling 14 days | 59 |
| Total clones, rolling 14 days | 124 |
| Unique repository visitors, rolling 14 days | 1 |
| Total repository views, rolling 14 days | 5 |
| Stars | 0 |
| Forks | 0 |
| v1.2.0 installer downloads | 0 |
| Referring sites reported | none |

The clone baseline is **not** a user count. It may include automated systems, repeated environments,
and owner/development activity. Treat changes after launch as directional until a user self-identifies
or a platform exposes an install metric.

## Weekly scorecard

Record each Monday with a timestamp and source:

```text
Week ending:
GitHub unique cloners (14d):
GitHub total clones (14d):
Stars / forks:
Release downloads:
Top referrers:
Anthropic directory installs:
Product Hunt views / upvotes / outbound clicks:
LinkedIn impressions / link clicks / saves:
X impressions / link clicks / bookmarks:
Dev.to or Hashnode views / reactions:
Self-reported active teams or individuals:
Qualified consulting inquiries mentioning revüe:
Notes and source links:
```

## Reporting rule

Publicly report only dated, sourced numbers. Prefer:

> 17 people have told us they use revüe as of 2026-09-01.

Avoid:

> revüe has 59 users.

when the only evidence is GitHub's unique-cloner count.

