import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel Python serverless handler
def handler(event, context):\n    import json\n    import multiprocessing\n    from starlette.requests import Request\n    from starlette.responses import Response\n    \n    # Build Starlette request from Vercel event\n    body = event.get('body', b'')\n    if event.get('isBase64Encoded'):\n        body = base64.b64decode(body)\n    \n    headers = {k.lower(): v for k, v in event.get('headers', {}).items()}\n    \n    request = Request(\n        scope={\n            'type': 'http',\n            'method': event['httpMethod'],\n            'path': event['path'],\n            'query_string': event.get('queryString', ''),\n            'headers': [(k.lower(), v) for k, v in headers.items()],\n            'server': ('vercel', '3000'),\n            'client': ('0.0.0.0', 0),\n            'scheme': headers.get('x-forwarded-proto', 'https'),\n        },\n        receive=receive_body(body)\n    )\n    \n    # Run ASGI app\n    response = Response()\n    \n    async def receive():\n        return {'type': 'http.request', 'body': body}\n    \n    await app(request.scope, receive=receive, send=response)\n    \n    return {\n        'statusCode': response.status_code,\n        'headers': dict(response.headers),\n        'body': response.body,\n        'isBase64Encoded': False\n    }\n\nasync def receive_body(body):\n    return {'type': 'http.request', 'body': body}\n\nimport base64

