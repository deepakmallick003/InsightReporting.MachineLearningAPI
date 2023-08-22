# Application Settings
# From the enviornments vaiables

from pydantic import Field, BaseSettings

class ApplicationSettings(BaseSettings):
    SEQ_API_KEY: str = Field(default='',env='SEQ_API_KEY')
    SEQ_SERVER: str = Field(default='',env='SEQ_SERVER')
    DEPLOYED_BASE_PATH: str = Field(default='/',env='DEPLOYED_BASE_PATH')
    OPENAPI_CLIENT_ID: str = Field(default='', env='OpenApiAzureAd__ClientId')
    APP_CLIENT_ID: str = Field(default='', env='AzureAd__ClientId')
    TENANT_ID: str = Field(default='', env='AzureAd__TenantId')

class Settings(ApplicationSettings):
    PROJECT_NAME: str = 'Insight Reporting'
    DOC_URL: str = '/swagger'
    MLMODEL_PATH: str = '/mlmodels'
    MLMODEL_ALLFIELDS_NAME = 'model_allfields.pkl'
    MLMODEL_TEXTONLY_NAME = 'model_textonly.pkl'

    MLMODEL_ALLFIELDS_VECTOR_NAME = 'model_allfields_vectorizer.joblib'
    MLMODEL_TEXTONLY_VECTOR_NAME = 'model_textonly_vectorizer.joblib'

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()