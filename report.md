# Report — AI Research Video Transcript Summarizer

## Business Use Case

This prototype automates the process of converting raw YouTube video transcripts into structured R&D knowledge summaries. The target user is a technology research team member who regularly monitors AI-related video content — news roundups, market analysis, documentary essays, opinion pieces, and short-form commentary — and needs to extract, organize, and share key findings efficiently with their team.

The system takes a raw transcript (with timestamps, as copied from YouTube's transcript feature) as input and produces a markdown summary with six sections: Video Overview, Key Findings, Technical Details, Action Items, Open Questions, and a Confidence Assessment. In batch mode, it additionally generates a cross-video synthesis that surfaces themes, contradictions, and priority actions across the full set of videos.

The value proposition is straightforward: manually watching and noting a 20-minute video takes 20 minutes. This system processes the transcript in under 10 seconds and produces a structured summary that is scannable, searchable, and shareable. For a team monitoring AI developments across dozens of channels, this represents an order-of-magnitude efficiency gain.

## Model Choice

I used **Google Gemini 2.5 Flash** via the Gemini API (Google AI Studio). I chose Gemini Flash for three practical reasons: it is free to use with generous rate limits, it handles long-context inputs well (transcripts can exceed 5,000 words), and response times are fast enough for interactive iteration (under 10 seconds per transcript).

During development, I initially attempted to use `gemini-2.0-flash`, which was no longer available. I then tried `gemini-3.1-pro-preview`, which proved far too slow — a 289-word transcript took over two minutes with no response before I killed the process. Switching to `gemini-2.5-flash` resolved both issues: fast response times and high-quality structured output. I also migrated from the deprecated `google-generativeai` Python package to the newer `google-genai` SDK to eliminate deprecation warnings that were cluttering the output during evaluation.

I did not compare against other providers (OpenAI, Anthropic) for this prototype, but the architecture is provider-agnostic. The system prompt and evaluation set would transfer directly — only the API call function would need to change.

## Baseline vs. Final Design

The baseline prompt (V1) was intentionally minimal: "You are an AI research analyst. Given a YouTube video transcript, produce a structured summary with these sections: Key Findings, Technical Details, Action Items, Open Questions." This produced functional output but lacked context about the video's format, had no self-assessment of reliability, and struggled with multi-topic videos where findings from different subjects were interleaved into a flat list.

The final prompt (V3) added a Video Overview section that contextualizes each video's format, speaker style, and tone. It added a Confidence Assessment that lets the system flag when it is less confident in its output — this proved especially useful for the YouTube Shorts test case, where the system correctly identified limited input as a constraint. It added explicit instructions to organize findings by topic when multiple subjects are covered, which solved the interleaving problem observed in Test Case 1. And it refined Action Items with concrete examples of what actionable output looks like.

Beyond prompt changes, two significant application-level improvements were made. The batch processing function was rewritten to prevent it from overwriting individually generated summary files, which was a bug discovered during real usage. And a cross-video synthesis step was added to batch mode, which sends all individual summaries back to the model for a meta-analysis of common themes, contradictions, and priority actions — transforming batch output from a simple concatenation into a genuinely useful intelligence report.

## Where the Prototype Still Fails or Requires Human Review

The system's main weaknesses, observed across the five evaluation cases, are as follows.

Very short transcripts (Test Case 4, YouTube Shorts at 289 words) receive the same six-section treatment as a 40,000-word documentary. The structure feels heavy for such light input, and some sections feel padded. A production system should detect input length and switch to a brief format automatically.

Unscripted conversational content (Test Case 2, a live market reaction video) produces slightly less crisp findings because the source material contains filler, tangents, and self-corrections. The model handles this reasonably well but occasionally includes points the speaker retracted or repeated. A human reviewer should verify Key Findings for accuracy on unscripted content.

Fact verification is entirely absent. The system faithfully preserves claims from the transcript but has no mechanism to verify whether those claims are accurate. Any summary of factual or technical content should be understood as "this is what the speaker said," not "this is verified truth." For a production deployment, a fact-checking layer or explicit disclaimer would be necessary.

The cross-video synthesis, while useful, can sometimes surface connections that are superficial rather than substantive, especially when the five videos cover very different topics. A human reviewer should assess whether the identified "common themes" are genuinely meaningful or just surface-level keyword overlap.

## Deployment Recommendation

This workflow is suitable for deployment as a first-pass summarization tool with human review. The Confidence Assessment helps the reviewer know when to pay closer attention, and the structured format makes it easy to scan and spot-check individual sections rather than reading the entire output.

I would recommend deploying this for internal R&D use where summaries feed into a team knowledge base that is periodically reviewed by a human analyst. The batch synthesis feature adds particular value for weekly content reviews where a team processes multiple videos at once and needs to identify cross-cutting themes. I would not recommend deploying this for any public-facing or decision-critical application without human oversight, primarily due to the fact verification limitation described above.
