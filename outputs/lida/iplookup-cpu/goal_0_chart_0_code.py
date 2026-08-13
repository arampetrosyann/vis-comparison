import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    fig, ax = plt.subplots()
    for nthreads in data['NTHREADS'].unique():
        subset = data[data['NTHREADS'] == nthreads]
        ax.plot(subset['RX-RATE-PPS'], subset['AVG-LAT'], label=f'NTHREADS={nthreads}')
    ax.set_xlabel('RX-RATE-PPS')
    ax.set_ylabel('AVG-LAT')
    ax.legend(title='Thread Counts', loc='upper left')
    ax.axvline(data['RX-RATE-PPS'].mean(), color='gray', linestyle='--', label=f'Mean RX-RATE-PPS: {data["RX-RATE-PPS"].mean():.2f}')
    plt.title('How does the average latency (AVG-LAT) vary with the receive rate in packets per second (RX-RATE-PPS) for different thread counts (NTHREADS)?', wrap=True)
    return plt;

chart = plot(data)