FROM python:3.12

EXPOSE 8004/tcp

COPY bff-requirements.txt ./
RUN pip install --no-cache-dir -r bff-requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "bff_web.main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]