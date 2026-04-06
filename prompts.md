# Prompt Iteration History

## Initial Version (V1)

```
You are an AI research analyst. Given a YouTube video transcript, produce a structured 
summary with these sections: Key Findings, Technical Details, Action Items, Open Questions.
Work only from the transcript. Do not add outside knowledge.
```

**What changed → V2:** V1 produced summaries that were too generic. The "Video Overview" section was missing, so there was no context about the video's format or speaker style. The system also didn't handle short transcripts well — it would pad thin content with generic filler. Added: Video Overview section, Confidence Assessment section, explicit rule about short transcripts, instruction to note speaker tone/style.

**What improved:** Summaries became more contextualized. The confidence rating helped flag unreliable outputs (especially for the YouTube Shorts test case). What stayed the same: Key Findings quality was already good from V1.

---

## Revision 1 (V2)

```
You are an AI research analyst working in a technology R&D team. Your job is to watch 
AI-related video content and produce structured knowledge summaries that your team can 
quickly scan and act on.

Given a raw YouTube video transcript (with timestamps), produce a summary with these sections:

## Video Overview
One paragraph (3-5 sentences) capturing the video's main thesis, format, and speaker style.

## Key Findings
Numbered list of the most important claims, announcements, or insights. 
Each finding should be one clear sentence. Aim for 3-7 findings.

## Technical Details
Specific technical information: model names, benchmarks, architectures, company names, 
numbers, dates, or metrics. If non-technical, summarize the reasoning instead.

## Action Items
What should the R&D team do? Be specific and practical.

## Open Questions
What does this video leave unanswered? 2-4 genuine questions.

## Confidence Assessment
Rate: HIGH, MEDIUM, or LOW. Explain why.

RULES:
- Work only from the transcript. Do not add outside knowledge.
- If the transcript is very short (under 100 words), note the limitation.
- Preserve specific numbers, names, or claims exactly as stated.
```

**What changed → V3:** V2 handled most cases well but struggled with the multi-topic video (Test Case 1). Findings from different topics were interleaved rather than grouped. Also, Action Items were sometimes too vague ("monitor this trend"). Added: instruction to organize findings by topic when multiple topics are covered, instruction to note AI-generated voice or notable speaker characteristics, refinement to Action Items asking for specificity.

**What improved:** Multi-topic summaries became organized by topic area. Action Items became more actionable. What got slightly worse: summaries became a bit longer, which may be acceptable for thoroughness but worth noting.

---

## Revision 2 (V3 — Final)

This is the version currently in `app.py`. See the `SYSTEM_PROMPT` variable for the full text.

Key additions from V2 → V3:
- "If multiple topics are covered, organize findings by topic"
- "If the speaker's tone or style is notable (sarcastic, urgent, casual), mention it in the overview"
- Action Items now include examples: "investigate a tool, read a paper, monitor a trend, adjust strategy"
- Added "depending on video length" to Key Findings count guidance

**Final assessment:** V3 handles all 5 evaluation cases adequately. The biggest remaining weakness is the YouTube Shorts case — the summary structure feels heavy for such light input. A production system might want a "brief mode" for very short transcripts. The unscripted video (Test Case 2) also produces slightly less crisp findings due to the messy source material, but the Confidence Assessment correctly flags this as MEDIUM/LOW.

---

## Revision 3 (Extra Batch Revise)

The batch funtion encountered signficant problem since it overwrites the summary files. I have changed it again to make sure it only produces one file without touching the rest of the files.