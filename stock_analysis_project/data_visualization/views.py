import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse
import io
import base64
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

def temperature_plot(request):
    # Read temperature data
    df = pd.read_csv('data/temperature_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')  # Ensure data is sorted by date

    # Handle missing or NaN values
    df = df.dropna()

    # Create plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['temperature'])

    # Add annotations for max and min temperatures
    max_temp = df['temperature'].max()
    min_temp = df['temperature'].min()
    max_date = df.loc[df['temperature'].idxmax(), 'date']
    min_date = df.loc[df['temperature'].idxmin(), 'date']

    plt.annotate(f'Max: {max_temp}°C on {max_date.strftime("%Y-%m-%d")}',
                 xy=(max_date, max_temp),
                 xytext=(10, 10),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))
    plt.annotate(f'Min: {min_temp}°C on {min_date.strftime("%Y-%m-%d")}',
                 xy=(min_date, min_temp),
                 xytext=(10, -10),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    # Customize plot
    plt.title('Daily Temperature Variations')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, linestyle='--', alpha=0.7)

    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels

    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode()

    return render(request, 'data_visualization/temperature_plot.html', {'graphic': graphic})

def sales_analysis(request):
    # Read sales data
    df = pd.read_csv('data/sales_data.csv')
    
    # Handle missing or duplicated product_id values
    df = df.dropna(subset=['product_id'])
    df['product_id'] = df['product_id'].astype(str)  # Convert to string to handle potential mixed types
    
    # Calculate total sales
    df['total_sales'] = df['price'] * df['quantity']
    
    # Group by region
    region_sales = df.groupby('region')['total_sales'].sum().reset_index()
    
    # Calculate average price per unit
    avg_price = df.groupby('product_id').agg({
        'price': 'mean',
        'total_sales': 'sum',
        'quantity': 'sum'
    }).reset_index()
    avg_price['average_price_per_unit'] = avg_price['total_sales'] / avg_price['quantity']
    
    # Filter products with sales > 10000
    high_sales = avg_price[avg_price['total_sales'] > 10000]
    
    context = {
        'region_sales': region_sales.to_dict('records'),
        'high_sales': high_sales.to_dict('records')
    }
    
    return render(request, 'data_visualization/sales_analysis.html', context)