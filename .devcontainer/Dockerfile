FROM mcr.microsoft.com/devcontainers/python:3.10

# Install Jupyter and common data science packages
RUN pip install --no-cache-dir \
    jupyter \
    jupyterlab \
    notebook \
    ipywidgets \
    nbformat \
    nbconvert

# Install requirements
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create workspace directory
WORKDIR /workspace

# Configure Jupyter
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py

# Set up git
RUN git config --global user.email "codespaces@github.com" && \
    git config --global user.name "GitHub Codespaces"

EXPOSE 8888

CMD ["bash"]
