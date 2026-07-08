import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='SIZE', y='y_LOSE-RATE', hue='NTHREADS', data=data, markers=True, dashes=False)
    plt.title('What is the relationship between the lose rate (y_LOSE-RATE) and packet size (SIZE), and how does it change with the number of threads (NTHREADS)?', wrap=True)
    plt.xlabel('Packet Size (SIZE)')
    plt.ylabel('Lose Rate (y_LOSE-RATE)')
    plt.legend(title='Number of Threads (NTHREADS)')
    return plt

chart = plot(data)