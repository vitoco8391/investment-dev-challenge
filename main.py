from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pandas as pd
from optimizer import (
    markowitz_optimizer,
    risk_parity_optimizer,
    hrp_optimizer,
    uryasev_cvar_optimizer,
)

app = FastAPI()

@app.post("/optimize-portfolio")
async def optimize_portfolio(
    file: UploadFile = File(...),
    risk_level: float = Form(...),
    max_weight: float = Form(...),
    method: str = Form("markowitz")
):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        return JSONResponse(content={"error": "Failed to read CSV file"}, status_code=400)

    try:
        if method == "markowitz":
            weights = markowitz_optimizer(df, risk_level, max_weight)
        elif method == "risk_parity":
            weights = risk_parity_optimizer(df, max_weight)
        elif method == "hrp":
            weights = hrp_optimizer(df, max_weight)
        elif method == "cvar":
            weights = uryasev_cvar_optimizer(df, risk_level, max_weight)
        else:
            return JSONResponse(content={"error": "Unsupported optimization method"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={"optimal_portfolio": weights})
