FROM python:slim
WORKDIR /optar

# Copy and run requirements install first to save time in following builds
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY prod.py prod.py
COPY src ./src
COPY cache ./cache

# yes, coping them at build time is not ideal, this is a PoC
COPY keywords.txt keywords.txt
COPY sites.txt sites.txt

ENTRYPOINT [ "python", "prod.py" ]