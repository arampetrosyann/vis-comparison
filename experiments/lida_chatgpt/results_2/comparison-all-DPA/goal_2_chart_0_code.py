import matplotlib.pyplot as plt
import pandas as pd

def plot(data: pd.DataFrame):
    grouped_data = data.groupby('run_index')['y_RX-GOODPUT-GBPS-PKTGEN'].mean()
    ax = grouped_data.plot(kind='bar', color=['skyblue', 'salmon', 'lightgreen'])
    
    for i, value in enumerate(grouped_data):
        ax.text(i, value + 1, f'{value:.2f}', ha='center', va='bottom')
    
    ax.set_xlabel('Test Run')
    ax.set_ylabel('Goodput Rate (Gbps)')
    ax.legend(title='Run Index', loc='upper right')
    plt.title('What is the goodput rate in Gbps for each test run?', wrap=True)
    
    return plt;

chart = plot(data)