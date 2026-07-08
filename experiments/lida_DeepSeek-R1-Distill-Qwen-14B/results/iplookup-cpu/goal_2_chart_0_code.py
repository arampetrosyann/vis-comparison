import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot(data: pd.DataFrame):
    # Aggregate data by test_index for mean values
    data_agg = data.groupby('test_index').agg({
        'LOSE-RATE': 'mean',
        'RX-GOODPUT-GBPS-PKTGEN': 'mean'
    }).reset_index()
    
    # Melt the dataframe to prepare for plotting
    data_melt = data_agg.melt(id_vars='test_index', 
                              value_vars=['LOSE-RATE', 'RX-GOODPUT-GBPS-PKTGEN'],
                              var_name='metric', 
                              value_name='value')
    
    # Create a bar plot
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='test_index', y='value', hue='metric', data=data_melt)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid lines
    ax.grid(True, alpha=0.3)
    
    # Set title and labels
    plt.title('Relationship between Loss Rate and Goodput Rate across Test Conditions', wrap=True)
    plt.xlabel('Test Index')
    plt.ylabel('Value')
    
    # Adjust legend
    plt.legend(title='Metric', bbox_to_anchor=(1.05, 1), borderaxespad=0)
    
    return plt;

chart = plot(data)