# API Configuration
$API_BASE_URL = "http://localhost:5000/api"
$TOKEN = ""

# Colors for output
$GREEN = [System.ConsoleColor]::Green
$RED = [System.ConsoleColor]::Red
$YELLOW = [System.ConsoleColor]::Yellow

# Helper function to print colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [System.ConsoleColor]$Color
    )
    Write-Host $Message -ForegroundColor $Color
}

# Test registration
Write-ColorOutput "`nTesting Registration..." $YELLOW
$registerResponse = Invoke-RestMethod -Uri "$API_BASE_URL/auth/register" -Method Post -ContentType "application/json" -Body @{
    username = "testuser"
    email = "test@example.com"
    password = "Test123456"
    department = "computer"
} | ConvertTo-Json

Write-ColorOutput "Registration Response: $($registerResponse | ConvertTo-Json)" $GREEN

# Test login
Write-ColorOutput "`nTesting Login..." $YELLOW
$loginResponse = Invoke-RestMethod -Uri "$API_BASE_URL/auth/login" -Method Post -ContentType "application/json" -Body @{
    username = "testuser"
    password = "Test123456"
} | ConvertTo-Json

$TOKEN = $loginResponse.access_token
Write-ColorOutput "Login Response: $($loginResponse | ConvertTo-Json)" $GREEN

# Test creating a post
Write-ColorOutput "`nTesting Post Creation..." $YELLOW
$postData = @{
    title = "Test Post"
    content = "This is a test post content"
    category = "announcement"
}

$postResponse = Invoke-RestMethod -Uri "$API_BASE_URL/posts" -Method Post -Headers @{
    "Authorization" = "Bearer $TOKEN"
} -ContentType "application/json" -Body ($postData | ConvertTo-Json)

Write-ColorOutput "Post Creation Response: $($postResponse | ConvertTo-Json)" $GREEN

# Test getting all posts
Write-ColorOutput "`nTesting Get Posts..." $YELLOW
$getPostsResponse = Invoke-RestMethod -Uri "$API_BASE_URL/posts" -Method Get -Headers @{
    "Authorization" = "Bearer $TOKEN"
}

Write-ColorOutput "Get Posts Response: $($getPostsResponse | ConvertTo-Json)" $GREEN

# Test creating an event
Write-ColorOutput "`nTesting Event Creation..." $YELLOW
$eventData = @{
    title = "Test Event"
    description = "This is a test event"
    date = (Get-Date).AddDays(7).ToString("yyyy-MM-ddTHH:mm:ss")
    location = "Test Location"
}

$eventResponse = Invoke-RestMethod -Uri "$API_BASE_URL/events" -Method Post -Headers @{
    "Authorization" = "Bearer $TOKEN"
} -ContentType "application/json" -Body ($eventData | ConvertTo-Json)

Write-ColorOutput "Event Creation Response: $($eventResponse | ConvertTo-Json)" $GREEN

# Test getting all events
Write-ColorOutput "`nTesting Get Events..." $YELLOW
$getEventsResponse = Invoke-RestMethod -Uri "$API_BASE_URL/events" -Method Get -Headers @{
    "Authorization" = "Bearer $TOKEN"
}

Write-ColorOutput "Get Events Response: $($getEventsResponse | ConvertTo-Json)" $GREEN

# Test getting stats
Write-ColorOutput "`nTesting Get Stats..." $YELLOW
$statsResponse = Invoke-RestMethod -Uri "$API_BASE_URL/stats" -Method Get -Headers @{
    "Authorization" = "Bearer $TOKEN"
}

Write-ColorOutput "Get Stats Response: $($statsResponse | ConvertTo-Json)" $GREEN

# Test updating a post
Write-ColorOutput "`nTesting Post Update..." $YELLOW
$updatePostData = @{
    title = "Updated Test Post"
    content = "This is an updated test post content"
    category = "announcement"
}

$updatePostResponse = Invoke-RestMethod -Uri "$API_BASE_URL/posts/$($postResponse.id)" -Method Put -Headers @{
    "Authorization" = "Bearer $TOKEN"
} -ContentType "application/json" -Body ($updatePostData | ConvertTo-Json)

Write-ColorOutput "Post Update Response: $($updatePostResponse | ConvertTo-Json)" $GREEN

# Test deleting a post
Write-ColorOutput "`nTesting Post Deletion..." $YELLOW
$deletePostResponse = Invoke-RestMethod -Uri "$API_BASE_URL/posts/$($postResponse.id)" -Method Delete -Headers @{
    "Authorization" = "Bearer $TOKEN"
}

Write-ColorOutput "Post Deletion Response: $($deletePostResponse | ConvertTo-Json)" $GREEN

# Test deleting an event
Write-ColorOutput "`nTesting Event Deletion..." $YELLOW
$deleteEventResponse = Invoke-RestMethod -Uri "$API_BASE_URL/events/$($eventResponse.id)" -Method Delete -Headers @{
    "Authorization" = "Bearer $TOKEN"
}

Write-ColorOutput "Event Deletion Response: $($deleteEventResponse | ConvertTo-Json)" $GREEN

Write-ColorOutput "`nAPI Testing Complete!" $GREEN 