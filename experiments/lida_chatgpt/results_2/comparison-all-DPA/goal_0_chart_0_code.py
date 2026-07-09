import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    data_grouped = data.groupby(['build', 'SIZE']).size().unstack()
    data_grouped.plot(kind='bar', stacked=True, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    plt.xlabel('Build')
    plt.ylabel('Count')
    plt.legend(title='SIZE', title_fontsize='medium', bbox_to_anchor=(1, 1))
    plt.title('What is the distribution of test sizes across different builds?', wrap=True)
    
    return plt;

chart = plot(data)