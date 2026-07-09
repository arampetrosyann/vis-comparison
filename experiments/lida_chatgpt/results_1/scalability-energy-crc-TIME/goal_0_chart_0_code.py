import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    sns.countplot(data=data, x='build', palette='Set1')
    plt.title('What is the distribution of CPU builds in the dataset?', wrap=True)
    plt.legend(title='CPU Builds', labels=data['build'].unique())
    return plt;

chart = plot(data)