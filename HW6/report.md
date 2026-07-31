# HW6 Report - A/B Test Analysis

## Experiment overview

This report analyzes the Android A/B test for `firebase_exp_84` in the period from 2024-02-02 to 2024-02-20.

The experiment compares:

| Group | Experiment value |
|---|---|
| Control | `firebase_exp_84_0` |
| Treatment | `firebase_exp_84_1` |

The product change is related to event voting. The main question is whether the treatment improves user voting behavior on event details.

## Hypothesis and metrics

The hypothesis is that the treatment increases voting engagement without hurting event detail engagement.

Primary metric:

| Metric | Definition |
|---|---|
| Vote conversion | Share of experiment users who triggered at least one `event_vote` |

Secondary metrics:

| Metric | Definition |
|---|---|
| Average votes per user | Average number of `event_vote` events per experiment user |
| Repeat vote user rate | Share of users with at least two `event_vote` events |

Guardrail metrics:

| Metric | Definition |
|---|---|
| Open event user rate | Share of users who triggered at least one `open_event` |
| Average open events per user | Average number of `open_event` events per experiment user |

The primary metric is a user-level conversion metric, so I used a two-proportion z-test with significance level 0.05.

## Data quality check

Before interpreting the result, I checked whether users were split evenly between control and treatment.

| Metric | Value |
|---|---:|
| Control users | 19,551 |
| Treatment users | 20,543 |
| Invalid or both groups | 7 |
| Clean users | 40,094 |
| Control share | 48.76% |
| Treatment share | 51.24% |
| SRM p-value | 0.000001 |

The SRM check fails. Treatment has more users than expected under a 50/50 split, and the difference is statistically significant. This does not automatically invalidate every result, but it means the experiment should be interpreted with caution.

The imbalance was not caused by a single outlier day. Treatment had slightly more users on most exposure dates, so this looks like a consistent assignment imbalance rather than one isolated data issue.

## Results

### Primary metric

| Metric | Control | Treatment | Difference |
|---|---:|---:|---:|
| Users | 19,551 | 20,543 | +992 |
| Voters | 18,269 | 19,246 | +977 |
| Vote conversion | 93.4428% | 93.6864% | +0.2436 pp |
| Relative lift | - | - | +0.2607% |
| z-score | - | - | 0.9939 |
| p-value | - | - | 0.320267 |

Treatment has a slightly higher vote conversion rate than control, but the effect is very small: +0.2436 percentage points. The p-value is 0.320267, which is above 0.05, so the result is not statistically significant.

This means there is not enough evidence that the treatment truly improves the share of users who vote.

### Secondary and guardrail metrics

| Metric | Control | Treatment | Interpretation |
|---|---:|---:|---|
| Average votes per user | 14.1450 | 13.6143 | Lower in treatment |
| Repeat vote user rate | 65.66% | 65.70% | Practically unchanged |
| Open event user rate | 99.24% | 99.23% | No negative guardrail signal |
| Average open events per user | 232.5338 | 237.9838 | Higher in treatment |
| Votes per open event | 0.0608 | 0.0572 | Lower in treatment |

The guardrail metrics do not show a clear product problem. Users in treatment still open event details at the same rate, and average open events per user is even higher.

However, the voting intensity metrics do not support a strong positive result. Average votes per user and votes per open event are lower in treatment. Repeat voting is almost unchanged.

### Segment sanity check

Country-level results are mixed. Some larger countries show a small positive lift, while others show a negative lift.

| Country | Control users | Treatment users | Control vote rate | Treatment vote rate | Lift |
|---|---:|---:|---:|---:|---:|
| Italy | 5,282 | 5,693 | 97.22% | 97.59% | +0.37 pp |
| Germany | 3,882 | 4,046 | 80.83% | 81.83% | +1.00 pp |
| Croatia | 2,768 | 2,953 | 99.02% | 97.97% | -1.05 pp |
| Serbia | 2,612 | 2,767 | 98.12% | 98.77% | +0.65 pp |
| Romania | 667 | 677 | 97.90% | 96.75% | -1.15 pp |

There is no strong and consistent segment-level improvement. This supports the conclusion that the treatment effect is weak and not reliable enough for rollout.

## Recommendation

I would not roll out the treatment yet.

The treatment shows a small positive movement in the primary metric, but the improvement is not statistically significant. The experiment also fails the SRM check, which reduces confidence in the result. Secondary metrics do not provide a strong positive signal, and voting intensity is slightly worse in treatment.

Recommended next steps:

1. Investigate why the experiment allocation was not close to 50/50.
2. Check the Firebase assignment setup and whether the experiment was ramped or targeted unevenly.
3. Re-run the experiment after fixing the sample split issue.
4. Keep the current version until there is statistically reliable evidence of improvement.

Final decision: do not ship the treatment based on this experiment result.