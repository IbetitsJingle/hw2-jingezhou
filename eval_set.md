# Evaluation Set — AI Research Video Transcript Summarizer

## Test Case 1: Multi-Topic AI News Roundup (Normal Case)
- **File:** `transcript_1_ai_memory.txt`
- **Source:** "They solved AI's memory problem!" — AI-voiced news roundup
- **Length:** ~690 lines, medium-long
- **Challenge:** Multiple distinct topics within one video. Speaker shifts between AI breakthroughs rapidly.
- **What a good output should do:** Clearly segment findings by topic rather than blending them. Capture all major announcements. Note the AI-generated voice in the overview. Confidence should be MEDIUM or HIGH since the content is scripted but covers many topics.

## Test Case 2: Unscripted Market Reaction (Likely-to-Fail Case)
- **File:** `transcript_2_ram_prices.txt`
- **Source:** "RAM Companies' Stock Price Plummet, RAM Prices Go Down, But..." — live human reaction
- **Length:** ~635 lines, medium-long
- **Challenge:** Unscripted speech with filler words, tangents, repeated points, and conversational style. Speaker reacts in real-time to news.
- **What a good output should do:** Extract the core market information despite conversational noise. Not get confused by repeated or self-corrected statements. Confidence should be MEDIUM or LOW due to unscripted nature.

## Test Case 3: Scripted Documentary Essay (Normal Case — Baseline)
- **File:** `transcript_3_ai_endgame.txt`
- **Source:** "The AI Endgame (12 Scenarios)" — documentary-style video essay
- **Length:** ~850 lines, longest transcript
- **Challenge:** Dense, scripted content with 12 distinct scenarios to capture. Mix of documentary narration and live commentary.
- **What a good output should do:** Capture all 12 scenarios or at least the major ones. Maintain the structure the original video provides. This is the cleanest input — if the system fails here, the prompt needs fundamental revision. Confidence should be HIGH.

## Test Case 4: YouTube Shorts — Minimum Input (Edge Case)
- **File:** `transcript_4_silicon_valley_shorts.txt`
- **Source:** "Silicon Valley has a NEW problem" — YouTube Shorts format
- **Length:** ~35 lines, very short (~75 seconds of speech)
- **Challenge:** Extremely short transcript. Can the system produce a useful structured summary without hallucinating or padding? Does every section still make sense with minimal input?
- **What a good output should do:** Produce a concise but complete summary. The "Technical Details" section may be thin and should acknowledge that honestly rather than inventing details. Confidence should note the limitation of short input.

## Test Case 5: High-Production Documentary (Normal Case)
- **File:** `transcript_5_rise_fall_openclaw.txt`
- **Source:** "The Rise and Fall of OpenAI" — Cold Fusion, professional production
- **Length:** ~832 lines, long
- **Challenge:** Information-dense professional narration. Many factual claims packed tightly — company names, dates, funding rounds, personnel changes. Can the system prioritize rather than regurgitate everything?
- **What a good output should do:** Identify the narrative arc (rise and fall structure). Capture key factual details (dates, funding, key people) without overwhelming the reader. Confidence should be HIGH given the polished, scripted delivery.
