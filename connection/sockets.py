from aiohttp import web
import socketio
import asyncio

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

@sio.event
def connect(sid, environ):
   print('[Server] connect with socket-id ', sid)

@sio.event
def my_message(sid, data):
   print('message', data)

@sio.event
def disconnect(sid):
    print('[Server] disconnect with socket-id ', sid)

def start_server():
   web.run_app(app)