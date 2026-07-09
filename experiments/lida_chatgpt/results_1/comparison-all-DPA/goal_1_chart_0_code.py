import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    sns.lineplot(x='NTHREADS', y='y_AVG-LAT', data=data)
    plt.title('How does the average latency vary with the number of threads used?', wrap=True)
    plt.legend(title='Legend', loc='best')
    plt.axhline(data['y_AVG-LAT'].mean(), color='r', linestyle='--', label=f'Mean: {data["y_AVG-LAT"].mean():.2f}')
    return plt;

chart = plot(data)