import numpy as np
import torchvision.datasets as datasets
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler

colors = [
    "#1F77B4",
    "#FF7F0E",
    "#2CA02C",
    "#D62728",
    "#9467BD",
    "#8C564B",
    "#E377C2",
    "#7F7F7F",
    "#BCBD22",
    "#17BDCF",
    "#FF1493",
    "#A020F0",
    "#FF82AB",
    "#3A5FCD",
    "#045204",
    "#DDC0A0",
    "#4EEE94",
    "#CAFF70",
    "#FFB90F",
    "#CD9B9B",
    "#CF23DA",
]

markers = [".", "+"]


def tSNE_visualize(feature, centroids, label, output_name="visual.png"):
    fig, axs = plt.subplots(1, 1, figsize=(10, 10), constrained_layout=True)
    # print("processing t-SNE...")
    X = np.vstack((feature, centroids))
    label = np.hstack(
        (label, -1 * np.arange(0, centroids.shape[0], dtype=np.int64) - 1)
    )
    X_embed = TSNE(
        n_components=2, perplexity=80, init="pca", learning_rate="auto"
    ).fit_transform(X)
    # print("plotting... ")
    plot_embedding(X_embed, label, "t-SNE", axs)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(output_name)
    plt.close()
    print("figure saved", output_name)


def tSNE_visualize_2view(feature, centroids, label, output_name="visual.png"):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # print("processing t-SNE...")
    n_views, n_samples, n_dim = feature.shape

    feature = feature.reshape(n_views * n_samples, n_dim)
    feature_embed = TSNE(
        n_components=2, perplexity=30, init="pca", learning_rate="auto"
    ).fit_transform(feature)

    feature_embed = MinMaxScaler().fit_transform(feature_embed)
    feature_embed = feature_embed.reshape(n_views, n_samples, 2)

    for i in range(n_views):
        X = feature_embed[i]
        for j in range(0, X.shape[0]):
            size, color = 19, colors[label[j]]
            ax.scatter(X[j, 0], X[j, 1], size, c=color, marker=markers[i])

    ax.set_title("t_SNE")

    plt.savefig(output_name)
    plt.close()
    print("figure saved", output_name)


def tSNE_visualize_both(X, c, rec_x, label, output_name="visual.png"):
    fig, axs = plt.subplots(1, 2, figsize=(20, 10))
    # print("processing t-SNE...")

    label = np.hstack((label, 10 * np.ones(c.shape[0], dtype=np.int64)))
    X_embed = TSNE(
        n_components=2, perplexity=20, init="pca", learning_rate="auto"
    ).fit_transform(X)

    X_r = np.vstack((rec_x.numpy(), c))
    X_r_embed = TSNE(
        n_components=2, perplexity=20, init="pca", learning_rate="auto"
    ).fit_transform(X_r)

    # print("plotting")
    plot_embedding(X_embed, label, "t-SNE X", axs[0])
    plot_embedding(X_r_embed, label, "t-SNE Recon X", axs[1])

    plt.savefig(output_name)
    print("figure saved", output_name)
    plt.close()


def plot_embedding(data, label, title, ax: Axes):
    X = MinMaxScaler().fit_transform(data)
    for i in range(0, X.shape[0]):
        if label[i] < 0:
            pass
            # true_label = -(label[i] + 1)
            # ax.text(
            #     X[i, 0],
            #     X[i, 1],
            #     str(true_label),
            #     color='#000000',
            #     fontdict={'weight': 'bold', 'size': 17},
            # )
        else:
            size, color = 15, colors[label[i]]
            ax.scatter(X[i, 0], X[i, 1], size, c=color)
    # font2 = {'family': 'Times New Roman',
    #          'weight': 'normal',
    #          'size': 30,
    #          }
    # ax.set_title(title, font2)
