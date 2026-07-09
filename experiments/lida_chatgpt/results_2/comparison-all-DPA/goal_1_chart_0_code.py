import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    plt.plot(data['NTHREADS'], data['y_AVG-LAT'], marker='o', color='b', label='Average Latency')
    plt.xlabel('Number of Threads')
    plt.ylabel('Average Latency')
    plt.axhline(y=data['y_AVG-LAT'].mean(), color='r', linestyle='--', label=f'Mean: {data["y_AVG-LAT"].mean():.2f}')
    plt.legend()
    plt.title('How does the average latency vary with the number of threads used?', wrap=True)
    return plt;

chart = plot(data)