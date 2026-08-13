import matplotlib.pyplot as plt
import pandas as pd

# plan -
def plot(data: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    plt.hist(data['SIZE'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Packet Size (SIZE)')
    plt.ylabel('Frequency')
    plt.axvline(data['SIZE'].mean(), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {data["SIZE"].mean():.2f}')
    plt.legend()
    plt.title('What is the distribution of packet sizes (SIZE) in the dataset?', wrap=True)
    return plt;

chart = plot(data)