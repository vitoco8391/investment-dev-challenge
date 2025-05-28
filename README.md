
# Portfolio Optimization API

This is a RESTful API built with **FastAPI** to calculate optimal portfolio allocations using various optimization strategies.

## 🚀 How to Run

Make sure you have `uvicorn`, `pandas`, `numpy`, and `FastAPI` installed.

```bash
uvicorn main:app --reload
```

Access Swagger docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔧 Endpoint

### `POST /optimize-portfolio`

**Request format:** `multipart/form-data`

| Field        | Type      | Description                                       |
|--------------|-----------|---------------------------------------------------|
| `file`       | file (.csv)| CSV with daily returns. Columns = tickers        |
| `risk_level` | float     | Max portfolio risk (std deviation or CVaR bound) |
| `max_weight` | float     | Max weight per asset                             |
| `method`     | string    | Optimization method: see below                   |

### Example CURL request:
```bash
curl -X POST "http://127.0.0.1:8000/optimize-portfolio" \
  -F "file=@returns.csv" \
  -F "risk_level=0.03" \
  -F "max_weight=0.25" \
  -F "method=hrp"
```

### Example Response:
```json
{
  "optimal_portfolio": {
    "AAPL": 0.2,
    "MSFT": 0.18,
    "GOOG": 0.25,
    "AMZN": 0.22,
    "META": 0.15
  }
}
```

---

## 📈 Supported Methods

### `equal_weight`
Simple benchmark. Equal allocation across all assets.

### `markowitz`
Mean-variance optimization. Maximizes expected return for a given level of risk or minimizes risk for a given return target.

### `risk_parity`
Allocates weights such that each asset contributes equally to total risk.

### `hrp`
Hierarchical Risk Parity (López de Prado):
- Clusters assets based on correlations
- Avoids matrix inversion
- More robust in high-dimensional/low-sample environments

### `cvar`
CVaR optimization (Uryasev):
- Focuses on downside risk (tail losses)
- Optimizes expected loss under the worst α% scenarios (default α = 95%)

---

## 📎 Notes
- CSV file must contain daily return series with tickers as column headers.
- All optimization results return weights that sum ≈ 1, and each ≤ `max_weight`.

---

## 🧠 Why these methods?
Each included strategy covers a different investment philosophy:
- Markowitz: mean-variance optimization
- Risk Parity: balance risk, not returns
- HRP: structure-aware and robust
- CVaR: tail-risk focused
- Equal Weight: reference benchmark

---

## 👤 Author
Víctor Valdenegro Cabrera
