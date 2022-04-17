export TASQUE_SECRET_KEY=$(openssl rand -hex 16)
export TASQUE_JWT_EXPIRATION_MINUTES="60"
uvicorn tasque:app --reload
