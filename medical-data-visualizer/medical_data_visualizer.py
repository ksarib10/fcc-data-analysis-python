import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os


# Loading the data
df = pd.read_csv("medical-data-visualizer/medical_examination.csv")

# Adding 'overweight' column
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# Normalizing cholesterol and gluc
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

def draw_cat_plot():

    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"]
    )

    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="total")

    g = sns.catplot(
        data=df_cat,
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        kind="bar"
    )

    fig = g.fig
    os.makedirs("medical-data-visualizer/examples", exist_ok=True)
    fig.savefig("medical-data-visualizer/examples/catplot.png")

    return fig


def draw_heat_map():

    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    corr = df_heat.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        cbar_kws={"shrink": .5}
    )

    os.makedirs("medical-data-visualizer/examples", exist_ok=True)
    fig.savefig("medical-data-visualizer/examples/heatmap.png")
    return fig
