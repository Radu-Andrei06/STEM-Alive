# LoginSystem-FullSetup.ps1
# Complete MySQL Login System Setup

# Configuration
$baseDir = "D:\LoginSystem"
$backendDir = "$baseDir\backend"
$frontendDir = "$baseDir\frontend"
$scriptsDir = "$frontendDir\scripts"
$mysqlUser = "auth_user"
$mysqlPass = "Auth@1234"
$dbName = "auth_system"

# Clean up previous installation
Write-Host "Cleaning up previous installation..." -ForegroundColor Yellow
if (Test-Path $baseDir) {
    Remove-Item -Path $baseDir -Recurse -Force
    Write-Host "Removed existing LoginSystem directory" -ForegroundColor Green
}

# Create directory structure
Write-Host "Creating directory structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $baseDir -Force | Out-Null
New-Item -ItemType Directory -Path $backendDir -Force | Out-Null
New-Item -ItemType Directory -Path $frontendDir -Force | Out-Null
New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null

# Create MySQL setup script
$mysqlScript = @"
CREATE DATABASE IF NOT EXISTS $dbName;
USE $dbName;
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE USER IF NOT EXISTS '$mysqlUser'@'localhost' IDENTIFIED BY '$mysqlPass';
GRANT ALL PRIVILEGES ON $dbName.* TO '$mysqlUser'@'localhost';
FLUSH PRIVILEGES;
INSERT INTO users (username, email, password) VALUES 
('testuser', 'test@example.com', '\$2a\$10\$N9qo8uLOickgx2ZMRZoMy.MQRqQz6Y3hN5oW3OQnO7O0XQYfX1J1K');
"@
$mysqlScript | Out-File -FilePath "$baseDir\mysql_setup.sql" -Encoding UTF8

# Create backend files
$envFile = @"
DB_HOST=localhost
DB_USER=$mysqlUser
DB_PASSWORD=$mysqlPass
DB_NAME=$dbName
JWT_SECRET=your-strong-secret-key
"@
$envFile | Out-File -FilePath "$backendDir\.env" -Encoding UTF8

# Initialize Node.js project
Write-Host "Initializing Node.js project..." -ForegroundColor Cyan
Set-Location -Path $backendDir
npm init -y | Out-Null
npm install bcrypt cors dotenv express jsonwebtoken mysql2 | Out-Null

Write-Host " Setup completed successfully!" -ForegroundColor Green
Write-Host "Run these commands to start:" -ForegroundColor Yellow
Write-Host "1. mysql -u root -p < D:\LoginSystem\mysql_setup.sql"
Write-Host "2. cd D:\LoginSystem\backend"
Write-Host "3. node server.js"
