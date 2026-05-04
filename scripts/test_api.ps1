param(
    [string]$BaseUrl = "http://127.0.0.1:5000"
)

$ErrorActionPreference = "Stop"

Write-Host "1. Health check"
Invoke-RestMethod -Uri "$BaseUrl/health"

Write-Host "`n2. Create user"
$createBody = @{
    name = "Div"
    email = "div-$(Get-Random)@example.com"
    age = 25
} | ConvertTo-Json

$created = Invoke-RestMethod -Method Post `
    -Uri "$BaseUrl/api/v1/users" `
    -ContentType "application/json" `
    -Body $createBody

$created
$userId = $created.data.id

Write-Host "`n3. Get all users"
Invoke-RestMethod -Uri "$BaseUrl/api/v1/users"

Write-Host "`n4. Get one user: $userId"
Invoke-RestMethod -Uri "$BaseUrl/api/v1/users/$userId"

Write-Host "`n5. Update user: $userId"
$updateBody = @{
    name = "Div Updated"
    age = 26
} | ConvertTo-Json

Invoke-RestMethod -Method Put `
    -Uri "$BaseUrl/api/v1/users/$userId" `
    -ContentType "application/json" `
    -Body $updateBody

Write-Host "`n6. Delete user: $userId"
Invoke-RestMethod -Method Delete -Uri "$BaseUrl/api/v1/users/$userId"

Write-Host "`nDone."

