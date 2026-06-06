"""
Social Media Addiction — Exploratory Data Analysis
====================================================
Datasets:
  - country_wise_analysis_addiction.xlsx  (100 rows, country-level aggregates)
  - screen_time_behavior.xlsx             (50,000 rows, individual behaviour)
  - tiktok_instagram_global_100countries.xlsx (10,000 rows, individual + socioeconomic)

Run:
    python src/eda_analysis.py

Outputs:
    images/01_screen_time_overview.png
    images/02_addiction_level_breakdown.png
    images/03_correlation_heatmap.png
    images/04_country_analysis.png
    images/05_relationship_deep_dive.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import io
import warnings
warnings.filterwarnings('ignore')

# ── Palette ───────────────────────────────────────────────────────────────────
BLUE   = '#185FA5'
TEAL   = '#0F6E56'
AMBER  = '#BA7517'
PURPLE = '#534AB7'
CORAL  = '#993C1D'
GRAY   = '#888780'

LEVEL_COLORS  = {'Low': TEAL, 'Medium': AMBER, 'High': BLUE, 'Severe': CORAL}
AGE_COLORS    = [BLUE, TEAL, AMBER, PURPLE, CORAL]
GENDER_COLORS = {'Female': BLUE, 'Male': TEAL, 'Other': AMBER}

plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.facecolor':     '#FAFAF8',
    'figure.facecolor':   'white',
    'axes.grid':          True,
    'grid.color':         '#E0DED8',
    'grid.linewidth':     0.5,
    'axes.labelsize':     11,
    'axes.titlesize':     13,
    'axes.titleweight':   'bold',
    'xtick.labelsize':    10,
    'ytick.labelsize':    10,
})

# ── Data loading ──────────────────────────────────────────────────────────────
def read_csv_xlsx(path):
    """Read files that are stored as CSV inside an xlsx wrapper."""
    df_raw = pd.read_excel(path, header=0)
    col    = df_raw.columns[0]
    rows   = [col] + df_raw[col].tolist()
    return pd.read_csv(io.StringIO('\n'.join(rows)))


def load_data():
    screen  = read_csv_xlsx('data/screen_time_behavior.xlsx')
    tiktok  = pd.read_excel('data/tiktok_instagram_global_100countries.xlsx')
    country = read_csv_xlsx('data/country_wise_analysis_addiction.xlsx')

    # Derive age groups for tiktok dataset (Age is continuous)
    bins   = [0, 17, 25, 40, 60, 120]
    labels = ['Under 18', '18–25', '26–40', '41–60', '60+']
    tiktok['Age Group'] = pd.cut(tiktok['Age'], bins=bins, labels=labels)

    # Ordered categorical for clean plot ordering
    lvl_order = ['Low', 'Medium', 'High', 'Severe']
    tiktok['Addiction Level'] = pd.Categorical(
        tiktok['Addiction Level'], categories=lvl_order, ordered=True
    )
    return screen, tiktok, country


# ── Helpers ───────────────────────────────────────────────────────────────────
def save(fig, name):
    fig.savefig(f'images/{name}', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved images/{name}')


def section_title(fig, text, y=0.98):
    fig.text(0.5, y, text, ha='center', va='top',
             fontsize=16, fontweight='bold', color='#2C2C2A')


def annotate_bars(ax, fmt='{:.1f}', fontsize=9):
    for p in ax.patches:
        h = p.get_height()
        if pd.notna(h) and h > 0:
            ax.annotate(fmt.format(h),
                        (p.get_x() + p.get_width() / 2, h),
                        ha='center', va='bottom', fontsize=fontsize, color='#2C2C2A')


def trend_line(ax, x, y, color=CORAL):
    m, b = np.polyfit(x, y, 1)
    xs   = np.linspace(x.min(), x.max(), 100)
    r    = np.corrcoef(x, y)[0, 1]
    ax.plot(xs, m * xs + b, '--', color=color, linewidth=1.5)
    return r


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Dataset 2: Screen Time Overview & Pivot Tables
# ══════════════════════════════════════════════════════════════════════════════
def chart_screen_time(screen):
    fig = plt.figure(figsize=(18, 14))
    section_title(fig, 'Dataset 2 — Screen Time Behaviour: Overview & Pivot Tables')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35,
                            top=0.92, bottom=0.06)
    age_order = ['Children', 'Teen', 'Young Adult', 'Adult', 'Senior']

    # Pivot 1: avg weekday screen hours by age group
    ax = fig.add_subplot(gs[0, 0])
    p1 = screen.groupby('age_group')['weekday_screen_hours'].mean().reindex(age_order)
    ax.bar(p1.index, p1.values, color=AGE_COLORS, edgecolor='white', linewidth=0.8)
    ax.set_title('Avg Weekday Screen Hours\nby Age Group')
    ax.set_ylabel('Hours')
    ax.set_ylim(0, p1.max() * 1.25)
    ax.tick_params(axis='x', rotation=20)
    annotate_bars(ax)

    # Pivot 2: avg focus span by age group × gender
    ax = fig.add_subplot(gs[0, 1])
    p2 = screen.pivot_table(index='age_group', columns='gender',
                             values='focus_span_minutes',
                             aggfunc='mean').reindex(age_order)
    x, w = np.arange(len(p2)), 0.25
    for i, (g, col) in enumerate(GENDER_COLORS.items()):
        ax.bar(x + i * w, p2[g], w, label=g, color=col, edgecolor='white')
    ax.set_xticks(x + w)
    ax.set_xticklabels(p2.index, rotation=20)
    ax.set_title('Avg Focus Span (mins)\nby Age Group & Gender')
    ax.set_ylabel('Minutes')
    ax.legend(fontsize=8, frameon=False)
    ax.set_ylim(0, p2.max().max() * 1.25)

    # Pivot 3: avg focus span by platform
    ax = fig.add_subplot(gs[0, 2])
    p3 = screen.groupby('platform')['focus_span_minutes'].mean().sort_values()
    colors_p = [BLUE if v == p3.max() else CORAL if v == p3.min() else GRAY for v in p3.values]
    ax.barh(p3.index, p3.values, color=colors_p, edgecolor='white')
    ax.set_title('Avg Focus Span (mins)\nby Platform')
    ax.set_xlabel('Minutes')
    for i, val in enumerate(p3.values):
        ax.text(val + 0.05, i, f'{val:.1f}', va='center', fontsize=9)

    # Relationship: weekday vs weekend screen hours
    ax = fig.add_subplot(gs[1, 0])
    for i, ag in enumerate(age_order):
        sub = screen[screen['age_group'] == ag]
        ax.scatter(sub['weekday_screen_hours'], sub['weekend_screen_hours'],
                   alpha=0.08, s=8, color=AGE_COLORS[i], label=ag)
    lims = [screen[['weekday_screen_hours', 'weekend_screen_hours']].min().min(),
            screen[['weekday_screen_hours', 'weekend_screen_hours']].max().max()]
    ax.plot(lims, lims, '--', color=GRAY, linewidth=1, alpha=0.6)
    ax.set_title('Weekday vs Weekend Screen Hours\n(relationship)')
    ax.set_xlabel('Weekday Hours')
    ax.set_ylabel('Weekend Hours')
    ax.legend(fontsize=7, frameon=False, markerscale=2)

    # Relationship: physical activity vs focus span
    ax = fig.add_subplot(gs[1, 1])
    for i, ag in enumerate(age_order):
        sub = screen[screen['age_group'] == ag].sample(500, random_state=42)
        ax.scatter(sub['physical_activity_hours_weekly'], sub['focus_span_minutes'],
                   alpha=0.2, s=8, color=AGE_COLORS[i], label=ag)
    ax.set_title('Physical Activity vs Focus Span\n(relationship)')
    ax.set_xlabel('Physical Activity (hrs/week)')
    ax.set_ylabel('Focus Span (mins)')
    ax.legend(fontsize=7, frameon=False, markerscale=2)

    # Multitasking frequency distribution by age
    ax = fig.add_subplot(gs[1, 2])
    data_box = [screen[screen['age_group'] == ag]['multitasking_frequency'].values
                for ag in age_order]
    bp = ax.boxplot(data_box, patch_artist=True,
                    medianprops=dict(color='white', linewidth=2))
    for patch, col in zip(bp['boxes'], AGE_COLORS):
        patch.set_facecolor(col)
        patch.set_alpha(0.85)
    ax.set_xticklabels(age_order, rotation=20)
    ax.set_title('Multitasking Frequency\nby Age Group')
    ax.set_ylabel('Frequency')

    save(fig, '01_screen_time_overview.png')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 — Dataset 3: Addiction Level Breakdown
# ══════════════════════════════════════════════════════════════════════════════
def chart_addiction_breakdown(tiktok):
    fig = plt.figure(figsize=(18, 14))
    section_title(fig, 'Dataset 3 — TikTok/Instagram: Addiction Level Breakdown')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35,
                            top=0.92, bottom=0.06)
    lvl_order    = ['Low', 'Medium', 'High', 'Severe']
    lvl_palette  = [LEVEL_COLORS[l] for l in lvl_order]

    for col_idx, (metric, title, ylabel) in enumerate([
        ('Tiktok Minutes Daily', 'Avg TikTok Minutes/Day\nby Addiction Level', 'Minutes'),
        ('Sleep Hours',          'Avg Sleep Hours\nby Addiction Level',          'Hours'),
        ('Attention Span Score', 'Avg Attention Span Score\nby Addiction Level', 'Score'),
    ]):
        ax = fig.add_subplot(gs[0, col_idx])
        p  = tiktok.groupby('Addiction Level', observed=True)[metric].mean().reindex(lvl_order)
        ax.bar(p.index, p.values, color=lvl_palette, edgecolor='white')
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_ylim(0, p.max() * 1.3)
        annotate_bars(ax, fmt='{:.1f}')

    # Relationship: TikTok minutes vs addiction score
    ax = fig.add_subplot(gs[1, 0])
    for lvl in ['Low', 'Medium', 'High']:
        sub = tiktok[tiktok['Addiction Level'] == lvl].sample(
            min(300, (tiktok['Addiction Level'] == lvl).sum()), random_state=1)
        ax.scatter(sub['Tiktok Minutes Daily'], sub['Addiction Score'],
                   alpha=0.35, s=14, color=LEVEL_COLORS[lvl], label=lvl)
    r = trend_line(ax, tiktok['Tiktok Minutes Daily'], tiktok['Addiction Score'])
    ax.set_title(f'TikTok Minutes vs Addiction Score\n(r = {r:.2f})')
    ax.set_xlabel('TikTok Minutes/Day')
    ax.set_ylabel('Addiction Score')
    ax.legend(fontsize=8, frameon=False)

    # Relationship: sleep hours vs attention span
    ax = fig.add_subplot(gs[1, 1])
    for lvl in ['Low', 'Medium', 'High']:
        sub = tiktok[tiktok['Addiction Level'] == lvl].sample(
            min(300, (tiktok['Addiction Level'] == lvl).sum()), random_state=2)
        ax.scatter(sub['Sleep Hours'], sub['Attention Span Score'],
                   alpha=0.35, s=14, color=LEVEL_COLORS[lvl], label=lvl)
    ax.set_title('Sleep Hours vs Attention Span Score\n(relationship)')
    ax.set_xlabel('Sleep Hours')
    ax.set_ylabel('Attention Span Score')
    ax.legend(fontsize=8, frameon=False)

    # Relationship: dopamine dependency vs impulsivity
    ax = fig.add_subplot(gs[1, 2])
    for lvl in ['Low', 'Medium', 'High']:
        sub = tiktok[tiktok['Addiction Level'] == lvl].sample(
            min(300, (tiktok['Addiction Level'] == lvl).sum()), random_state=3)
        ax.scatter(sub['Dopamine Dependency Score'], sub['Impulsivity Index'],
                   alpha=0.35, s=14, color=LEVEL_COLORS[lvl], label=lvl)
    r = np.corrcoef(tiktok['Dopamine Dependency Score'], tiktok['Impulsivity Index'])[0, 1]
    ax.set_title(f'Dopamine Dependency vs Impulsivity\n(r = {r:.2f})')
    ax.set_xlabel('Dopamine Dependency Score')
    ax.set_ylabel('Impulsivity Index')
    ax.legend(fontsize=8, frameon=False)

    save(fig, '02_addiction_level_breakdown.png')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 — Correlation Heatmap (Dataset 3)
# ══════════════════════════════════════════════════════════════════════════════
def chart_correlation(tiktok):
    fig, ax = plt.subplots(figsize=(14, 11))
    section_title(fig, 'Dataset 3 — Spearman Correlation Matrix', y=0.99)

    num_cols = [
        'Tiktok Minutes Daily', 'Instagram Minutes Daily', 'Night Usage Ratio',
        'Scroll Velocity', 'Addiction Score', 'Attention Span Score',
        'Dopamine Dependency Score', 'Impulsivity Index',
        'Sleep Hours', 'Sleep Quality Index', 'Gdp Index',
        'Internet Penetration', 'MHRI', 'ASI',
    ]
    corr = tiktok[num_cols].corr(method='spearman')
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(220, 20, as_cmap=True)

    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
                annot=True, fmt='.2f', annot_kws={'size': 8},
                linewidths=0.4, linecolor='white', ax=ax,
                cbar_kws={'shrink': 0.7, 'label': 'Spearman r'})
    ax.set_title('Spearman Correlation — Key Variables', pad=15)
    ax.tick_params(axis='x', rotation=40, labelsize=9)
    ax.tick_params(axis='y', rotation=0,  labelsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    save(fig, '03_correlation_heatmap.png')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 — Country-Level Analysis (Dataset 1)
# ══════════════════════════════════════════════════════════════════════════════
def chart_country(country):
    fig = plt.figure(figsize=(18, 12))
    section_title(fig, 'Country-Level Analysis — Addiction, GDP & Mental Health')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38,
                            top=0.92, bottom=0.06)

    # Top 15 countries by addiction score
    ax    = fig.add_subplot(gs[0, :2])
    top15 = country.sort_values('addiction_rank').head(15)
    colors_rank = [CORAL if r <= 5 else AMBER if r <= 10 else BLUE
                   for r in top15['addiction_rank']]
    ax.barh(top15['country'], top15['addiction_score'],
            color=colors_rank, edgecolor='white')
    ax.set_title('Top 15 Countries by Addiction Score')
    ax.set_xlabel('Addiction Score')
    ax.invert_yaxis()
    for score, rank in zip(top15['addiction_score'], top15['addiction_rank']):
        ax.text(score + 0.05, list(top15['addiction_rank']).index(rank),
                f'#{rank}  {score:.1f}', va='center', fontsize=9)
    patches = [mpatches.Patch(color=CORAL, label='Rank 1–5'),
               mpatches.Patch(color=AMBER, label='Rank 6–10'),
               mpatches.Patch(color=BLUE,  label='Rank 11–15')]
    ax.legend(handles=patches, fontsize=8, frameon=False)

    # Addiction score distribution
    ax = fig.add_subplot(gs[0, 2])
    ax.hist(country['addiction_score'], bins=20, color=BLUE,
            edgecolor='white', alpha=0.85)
    ax.axvline(country['addiction_score'].mean(), color=CORAL,
               linewidth=1.5, linestyle='--',
               label=f'Mean: {country["addiction_score"].mean():.1f}')
    ax.set_title('Distribution of Addiction Score\n(all 100 countries)')
    ax.set_xlabel('Addiction Score')
    ax.set_ylabel('Count')
    ax.legend(fontsize=9, frameon=False)

    # MHRI vs addiction score
    ax = fig.add_subplot(gs[1, 0])
    ax.scatter(country['MHRI'], country['addiction_score'],
               color=PURPLE, alpha=0.6, s=40, edgecolors='white', linewidth=0.5)
    r = trend_line(ax, country['MHRI'], country['addiction_score'])
    ax.set_title(f'MHRI vs Addiction Score\n(r = {r:.2f})')
    ax.set_xlabel('Mental Health Resource Index (MHRI)')
    ax.set_ylabel('Addiction Score')

    # TikTok minutes vs addiction score (country level)
    ax = fig.add_subplot(gs[1, 1])
    ax.scatter(country['tiktok_minutes_daily'], country['addiction_score'],
               color=TEAL, alpha=0.6, s=40, edgecolors='white', linewidth=0.5)
    r = trend_line(ax, country['tiktok_minutes_daily'], country['addiction_score'])
    ax.set_title(f'TikTok Minutes vs Addiction Score\nby Country (r = {r:.2f})')
    ax.set_xlabel('Avg TikTok Minutes/Day')
    ax.set_ylabel('Addiction Score')

    # Sleep hours vs attention span (country level)
    ax = fig.add_subplot(gs[1, 2])
    ax.scatter(country['sleep_hours'], country['attention_span_score'],
               color=AMBER, alpha=0.6, s=40, edgecolors='white', linewidth=0.5)
    r = trend_line(ax, country['sleep_hours'], country['attention_span_score'])
    ax.set_title(f'Sleep Hours vs Attention Span\nby Country (r = {r:.2f})')
    ax.set_xlabel('Avg Sleep Hours')
    ax.set_ylabel('Avg Attention Span Score')

    save(fig, '04_country_analysis.png')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 5 — Relationship Deep Dive (Dataset 3)
# ══════════════════════════════════════════════════════════════════════════════
def chart_relationships(tiktok, country):
    fig = plt.figure(figsize=(18, 14))
    section_title(fig, 'Relationship Deep Dive — Usage, Wellbeing & Addiction')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38,
                            top=0.92, bottom=0.06)
    lvl_order  = ['Low', 'Medium', 'High', 'Severe']
    age_order  = ['Under 18', '18–25', '26–40', '41–60', '60+']

    # Night usage ratio by addiction level (violin)
    ax = fig.add_subplot(gs[0, 0])
    data_v = [tiktok[tiktok['Addiction Level'] == lvl]['Night Usage Ratio'].dropna().values
              for lvl in lvl_order[:-1]]
    parts = ax.violinplot(data_v, positions=range(3), showmedians=True)
    for pc, lvl in zip(parts['bodies'], lvl_order):
        pc.set_facecolor(LEVEL_COLORS[lvl])
        pc.set_alpha(0.7)
    parts['cmedians'].set_color('white')
    parts['cmedians'].set_linewidth(2)
    ax.set_xticks(range(3))
    ax.set_xticklabels(['Low', 'Medium', 'High'])
    ax.set_title('Night Usage Ratio\nby Addiction Level')
    ax.set_ylabel('Night Usage Ratio')

    # Scroll velocity vs addiction score (coloured by TikTok usage)
    ax = fig.add_subplot(gs[0, 1])
    sample = tiktok.sample(2000, random_state=10)
    sc = ax.scatter(sample['Scroll Velocity'], sample['Addiction Score'],
                    c=sample['Tiktok Minutes Daily'], cmap='YlOrRd',
                    alpha=0.5, s=18, edgecolors='none')
    plt.colorbar(sc, ax=ax, label='TikTok Mins/Day', shrink=0.8)
    r = np.corrcoef(tiktok['Scroll Velocity'], tiktok['Addiction Score'])[0, 1]
    ax.set_title(f'Scroll Velocity vs Addiction Score\n(colour = TikTok mins, r = {r:.2f})')
    ax.set_xlabel('Scroll Velocity')
    ax.set_ylabel('Addiction Score')

    # Addiction score distribution by derived age group
    ax = fig.add_subplot(gs[0, 2])
    data_age = [tiktok[tiktok['Age Group'] == ag]['Addiction Score'].dropna().values
                for ag in age_order]
    bp = ax.boxplot(data_age, patch_artist=True,
                    medianprops=dict(color='white', linewidth=2))
    for patch, col in zip(bp['boxes'], AGE_COLORS):
        patch.set_facecolor(col)
        patch.set_alpha(0.85)
    ax.set_xticklabels(age_order, rotation=20)
    ax.set_title('Addiction Score Distribution\nby Age Group')
    ax.set_ylabel('Addiction Score')

    # TikTok vs Instagram minutes by addiction level
    ax = fig.add_subplot(gs[1, 0])
    for lvl in ['Low', 'Medium', 'High']:
        sub = tiktok[tiktok['Addiction Level'] == lvl].sample(
            min(300, (tiktok['Addiction Level'] == lvl).sum()), random_state=4)
        ax.scatter(sub['Tiktok Minutes Daily'], sub['Instagram Minutes Daily'],
                   alpha=0.35, s=14, color=LEVEL_COLORS[lvl], label=lvl)
    ax.set_title('TikTok vs Instagram Minutes\nby Addiction Level')
    ax.set_xlabel('TikTok Minutes/Day')
    ax.set_ylabel('Instagram Minutes/Day')
    ax.legend(fontsize=8, frameon=False)

    # ASI vs MHRI by country (coloured by addiction score)
    ax = fig.add_subplot(gs[1, 1])
    sc = ax.scatter(country['ASI'], country['MHRI'],
                    c=country['addiction_score'], cmap='RdYlGn_r',
                    s=55, alpha=0.75, edgecolors='white', linewidth=0.5)
    plt.colorbar(sc, ax=ax, label='Addiction Score', shrink=0.8)
    r = np.corrcoef(country['ASI'], country['MHRI'])[0, 1]
    ax.set_title(f'ASI vs MHRI by Country\n(colour = addiction score, r = {r:.2f})')
    ax.set_xlabel('Addiction Severity Index (ASI)')
    ax.set_ylabel('Mental Health Resource Index (MHRI)')

    # Summary heatmap — key metrics by addiction level (normalised)
    ax = fig.add_subplot(gs[1, 2])
    metrics = ['Tiktok Minutes Daily', 'Instagram Minutes Daily', 'Sleep Hours',
               'Attention Span Score', 'Dopamine Dependency Score', 'Impulsivity Index']
    short   = ['TikTok\nmins', 'Instagram\nmins', 'Sleep\nhours',
               'Attention\nspan', 'Dopamine\ndep.', 'Impulsivity']
    summary      = tiktok.groupby('Addiction Level', observed=True)[metrics].mean().reindex(lvl_order[:-1])
    summary_norm = (summary - summary.min()) / (summary.max() - summary.min())

    sns.heatmap(summary_norm.T, annot=summary.T.round(1), fmt='.1f',
                cmap='RdYlGn_r', ax=ax, linewidths=0.5, linecolor='white',
                cbar_kws={'shrink': 0.7, 'label': 'Normalised'},
                yticklabels=short)
    ax.set_title('Key Metrics by Addiction Level\n(normalised, raw values annotated)')
    ax.set_xlabel('Addiction Level')
    ax.tick_params(axis='y', rotation=0, labelsize=8)

    save(fig, '05_relationship_deep_dive.png')


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Loading data...')
    screen, tiktok, country = load_data()

    print('Generating charts...')
    chart_screen_time(screen)
    chart_addiction_breakdown(tiktok)
    chart_correlation(tiktok)
    chart_country(country)
    chart_relationships(tiktok, country)

    print('\nDone. All charts saved to images/')
