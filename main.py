from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/stream")
async def message_stream():
    async def event_generator():
        count = 0
        while True:
            count += 1
            # Send a simple key-value pair for state1
            state_update = {"state1": count }
            yield state_update
            await asyncio.sleep(0.1)

    async def event_source_wrapper():
        async for state_update in event_generator():
            # Send the state update as a simple JSON object
            message = f'data: {json.dumps(state_update)}\r\n\r\n'
            yield message.encode('utf-8')

    return StreamingResponse(
        event_source_wrapper(),
        media_type='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
    )
