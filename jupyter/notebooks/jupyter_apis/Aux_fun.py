import ipywidgets as widgets
from ipywidgets import interact
import folderstats
import matplotlib.pyplot as plt
import squarify
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import qgrid


# Supported files list:
GW_supported_files = ['pdf', 'PDF', 'jpg', 'JPG', 'gif', 'GIF', 'png', 'PNG', 'emf', 'EMF', 'wmf', 'WMF', 'tiff', 'TIFF',
                      'GeoTIFF', 'geotiff', 'bmp', 'BMP', 'doc', 'DOC', 'dot', 'DOT', 'xls', 'XLS', 'xlt', 'XLT', 'ppt',
                      'PPT', 'pot', 'POT', 'docx', 'DOCX', 'docm', 'DOCM', 'dotx', 'DOTX', 'dotm', 'DOTM', 'xlsx', 'XLSX',
                      'xlam', 'XLAM', 'xlsm', 'XLSM', 'xltx', 'XLTX', 'xltm', 'XLTM', 'xpptx', 'XPPTX', 'potx', 'POTX',
                      'potm', 'POTM', 'pptm', 'PPTM', 'ppsx', 'PPSX', 'ppam', 'PPAM', 'ppsm', 'PPSM', 'wab', 'WAB', 'mp3',
                      'MP3', 'mpg', 'MPG', 'mp4', 'MP4','pe', 'PE', 'dll', 'DLL', 'mui', 'MUI', 'exe', 'EXE', 'mach-o',
                      'MACH-O', 'coff', 'COFF', 'elf', 'ELF']



def get_df(folder_path, all_files=True, supported_files=GW_supported_files):
    df = folderstats.folderstats(folder_path, ignore_hidden=True)

    if all_files:
        return df
    else:
        df_supported = df[df['extension'].isin(supported_files)]
        df_not_supported = df[~df['extension'].isin(supported_files)]

        return df_supported, df_not_supported


def Treemap(df):
    # Group by extension and sum all sizes for each extension
    extension_sizes = df.groupby('extension')['size'].sum()
    # Sort elements by size
    extension_sizes = extension_sizes.sort_values(ascending=False)

    m = len(extension_sizes)
    if m >= 20:
        if m <= 30: p = 0.7
        elif m <= 40: p = 0.6
        elif m <= 60: p = 0.4
        else: p = 0.35
    else:
        p = 1

    w = widgets.IntSlider(
            value= p*len(extension_sizes),
            min=1,
            max=len(extension_sizes),
            step=1,
            description='Extensions',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )

    @interact
    def treemap(w = w):

        plt.rcParams.update({'font.size': 22}) 

        plt.figure(figsize=(25,15))

        squarify.plot(sizes=extension_sizes[:w].values, label=extension_sizes[:w].index.values)
        plt.title('Extension Treemap by Size')
        plt.axis('off');


def create_graph(df):
    # Sort the index
    df_sorted = df.sort_values(by='id')

    G = nx.Graph()
    # To build the graph we iterate over the dataframe and create an edge from row.id to row.parent
    for i, row in df_sorted.iterrows():
        if row.parent:
            G.add_edge(row.id, row.parent)

    # Print some additional information
    print(nx.info(G))
    return G


def show_graph(G, layout='default'):

    if layout=='radial':
        pos_twopi = graphviz_layout(G, prog='twopi', root=1)

        fig = plt.figure(figsize=(14, 14))
        nodes = nx.draw_networkx_nodes(G, pos_twopi, node_size=2, node_color='C0')
        edges = nx.draw_networkx_edges(G, pos_twopi, edge_color='C0', width=0.5)
        plt.axis('off')
        plt.axis('equal');

    else: # default layout
        pos_dot = graphviz_layout(G, prog='dot')

        fig = plt.figure(figsize=(16, 8))
        nodes = nx.draw_networkx_nodes(G, pos_dot, node_size=2, node_color='C0')
        edges = nx.draw_networkx_edges(G, pos_dot, edge_color='C0', width=0.5)
        plt.axis('off');


def qgrid_widget(df):
    return qgrid.show_grid(df, show_toolbar=True)


def count_extentions_bar_chart(df):
    w = widgets.IntSlider(
        value=len(df['extension'].value_counts()),
        min=1,
        max=len(df['extension'].value_counts()),
        step=1,
        description='Extensions',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )

    @interact
    def bar_chart(w = w):

        plt.figure(figsize=(20,10))

        with plt.style.context('ggplot'):
            df['extension'].value_counts()[:w].plot(kind='bar', color='C1', title='Extension Distribution by Count');


def extetions_size_bar_chart(df):
    # To do this you can use the Pandas .groupby() method to group all extensions. 
    # After grouping the files by file extension you can sum all of their sizes

    # Group by extension and sum all sizes for each extension 
    extension_sizes = df.groupby('extension')['size'].sum()
    # Sort elements by size
    extension_sizes = extension_sizes.sort_values(ascending=False)

    w = widgets.IntSlider(
            value=len(extension_sizes),
            min=1,
            max=len(extension_sizes),
            step=1,
            description='Extensions',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )

    @interact
    def bar_chart(w = w):

        with plt.style.context('ggplot'):

            extension_sizes = df.groupby('extension')['size'].sum()
            extension_sizes = extension_sizes.sort_values(ascending=False)
            extension_sizes = extension_sizes[:w]

            plt.figure(figsize=(20,10))

            extension_sizes.plot(kind='bar', color='C1', title='Extension Distribution by Size');


def folder_sizes_bar_chart(df):
    # Filter the data set to only folders
    df_folders = df[df['folder']]
    # Set the name to be the index (so we can use it as a label later)
    df_folders.set_index('name', inplace=True)
    # Sort the folders by size
    df_folders = df_folders.sort_values(by='size', ascending=False)


    if len(df_folders) != 0:

        w = widgets.IntSlider(
                value=len(df_folders)//5,
                min=1,
                max=len(df_folders),
                step=1,
                description='Num Folders',
                disabled=False,
                continuous_update=False,
                orientation='horizontal',
                readout=True,
                readout_format='d'
            )

        @interact
        def bar_chart(w = w):

            with plt.style.context('ggplot'):

                plt.figure(figsize=(20,10))
                df_folders['size'][:w].plot(kind='bar', color='C0', title='Folder Sizes');

