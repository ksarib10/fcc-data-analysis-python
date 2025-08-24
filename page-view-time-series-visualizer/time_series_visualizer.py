import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import os, math
register_matplotlib_converters()

# Import data (parse dates and set index column to 'date')
df = pd.read_csv("page-view-time-series-visualizer/fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Method 1 (using slicing)
import math
tot = df['value'].count()
dfc = pd.concat([df.iloc[:math.floor(tot*0.025)], df.iloc[math.floor(tot*0.975)-1:]])['value']
df = df.drop(dfc.index)

# Method 2 (using quantile)
# Clean data: remove top 2.5% and bottom 2.5%
# low = df["value"].quantile(0.025)
# high = df["value"].quantile(0.975)
# df = df[(df["value"] >= low) & (df["value"] <= high)]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], color="red", linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Saving image to examples folder and return fig
    os.makedirs("page-view-time-series-visualizer/examples", exist_ok=True)
    fig.savefig("page-view-time-series-visualizer/examples/line_plot.png")
    return fig
    

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack() 

    # Draw bar plot
    fig = df_bar.plot.bar(figsize=(10, 7), ylabel="Average Page Views", xlabel="Years").get_figure()
    plt.legend(
        title="Months",
        labels=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
    )
    # Saving image to examples folder and return fig
    os.makedirs("page-view-time-series-visualizer/examples", exist_ok=True)
    fig.savefig("page-view-time-series-visualizer/examples/bar_plot.png")
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy().reset_index()
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise Box Plot (Seasonality)
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    y_ticks = list(range(0, 200001, 20000))
    axes[0].set_ylim(0, 200000)
    axes[0].set_yticks(y_ticks)
    axes[0].set_yticklabels([str(v) for v in y_ticks])

    # Save and return
    os.makedirs("page-view-time-series-visualizer/examples", exist_ok=True)
    fig.savefig("page-view-time-series-visualizer/examples/box_plot.png")
    return fig

draw_line_plot()
draw_bar_plot()
draw_box_plot()