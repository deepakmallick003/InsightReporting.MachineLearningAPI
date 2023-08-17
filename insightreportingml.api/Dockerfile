# 
FROM python:3.9

# 
WORKDIR /app

#
#COPY requirements.txt ./ 
COPY insightreportingml.api/requirements.txt ./

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
RUN python -m spacy download en_core_web_sm

#
RUN python -m nltk.downloader punkt

#
RUN python -m nltk.downloader stopwords

# 
#COPY ./ ./
COPY insightreportingml.api/. ./

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
