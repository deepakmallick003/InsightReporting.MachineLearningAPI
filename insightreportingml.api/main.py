import logging
from core import logger
from fastapi import FastAPI, Request, Security, Body
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from core.config import settings
from routers import health
from scripts import transform

logger.initialize()

def get_application() -> FastAPI:

    tags_metadata = [
        {
            "name": "process",
            "description": "**Transform** the raw json data from EIOS, extract **keywords** and compute **prediction** score",
        }
    ]
    app = FastAPI(
        version='1.0.0',
        title=settings.PROJECT_NAME,
        description="API's to process data from EIOS, add keyword and predication",
        docs_url=settings.DOC_URL,
        root_path=settings.DEPLOYED_BASE_PATH,
        swagger_ui_oauth2_redirect_url='/oauth2-redirect',
        swagger_ui_init_oauth={
            'usePkceWithAuthorizationCodeGrant': True,
            'clientId': settings.OPENAPI_CLIENT_ID,
        },
        openapi_tags=tags_metadata
    )

    # Enabled CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
        app_client_id=settings.APP_CLIENT_ID,
        tenant_id=settings.TENANT_ID,
        scopes={
            f'api://{settings.APP_CLIENT_ID}/user_impersonation': 'user_impersonation',
        }
    )

    @app.on_event('startup')
    async def load_config() -> None:
        """
        Load OpenID config on startup.
        """
        await azure_scheme.openid_config.load_config()

    # include healthcheck router
    app.include_router(health.router)

    # redirect to swagger endpoint
    @app.get("/", include_in_schema=False)
    async def root(request: Request):
        return RedirectResponse('swagger')

    # endpoint tp process EIOS data
    @app.post("/process/{modelVersion}", dependencies=[Security(azure_scheme)], tags=["API"])
    async def process_data(modelVersion, payload: dict = Body(...)):

        return transform.transform(payload, modelVersion)

    return app


app = get_application()
