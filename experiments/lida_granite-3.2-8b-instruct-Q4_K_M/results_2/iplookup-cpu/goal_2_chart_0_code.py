import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='SIZE', y='AVG-LAT', hue='NTHREADS', data=data)
    sns.boxplot(x='SIZE', y='LOSE-RATE', hue='NTHREADS', data=data)
    plt.title('What is the distribution of latency (AVG-LAT) and loss rate (LOSE-RATE) across different packet sizes (SIZE) and number of threads (NTHREADS)?', wrap=True)
    plt.legend(title='Number of Threads')
    return plt

chart = plot(data)