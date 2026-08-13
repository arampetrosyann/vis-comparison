import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    avg_gpu_power = data.groupby('build')['y_GPU-POWER'].mean()
    avg_gpu_power.plot(kind='bar', color=['blue', 'green', 'red'])
    plt.xlabel('Build Type')
    plt.ylabel('Average GPU Power Consumption')
    plt.axhline(avg_gpu_power.mean(), color='gray', linestyle='dashed', label=f'Mean: {avg_gpu_power.mean():.2f}')
    plt.legend()
    plt.title('What is the average GPU power consumption for each build type?', wrap=True)
    return plt;

chart = plot(data)