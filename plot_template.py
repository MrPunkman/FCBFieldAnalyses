import matplotlib.pyplot as plt

def create_plot_template():
    """
    Create a plot template for the data series with 2x2 subplots.
    Returns the figure and axes objects for further customization.
    """
    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    
    # Set titles for each subplot
    titles = ["X - Pos", "X - Neg", "Y - Pos", "Y - Neg"]
    for ax, title in zip(axs.flatten(), titles):
        ax.set_title(title)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Magnetic Induction (µT)")
    
    # Optional: Set grid and style for the plots
    for ax in axs.flatten():
        ax.grid(False)
        ax.set_facecolor('lightgray')
    
    return fig, axs