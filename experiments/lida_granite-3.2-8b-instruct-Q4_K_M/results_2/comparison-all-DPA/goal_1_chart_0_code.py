import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(10, 8))
    sns.heatmap(data[['SIZE', 'NTHREADS', 'y_RX-RATE-PPS', 'y_RX-RATE-MBPS']], cmap='viridis', annot=True, fmt=".2f", linewidths=.5, cbar_kws={"shrink": .5})
    plt.title('How does the receive rate (y_RX-RATE-PPS) and receive rate in MBPS (y_RX-RATE-MBPS) vary across different packet sizes (SIZE) and number of threads (NTHREADS)?', wrap=True)
    return plt

chart = plot(data)