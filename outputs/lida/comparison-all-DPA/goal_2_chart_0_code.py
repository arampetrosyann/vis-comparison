import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    avg_loss_rate = data.groupby('SIZE')['y_LOSE-RATE'].mean()
    avg_loss_rate.plot(kind='bar', color='skyblue', edgecolor='black', legend=True)
    plt.xlabel('Packet Size (SIZE)')
    plt.ylabel('Average Loss Rate (y_LOSE-RATE)')
    plt.axhline(avg_loss_rate.mean(), color='red', linestyle='--', label=f'Mean: {avg_loss_rate.mean():.2f}')
    plt.legend()
    plt.title('What is the average loss rate (y_LOSE-RATE) across different packet sizes (SIZE)?', wrap=True)
    return plt;

chart = plot(data)