import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='test_index', y='LOSE-RATE', data=data)
    plt.title('What is the distribution of LOSE-RATE across different test indices?', wrap=True)
    plt.xlabel('test_index')
    plt.ylabel('LOSE-RATE')
    plt.xticks(rotation=45)
    return plt

chart = plot(data)