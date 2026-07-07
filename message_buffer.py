import asyncio
import traceback
import redis.asyncio as redis
from collections import defaultdict

from langgraph.graph import MessagesState
from langgraph.graph.state import CompiledStateGraph

from evolution_api import send_whatsapp_message

from core.config import (
    REDIS_CACHE_URL,
    BUFFER_KEY_SUFFIX,
    BUFFER_TTL,
    DEBOUNCE_SECONDS
)


redis_client = redis.Redis.from_url(REDIS_CACHE_URL, decode_responses=True)
debounce_tasks = defaultdict(asyncio.Task)

def log(*args):
    print('[BUFFER]', *args)

async def message_buffer(chat_id: str, message: str, graph: CompiledStateGraph[MessagesState, None, MessagesState, MessagesState]):
    chat_buffer_key = f'{chat_id}{BUFFER_KEY_SUFFIX}'

    await redis_client.rpush(chat_buffer_key, message)
    await redis_client.expire(chat_buffer_key, BUFFER_TTL)

    log(f'Mensagem adicionada ao buffer de {chat_id}: {message}')

    if debounce_tasks.get(chat_id):
        debounce_tasks[chat_id].cancel()
        log(f'Debounce resetado para {chat_id}')

    debounce_tasks[chat_id] = asyncio.create_task(debounce_message(chat_id=chat_id, graph=graph))

async def debounce_message(chat_id: str, graph: CompiledStateGraph[MessagesState, None, MessagesState, MessagesState]):
    try:
        log(f'Iniciando debounce para  {chat_id}')

        await asyncio.sleep(float(DEBOUNCE_SECONDS))

        buffer_key = f'{chat_id}{BUFFER_KEY_SUFFIX}'
        messages = await redis_client.lrange(buffer_key, 0, -1)

        full_message = ' '.join(messages).strip()

        if full_message:
            result = graph.invoke(
                {
                    'messages':[
                        {'role': 'human', 'content': full_message}
                    ]
                },
                config={
                    'configurable': {
                        'thread_id': chat_id
                    }
                }
            )

            ai_answer = result['messages'][-1].content
            log(f'Resposta gerada para {chat_id}: {len(ai_answer)} caracteres')

            send_whatsapp_message(chat_id, ai_answer)
            log(f'Resposta enviada para {chat_id}')

            await redis_client.delete(buffer_key)
    except asyncio.CancelledError:
        log(f'Debounce cancelado para {chat_id}')
    except Exception:
        log(f'Erro ao processar mensagem de {chat_id}')
        traceback.print_exc()
