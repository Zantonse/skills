---
name: fact-checker
description: This skill should be used when the user asks to "check for hallucinations",
  "verify facts", "audit content accuracy", "find AI inference", or mentions
  reviewing content for factual claims, unverified assertions, or made-up references.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch, Bash(wc *)
---

# Content Fact-Checker

Audit content files for factual accuracy. Identify hallucinations, unverified claims, AI inference stated as fact, and fabricated references.

## Process

This skill uses **parallel subagents** for efficient, isolated fact-checking.

1. Identify the target files. If the user specifies files, use those. If not, scan `content/` for all `.mdx` files using Glob.

2. Group files logically (by module, by directory, or by content type). Aim for 3-5 files per group to balance subagent context usage.

3. **Dispatch parallel subagents** — one per group. Use the Task tool with `subagent_type: "general-purpose"`. Each subagent receives:
   - The list of files to audit
   - The full classification system (copied below)
   - The verification standards (copied below)
   - Instructions to return a structured report

4. Wait for all subagents to complete. Aggregate their reports into a single consolidated finding.

## For Each Subagent: Classification System

Read each assigned file completely. For every factual claim, classify it:

   **VERIFIABLE FACT** — A specific, checkable claim. Examples:
   - Named tools, libraries, or products (do they exist?)
   - URLs or repository references (are they real?)
   - Statistics or numbers with implied sources
   - Feature descriptions of real platforms (Claude Code, MCP, etc.)
   - Dates, version numbers, or release timelines

   **INFERENCE** — A reasonable conclusion drawn from facts but stated as certainty. Examples:
   - "Most SEs spend 40-60% less time on prep" (unsourced metric)
   - "This is the strongest pattern for..." (subjective judgment as fact)
   - Causal claims ("because X, Y happens")

   **OPINION AS FACT** — A value judgment presented without qualification. Examples:
   - "The best approach is..." without evidence
   - Rankings or comparisons without criteria
   - Predictions stated as certainties

## For Each Subagent: Verification Process

For each flagged item, attempt verification:
   - For tool/product claims: search the web to confirm existence and described capabilities
   - For statistics: search for the original source
   - For feature claims about Claude Code: check against official documentation at code.claude.com
   - For URLs/repos: verify they resolve

## For Each Subagent: Report Format

Each subagent should generate a report organized by file, with findings sorted by severity:

   ```
   ## [filename]

   ### HIGH — Likely Hallucination or Fabrication
   - Line/section: [location]
   - Claim: [the specific claim]
   - Finding: [what verification found]
   - Recommendation: Remove, correct, or add qualification

   ### MEDIUM — Unverified or Unsourced
   - Line/section: [location]
   - Claim: [the specific claim]
   - Finding: [unable to verify / no source found]
   - Recommendation: Add source, soften language, or mark as estimate

   ### LOW — Inference Stated as Fact
   - Line/section: [location]
   - Claim: [the specific claim]
   - Finding: [reasonable inference but not established fact]
   - Recommendation: Add qualifier ("typically", "in our experience", etc.)
   ```

## Verification Standards

- A claim about a tool or product is HIGH severity if the tool does not exist or the described capability is inaccurate.
- A statistic without a source is MEDIUM severity.
- A URL or repository reference that does not resolve is HIGH severity.
- A qualitative judgment ("best", "most effective", "strongest") without criteria is LOW severity.
- A claim qualified with "typically", "often", "in many cases" is acceptable and should not be flagged.
- Educational simplifications are acceptable — flag only when the simplification is misleading, not when it omits detail.

## Aggregation (Main Conversation)

After all subagents return their reports:

1. Combine all HIGH findings into a single priority list
2. Group MEDIUM findings by type (unsourced stats, unverified tools, etc.)
3. Summarize LOW findings without listing every instance
4. Provide an overall summary:

```
## Consolidated Summary
- Files audited: [count across all subagents]
- Subagents dispatched: [count]
- HIGH findings: [count] (action required)
- MEDIUM findings: [count] (review recommended)
- LOW findings: [count] (optional improvements)

Top 5 priority fixes: [list the 5 most critical HIGH findings]
```

## Why Parallel Subagents

This architecture provides:
- **Context isolation** — Each file group gets a clean context window, preventing context rot
- **Parallel execution** — Web searches happen simultaneously across subagents
- **Better verification** — Each subagent can do thorough research without competing for context budget
- **Faster execution** — 5 groups checked in parallel vs. 20 files checked serially

Prioritize HIGH findings. An SE reading this content and acting on a fabricated tool name or false feature claim loses credibility with prospects.
