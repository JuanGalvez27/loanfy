FROM python:3.12-slim
RUN useradd -m loanfy
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app
COPY apps apps
COPY core core
COPY manage.py requirements.txt /app/
RUN pip install -r requirements.txt
RUN chown -R loanfy:loanfy /app
USER loanfy
EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]