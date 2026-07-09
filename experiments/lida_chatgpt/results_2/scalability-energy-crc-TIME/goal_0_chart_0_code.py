import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    build_counts = data['build'].value_counts()
    build_counts.plot(kind='bar', color='skyblue', edgecolor='black', legend=True)
    plt.xlabel('CPU Builds')
    plt.ylabel('Count')
    plt.axhline(build_counts.mean(), color='red', linestyle='--', label=f'Mean: {build_counts.mean():.2f}')
    plt.legend()
    plt.title('What is the distribution of CPU builds in the dataset?', wrap=True)
    return plt;

chart = plot(data)