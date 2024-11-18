# 
FROM python:3.9

# 
WORKDIR /app

#
#COPY requirements.txt ./ 
COPY /requirements.txt ./

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
RUN python -m spacy download en_core_web_sm

#
RUN python -m nltk.downloader punkt

#
RUN python -m nltk.downloader stopwords

#
RUN python -m nltk.downloader averaged_perceptron_tagger

#
RUN python -m nltk.downloader wordnet

# 
#COPY ./ ./
COPY /. ./

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
