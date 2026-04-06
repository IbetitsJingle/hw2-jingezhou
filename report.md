# Report — AI Research Video Transcript Summarizer

## Business Use Case

This prototype automates the process of converting raw YouTube video transcripts into structured R&D knowledge summaries. The target user is a technology research team member who monitors AI-related video content (news roundups, market analysis, documentary essays, opinion pieces) and needs to extract, organize, and share key findings efficiently.

The system takes a raw transcript as input and produces a markdown summary with six sections: Video Overview, Key Findings, Technical Details, Action Items, Open Questions, and a Confidence Assessment.

## Model Choice

I used **Google Gemini 2.0 Flash** via the Gemini API (Google AI Studio). I chose Gemini Flash for three reasons: it is free to use with generous rate limits, it handles long-context inputs well (transcripts can be thousands of words), and the response quality is strong for structured summarization tasks. I did not compare against other models for this prototype, but the architecture is provider-agnostic — swapping to Claude or GPT would require only changing the API call.

## Baseline vs. Final Design

**Baseline (V1):** A minimal prompt asking for Key Findings, Technical Details, Action Items, and Open Questions. The output was functional but lacked context — no video overview, no confidence signal, and multi-topic videos produced disorganized findings.

**Final (V3):** Added Video Overview (contextualizes format and speaker style), Confidence Assessment (flags unreliable outputs), explicit handling for short transcripts, topic-based organization for multi-topic videos, and more specific Action Item guidance. The improvements were driven by running the 5 evaluation cases and observing specific failure patterns at each revision.

## Where the Prototype Still Fails or Requires Human Review

The system's main weaknesses are:

1. **Very short transcripts** (Test Case 4, YouTube Shorts): The structured format feels heavy for 75 seconds of content. The system produces all six sections but some feel padded. A production system should detect input length and switch to a brief format.

2. **Unscripted conversational content** (Test Case 2): The model handles filler and tangents reasonably well but occasionally includes repeated points that the speaker self-corrected. A human reviewer should verify Key Findings for accuracy.

3. **Fact verification**: The system preserves claims from the transcript but cannot verify whether those claims are accurate. Any summary of factual/technical content should be treated as "this is what the speaker said" not "this is true."

## Deployment Recommendation

This workflow is suitable for deployment as a **first-pass summarization tool** with human review. The Confidence Assessment helps the reviewer know when to pay closer attention. I would recommend deploying this for internal R&D use where the summaries feed into a team knowledge base that is periodically reviewed, rather than for any public-facing or decision-critical application without human oversight.
