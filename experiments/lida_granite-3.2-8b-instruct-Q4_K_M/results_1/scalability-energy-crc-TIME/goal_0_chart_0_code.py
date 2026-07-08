import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x='build', data=data, hue='test_index', palette='viridis')
    ax.set_title('What is the distribution of build types across all tests?', wrap=True)
    ax.legend(title='test_index')
    return plt

chart = plot(data)