import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x='test_index', y='y_RX-RATE-PPS', hue='build', marker='o')

    plt.title('How does the packet rate (PPS) vary across different build types and test indices?', wrap=True)
    plt.xlabel('Test Index')
    plt.ylabel('Packet Rate (PPS)')
    plt.legend(title='Build Type')

    return plt

chart = plot(data)