FROM conda/miniconda3:latest

WORKDIR /app

COPY environment.yml .

RUN pip install --no-cache-dir virtualenv
RUN virtualenv venv

RUN conda env create --name website python=3.10 && conda clean -afy \
    && conda env update --name website --file environment.yml && conda clean -afy

ENV PATH /opt/conda/envs/website/bin:$PATH

COPY /app .

ENV REDIS_HOST=redis-service
ENV REDIS_PORT=6379

EXPOSE 4001

COPY entrypoint.sh /app/entrypoint.sh

# Dar permissão de execução ao script
RUN chmod +x /app/entrypoint.sh

# Usar o script de entrada como comando principal
ENTRYPOINT ["/app/entrypoint.sh"]