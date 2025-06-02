import joblib
import numpy as np
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Load dictionary and model once at startup
fraud_dict = joblib.load(r"C:\Users\Avijit\Desktop\FRAUD-DETECTION\src\test\fraudterminaldict.pkl")
model = joblib.load(r"C:\Users\Avijit\Desktop\FRAUD-DETECTION\src\test\model.pkl")

@app.post("/predict", response_class=PlainTextResponse)
def predict(
    TRANSACTION_ID: int = Form(...),
    CUSTOMER_ID: int = Form(...),
    TX_YEAR: int = Form(...),
    TX_MONTH: int = Form(...),
    TX_DAY: int = Form(...),
    TERMINAL_ID: int = Form(...),
    TX_AMOUNT: int = Form(...)
):
    Above220 = 1 if TX_AMOUNT > 200 else 0
    fraudscore = fraud_dict.get(TERMINAL_ID, 0)

    input_array = np.array([[
        TRANSACTION_ID,
        CUSTOMER_ID,
        TX_YEAR,
        TX_MONTH,
        TX_DAY,
        TERMINAL_ID,
        TX_AMOUNT,
        Above220,
        fraudscore
    ]])

    prediction = model.predict(input_array)[0]

    if prediction == 1:
        return "FRAUD"
    else:
        return "CLEAN CUSTOMER"
