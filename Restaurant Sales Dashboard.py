import os
import matplotlib.pyplot as plt
import pandas as pd


def load_and_clean_data(filename):
    # Check if the file exists (Test Case 3b)
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return None

    try:
        raw_df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    valid_rows = []
    # Iterate through rows to validate and skip invalid entries (Test Case 3a)
    for idx, row in raw_df.iterrows():
        # Excel/CSV line number (header is row 1, first data row is row 2)
        row_num = idx + 2

        if (
            pd.isna(row.get('Date'))
            or pd.isna(row.get('Item'))
            or pd.isna(row.get('Category'))
        ):
            print(f'Warning: Row {row_num} skipped - Missing text fields.')
            continue

        try:
            qty = float(row['Quantity'])
            if qty <= 0:
                raise ValueError
        except (ValueError, TypeError):
            print(
                f'Warning: Row {row_num} skipped - Quantity must be a number.'
            )
            continue

        try:
            price = float(row['Price'])
            if price < 0:
                raise ValueError
        except (ValueError, TypeError):
            print(f'Warning: Row {row_num} skipped - Price must be a number.')
            continue

        valid_rows.append({
            'Date': str(row['Date']).strip(),
            'Item': str(row['Item']).strip(),
            'Category': str(row['Category']).strip(),
            'Quantity': int(qty) if qty.is_integer() else qty,
            'Price': int(price) if price.is_integer() else price,
        })

    if not valid_rows:
        print('No valid sales records found.')
        return None

    df = pd.DataFrame(valid_rows)
    # Compute Sales = Quantity x Price
    df['Sales'] = df['Quantity'] * df['Price']
    return df


def sales_by_category(df, show_chart=True):
    cat_sales = df.groupby('Category')['Sales'].sum()
    # Sort descending to match Test Case 1 output order (Main, Starter, Dessert)
    cat_sales = cat_sales.sort_values(ascending=False)

    for category, total in cat_sales.items():
        print(f'{category} : Rs. {int(total)}')
    print(f"Total sales: Rs. {int(df['Sales'].sum())}")

    if show_chart:
        plt.figure(figsize=(7, 5))
        cat_sales.plot(
            kind='bar', color=['#4C72B0', '#55A868', '#C44E52'], edgecolor='black'
        )
        plt.title('Total Sales by Category')
        plt.xlabel('Category')
        plt.ylabel('Sales (Rs.)')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()


def top_items(df, show_chart=True):
    item_group = df.groupby('Item').agg({'Quantity': 'sum', 'Sales': 'sum'})

    top_qty_item = item_group['Quantity'].idxmax()
    top_qty_val = int(item_group['Quantity'].max())
    unit_label = 'unit' if top_qty_val == 1 else 'units'

    top_rev_item = item_group['Sales'].idxmax()
    top_rev_val = int(item_group['Sales'].max())

    print(
        f'Top item by quantity: {top_qty_item} ({top_qty_val} {unit_label})'
    )
    print(f'Top item by revenue: {top_rev_item} (Rs. {top_rev_val})')

    if show_chart:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

        item_group['Quantity'].plot(
            kind='bar', ax=ax1, color='#4C72B0', edgecolor='black'
        )
        ax1.set_title('Quantity Sold by Item')
        ax1.set_ylabel('Units Sold')
        ax1.tick_params(axis='x', rotation=25)

        item_group['Sales'].plot(
            kind='bar', ax=ax2, color='#55A868', edgecolor='black'
        )
        ax2.set_title('Revenue by Item')
        ax2.set_ylabel('Sales (Rs.)')
        ax2.tick_params(axis='x', rotation=25)

        plt.tight_layout()
        plt.show()


def daily_sales(df, show_chart=True):
    date_sales = df.groupby('Date')['Sales'].sum()

    for date, total in date_sales.items():
        print(f'{date} : Rs. {int(total)}')

    best_day = date_sales.idxmax()
    print(f'Best day: {best_day}')

    if show_chart:
        plt.figure(figsize=(7, 5))
        date_sales.plot(
            kind='line', marker='o', color='#DD8452', linewidth=2.5
        )
        plt.title('Daily Sales Trend')
        plt.xlabel('Date')
        plt.ylabel('Sales (Rs.)')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()


def main():
    filename = input(
        'Enter CSV filename (default: restaurant_sales.csv): '
    ).strip()
    if not filename:
        filename = 'restaurant_sales.csv'

    df = load_and_clean_data(filename)
    if df is None: 
        return

    while True:
        print('\n--- Restaurant Sales Dashboard ---')
        print('1. Sales by category')
        print('2. Top items')
        print('3. Daily sales')
        print('4. Top items and daily sales')
        print('5. Exit')

        choice = input('Select an option (1-5): ').strip()

        if choice == '1':
            sales_by_category(df)
        elif choice == '2':
            print(f"Total sales: Rs. {int(df['Sales'].sum())}")
            top_items(df)
        elif choice == '3':
            daily_sales(df)
        elif choice == '4':
            top_items(df, show_chart=False)
            daily_sales(df, show_chart=True)
        elif choice == '5':
            print('Exiting dashboard.')
            break
        else:
            print('Invalid choice. Please select 1-5.')


if __name__ == '__main__':
    main()