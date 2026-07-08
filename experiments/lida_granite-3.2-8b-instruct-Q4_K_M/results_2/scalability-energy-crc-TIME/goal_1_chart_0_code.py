import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x='NTHREADS', y='TIME', hue='UNCORE_PSTATE', marker='o', markersize=5)
    plt.title('How does the number of NTHREADS affect the TIME taken for each task?', wrap=True)
    plt.legend(title='UNCORE_PSTATE')
    return plt

chart = plot(data)