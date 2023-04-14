import matplotlib.pyplot as plot


def generate_bar_chart(names, counts):
    fig, ax = plot.subplots()
    indexer = 1
    for i in range(len(names)):
        if names[i] in names[:i]:
            names[i] = f'{names[i]}{indexer}'
            indexer += 1
    ax.bar(names, counts)
    plot.savefig('fig.png')
