import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    avg_lat_by_size = data.groupby('SIZE')['AVG-LAT'].mean()
    avg_lat_by_size.plot(kind='bar', color='skyblue', edgecolor='black', legend=True)
    plt.xlabel('SIZE')
    plt.ylabel('Average AVG-LAT')
    plt.axhline(y=avg_lat_by_size.mean(), color='red', linestyle='--', label=f'Mean: {avg_lat_by_size.mean():.2f}')
    plt.legend()
    plt.title('What is the average AVG-LAT for each SIZE category?', wrap=True)
    return plt;

chart = plot(data)