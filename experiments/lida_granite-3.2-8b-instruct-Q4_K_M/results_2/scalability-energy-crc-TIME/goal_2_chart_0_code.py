import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='UNCORE_PSTATE', y='y_GPU-POWER', data=data, palette='viridis')
    sns.boxplot(x='UNCORE_PSTATE', y='y_IPMI-POWER', data=data, palette='viridis', ax=plt.gca())
    sns.boxplot(x='UNCORE_PSTATE', y='y_RAPL-POWER', data=data, palette='viridis', ax=plt.gca())
    sns.boxplot(x='UNCORE_PSTATE', y='y_PDU-POWER', data=data, palette='viridis', ax=plt.gca())
    plt.title('What is the distribution of power consumption (y_GPU-POWER, y_IPMI-POWER, y_RAPL-POWER, y_PDU-POWER) across different tasks?', wrap=True)
    plt.legend(labels=['y_GPU-POWER', 'y_IPMI-POWER', 'y_RAPL-POWER', 'y_PDU-POWER'])
    return plt

chart = plot(data)