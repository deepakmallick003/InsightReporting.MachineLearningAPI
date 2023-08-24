# Insight Reporting Machine learing Service

## Project Overview
The purpose of the PlantwisePlus.InsightReporting.MicroService.MachineLearningAPI project is use Machine learning to predict relevant articles

## Contact Details
* **Technical Contact:** Ravi Bhushan Sinha, Deepak Mallick
* **Business Owner:** Hannah Fiedler
* **Project Manager:** Michelle Jones

## Key Details

### Production URLs
* **Base URL:** https://rest.cabi.org/insightreportingml/

### Development Team(s) or Suppliers
* CABI

### Technology
* **Version:** Python 3.9
* **Logging:** Seq
* **Authentication:** Azure AD

## Dependencies
* fastapi>=0.68.0,<0.69.0
* pydantic>=1.8.0,<2.0.0
* uvicorn>=0.15.0,<0.16.0
* python-dotenv>=1.0.0
* seqlog>=0.3.27
* fastapi_azure_auth>=4.2.1
* spacy>=3.6
* rake_nltk>=1.0.6
* httpx==0.19.0
* pytest>=7.4.0

### Notes
* Create virtual enviornment 
**python -m venv .venv**
* Activate Virtual Environment
**.venv\Scripts\activate**
* Change Project Directory to insightreportingml.api
**cd insight***
* Install dependencies
**pip install -r requirements.txt**
* Run application
**uvicorn main:app --host localhost --port 8080 --reload**
* Run test
**pytest**
* Install other libraries
  * python -m spacy download en_core_web_sm
  * python -m nltk.downloader punkt
  * python -m nltk.downloader stopwords
  * python -m nltk.downloader wordnet
