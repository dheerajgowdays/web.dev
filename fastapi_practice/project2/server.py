from fastapi import FastAPI,HTTPException,status

app = FastAPI()

@app.get("/add/{num1}/{num2}")
def add(num1:int,num2: int):
    return {"Sum":num1+num2}

@app.get("/mul/{num1}/{num2}")
def mul(num1:int,num2:int):
    return {"Mul":num1*num2}

@app.get("/div/{num1}/{num2}")
def div(num1: float,num2:float):
    if num2==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Division by zero is not allowed")
    return {"Div":num1/num2}

@app.get("/sub/{num1}/{num2}")
def sub(num1:int ,num2:int):
    return {"Diff":num1-num2}

@app.get("/remi/{num1}/{num2}")
def rem(num1:float ,num2: float):
    if num2==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Division by zero is not allowed")
    return {"Reminder":num1%num2}