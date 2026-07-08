import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='SIZE', y='y_LOSE-RATE', hue='build', data=data, palette='viridis', s=100)
    plt.title('What is the relationship between packet loss rate and packet size for each build type?', wrap=True)
    plt.legend(title='Build Type')
    return plt

chart = plot(data)