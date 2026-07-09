import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    plt.hist(data['RX-RATE-PPS'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(data['RX-RATE-PPS'].mean(), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {data["RX-RATE-PPS"].mean():.2f}')
    plt.xlabel('RX-RATE-PPS')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title('What is the distribution of RX-RATE-PPS?', wrap=True)
    return plt;

chart = plot(data)