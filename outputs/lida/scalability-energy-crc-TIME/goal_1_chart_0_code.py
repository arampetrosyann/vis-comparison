import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    avg_gpu_power = data.groupby('UNCORE_PSTATE')['y_GPU-POWER'].mean()
    avg_gpu_power.plot(kind='bar', color='skyblue', edgecolor='black', legend=True)
    plt.xlabel('UNCORE_PSTATE')
    plt.ylabel('Average y_GPU-POWER')
    plt.axhline(avg_gpu_power.mean(), color='red', linestyle='--', label=f'Mean: {avg_gpu_power.mean():.2f}')
    plt.title('What is the distribution of GPU power consumption (y_GPU-POWER) across different uncore pstates (UNCORE_PSTATE)?', wrap=True)
    return plt;

chart = plot(data)