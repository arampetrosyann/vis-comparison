import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    avg_loss_rate = data.groupby('NTHREADS')['LOSE-RATE'].mean()
    avg_loss_rate.plot(kind='bar', color='skyblue', edgecolor='black', legend=True)
    plt.xlabel('Number of Threads')
    plt.ylabel('Average Loss Rate')
    plt.axhline(y=avg_loss_rate.mean(), color='red', linestyle='--', label=f'Mean: {avg_loss_rate.mean():.2f}')
    plt.legend()
    plt.title('What is the distribution of packet loss rates (LOSE-RATE) across different thread counts (NTHREADS)?', wrap=True)
    return plt;

chart = plot(data)