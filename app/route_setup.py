from pkgutil import iter_modules
from importlib import import_module
import app.routers as routers
from app.logger import logger

def bind_routers(app):
    """
    Load all router files defined in the routers folder to the app.

    Each file must have a router property exposing an APIRouter object.
    Additionaly, prefix and tags properties may also be included to
    specify the path and the route group to be displayed in OpenAPI (swagger) page
    """
    for (_, name, _) in iter_modules(routers.__path__):
        router_module = import_module(f'app.routers.{name}')

        try:
            router_obj = router_module.router
            prefix = getattr(router_module, 'prefix', f'/{name}')
            tags = getattr(router_module, 'tags', [])

            app.include_router(
                router_obj,
                prefix=prefix,
                tags=tags
            )
        except Exception as e:
            logger.error(f"Cannot load router '{name}'")
            logger.error(e)


