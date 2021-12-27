$env:TASQUE_SECRET_KEY="$([System.Web.Security.Membership]::GeneratePassword(16, 0))"
$env:TASQUE_JWT_EXPIRATION_MINUTES=60
uvicorn tasque:app --no-use-colors --reload
