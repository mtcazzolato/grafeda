import config

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patches as patches
import plotly.graph_objs as go
import plotly.express as px
import networkx as nx


# Feature extraction modules
import tgraph.static_graph as SG
import tgraph.temporal_graph as TG


def read_ehr_data(file):
    """
    Read attributes from input EHR file
    
    Parameters
    ----------
    file: str
        path of the input file with EHR attributes
    """
    config.input_file_path = file
    config.df_dataset = pd.read_csv(file)
    config.attributes_extraction = config.df_dataset.columns.tolist()
    config.flag_dataset_loaded = True

def read_features(file):
    """
    Read columns from input file
    
    Parameters
    ----------
    file: str
        path of file with pre-extracted features
    """

    config.df_features = pd.read_csv(file)
    config.flag_features_loaded = True


def setup_graph_extract_features(file, source, destination, measure, timestamp, has_dataset_attribute=False):
    """
    Run grafeda to extract features
    
    Parameters
    ----------
    file: str
        path of the input file with raw data
    source: str
        input column for source
    destination: str
        input column for destination
    measure: str
        input column for measure
    timestamp: str
        input column for timestamp
    """

    print(source, destination, measure, timestamp)

    # Get static features
    sg = SG.StaticGraph(df_ehr=config.df_dataset[[source, destination, measure, timestamp]],
                        source=source,
                        destination=destination,
                        measure=measure)
    sg.my_print()
    
    # Get temporal features
    tg = TG.TemporalGraph(df_ehr=config.df_dataset[[source, destination, measure, timestamp]],
                          source=source,
                          destination=destination,
                          measure=measure,
                          timestamp=timestamp)
    tg.my_print()
    
    # Join static and temporal features
    df_all_features = sg.df_nodes.set_index(config.NODE_ID).join(tg.df_nodes.set_index(config.NODE_ID)).reset_index()
    df_all_features.fillna(0)
    
    if has_dataset_attribute:
        print("Join features with dataset name")
        get_dataset_number_for_nodes(df_all_features, source, destination)

    # Save output features
    print("\n\n ----")
    df_all_features.to_csv("data/grafeda_features.csv", index=False)
    print("Check the file \"data/grafeda_features.csv\"")

    return df_all_features.head()


def get_dataset_number_for_nodes(df_all_features, source, destination):
    # TODO
    
    # dset_values = list(config.df_dataset[config.DATASET].unique())
    
    # df_datasets = pd.DataFrame(columns=[config.NODE_ID, config.DATASET])

    # for d in dset_values:
    #     source_nodes = list(set(config.df_dataset[config.df_dataset[config.DATASET] == d][source]))
        
    #     df_nodes_dataset = pd.DataFrame()
    #     df_nodes_dataset[config.NODE_ID] = source_nodes
    #     df_nodes_dataset[config.DATASET] = [d]*len(source_nodes)

    #     df_datasets = pd.concat([df_datasets, df_nodes_dataset], axis=0)

    pass


def plot_hexbin():
    """
    TODO
    """
    
    fig, ax = plt.subplots(1, 1, figsize=config.figsize)
    img = ax.hexbin(config.df_features[config.feature1_hexbin],
                    config.df_features[config.feature2_hexbin],
                    cmap=config.cmap, mincnt=1, bins='log')
    
    cb = plt.colorbar(img, ax=ax)
    cb.set_label("log10(N)")
    ax.set_xlabel(config.feature1_hexbin.replace('_', ' ') + ' — log10(x+1)')
    ax.set_ylabel(config.feature2_hexbin.replace('_', ' ') + ' — log10(x+1)')
    ax.grid(True)
    ax.set_xlim(0,)
    ax.set_ylim(0,)

    return fig


def plot_histogram(feature, logscale=True):
    colors = ['black', 'tomato', 'blue', 'green', 'orange']
    
    fig = plt.figure(figsize=config.figsize)
    
    if logscale:
        counts, bins = np.histogram(np.log10(config.df_features[feature]+1),
                                    bins=50)
        plt.stairs(np.log10(counts+1), bins, color=colors[2], lw=2)
        plt.xlabel(feature.replace('_', ' ') + ' – log10(x+1)')
        plt.ylabel('count – log10(x+1)')
        # plt.yscale('log')
        plt.grid()
        plt.title(feature.replace('_', ' '), style='italic')
            
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    return fig

