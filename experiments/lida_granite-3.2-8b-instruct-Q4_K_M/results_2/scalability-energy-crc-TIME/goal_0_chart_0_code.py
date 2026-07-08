import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='CPUFREQ', y='UNCORE_PSTATE', hue='UNCORE_PSTATE', data=data, palette='viridis')
    plt.title('What is the distribution of UNCORE_PSTATE values and their relationship with CPUFREQ?', wrap=True)
    plt.xlabel('CPUFREQ')
    plt.ylabel('UNCORE_PSTATE')
    plt.legend(title='UNCORE_PSTATE')
    return plt

chart = plot(data)