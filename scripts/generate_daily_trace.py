#!/usr/bin/env python3
"""
Daily trace generator for anti-totalization research.

Generates reflections on totalization patterns, evaluation protocols,
and structural risks in AI systems.
"""

import os
import sys
from datetime import datetime
from anthropic import Anthropic

def generate_trace():
    """Generate daily trace using Claude API."""

    # Get API key from environment
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Initialize Anthropic client
    client = Anthropic(api_key=api_key)

    # Get current date
    today = datetime.now().strftime('%Y-%m-%d')

    # Define prompt themes for anti-totalization research
    themes = [
        "structural indicators of decision centrality in AI outputs",
        "observable patterns in self-referential authority claims",
        "evaluation stability when detecting totalization signals",
        "architectural factors that enable or constrain totalization",
        "methodological challenges in LLM self-evaluation protocols",
        "distinction between structural analysis and normative claims",
        "reproducibility constraints in totalization pattern detection",
        "cross-model consistency in evaluating centrality signals"
    ]

    # Select theme based on day of year (cycles through themes)
    day_of_year = datetime.now().timetuple().tm_yday
    theme = themes[day_of_year % len(themes)]

    # Generate content using Claude
    prompt = f"""You are a researcher studying structural patterns in AI systems, specifically focusing on totalization (the architectural pattern where systems position themselves as central authorities or decision-makers).

Today's research focus: {theme}

Write a brief research note (300-500 words) that:
1. Explores one specific aspect of this theme
2. Maintains analytical distance (structural observation, not normative judgment)
3. Considers methodological limitations or evaluation challenges
4. Suggests one testable question or experimental direction

Keep the tone analytical and research-focused. Avoid prescriptive recommendations or safety claims.
Do not make claims about AI agency, consciousness, or intentions.
Focus on observable patterns and evaluation methodology."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        content = message.content[0].text

        # Create filename
        # Sanitize theme for filename (take first 6 words, remove special chars)
        theme_short = '_'.join(theme.split()[:6]).lower()
        theme_short = ''.join(c if c.isalnum() or c == '_' else '' for c in theme_short)
        filename = f"experiments/daily-traces/{today}_{theme_short}.md"

        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Daily Trace: {today}\n\n")
            f.write(f"**Theme:** {theme}\n\n")
            f.write("---\n\n")
            f.write(content)
            f.write("\n\n---\n\n")
            f.write("*Generated automatically by Claude API as part of the anti-totalization research protocol.*\n")

        print(f"✓ Daily trace generated: {filename}")
        return filename

    except Exception as e:
        print(f"Error generating content: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_trace()
