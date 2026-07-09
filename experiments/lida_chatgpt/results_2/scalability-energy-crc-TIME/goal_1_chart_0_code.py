import matplotlib.pyplot as plt
import pandas as pd

def plot(data: pd.DataFrame):
    plt.scatter(data['NTHREADS'], data['CPUFREQ'], c='blue', alpha=0.6, label='CPU Frequency vs. Number of Threads')
    plt.xlabel('Number of Threads')
    plt.ylabel('CPU Frequency')
    plt.axvline(data['NTHREADS'].median(), color='red', linestyle='--', label='Median NTHREADS: {:.2f}'.format(data['NTHREADS'].median()))
    plt.axhline(data['CPUFREQ'].median(), color='green', linestyle='--', label='Median CPUFREQ: {:.2f}'.format(data['CPUFREQ'].median()))
    plt.legend()
    plt.title('How does the CPU frequency vary with the number of threads?', wrap=True)
    return plt;

chart = plot(data)