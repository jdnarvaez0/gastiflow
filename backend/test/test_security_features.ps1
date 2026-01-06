# ============================================
# Gastiflow API Security Testing Script
# ============================================

Write-Host "`n🔒 GASTIFLOW API SECURITY TESTS`n" -ForegroundColor Cyan
Write-Host "Testing API at: http://localhost:8000`n" -ForegroundColor Yellow

$baseUrl = "http://localhost:8000"
$testsPassed = 0
$testsFailed = 0

# Helper function to test endpoint
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [string]$Body = $null,
        [string]$ContentType = "application/json",
        [int]$ExpectedStatus = 200,
        [string]$ExpectedContent = $null
    )
    
    Write-Host "Testing: $Name" -NoNewline
    
    try {
        $params = @{
            Uri = $Url
            Method = $Method
            Headers = $Headers
            ContentType = $ContentType
            ErrorAction = "Stop"
        }
        
        if ($Body) {
            $params.Body = $Body
        }
        
        $response = Invoke-WebRequest @params
        
        if ($response.StatusCode -eq $ExpectedStatus) {
            if ($ExpectedContent -and $response.Content -notlike "*$ExpectedContent*") {
                Write-Host " ❌ FAILED (Wrong content)" -ForegroundColor Red
                $script:testsFailed++
                return $false
            }
            Write-Host " ✅ PASSED" -ForegroundColor Green
            $script:testsPassed++
            return $true
        } else {
            Write-Host " ❌ FAILED (Status: $($response.StatusCode), Expected: $ExpectedStatus)" -ForegroundColor Red
            $script:testsFailed++
            return $false
        }
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq $ExpectedStatus) {
            Write-Host " ✅ PASSED (Expected error: $statusCode)" -ForegroundColor Green
            $script:testsPassed++
            return $true
        } else {
            Write-Host " ❌ FAILED (Status: $statusCode, Expected: $ExpectedStatus)" -ForegroundColor Red
            Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
            $script:testsFailed++
            return $false
        }
    }
}

# ============================================
# TEST 1: Password Validation
# ============================================
Write-Host "`n📋 TEST SUITE 1: Password Validation" -ForegroundColor Cyan

# Test weak password (too short)
$weakBody = @{
    username = "weakuser1"
    password = "weak"
    email = "weak1@example.com"
} | ConvertTo-Json

Test-Endpoint -Name "Reject password too short" `
    -Url "$baseUrl/api/register" `
    -Method "POST" `
    -Body $weakBody `
    -ExpectedStatus 422

# Test password without uppercase
$noUpperBody = @{
    username = "weakuser2"
    password = "test123!@#"
    email = "weak2@example.com"
} | ConvertTo-Json

Test-Endpoint -Name "Reject password without uppercase" `
    -Url "$baseUrl/api/register" `
    -Method "POST" `
    -Body $noUpperBody `
    -ExpectedStatus 422

# Test password without digit
$noDigitBody = @{
    username = "weakuser3"
    password = "TestTest!@#"
    email = "weak3@example.com"
} | ConvertTo-Json

Test-Endpoint -Name "Reject password without digit" `
    -Url "$baseUrl/api/register" `
    -Method "POST" `
    -Body $noDigitBody `
    -ExpectedStatus 422

# Test password without special char
$noSpecialBody = @{
    username = "weakuser4"
    password = "TestTest123"
    email = "weak4@example.com"
} | ConvertTo-Json

Test-Endpoint -Name "Reject password without special char" `
    -Url "$baseUrl/api/register" `
    -Method "POST" `
    -Body $noSpecialBody `
    -ExpectedStatus 422

# ============================================
# TEST 2: Email Validation
# ============================================
Write-Host "`n📋 TEST SUITE 2: Email Validation" -ForegroundColor Cyan

# Test invalid email format
$invalidEmailBody = @{
    username = "emailtest1"
    password = "Test123!@#"
    email = "not-an-email"
} | ConvertTo-Json

Test-Endpoint -Name "Reject invalid email format" `
    -Url "$baseUrl/api/register" `
    -Method "POST" `
    -Body $invalidEmailBody `
    -ExpectedStatus 422

# ============================================
# TEST 3: Rate Limiting
# ============================================
Write-Host "`n📋 TEST SUITE 3: Rate Limiting" -ForegroundColor Cyan

# Test login rate limit (5 per minute)
Write-Host "Testing login rate limit (5/minute)..." -ForegroundColor Yellow
$loginAttempts = 0
$rateLimitHit = $false

