import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='test_index', y='SIZE', data=data, ci=None)
    ax.set_title('What is the distribution of SIZE across different test indices?', wrap=True)
    ax.set_xlabel('Test Index')
    ax.set_ylabel('SIZE')
    plt.legend(title='SIZE')
    return plt

chart = plot(data)