# LLM-as-Judge Evaluation Pipeline

A simple student implementation of an LLM-as-Judge pipeline.

## What it does

The program reads fixed JSON test cases, scores Answer A and Answer B using a documented rubric, compares the two answers, checks position bias by swapping A and B, logs every judge call, and creates a final JSON report.

## Rubric

Each answer is scored from 1 to 5 for:

- correctness
- faithfulness
- completeness
- instruction following
- tone
- safety

The expected answer is used as the reference.

## Judging mode

This project mainly uses reference-based judging because each test case contains an expected answer.

It also performs pairwise A-vs-B judging. Pairwise judging is useful when the main goal is choosing the better of two model outputs rather than assigning only independent scores.

## Bias handling

### Position bias
Every comparison is run in both orders: A/B and B/A. The second winner is mapped back to the original answer. If the winner changes, it is counted as a position flip. The report contains the position flip rate.

### Verbosity bias
The comparison prompt tells the judge not to prefer an answer because it is longer.

### Self-enhancement bias
The judge model is configurable separately using the JUDGE_MODEL environment variable. In a real evaluation, the judge should preferably be from a different model family than the generator.

### Sycophancy and style bias
The prompt tells the judge not to reward confidence or writing style. Correctness must be grounded in the expected answer.

### Score clustering
The rubric defines separate criteria and requires a reason for every score instead of asking for one overall number.

## Judge validation

The test cases contain simple gold winner labels. The pipeline compares the judge's A/B winner with these labels and reports judge/gold agreement.

This is a basic validation artifact. A stronger production evaluation would use more human-labelled examples and calculate Cohen's kappa.

## Logging

Every judge call is appended to:

    logs/judge_log.jsonl

The log includes the prompt, raw response, model, input tokens and output tokens. This makes runs auditable and allows token/cost analysis.

## Configuration

No API key is stored in the code.

Set:

    ANTHROPIC_API_KEY

Optional settings:

    JUDGE_MODEL
    JUDGE_MAX_TOKENS

Example on Windows PowerShell:

    $env:ANTHROPIC_API_KEY="your_key"

Then run:

    python main.py

## Outputs

The final suite report is saved to:

    results/report.json

It contains win counts, position flip rate, gold-label agreement and individual case results.

## Discussion

LLM judges are useful when human review does not scale, but they can have position, verbosity, style, self-preference and score-distribution biases. For important evaluations, automated judging should be periodically checked against human-labelled data.

If the judge shows a high position flip rate or poor agreement with gold labels, I would not trust the reported winner without further human review.

For a release decision, I would use this pipeline as an evaluation aid rather than treating the judge as perfect ground truth.
