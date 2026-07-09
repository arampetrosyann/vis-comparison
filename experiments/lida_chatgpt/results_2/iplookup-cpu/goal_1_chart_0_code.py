import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    data_grouped = data.groupby('NTHREADS')['RX-RATE-MBPS'].mean()
    data_grouped.plot(kind='bar', color='skyblue', edgecolor='black', legend=True)
    plt.xlabel('NTHREADS')
    plt.ylabel('Average RX-RATE-MBPS')
    plt.axhline(data['RX-RATE-MBPS'].mean(), color='red', linestyle='--', label=f'Mean RX-RATE-MBPS: {data["RX-RATE-MBPS"].mean():.2f}')
    plt.legend()
    return plt;

chart = plot(data)