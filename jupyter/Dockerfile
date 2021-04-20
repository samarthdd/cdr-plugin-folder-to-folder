FROM    jupyter/base-notebook

USER    root
RUN     apt-get update
RUN     apt-get install unzip git -y
COPY    requirements.txt ./

USER    jovyan
RUN     pip install -r requirements.txt
RUN     rm requirements.txt
#RUN     conda install python-graphviz
RUN     jupyter nbextension enable --py --sys-prefix qgrid
RUN     jupyter nbextension enable --py --sys-prefix widgetsnbextension

ENV     PYTHONPATH=.

EXPOSE 8888
