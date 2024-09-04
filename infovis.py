def load_and_visualize(csv_file_path):
    # Step 1: Load the CSV file with a specified encoding
    try:
        data = pd.read_csv(csv_file_path, encoding='utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(csv_file_path, encoding='ISO-8859-1')

    # Step 2: Summarize the sales data by Item
    item_summary = data.groupby('Item').sum().reset_index()
