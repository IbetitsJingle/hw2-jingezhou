# HW2 — AI Research Video Transcript Summarizer

**Author:** Jinge Zhou  
**Course:** Generative AI (Professor Harang Ju), Johns Hopkins University  
**Date:** April 2026

## Workflow

This tool takes raw YouTube video transcripts and produces structured knowledge summaries for an R&D team. The goal is to turn passive video consumption into actionable research intelligence.

**Who the user is:** An AI R&D team member who regularly watches AI-related YouTube content (news roundups, market analysis, documentaries, opinion pieces) and needs to quickly extract and share key findings with their team.

**What input the system receives:** A raw YouTube transcript (with timestamps) copied from the video's caption/transcript feature.

**What output the system should produce:** A structured markdown summary containing: Video Overview, Key Findings, Technical Details, Action Items, Open Questions, and a Confidence Assessment.

**Why this task is valuable to automate:** Manually watching and noting a 20-minute video takes 20 minutes. An LLM can process the transcript in seconds and produce a structured summary that is scannable, searchable, and shareable. This enables an R&D team to monitor 10x more content with the same time investment.

## Setup

```bash
pip install google-generativeai
export GEMINI_API_KEY="your-key-here"
```

## Usage

```bash
# Single transcript
python app.py transcript_1_ai_memory.txt

# All transcripts (batch mode)
python app.py --batch

# Custom output path
python app.py transcript_1_ai_memory.txt -o my_summary.md
```

## Repository Structure

```
hw2-jingezhou/
├── README.md
├── app.py
├── prompts.md
├── eval_set.md
├── report.md
├── transcript_1_ai_memory.txt
├── transcript_2_ram_prices.txt
├── transcript_3_ai_endgame.txt
├── transcript_4_silicon_valley_shorts.txt
└── transcript_5_rise_fall_openclaw.txt
```

## Video Walkthrough

[Link to be added after recording]
