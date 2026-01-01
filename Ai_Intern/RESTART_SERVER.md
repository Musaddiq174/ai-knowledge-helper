# How to Restart FastAPI Server

## If you're seeing errors, follow these steps:

### Step 1: Stop the current server
Press `CTRL+C` in the terminal where the server is running.

Or if you can't find it, run:
```powershell
Get-Process python | Stop-Process -Force
```

### Step 2: Start the server again
```powershell
python main.py
```

### Step 3: Wait for server to start
You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 4: Test the endpoint
Open browser: `http://localhost:8000/docs`

Or test with:
```powershell
python check_server.py
```

## Common Issues:

1. **Port already in use**: Change port in `main.py` line 137 to `port=8001`
2. **Old code running**: Make sure you restart after code changes
3. **Browser cache**: Hard refresh with `Ctrl+F5`

## Verify it's working:
- Visit: `http://localhost:8000/health`
- Should return: `{"status": "healthy", "vector_db_loaded": true}`

