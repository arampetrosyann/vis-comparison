import matplotlib.pyplot as plt
import pandas as pd

def plot(data: pd.DataFrame):
    plt.scatter(data['NTHREADS'], data['CPUFREQ'], c=data['CPUFREQ'], cmap='viridis', alpha=0.6)
    plt.colorbar(label='CPU Frequency')
    plt.xlabel('Number of Threads')
    plt.ylabel('CPU Frequency')
    plt.axvline(data['NTHREADS'].median(), color='red', linestyle='--', label=f'Median NTHREADS: {data["NTHREADS"].median():.2f}')
    plt.axhline(data['CPUFREQ'].median(), color='blue', linestyle='--', label=f'Median CPUFREQ: {data["CPUFREQ"].median():.2f}')
    plt.legend()
    plt.title('How does the CPU frequency (CPUFREQ) vary with the number of threads (NTHREADS)?', wrap=True)
    return plt;

chart = plot(data)