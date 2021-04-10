FROM    jupyter/base-notebook

RUN     pip install matplotlib pandas networkx pydot squarify folderstats qgrid ipywidgets ipython-blocking
RUN     conda install python-graphviz
RUN     jupyter nbextension enable --py --sys-prefix qgrid
RUN     jupyter nbextension enable --py --sys-prefix widgetsnbextension
EXPOSE 8888
