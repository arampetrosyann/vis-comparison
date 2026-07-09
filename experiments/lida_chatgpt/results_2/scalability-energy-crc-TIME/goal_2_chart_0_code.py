import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    power_columns = ['y_GPU-POWER', 'y_IPMI-POWER', 'y_RAPL-POWER', 'y_PDU-POWER']
    power_data = data[power_columns].sum()
    
    plt.bar(power_data.index, power_data, color=['blue', 'green', 'orange', 'red'])
    plt.xlabel('Power Sources')
    plt.ylabel('Total Power Consumption')
    
    for i, v in enumerate(power_data):
        plt.text(i, v + 1, str(round(v, 2)), ha='center')
    
    plt.legend(power_columns)
    plt.title('What is the power consumption distribution across different power sources (GPU, IPMI, RAPL, PDU)?', wrap=True)
    
    return plt;

chart = plot(data)