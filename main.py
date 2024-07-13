from fastapi import FastAPI

app = FastAPI(
    title="RiffRaff Inventory",
)

@app.get("/")
def root():
    return {"message": "Welcome to RiffRaff Inventory"}
