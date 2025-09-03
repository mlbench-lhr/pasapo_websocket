# websocket/apps.py - DEBUG VERSION
from django.apps import AppConfig
import os
from .funcs.common_funcs import *
class WebsocketConfig(AppConfig):  # Make sure class name matches
    default_auto_field = "django.db.models.BigAutoField"
    name = "websocket"

    def ready(self):
        
        # Prevent multiple threads on autoreload (only for runserver, not daphne)
        if os.environ.get("RUN_MAIN") == "true" or True:  # Always run for daphne
            try:
                from .funcs.mongo_listener import start_mongo_listener
                start_mongo_listener()
                
            except Exception as e:
                logger.debug(f"❌ Error starting mongo listener: {e}")
                import traceback
                traceback.logger.debug_exc()
        else:
            logger.debug("🔧 Skipping mongo listener (RUN_MAIN != 'true')")