import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

output_dir = 'results'
csv_files = [f for f in os.listdir(output_dir) if f.endswith('_scores.csv')]
for csv_file in csv_files:
    df = pd.read_csv(os.path.join(output_dir, csv_file))
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Affinity (kcal/mol)'], bins=10, kde=True)
    plt.title(f'Binding Affinity Distribution: {csv_file}')
    plt.xlabel('Affinity (kcal/mol)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, f'{csv_file}_plot.png'))
    plt.close()
