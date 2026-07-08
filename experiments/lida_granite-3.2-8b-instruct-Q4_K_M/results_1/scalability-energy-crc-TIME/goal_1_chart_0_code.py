import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='CPUFREQ', y='TIME', hue='build', data=data, s=100)
    plt.title('How does the CPU frequency (CPUFREQ) impact the execution time (TIME) for each build type?', wrap=True)
    plt.legend(title='Build Type')
    return plt

chart = plot(data)