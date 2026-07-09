import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    sns.barplot(x='NTHREADS', y='RX-RATE-MBPS', data=data, ci=None, palette='viridis')
    plt.title('How does RX-RATE-MBPS vary with different values of NTHREADS?', wrap=True)
    plt.legend(title='RX-RATE-MBPS', loc='upper right')
    plt.axhline(data['RX-RATE-MBPS'].mean(), color='red', linestyle='--', label=f'Mean: {data["RX-RATE-MBPS"].mean():.2f}')
    return plt;

chart = plot(data)