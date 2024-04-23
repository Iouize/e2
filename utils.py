import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

train.drop(columns="id", axis=1, inplace=True)
test.drop(columns="id", axis=1, inplace=True)


def plot_distrib_target(df, target):
    fig, ax = plt.subplots()

    target_counts = df[target].value_counts()

    ax.pie(
        target_counts,
        autopct='%.1f%%'
    )

    ax.legend(
        target_counts.index.tolist(),
        loc='upper left',
        bbox_to_anchor=(1, 1)
    )

    ax.set_title(f"Distribution de {target}")

    return fig


def plot_numerical_features(df_train, df_test):
    num_features = df_train.select_dtypes(include=['int64', 'float64']).columns.to_list()
    n_features = len(num_features)

    fig, axes = plt.subplots(
        n_features, 3, figsize=(15, 6 * n_features),
        gridspec_kw={'width_ratios': [4, 1, 1]}
    )

    if n_features == 1:
        axes = [axes]

    for i, feature in enumerate(num_features):
        sns.kdeplot(data=df_train, x=feature, label='Train', ax=axes[i][0], color="blue")
        sns.kdeplot(data=df_test, x=feature, label='Test', ax=axes[i][0], color="red")
        axes[i][0].set_title(f"Densité de distribution (kde) pour train et test - {feature}")
        axes[i][0].legend()

        sns.boxplot(data=df_train, y=feature, ax=axes[i][1], color="blue")
        axes[i][1].set_title("Boxplot - Train")

        sns.boxplot(data=df_test, y=feature, ax=axes[i][2], color="red")
        axes[i][2].set_title("Boxplot - Test")

    plt.tight_layout()

    return fig


def plot_categorical_features(df_train, df_test):
    cat_features = df_test.select_dtypes(include=['object']).columns.to_list()
    n_features = len(cat_features)
    fig, axes = plt.subplots(n_features, 2, figsize=(10, 5 * n_features))

    if n_features == 1:
        axes = [axes]

    for i, feature in enumerate(cat_features):
        train_dist = train[feature].value_counts()
        test_dist = test[feature].value_counts()

        axes[i][0].pie(
            train_dist,
            shadow=True,
            autopct='%.1f%%',
            explode=[.05]*len(train_dist),
        )
        axes[i][0].legend(train_dist.index.tolist(), loc='upper left', bbox_to_anchor=(1, 1))
        axes[i][0].set_title(f'Train {feature}')

        axes[i][1].pie(
            test_dist,
            shadow=True,
            autopct='%.1f%%',
            explode=[.05]*len(test_dist),
        )
        axes[i][1].legend(test_dist.index.tolist(), loc='upper left', bbox_to_anchor=(1, 1))
        axes[i][1].set_title(f'Test {feature}')

    plt.tight_layout()
    return fig


def plot_count_plot_by_target(df, feature, target):
    fig = px.histogram(
        data_frame=df,
        x=feature,
        color=target,
        barmode='group',
        title=f"Répartition de {feature} par {target}",
        labels={'x': feature, 'y': 'Count'}
    )

    return fig


# def plot_kde_by_target(df, feature, target):
#     hist_fig = px.histogram(
#         data_frame=df,
#         x=feature,
#         color=target,
#         marginal='violin',
#         nbins=30,
#         opacity=0.7,
#         title=f"Répartition de{feature} par {target}"
#     )

#     # fig.update_traces(histnorm='density', kde=True)
#     x_vals = np.linspace(df[feature].min(), df[feature].max(), 100)

#     for i, tg in enumerate(df[target].unique()):
#         tg_data = df[df[target] == tg][feature]
#         tg_density = gaussian_kde(tg_data)

#         hist_fig.add_trace(
#             go.Scatter(
#                 x=x_vals,
#                 y=tg_density(x_vals),
#                 mode='lines',
#                 name=f'KDE - {tg}'
#             )
#         )

#     return hist_fig

def plot_kde_by_target(df, feature, target):
    fig, ax = plt.subplots()

    sns.histplot(data=df, x=feature, hue=target, kde=True, bins=30)
    ax.set_title(f"Répartition de{feature} par {target}")
    plt.tight_layout()
    return fig
