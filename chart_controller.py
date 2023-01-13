import matplotlib.pyplot as plot


def generate_bar_chart(names, counts):
    fig, ax = plot.subplots()
    ax.bar(names, counts)
    plot.savefig('fig.png')
