Add-Type -AssemblyName System.Web

$env:POSTGRES_USERNAME="localdb"
$env:POSTGRES_PASSWORD="$([System.Web.Security.Membership]::GeneratePassword(16, 0))"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_CONTAINER="tasque_be_database"
$env:TASQUE_DATABASE_PASSWORD=$env:POSTGRES_PASSWORD
$env:TASQUE_DATABASE_USERNAME=$env:POSTGRES_USERNAME
$env:TASQUE_DATABASE="localdb"
$env:TASQUE_DATABASE_HOST="localhost"
$env:TASQUE_DATABASE_PORT="5432"
$env:FLYWAY_URL="jdbc:postgresql://localhost:$env:POSTGRES_PORT/localdb"
$env:FLYWAY_USER=$env:TASQUE_DATABASE_USERNAME
$env:FLYWAY_PASSWORD=$env:TASQUE_DATABASE_PASSWORD

Write-Output "Database password: $env:POSTGRES_PASSWORD"

docker stop $env:POSTGRES_CONTAINER
docker run --name $env:POSTGRES_CONTAINER --rm `
  -p "5432:$env:POSTGRES_PORT" `
  -e "POSTGRES_PASSWORD=$env:POSTGRES_PASSWORD" -e "POSTGRES_USER=$env:POSTGRES_USERNAME" `
  -d `
  postgres
flyway migrate
