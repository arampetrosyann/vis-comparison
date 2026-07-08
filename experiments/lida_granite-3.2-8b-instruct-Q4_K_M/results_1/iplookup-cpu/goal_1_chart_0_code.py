import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='SIZE', y='RX-RATE-PPS', hue='NTHREADS', data=data, s=100, alpha=0.7)
    plt.title('How does the RX-RATE-PPS vary with SIZE for different NTHREADS?', wrap=True)
    plt.xlabel('SIZE')
    plt.ylabel('RX-RATE-PPS')
    plt.legend(title='NTHREADS')
    return plt

chart = plot(data)