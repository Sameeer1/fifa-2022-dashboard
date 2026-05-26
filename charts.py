import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ---------------------------------------------------------
# FIFA 2022 THEME COLORS
# ---------------------------------------------------------
FIFA_MAROON = '#8A1538'
FIFA_GOLD = '#EEB211'
DARK_GREY = '#333333'
LIGHT_BG = '#F8F9FA'

def set_theme():
    """Sets the global FIFA 2022 theme for all plots."""
    sns.set_theme(style="whitegrid")
    plt.rcParams['axes.facecolor'] = LIGHT_BG
    plt.rcParams['figure.facecolor'] = LIGHT_BG
    plt.rcParams['text.color'] = DARK_GREY
    plt.rcParams['axes.labelcolor'] = DARK_GREY
    plt.rcParams['xtick.color'] = DARK_GREY
    plt.rcParams['ytick.color'] = DARK_GREY

# ---------------------------------------------------------
# CHART FUNCTIONS (10 REQUIRED CHARTS)
# ---------------------------------------------------------

# 1. Pie Chart
def plot_pie_chart(df, category_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(6, 6))
    data = df[category_col].value_counts()
    colors = [FIFA_MAROON, FIFA_GOLD, DARK_GREY, '#A42A4F', '#F5D061']
    ax.pie(data, labels=data.index, autopct='%1.1f%%', colors=colors, startangle=140)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    return fig

# 2. Histogram
def plot_histogram(df, numeric_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df[numeric_col], bins=15, color=FIFA_MAROON, kde=False, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    return fig

# 3. Line Chart
def plot_line_chart(df, x_col, y_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x=x_col, y=y_col, color=FIFA_GOLD, linewidth=2.5, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 4. Bar Chart
def plot_bar_chart(df, x_col, y_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=df, x=x_col, y=y_col, color=FIFA_MAROON, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 5. Scatter Plot
def plot_scatter_plot(df, x_col, y_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x=x_col, y=y_col, color=FIFA_GOLD, edgecolor=FIFA_MAROON, s=100, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    return fig

# 6. Box Plot
def plot_box_plot(df, x_col, y_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x=x_col, y=y_col, color=FIFA_GOLD, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    return fig

# 7. Heatmap
def plot_heatmap(df, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(8, 6))
    # Select only numeric columns for correlation matrix
    numeric_df = df.select_dtypes(include=['number'])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap=sns.light_palette(FIFA_MAROON, as_cmap=True), ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    return fig

# 8. Area Chart
def plot_area_chart(df, x_col, y_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(df[x_col], df[y_col], color=FIFA_GOLD, alpha=0.5)
    ax.plot(df[x_col], df[y_col], color=FIFA_MAROON, alpha=0.8, linewidth=2)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 9. Count Plot
def plot_count_plot(df, category_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(data=df, y=category_col, order=df[category_col].value_counts().index, color=FIFA_MAROON, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    return fig

# 10. Violin Plot
def plot_violin_plot(df, x_col, y_col, title):
    set_theme()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.violinplot(data=df, x=x_col, y=y_col, color=FIFA_GOLD, ax=ax)
    ax.set_title(title, fontsize=14, fontweight='bold', color=FIFA_MAROON)
    return fig