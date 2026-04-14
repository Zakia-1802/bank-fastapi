from fastapi import FastAPI, HTTPException

app = FastAPI()

# Base de données temporaire en mémoire
accounts = [
    {"id": 1, "owner": "Alice", "balance": 1200},
    {"id": 2, "owner": "Bob", "balance": 500}
]

@app.get("/")
def home():
    return {"message": "Bank API is running"}

@app.get("/accounts")
def get_accounts():
    return accounts

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    for account in accounts:
        if account["id"] == account_id:
            return account

    raise HTTPException(status_code=404, detail="Account not found")

@app.post("/accounts")
def create_account(account: dict):
    if "owner" not in account:
        raise HTTPException(status_code=400, detail="Missing owner")

    balance = account.get("balance", 0)

    if balance < 0:
        raise HTTPException(status_code=400, detail="Initial balance cannot be negative")

    new_id = max(item["id"] for item in accounts) + 1 if accounts else 1

    new_account = {
        "id": new_id,
        "owner": account["owner"],
        "balance": balance
    }

    accounts.append(new_account)
    return new_account

@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: int, data: dict):
    for account in accounts:
        if account["id"] == account_id:
            if "amount" not in data:
                raise HTTPException(status_code=400, detail="Missing amount")

            amount = data["amount"]

            if amount <= 0:
                raise HTTPException(status_code=400, detail="Deposit amount must be positive")

            account["balance"] += amount

            return {
                "message": "Deposit successful",
                "account": account
            }

    raise HTTPException(status_code=404, detail="Account not found")

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: int, data: dict):
    for account in accounts:
        if account["id"] == account_id:
            if "amount" not in data:
                raise HTTPException(status_code=400, detail="Missing amount")

            amount = data["amount"]

            if amount <= 0:
                raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")

            if amount > account["balance"]:
                raise HTTPException(status_code=400, detail="Insufficient funds")

            account["balance"] -= amount

            return {
                "message": "Withdrawal successful",
                "account": account
            }

    raise HTTPException(status_code=404, detail="Account not found")
