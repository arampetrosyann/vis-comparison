import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='NTHREADS', y='SIZE', hue='SIZE', data=data, s=100, alpha=0.7)
    plt.title('What is the distribution of packet sizes (SIZE) and how does it vary with the number of threads (NTHREADS)?', wrap=True)
    plt.legend(title='Packet Size (Bytes)')
    return plt

chart = plot(data)