import numpy as np
import matplotlib.pyplot as plt

def stacked_bar_chart(x, y, title, width = 0.8):
    """
    Example:
        x = ('Adelie', 'Chinstrap', 'Gentoo')
        y = {
            'Male': np.array([73, 34, 61]),
            'Female': np.array([73, 34, 58]),
        }
    """
    # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()
    bottom = np.zeros(len(x))

    for name, count in y.items():
        p = ax.bar(x, count, width, label=name, bottom=bottom)
        bottom += count
        # ax.bar_label(p, label_type='center')

    ax.set_title(title)
    ax.legend()
