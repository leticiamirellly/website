from fastapi import BackgroundTasks, FastAPI
from subscriber import RedisSubscriber
import asyncio
from contextlib import asynccontextmanager

subscriber = RedisSubscriber()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("sub startup")
    await subscriber.start()
    yield
    await subscriber.stop()
    
app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)



@app.get("/")
def read_root():
    return {"Hello": "World"}