# Team Truvia: AuthPrint (Identity Mismatch Detection)

## The Problem
First Dollar is losing value to AI-generated spam submissions. Existing tools like GPTZero analyze text in isolation and are easily bypassed when users simply prompt LLMs to mimic a casual tone. 

## Our Solution
AuthPrint introduces a different approach: **identity-based moderation**.
Instead of asking "Is this AI-generated?", our system asks "Does this match how this specific user normally writes?"

## How It Works
We built a multi-signal anomaly detection engine that evaluates:
1. **Stylometric Features:** Sentence variation, punctuation clustering, and casing habits.
2. **Character N-Gram Fingerprinting:** Captures micro-writing habits (spacing, suffixes) independent of the actual topic.
3. **Unified Anomaly Scoring:** A deterministic, offline mathematical model that flags severe stylistic drift.

## How to Run the Demo Locally
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
