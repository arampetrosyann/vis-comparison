import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='build', y='y_PDU-POWER', data=data)
    plt.title('What is the average power consumption (y_PDU-POWER) for each build type across all tests?', wrap=True)
    plt.xlabel('Build Type')
    plt.ylabel('Power Consumption (y_PDU-POWER)')
    return plt

chart = plot(data)