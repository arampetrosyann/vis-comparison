import matplotlib.pyplot as plt
import pandas as pd

def plot(data: pd.DataFrame):
    plt.scatter(data['NTHREADS'], data['y_RX-RATE-PPS'], c='blue', label='Receive Rate in PPS')
    plt.xlabel('Number of Threads')
    plt.ylabel('Receive Rate in Packets per Second (PPS)')
    plt.axvline(data['NTHREADS'].mean(), color='red', linestyle='--', label=f'Mean NTHREADS: {data["NTHREADS"].mean():.2f}')
    plt.axhline(data['y_RX-RATE-PPS'].mean(), color='green', linestyle='--', label=f'Mean PPS: {data["y_RX-RATE-PPS"].mean():.2f}')
    plt.legend()
    plt.title('How does the receive rate in packets per second (y_RX-RATE-PPS) vary with the number of threads (NTHREADS)?', wrap=True)
    return plt;

chart = plot(data)