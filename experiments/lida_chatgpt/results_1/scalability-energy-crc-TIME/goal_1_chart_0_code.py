import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    sns.scatterplot(data=data, x='NTHREADS', y='CPUFREQ', palette='viridis')
    plt.title('How does the CPU frequency vary with the number of threads?', wrap=True)
    plt.legend(title='CPU Frequency vs. Number of Threads')
    plt.axvline(data['NTHREADS'].mean(), color='red', linestyle='--', label=f'Mean NTHREADS: {data["NTHREADS"].mean():.2f}')
    plt.axhline(data['CPUFREQ'].mean(), color='blue', linestyle='--', label=f'Mean CPUFREQ: {data["CPUFREQ"].mean():.2f}')
    return plt;

chart = plot(data)