for ($i = 1; $i -le 7; $i++) {
    try {
        $loginBody = "username=nonexistent&password=wrong"
        $response = Invoke-WebRequest -Uri "$baseUrl/api/login" `
            -Method POST `
            -Body $loginBody `
            -ContentType "application/x-www-form-urlencoded" `
            -ErrorAction Stop
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 429) {
            $rateLimitHit = $true
            Write-Host "  Attempt $i" -NoNewline
            Write-Host " ✅ Rate limit triggered at attempt $i" -ForegroundColor Green
            $script:testsPassed++
            break
        } elseif ($statusCode -eq 401) {
            Write-Host "  Attempt $i" -NoNewline
            Write-Host " - Unauthorized (expected)" -ForegroundColor DarkGray
            $loginAttempts++
        }
    }
    Start-Sleep -Milliseconds 100
}

if (-not $rateLimitHit) {
    Write-Host " ❌ FAILED - Rate limit not triggered after 7 attempts" -ForegroundColor Red
    $script:testsFailed++
}

# ============================================
# TEST 4: Authentication Flow
# ============================================
Write-Host "`n📋 TEST SUITE 4: Authentication Flow" -ForegroundColor Cyan

# Generate unique username for this test
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$testUsername = "testuser_$timestamp"

# Register new user with strong password
$registerBody = @{
    username = $testUsername
    password = "Test123!@#"
    email = "test_${timestamp}@example.com"
} | ConvertTo-Json

Write-Host "Registering new user: $testUsername" -NoNewline
try {
    $registerResponse = Invoke-WebRequest -Uri "$baseUrl/api/register" `
        -Method POST `
        -Body $registerBody `
        -ContentType "application/json" `
        -ErrorAction Stop
    
    Write-Host " ✅ PASSED" -ForegroundColor Green
    $script:testsPassed++
} catch {
    Write-Host " ❌ FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
    $script:testsFailed++
}

# Login with new user
Write-Host "Login with new user" -NoNewline
try {
    $loginBody = "username=$testUsername&password=Test123!@#"
    $loginResponse = Invoke-WebRequest -Uri "$baseUrl/api/login" `
        -Method POST `
        -Body $loginBody `
        -ContentType "application/x-www-form-urlencoded" `
        -ErrorAction Stop
    
    $tokens = $loginResponse.Content | ConvertFrom-Json
    
    if ($tokens.access_token -and $tokens.refresh_token) {
        Write-Host " ✅ PASSED (Got access + refresh tokens)" -ForegroundColor Green
        $script:testsPassed++
        
        $accessToken = $tokens.access_token
        $refreshToken = $tokens.refresh_token
    } else {
        Write-Host " ❌ FAILED (Missing tokens)" -ForegroundColor Red
        $script:testsFailed++
    }
} catch {
    Write-Host " ❌ FAILED" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
    $script:testsFailed++
}

