from fastapi import FastAPI

# Entrypoint file

app = FastAPI()

@app.get("/")
async def read_item():
    return {"message": "Welcome to our app"}
