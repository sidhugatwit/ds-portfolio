import matplotlib.pyplot as plt


def plot_temperature(city, times, temperatures):
    """
    Plot 24-hour temperature forecast for a city.
    """
    if not times or not temperatures:
        print("No forecast data available to plot.")
        return

    short_times = [t[11:16] for t in times]

    plt.figure(figsize=(10, 5))
    plt.plot(short_times, temperatures, marker="o")
    plt.title(f"24-Hour Temperature Forecast for {city}")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
