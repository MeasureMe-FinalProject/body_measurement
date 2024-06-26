import uvicorn
from app.main import app  # noqa: F401

if __name__ == "__main__":
    uvicorn.run("debug:app", host="0.0.0.0", port=8000,
                reload=True, forwarded_allow_ips="*", )
