import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_visualize(csv_file_path):
    # Step 1: Load the CSV file with a specified encoding
    try:
        data = pd.read_csv(csv_file_path, encoding='utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(csv_file_path, encoding='ISO-8859-1')

    # Step 2: Summarize the sales data by Item
    item_summary = data.groupby('Item').sum().reset_index()

    # Step 3: Visualize the data
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Item', y='Total', data=item_summary)
    plt.title('Total Sales by Item')
    plt.xlabel('Item')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Step 4: Save and display the graph
    plt.savefig('outputImages/sales_summary.png')
    plt.show()

if __name__ == "__main__":
    load_and_visualize('extracted_data.csv')
