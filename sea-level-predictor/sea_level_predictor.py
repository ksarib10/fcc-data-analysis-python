import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

def draw_plot():
    # Read data from file
    df = pd.read_csv('sea-level-predictor/epa-sea-level.csv')

    # Create scatter plot
    fig = plt.figure(figsize=(14, 8))
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], label='Data', alpha=0.6)

    # Create first line of best fit
    slope_all, intercept_all, _, _, _ = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    years_all = pd.Series(range(1880, 2051))
    plt.plot(years_all, intercept_all + slope_all * years_all, 'r', label="Fit: 1880-2050")     

    # Create second line of best fit
    df_recent = df[df['Year'] >= 2000]
    slope_recent, intercept_recent, _, _, _ = linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    years_recent = pd.Series(range(2000, 2051))
    plt.plot(years_recent, intercept_recent + slope_recent * years_recent, 'g', label="Fit: 2000-2050")

    # Add labels and title
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")
    plt.legend()
    
    # Save plot and return data for testing (DO NOT MODIFY)
    os.makedirs("sea-level-predictor/", exist_ok=True)
    fig.savefig("sea-level-predictor/sea_level_plot.png")
    return plt.gca()

draw_plot()
