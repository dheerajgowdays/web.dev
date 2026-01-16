from fastapi import FastAPI #importing

app=FastAPI() #app instance

@app.get("/greet")
def get_greeting():
    return {"Message":"Hello World!"}