from fastapi import APIRouter
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect

from src.chat.connection_manager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def support_chat_websocket(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
