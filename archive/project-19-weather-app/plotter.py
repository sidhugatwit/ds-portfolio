"""24-hour temperature chart."""
import matplotlib.pyplot as plt


def plot_temperature(place, times, temperatures, timezone="local", save_to=None):
    """Plot the forecast. Shows a window, or writes a PNG when save_to is given. Returns the figure."""
    if not times or not temperatures:
        raise ValueError("No forecast data to plot")
    labels = [t[11:16] for t in times]  # "2026-11-10T14:00" -> "14:00"
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(labels, temperatures, marker="o")
    ax.set_title(f"Next 24 hours: {place}")
    ax.set_xlabel(f"Time ({timezone})")
    ax.set_ylabel("Temperature (°C)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    if save_to:
        fig.savefig(save_to, dpi=120)
        plt.close(fig)
    else:
        plt.show()
    return fig
