# ！/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from django.core.asgi import get_asgi_application

# 注意修改项目名
from web.websocket import websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebForTobii.settings')

django_application = get_asgi_application()


async def application(scope, receive, send):
    if scope['type'] == 'http':
        # Let Django handle HTTP requests
        await django_application(scope, receive, send)
    elif scope['type'] == 'websocket':
        # We'll handle Websocket connections here
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")

