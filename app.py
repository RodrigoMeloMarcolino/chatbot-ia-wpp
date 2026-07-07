from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from langgraph.checkpoint.redis import RedisSaver

from graph import build_graph
from message_buffer import message_buffer
from core.config import REDIS_CACHE_URL, ALLOWED_PHONES


GROUP_MESSAGE = '@g.'
ALLOWED_CHAT_IDS = {
    f'{phone.strip()}@s.whatsapp.net'
    for phone in ALLOWED_PHONES.split(',')
    if phone.strip()
}


def is_group_chat(*chat_ids):
    return any(
        chat_id and (GROUP_MESSAGE in chat_id or chat_id.endswith('@g.us'))
        for chat_id in chat_ids
    )


def is_allowed_chat(*chat_ids):
    return any(chat_id in ALLOWED_CHAT_IDS for chat_id in chat_ids)

@asynccontextmanager
async def lifespan(app: FastAPI):
    with RedisSaver.from_conn_string(REDIS_CACHE_URL) as checkpointer:
        checkpointer.setup()
        app.state.graph = build_graph(checkpointer=checkpointer)
        yield

app = FastAPI(lifespan=lifespan)

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    payload = data.get('data') or {}
    key = payload.get('key') or {}
    message_data = payload.get('message') or {}

    chat_id = key.get('remoteJid')
    chat_id_alt = key.get('remoteJidAlt')
    message = message_data.get('conversation')

    if not message or is_group_chat(chat_id, chat_id_alt) or not is_allowed_chat(chat_id, chat_id_alt):
        print(
            '[WEBHOOK] ignored',
            {
                'remoteJid': chat_id,
                'remoteJidAlt': chat_id_alt,
                'has_message': bool(message),
            },
        )
        return {'status': 'ok'}

    await message_buffer(
        chat_id=chat_id_alt or chat_id,
        message=message,
        graph=request.app.state.graph
    )

    return {'status': 'ok'}
