from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()

    df = pd.read_csv(io.StringIO(contents.decode("utf-8")), sep=";")

    df.columns = df.columns.str.strip()

    category_col = [c for c in df.columns if "category" in c.lower()][0]
    amount_col = [c for c in df.columns if "amount" in c.lower()][0]

    df[category_col] = (
        df[category_col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    def clean_amount(x):
        x = str(x).strip().replace(" ", "")

        if "," in x and "." in x:
            x = x.replace(",", "")
        elif "," in x:
            x = x.replace(",", ".")

        return float(x)

    df[amount_col] = df[amount_col].apply(clean_amount)

    total = round(
        df[df[category_col] == "food"][amount_col].sum(),
        2
    )

    return {
        "answer": total,
        "email": "YOUR_EMAIL_HERE",
        "exam": "tds-2025-05-roe"
    }
