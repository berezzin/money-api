from fastapi import APIRouter, Depends
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect

from src.chat.connection_manager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws/{username}")
async def support_chat_websocket(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client <b>{username}</b> says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{username} left the chat")
