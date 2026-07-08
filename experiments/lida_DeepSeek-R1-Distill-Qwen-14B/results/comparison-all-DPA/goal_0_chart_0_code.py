import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    # Create a bar plot showing the distribution of y_RX-RATE-MBPS across different builds
    sns.barplot(x='build', y='y_RX-RATE-MBPS', data=data, ci='sd', palette='deep')
    
    # Add title and axis labels
    plt.title('How does the RX rate in MBPS vary across different builds?', wrap=True)
    plt.xlabel('Build Type')
    plt.ylabel('RX Rate (MBPS)')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    return plt

chart = plot(data)