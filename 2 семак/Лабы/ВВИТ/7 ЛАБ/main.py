from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import json
from datetime import datetime
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional

app = FastAPI()
html_path = Path(__file__).parent / "templates"
app.mount("/static", StaticFiles(directory=html_path), name="static")
clients = []


class IncomingMessage(BaseModel):
    type: str
    text: str

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Message is empty")
        if len(v) > 200:
            raise ValueError("Message is too long (max 200 characters)")
        return v.strip()


class ErrorMessage(BaseModel):
    type: str = "error"
    detail: str


@app.get("/")
async def get():
    html = (html_path / "chat.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html, status_code=200)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    username = websocket.query_params.get("username")

    if not username or username.strip() == "":
        await websocket.close(code=1008)
        return

    await websocket.accept()
    clients.append({"websocket": websocket, "username": username})

    online_count = len(clients)

    for client in clients:
        if client["websocket"] != websocket:
            system_msg = {
                "type": "system",
                "user": username,
                "text": f"{username} joined",
                "ts": datetime.now().isoformat(),
                "online": online_count
            }
            await client["websocket"].send_text(json.dumps(system_msg))

    welcome_msg = {
        "type": "system",
        "user": "server",
        "text": f"Welcome {username}!",
        "ts": datetime.now().isoformat(),
        "online": online_count
    }
    await websocket.send_text(json.dumps(welcome_msg))

    try:
        while True:
            data = await websocket.receive_text()
            try:
                raw_msg = json.loads(data)

                try:
                    validated_msg = IncomingMessage(**raw_msg)
                    text = validated_msg.text

                    if text.startswith("/w "):
                        parts = text.split(" ", 2)
                        if len(parts) >= 3:
                            target_user = parts[1]
                            private_text = parts[2]

                            target_client = None
                            for client in clients:
                                if client["username"] == target_user:
                                    target_client = client
                                    break

                            if target_client:
                                private_msg = {
                                    "type": "private",
                                    "from": username,
                                    "to": target_user,
                                    "text": private_text,
                                    "ts": datetime.now().isoformat()
                                }
                                await target_client["websocket"].send_text(json.dumps(private_msg))

                                confirm_msg = {
                                    "type": "private",
                                    "from": username,
                                    "to": target_user,
                                    "text": f"[To {target_user}]: {private_text}",
                                    "ts": datetime.now().isoformat()
                                }
                                await websocket.send_text(json.dumps(confirm_msg))
                            else:
                                error_msg = ErrorMessage(detail=f"User {target_user} not found")
                                await websocket.send_text(json.dumps(error_msg.model_dump()))
                        else:
                            error_msg = ErrorMessage(detail="Usage: /w <username> <message>")
                            await websocket.send_text(json.dumps(error_msg.model_dump()))
                    else:
                        outgoing_msg = {
                            "type": "message",
                            "user": username,
                            "text": text,
                            "ts": datetime.now().isoformat()
                        }

                        for client in clients:
                            await client["websocket"].send_text(json.dumps(outgoing_msg))

                except ValidationError as e:
                    error_detail = str(e.errors()[0].get('msg', 'Validation error'))
                    error_msg = ErrorMessage(detail=error_detail)
                    await websocket.send_text(json.dumps(error_msg.model_dump()))

            except json.JSONDecodeError:
                error_msg = ErrorMessage(detail="Invalid JSON format")
                await websocket.send_text(json.dumps(error_msg.model_dump()))

    except WebSocketDisconnect:
        for client in clients:
            if client["websocket"] == websocket:
                clients.remove(client)
                break
        online_count = len(clients)
        for client in clients:
            system_msg = {
                "type": "system",
                "user": username,
                "text": f"{username} left",
                "ts": datetime.now().isoformat(),
                "online": online_count
            }
            await client["websocket"].send_text(json.dumps(system_msg))
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)