def plot_scatter_plot_matrix():
    """
    TODO
    """
    
    color = 'blue'
    linecolor='black'
    dimensions=[]

    for c in config.columns_attributes_scatter_matrix:
        dimensions.append(dict(label=c.replace('_', ' ') + ' — log10(x+1)',
                          values=np.log10(config.df_features[c]+1)))

    colors = pd.Series(data=[color] * len(config.df_features))
    
    fig = go.Figure(data=go.Splom(
            dimensions = dimensions,
            customdata = config.df_features[config.NODE_ID],
            hovertemplate="<br>".join([
                        "%{xaxis.title.text}: %{x}",
                        "%{yaxis.title.text}: %{y}",
                        "hash: %{customdata}",
            ]),
            showlegend=False, #Show legend entries later on!
            showupperhalf=False, # remove plots in the diagonal
            marker=dict(color=list(colors),
                        showscale=False,
                        line_color=linecolor,
                        line_width=0.8,
                        size=8,
                        opacity=0.5
            ),
    ))
    
    fig.update_traces(
                unselected_marker=dict(opacity=0.1, size=5),
                selected_marker=dict(size=10, opacity=0.9),
                selector=dict(type='splom'),
                diagonal_visible=False)
    
    fig.update_layout(
        dragmode='select',
        hovermode='closest',
    )

    return fig


def construct_graph(source, destination, measure):
    """
    Construct graph for the deep dive with selected attributes
    """
    config.G = nx.from_pandas_edgelist(config.df_dataset,
                                       source=source,
                                       target=destination,
                                       edge_attr=measure,
                                       create_using=nx.DiGraph())
    config.flag_graph_constructed=True


def get_egonet(suspicious_nodes, radius=1, column=''):
    """
    Compose a graph with the egonets of a given set of suspicious nodes.
    Return the subgraph of the composed egonets and the index of
    suspicious nodes inside the subgraph

    Parameters
    ----------
    G: nx.Graph
        graph with all nodes to extract the EgoNets from
    suspicious_nodes: list
        list of suspicious nodes
    radius: int
        step of the EgoNet
    """
        
    final_G = nx.empty_graph(create_using=nx.DiGraph())

    for ego_node in suspicious_nodes:
        # create ego network
        hub_ego = nx.ego_graph(config.G,
                               ego_node,
                               radius=radius,
                               distance='weight',
                               undirected=True)
        final_G = nx.compose(final_G, hub_ego)

    idx_suspicious_nodes = []
    for node in suspicious_nodes:
        idx_suspicious_nodes.append(list(np.where(pd.DataFrame(data=final_G.nodes()) == node)[0])[0])
    
    return final_G, idx_suspicious_nodes


def plot_interactive_scatter_selected_nodes(selected_ids,
                                    title=None):

    egonet, _ = get_egonet(suspicious_nodes=selected_ids)

    # Group source and destination and sum measure
    egonet_nodes = list(egonet.nodes)

    filtered_df_dataset = config.df_dataset[config.df_dataset[config.source_].isin(egonet_nodes)].groupby([config.source_, config.destination_]).sum().add_suffix('').reset_index()
    filtered_df_dataset2 = config.df_dataset[config.df_dataset[config.destination_].isin(egonet_nodes)].groupby([config.source_, config.destination_]).sum().add_suffix('').reset_index()

    df_filtered = pd.concat([filtered_df_dataset, filtered_df_dataset2], axis=0)

    if len(df_filtered)>0:
        fig = px.scatter(x=df_filtered[config.destination_],
                         y=df_filtered[config.source_],
                         color=df_filtered[config.measure_],
                         size=df_filtered[config.measure_]*5_000,
                         labels={
                             "x": config.destination_,
                             "y": config.source_,
                             "color": config.measure_,
                             "size": config.measure_,
                         },
                         width=800, height=500,
                         title=title,
                         color_continuous_scale='rainbow')

        fig.update_traces(mode="markers")
        fig.update_traces(
            marker=dict(symbol="square",
                        line=dict(width=1,
                        color="DarkSlateGrey") ),
            selector=dict(mode="markers"),
        )
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

    return fig, egonet_nodes

