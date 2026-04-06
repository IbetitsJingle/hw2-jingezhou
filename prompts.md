# Prompt Iteration History

This document traces the evolution of the system prompt and application logic across four revisions. Each revision was driven by observing real outputs from the evaluation set and identifying specific problems to fix.

---

## Initial Version (V1)

```
You are an AI research analyst. Given a YouTube video transcript, produce a structured 
summary with these sections: Key Findings, Technical Details, Action Items, Open Questions.
Work only from the transcript. Do not add outside knowledge.
```

This was the baseline prompt, intentionally minimal. It produced functional summaries but lacked several things that became obvious after running it against the evaluation set. There was no context about the video's format or speaker style, which meant a scripted documentary and an unscripted reaction video received identical treatment. The system also had no way to signal when it was less confident in its output, and short transcripts (like the YouTube Shorts test case at only 289 words) received the same heavy structure as a 40,000-word documentary transcript, resulting in padded or generic-sounding sections.

**What changed → V2:** Added a Video Overview section to contextualize each video's format and speaker. Added a Confidence Assessment section so the system could self-report reliability. Added an explicit rule for short transcripts (under 100 words) to acknowledge limitations honestly rather than padding.

**What improved:** Summaries became more contextualized and self-aware. The Confidence Assessment proved especially useful for the YouTube Shorts case (Test Case 4), where the system correctly flagged its output as MEDIUM confidence due to limited source material. Key Findings quality was already solid from V1, so that section stayed roughly the same.

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

**What changed → V3:** After running V2 against Test Case 1 (the multi-topic AI news roundup), I noticed that findings from different topics were interleaved rather than grouped. A video covering five different AI breakthroughs produced a flat list where item 1 was about memory, item 2 about something else, item 3 back to memory. This made the summaries harder to scan. Additionally, Action Items were sometimes too vague, offering suggestions like "monitor this trend" without specifying what trend or how to monitor it. I also noticed the system wasn't flagging when a video used AI-generated narration versus a live human speaker, which is relevant context for assessing credibility.

**What improved:** Multi-topic summaries became organized by topic area, making them far more scannable. Action Items became genuinely actionable with specific suggestions. What got slightly worse: summaries became a bit longer overall, but the added length was justified by improved organization.

---

## Revision 2 (V3 — Final Prompt)

This is the system prompt currently in `app.py`. The full text is in the `SYSTEM_PROMPT` variable. Key additions from V2:

The instruction "If multiple topics are covered, organize findings by topic" solved the interleaving problem. The instruction "If the speaker's tone or style is notable (sarcastic, urgent, casual), mention it in the overview" added useful characterization. Action Items now include concrete examples: "investigate a tool, read a paper, monitor a trend, adjust strategy, or no immediate action." The Key Findings guidance now says "depending on video length" to prevent the system from forcing exactly 5 findings on a 60-second Short.

**Final prompt assessment:** V3 handles all 5 evaluation cases well. The biggest remaining weakness is the YouTube Shorts case, where the six-section structure feels heavy for such light input. A production system might detect input length and switch to a brief mode automatically. The unscripted video (Test Case 2) also produces slightly less crisp findings due to messy source material, but the Confidence Assessment correctly flags this.

---

## Revision 3 — SDK Migration and Model Update

During initial testing, I used the `google-generativeai` package with `gemini-2.0-flash`. Two problems emerged. First, `gemini-2.0-flash` was no longer available, causing the script to fail entirely. I briefly tried `gemini-3.1-pro-preview`, but it was extremely slow — the shortest transcript (289 words) took over two minutes with no response before I killed the process. Second, the `google-generativeai` package printed a large deprecation warning on every run, cluttering the output and making it harder to read results during evaluation.

I migrated the codebase from `google.generativeai` to the newer `google.genai` SDK and switched the model to `gemini-2.5-flash`. The changes were in the import section and the `summarize_transcript` function, moving from `genai.GenerativeModel()` to `genai.Client()` with `client.models.generate_content()`. The system prompt itself was unchanged — this was purely an infrastructure fix.

**What improved:** The deprecation warning disappeared entirely, and response times dropped to under 10 seconds per transcript. The output quality remained the same since the prompt was unchanged, but the development experience improved significantly, making subsequent iteration cycles faster and easier to evaluate.

---

## Revision 4 — Batch Processing Fix and Cross-Video Synthesis

When I first ran `python app.py --batch`, I discovered that the batch function was calling `run_single()` for each transcript, which saved individual summary files. This meant batch mode was silently overwriting the individual summary files I had already generated and reviewed. This was a significant bug — running batch destroyed previously validated outputs.

I rewrote the `run_batch()` function to call `summarize_transcript()` directly instead of routing through `run_single()`, ensuring batch mode only writes to `batch_results.md` and never touches individual summary files.

Additionally, I added a cross-video synthesis step at the end of batch processing. After generating all individual summaries, the system sends all summaries back to the model with a synthesis prompt asking for Common Themes, Key Takeaways, Contradictions or Tensions, and Recommended Priority Actions. This transforms the batch output from a simple concatenation of individual summaries into a genuinely useful cross-video intelligence report — which is the actual value proposition of processing multiple videos together rather than one at a time.

**What improved:** Individual summary files are now preserved during batch runs. The cross-video synthesis adds a layer of analysis that no individual summary can provide, surfacing patterns and contradictions across the full set of videos. This feature alone justifies batch processing as a distinct mode rather than just a convenience wrapper.
