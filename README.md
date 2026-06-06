# Social Media Addiction — Exploratory Data Analysis

> An end-to-end EDA of social media usage, addiction levels, and wellbeing outcomes across 100 countries and 60,000+ individual records.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Datasets](#2-datasets)
3. [Repository Structure](#3-repository-structure)
4. [How to Run](#4-how-to-run)
5. [Pivot Tables](#5-pivot-tables)
6. [Chart 1 — Screen Time Overview](#6-chart-1--screen-time-overview)
7. [Chart 2 — Addiction Level Breakdown](#7-chart-2--addiction-level-breakdown)
8. [Chart 3 — Correlation Heatmap](#8-chart-3--correlation-heatmap)
9. [Chart 4 — Country-Level Analysis](#9-chart-4--country-level-analysis)
10. [Chart 5 — Relationship Deep Dive](#10-chart-5--relationship-deep-dive)
11. [Key Findings](#11-key-findings)
12. [Limitations](#12-limitations)

---

## 1. Project Overview

This project explores the relationship between social media usage (TikTok, Instagram, and others) and addiction, mental health, and cognitive outcomes. The analysis covers:

- How screen time varies across age groups, genders, and platforms
- How addiction levels relate to TikTok usage, sleep, and attention span
- Which countries have the highest addiction exposure
- How national-level mental health resources correlate with addiction scores

The data was pre-cleaned before this EDA. This notebook focuses entirely on **understanding patterns, distributions, and relationships**.

---

## 2. Datasets

| File | Rows | Columns | Description |
|---|---|---|---|
| `country_wise_analysis_addiction.xlsx` | 100 | 9 | One row per country. Pre-aggregated addiction scores, TikTok/Instagram usage, sleep, ASI, MHRI, addiction rank. |
| `screen_time_behavior.xlsx` | 50,000 | 11 | Individual user records. Platform, age group, gender, weekday/weekend screen hours, focus span, multitasking frequency, physical activity. |
| `tiktok_instagram_global_100countries.xlsx` | 10,000 | 23 | Individual records with both behaviour (TikTok/Instagram minutes, scroll velocity, night usage) and outcomes (addiction score, attention span, sleep quality, dopamine dependency). Also includes country-level socioeconomic fields (GDP index, internet penetration, MHRI). |

### Key Variables

| Variable | Dataset | Type | Role |
|---|---|---|---|
| `Addiction Score` | tiktok_instagram, country_wise | Continuous (0–100) | Primary outcome |
| `Addiction Level` | tiktok_instagram | Categorical (Low/Medium/High/Severe) | Grouping variable |
| `Tiktok Minutes Daily` | tiktok_instagram, country_wise | Continuous | Primary predictor |
| `Attention Span Score` | tiktok_instagram, country_wise | Continuous | Cognitive outcome |
| `Sleep Hours` | tiktok_instagram, country_wise | Continuous | Wellbeing outcome |
| `MHRI` | tiktok_instagram, country_wise | Continuous | National mental health resources |
| `age_group` | screen_time | Categorical | Demographic grouping |
| `platform` | screen_time | Categorical | Platform grouping |

---

## 3. Repository Structure

```
social_media_addiction_eda/
│
├── data/                          # Place your 3 xlsx files here
│   ├── country_wise_analysis_addiction.xlsx
│   ├── screen_time_behavior.xlsx
│   └── tiktok_instagram_global_100countries.xlsx
│
├── images/                        # All generated charts (auto-created)
│   ├── 01_screen_time_overview.png
│   ├── 02_addiction_level_breakdown.png
│   ├── 03_correlation_heatmap.png
│   ├── 04_country_analysis.png
│   └── 05_relationship_deep_dive.png
│
├── src/
│   └── eda_analysis.py            # Full analysis script
│
├── requirements.txt
└── README.md                      # This file
```

---

## 4. How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/social_media_addiction_eda.git
cd social_media_addiction_eda

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place your data files in the data/ folder

# 4. Run the analysis
python src/eda_analysis.py
```

Charts will be saved to `images/`.

---

## 5. Pivot Tables

These are the core summaries extracted from each dataset before visualisation.

### Dataset 2 — Screen Time Behavior

**Pivot 1: Average weekday screen hours by age group**

| Age Group | Avg Weekday Hours | Avg Weekend Hours | Avg Focus Span (mins) |
|---|---|---|---|
| Children | 5.49 | 8.05 | 17.89 |
| Teen | 5.49 | 8.01 | 17.96 |
| Young Adult | 5.51 | 8.00 | 17.88 |
| Adult | 5.49 | 8.04 | 18.02 |
| Senior | 5.51 | 7.95 | 17.99 |

> All age groups average ~5.5 hrs on weekdays and ~8 hrs on weekends. The jump to weekends is consistent across every group — screens fill leisure time regardless of age.

**Pivot 2: Average focus span by platform**

| Platform | Avg Focus Span (mins) |
|---|---|
| Instagram | 17.81 |
| YouTube | 17.87 |
| X/Twitter | 17.89 |
| LinkedIn | 17.91 |
| Twitch | 17.92 |
| Facebook | 17.93 |
| TikTok | 17.98 |
| Reddit | 18.02 |
| Discord | 18.04 |
| Snapchat | 18.11 |

> The spread across platforms is less than 0.3 minutes. Platform choice alone is not a meaningful predictor of focus span in this dataset.

---

### Dataset 3 — TikTok/Instagram Global

**Pivot 3: Key metrics by addiction level (the most important pivot)**

| Addiction Level | TikTok Mins/Day | Instagram Mins/Day | Sleep Hours | Attention Span Score | Dopamine Dependency | Addiction Score |
|---|---|---|---|---|---|---|
| Low | 18.51 | 19.05 | 7.27 | 96.87 | — | 18.01 |
| Medium | 54.10 | 54.48 | 6.92 | 90.95 | — | 40.54 |
| High | 131.55 | 107.52 | 7.00 | 80.08 | — | 61.59 |
| Severe | 268.45 | 234.29 | 7.23 | 58.11 | — | 75.14 |

> Moving from Low to High addiction: TikTok usage increases by **7×** (18 → 131 mins), and attention span drops by **17 points** (96 → 80). This is the central relationship in the dataset.

> **Note on Severe:** Only 1 user is classified as Severe. Treat those numbers as anecdotal — they cannot be generalised.

---

## 6. Chart 1 — Screen Time Overview

![Screen Time Overview](images/01_screen_time_overview.png)

### What this shows

Six panels covering Dataset 2:

- **Top left:** All age groups average ~5.5 weekday screen hours with almost no variation between groups. This tells us that age does not predict *how much* someone uses screens on weekdays.
- **Top middle:** Focus span by age group and gender. Differences are under 0.2 minutes — gender and age group do not meaningfully predict focus span in this dataset.
- **Top right:** Focus span by platform. Instagram users have the lowest average focus span (17.81 mins); Snapchat users the highest (18.11 mins). The range is narrow.
- **Bottom left:** Weekday vs weekend screen hours. Every point above the diagonal (the reference line) means that person uses screens more on weekends. The pattern is consistent — weekend usage is roughly 2.5 hours higher across all groups.
- **Bottom middle:** Physical activity vs focus span. No strong visible trend — physical activity does not clearly predict focus span within this dataset.
- **Bottom right:** Multitasking frequency distribution. Teens and Young Adults show slightly wider spread, suggesting more variability in how often they multitask.

### Key takeaway

Screen time is remarkably uniform across demographics in Dataset 2. The meaningful variation in outcomes (focus span, addiction) is captured better in Dataset 3, which has richer individual-level data.

---

## 7. Chart 2 — Addiction Level Breakdown

![Addiction Level Breakdown](images/02_addiction_level_breakdown.png)

### What this shows

- **TikTok minutes by addiction level:** Clear step-up pattern. Low = 18 mins, Medium = 54 mins, High = 131 mins, Severe = 268 mins. Each level roughly doubles the previous.
- **Sleep hours by addiction level:** Counterintuitively, sleep hours do not decline consistently with higher addiction. High users (7.00 hrs) sleep slightly less than Low users (7.27 hrs), but Severe users (7.23 hrs) sleep nearly as much as Low users. Sleep alone is not a clean indicator of addiction in this data.
- **Attention span by addiction level:** Consistent decline. Low = 96.87, Medium = 90.95, High = 80.08, Severe = 58.11. This is the clearest outcome gradient across addiction levels.
- **TikTok minutes vs addiction score scatter (r = 0.76):** Strong positive relationship. As TikTok usage goes up, addiction score goes up. The three colours (Low/Medium/High) cluster clearly, confirming the pivot table pattern.
- **Sleep vs attention span scatter:** No clear trend across the scatter — the relationship between sleep and attention span is weak at the individual level.
- **Dopamine dependency vs impulsivity:** Moderate correlation visible in the scatter. The two measures move together, suggesting they are capturing a shared underlying trait.

### Key takeaway

TikTok minutes is the strongest individual-level predictor of addiction score (r = 0.76). Attention span degrades progressively with addiction level. Sleep is not a reliable individual-level signal.

---

## 8. Chart 3 — Correlation Heatmap

![Correlation Heatmap](images/03_correlation_heatmap.png)

### What this shows

A Spearman correlation matrix of all 14 key numeric variables in Dataset 3. Spearman is used instead of Pearson because it is robust to the skewed distributions present (especially in `Tiktok Minutes Daily`).

### Strongest relationships

| Pair | Spearman r | Interpretation |
|---|---|---|
| TikTok Minutes Daily ↔ Addiction Score | **+0.76** | Strong positive — more TikTok = higher addiction |
| TikTok Minutes Daily ↔ Attention Span Score | **−0.76** | Strong negative — more TikTok = lower attention span |
| TikTok Minutes Daily ↔ Dopamine Dependency | **+0.76** | Strong positive — usage drives dependency |
| Addiction Score ↔ Attention Span Score | **−0.95** | Very strong negative — the two are near-inverse |
| Addiction Score ↔ Dopamine Dependency | **+0.95** | Very strong positive — dependency and addiction move together |
| Instagram Minutes Daily ↔ Addiction Score | **+0.016** | Near zero — Instagram alone is a weak predictor |

### Notable non-relationships

- `Night Usage Ratio`, `Scroll Velocity`, `Gdp Index`, `Internet Penetration`, `MHRI` all show very weak correlations with addiction score at the individual level. These factors may matter more at the country level (see Chart 4).

### Multicollinearity warning

`Addiction Score`, `Attention Span Score`, and `Dopamine Dependency Score` are very highly intercorrelated. If you use these in a regression model later, include only one of them as a predictor or outcome — do not use all three simultaneously.

---

## 9. Chart 4 — Country-Level Analysis

![Country Analysis](images/04_country_analysis.png)

### What this shows

- **Top 15 countries by addiction score:** Tanzania, Indonesia, and Argentina lead the ranking. Scores are clustered tightly between 59–61 across all 100 countries, suggesting the index is designed to be comparative rather than absolute.
- **Distribution of addiction score:** Near-normal distribution centred around the mean (~58.5). No extreme outliers at country level.
- **MHRI vs addiction score (r ≈ −0.06):** Almost no relationship. Countries with better mental health resources do not systematically have lower addiction scores in this dataset.
- **TikTok minutes vs addiction score by country (r ≈ +0.75):** Strong positive relationship — countries where people use TikTok more have higher national addiction scores.
- **Sleep hours vs attention span by country (r ≈ +0.35):** Moderate positive — countries where people sleep more tend to have higher attention span scores.

### Key takeaway

At the country level, TikTok usage is the clearest predictor of addiction score. National mental health infrastructure (MHRI) shows little relationship with addiction outcomes — suggesting structural investment alone does not offset usage-driven addiction.

---

## 10. Chart 5 — Relationship Deep Dive

![Relationship Deep Dive](images/05_relationship_deep_dive.png)

### What this shows

- **Night usage ratio by addiction level (violin plot):** The distribution shape is very similar across Low, Medium, and High groups. Night usage does not cleanly separate addiction levels — it is not a reliable individual signal.
- **Scroll velocity vs addiction score (colour = TikTok mins):** Scroll velocity shows near-zero correlation with addiction score (r ≈ 0.004). The colour gradient (TikTok minutes) shows that high TikTok users are spread across all scroll velocity levels — how fast you scroll matters less than how long.
- **Addiction score by derived age group (boxplot):** Median addiction scores are similar across age groups (all around 60–62). No age group is significantly more addicted than another — addiction is broadly distributed.
- **TikTok vs Instagram minutes by addiction level:** Low addiction users cluster in the bottom-left (low on both). High addiction users spread into the upper right. The two platforms are not strongly correlated with each other at the individual level (confirmed by the near-zero r in the heatmap).
- **ASI vs MHRI by country (colour = addiction score):** Countries with high ASI (Addiction Severity Index) and low MHRI (Mental Health Resources) tend to have higher addiction scores (shown in red). This suggests the combination of high baseline addiction pressure and weak mental health infrastructure is the risk profile to watch.
- **Summary heatmap:** Normalised view of all key metrics across addiction levels. TikTok minutes and dopamine dependency rise most steeply from Low to High. Attention span drops most steeply. Sleep and Instagram minutes show smaller gradients.

### Key takeaway

Usage duration (TikTok minutes) matters far more than usage pattern (scroll velocity, night usage ratio). Age does not predict addiction level. The country-level risk profile is high addiction pressure combined with low mental health resources.

---

## 11. Key Findings

### Finding 1 — TikTok usage is the dominant predictor
TikTok minutes daily has a Spearman correlation of **r = 0.76** with addiction score at the individual level, and a similar relationship at the country level. Instagram minutes show almost no independent relationship (r = 0.016).

### Finding 2 — Attention span is the clearest outcome
Attention span score correlates at **r = −0.95** with addiction score — the strongest relationship in the dataset. High addiction users score 80 on attention span vs 96 for Low addiction users. This 16-point gap is the most consistent finding across all analyses.

### Finding 3 — Screen time is uniform across demographics
In the screen_time_behavior dataset, all age groups, genders, and platforms show nearly identical weekday screen hours (~5.5 hrs) and focus span (~18 mins). Demographic variables do not predict usage intensity.

### Finding 4 — Sleep is not a reliable addiction signal
Despite TikTok usage driving addiction scores strongly, sleep hours do not decline consistently with addiction level. High addiction users sleep 7.00 hrs vs 7.27 hrs for Low — a 16-minute difference that is unlikely to be practically significant.

### Finding 5 — Mental health infrastructure does not offset usage-driven addiction
MHRI shows near-zero correlation with addiction score at both individual and country level. Countries with strong mental health resources are not protected from high addiction scores if TikTok usage is high.

---

## 12. Limitations

| Limitation | Implication |
|---|---|
| **Severe class has 1 user** | All Severe-level statistics are meaningless for generalisation. Merge with High for any further analysis. |
| **Class imbalance** | 86.8% of Dataset 3 is classified as High addiction. Medium and Low findings are based on far fewer users. |
| **Addiction Score is an index, not a clinical measure** | The score appears to be a constructed composite. It should not be interpreted as a clinical diagnosis. |
| **Ecological fallacy risk** | Country-level correlations (Dataset 1) do not imply individual-level effects. Do not use country findings to make claims about individuals. |
| **Synthetic year data** | The `year` column in Dataset 2 extends to 2038, suggesting simulated data. Trend-over-time analysis may not reflect reality. |
| **No causal claims** | All findings are correlational. TikTok usage correlating with addiction does not mean TikTok causes addiction. |

---

## Dependencies

```
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
numpy>=1.24.0
openpyxl>=3.1.0
```

---

*Analysis conducted as part of an Exploratory Data Analysis project on social media addiction patterns.*
