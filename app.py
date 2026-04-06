"""
AI Research Video Transcript Summarizer
========================================
Takes a YouTube video transcript and produces a structured knowledge summary
with Key Findings, Technical Details, Action Items, and Open Questions.

Usage:
    python app.py <transcript_file> [--output <output_file>]
    python app.py --batch  (runs all transcripts in current directory)

Requires:
    pip install google-generativeai
    GEMINI_API_KEY environment variable set
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("ERROR: google-generativeai not installed. Run: pip install google-generativeai")
    sys.exit(1)


# ── System prompt (V3 - Final) ──────────────────────────────────────────────
# See prompts.md for iteration history

SYSTEM_PROMPT = """You are an AI research analyst working in a technology R&D team. 
Your job is to watch AI-related video content and produce structured knowledge summaries 
that your team can quickly scan and act on.

Given a raw YouTube video transcript (with timestamps), produce a summary with these sections:

## Video Overview
One paragraph (3-5 sentences) capturing the video's main thesis, format, and speaker style.

## Key Findings
Numbered list of the most important claims, announcements, or insights from the video. 
Each finding should be one clear sentence. Aim for 3-7 findings depending on video length.

## Technical Details
Any specific technical information mentioned: model names, benchmarks, architectures, 
company names, product names, numbers, dates, or metrics. If the video is non-technical 
or opinion-based, note that and summarize the reasoning instead.

## Action Items
What should the R&D team do with this information? Possible responses include: 
investigate a tool, read a paper, monitor a trend, adjust strategy, or "no immediate action." 
Be specific and practical.

## Open Questions
What does this video leave unanswered? What would you want to know next? 
List 2-4 genuine questions that a researcher might ask after watching.

## Confidence Assessment
Rate your confidence in this summary: HIGH (clear, scripted content), MEDIUM (mostly clear 
with some ambiguity), or LOW (unscripted, noisy, or very short transcript). 
Briefly explain why.

RULES:
- Work only from what the transcript says. Do not add outside knowledge.
- If the transcript is very short (under 100 words), note the limitation and do your best.
- If multiple topics are covered, organize findings by topic.
- Preserve any specific numbers, names, or claims exactly as stated.
- If the speaker's tone or style is notable (sarcastic, urgent, casual), mention it in the overview.
"""


def load_transcript(filepath: str) -> str:
    """Read a transcript file and return its contents."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def summarize_transcript(transcript: str, model_name: str = "gemini-2.5-flash") -> str:
    """Send transcript to Gemini API and return the structured summary."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        print("Get your key at https://aistudio.google.com/apikey")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYSTEM_PROMPT
    )

    # Construct the user message with the transcript
    user_message = f"Here is the transcript to summarize:\n\n{transcript}"

    response = model.generate_content(user_message)
    return response.text


def save_output(summary: str, output_path: str):
    """Save summary to a file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary saved to: {output_path}")


def run_single(transcript_path: str, output_path: str = None):
    """Process a single transcript file."""
    print(f"\n{'='*60}")
    print(f"Processing: {transcript_path}")
    print(f"{'='*60}")

    transcript = load_transcript(transcript_path)
    word_count = len(transcript.split())
    print(f"Transcript length: {word_count} words")

    summary = summarize_transcript(transcript)

    # Print to console
    print(f"\n{summary}")

    # Save to file if specified
    if output_path:
        save_output(summary, output_path)
    else:
        # Auto-generate output filename
        stem = Path(transcript_path).stem
        out = f"summary_{stem.replace('transcript_', '')}.md"
        save_output(summary, out)

    return summary


def run_batch():
    """Process all transcript_*.txt files in current directory."""
    transcripts = sorted(Path(".").glob("transcript_*.txt"))
    if not transcripts:
        print("No transcript_*.txt files found in current directory.")
        sys.exit(1)

    print(f"Found {len(transcripts)} transcripts to process.\n")
    results = {}

    for t in transcripts:
        summary = run_single(str(t))
        results[t.name] = summary

    # Save combined results
    with open("batch_results.md", "w", encoding="utf-8") as f:
        for name, summary in results.items():
            f.write(f"# {name}\n\n{summary}\n\n{'='*60}\n\n")

    print(f"\n\nAll results saved to batch_results.md")
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Summarize AI research video transcripts using Gemini API"
    )
    parser.add_argument("transcript", nargs="?", help="Path to transcript file")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--batch", action="store_true", help="Process all transcript_*.txt files")
    parser.add_argument("--model", default="gemini-2.0-flash", help="Gemini model name")

    args = parser.parse_args()

    if args.batch:
        run_batch()
    elif args.transcript:
        run_single(args.transcript, args.output)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
