FROM continuumio/miniconda3

WORKDIR /workspace

COPY environment.yml .
RUN conda env create -f environment.yml && conda clean --all --yes

ENV PATH=/opt/conda/envs/task-analyzer/bin:$PATH

COPY . .

CMD ["python", "-m", "pytest"]
