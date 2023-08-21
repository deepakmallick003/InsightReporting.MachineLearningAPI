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

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()