# Access protected endpoint with token
if ($accessToken) {
    Write-Host "Access protected endpoint (/api/me)" -NoNewline
    try {
        $headers = @{
            Authorization = "Bearer $accessToken"
        }
        $meResponse = Invoke-WebRequest -Uri "$baseUrl/api/me" `
            -Method GET `
            -Headers $headers `
            -ErrorAction Stop
        
        $userData = $meResponse.Content | ConvertFrom-Json
        if ($userData.username -eq $testUsername) {
            Write-Host " ✅ PASSED" -ForegroundColor Green
            $script:testsPassed++
        } else {
            Write-Host " ❌ FAILED (Wrong user data)" -ForegroundColor Red
            $script:testsFailed++
        }
    } catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
        $script:testsFailed++
    }
}

# ============================================
# TEST 5: Refresh Token Flow
# ============================================
Write-Host "`n📋 TEST SUITE 5: Refresh Token Flow" -ForegroundColor Cyan

if ($refreshToken) {
    Write-Host "Refresh access token" -NoNewline
    try {
        $refreshBody = @{
            refresh_token = $refreshToken
        } | ConvertTo-Json
        
        $refreshResponse = Invoke-WebRequest -Uri "$baseUrl/api/refresh" `
            -Method POST `
            -Body $refreshBody `
            -ContentType "application/json" `
            -ErrorAction Stop
        
        $newTokens = $refreshResponse.Content | ConvertFrom-Json
        
        if ($newTokens.access_token -and $newTokens.refresh_token) {
            Write-Host " ✅ PASSED (Got new tokens)" -ForegroundColor Green
            $script:testsPassed++
            
            # Verify old refresh token is revoked
            Write-Host "Verify old refresh token is revoked" -NoNewline
            try {
                $oldRefreshBody = @{
                    refresh_token = $refreshToken
                } | ConvertTo-Json
                
                $oldRefreshResponse = Invoke-WebRequest -Uri "$baseUrl/api/refresh" `
                    -Method POST `
                    -Body $oldRefreshBody `
                    -ContentType "application/json" `
                    -ErrorAction Stop
                
                Write-Host " ❌ FAILED (Old token still valid)" -ForegroundColor Red
                $script:testsFailed++
            } catch {
                $statusCode = $_.Exception.Response.StatusCode.value__
                if ($statusCode -eq 401) {
                    Write-Host " ✅ PASSED (Old token rejected)" -ForegroundColor Green
                    $script:testsPassed++
                } else {
                    Write-Host " ❌ FAILED (Unexpected status: $statusCode)" -ForegroundColor Red
                    $script:testsFailed++
                }
            }
            
            $accessToken = $newTokens.access_token
        } else {
            Write-Host " ❌ FAILED (Missing tokens)" -ForegroundColor Red
            $script:testsFailed++
        }
    } catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
        $script:testsFailed++
    }
}

# ============================================
# TEST 6: Logout Flow
# ============================================
Write-Host "`n📋 TEST SUITE 6: Logout Flow" -ForegroundColor Cyan

if ($accessToken) {
    Write-Host "Logout user" -NoNewline
    try {
        $headers = @{
            Authorization = "Bearer $accessToken"
        }
        $logoutResponse = Invoke-WebRequest -Uri "$baseUrl/api/logout" `
            -Method POST `
            -Headers $headers `
            -ErrorAction Stop
        
        Write-Host " ✅ PASSED" -ForegroundColor Green
        $script:testsPassed++
    } catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
        $script:testsFailed++
    }
}

# ============================================
# TEST 7: Security Headers
# ============================================
Write-Host "`n📋 TEST SUITE 7: Security Headers" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/me" -Method GET -ErrorAction Stop
} catch {
    $response = $_.Exception.Response
}

$headers = $response.Headers

Write-Host "Check X-Content-Type-Options header" -NoNewline
if ($headers["X-Content-Type-Options"] -eq "nosniff") {
    Write-Host " ✅ PASSED" -ForegroundColor Green
    $script:testsPassed++
} else {
    Write-Host " ❌ FAILED" -ForegroundColor Red
    $script:testsFailed++
}

Write-Host "Check X-Frame-Options header" -NoNewline
if ($headers["X-Frame-Options"] -eq "DENY") {
    Write-Host " ✅ PASSED" -ForegroundColor Green
    $script:testsPassed++
} else {
    Write-Host " ❌ FAILED" -ForegroundColor Red
    $script:testsFailed++
}

Write-Host "Check X-XSS-Protection header" -NoNewline
if ($headers["X-XSS-Protection"] -like "*1*") {
    Write-Host " ✅ PASSED" -ForegroundColor Green
    $script:testsPassed++
} else {
    Write-Host " ❌ FAILED" -ForegroundColor Red
    $script:testsFailed++
}

# ============================================
# TEST SUMMARY
# ============================================
Write-Host "`n" -NoNewline
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$totalTests = $testsPassed + $testsFailed
$passRate = [math]::Round(($testsPassed / $totalTests) * 100, 2)

Write-Host "`nTotal Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: " -NoNewline -ForegroundColor White
Write-Host "$testsPassed" -ForegroundColor Green
Write-Host "Failed: " -NoNewline -ForegroundColor White
Write-Host "$testsFailed" -ForegroundColor Red
Write-Host "Pass Rate: " -NoNewline -ForegroundColor White
Write-Host "$passRate%" -ForegroundColor $(if ($passRate -ge 90) { "Green" } elseif ($passRate -ge 70) { "Yellow" } else { "Red" })

if ($testsFailed -eq 0) {
    Write-Host "`n🎉 ALL TESTS PASSED! Your API is secure and ready for deployment!" -ForegroundColor Green
} elseif ($passRate -ge 90) {
    Write-Host "`n⚠️  Most tests passed, but some issues need attention." -ForegroundColor Yellow
} else {
    Write-Host "`n❌ Multiple tests failed. Please review the security implementation." -ForegroundColor Red
}

Write-Host "`n"
