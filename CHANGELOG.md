
## 2026-09-06 BSX audit

I found that verification ignored changed parameters, missing manifest sections and paths outside the project. Verification now checks the parameter digest, schema, sections, file sizes and containment; construction rejects non-finite parameters. Regressions inject the defects.
