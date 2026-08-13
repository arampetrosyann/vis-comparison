import matplotlib.pyplot as plt
import pandas as pd

def plot(data: pd.DataFrame):
    plt.scatter(data['SIZE'], data['RX-GOODPUT-GBPS-PKTGEN'], c=data['RX-RATE-MBPS'], cmap='viridis', alpha=0.6)
    plt.colorbar(label='RX-RATE-MBPS')
    plt.xlabel('SIZE')
    plt.ylabel('RX-GOODPUT-GBPS-PKTGEN')
    plt.axvline(data['SIZE'].mean(), color='red', linestyle='--', label=f'Mean SIZE: {data["SIZE"].mean():.2f}')
    plt.axhline(data['RX-GOODPUT-GBPS-PKTGEN'].mean(), color='blue', linestyle='--', label=f'Mean RX-GOODPUT-GBPS-PKTGEN: {data["RX-GOODPUT-GBPS-PKTGEN"].mean():.2f}')
    plt.legend()
    plt.title('How does the receive goodput in gigabits per second (RX-GOODPUT-GBPS-PKTGEN) vary with the packet size (SIZE) for different receive rates in megabits per second (RX-RATE-MBPS)?', wrap=True)
    return plt;

chart = plot(data)