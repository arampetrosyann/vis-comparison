import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(10, 8))
    ax = sns.scatterplot(x='SIZE', y='RX-RATE-PPS', hue='RX-GOODPUT-GBPS-PKTGEN', data=data, s=100, alpha=0.7)
    ax.set_xlabel('Packet Size (SIZE)')
    ax.set_ylabel('Receive Rate (RX-RATE-PPS)')
    ax.set_title('How does the receive rate (RX-RATE-PPS) and goodput (RX-GOODPUT-GBPS-PKTGEN) vary across different packet sizes (SIZE) and number of threads (NTHREADS)?', wrap=True)
    ax.legend(title='Goodput (RX-GOODPUT-GBPS-PKTGEN)')
    return plt

chart = plot(data)