#!/bin/bash

# 시스템 업데이트
sudo yum update -y

# Nginx 설치
sudo yum install nginx -y

# Nginx 시작 및 자동 실행 설정
sudo systemctl start nginx
sudo systemctl enable nginx

# 웹 페이지 배포
sudo tee /usr/share/nginx/html/index.html > /dev/null << 'EOF'
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS 3-Tier Infrastructure</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 8px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 700px;
            width: 100%;
        }
        
        .header {
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #7f8c8d;
            font-size: 1em;
        }
        
        .status-badge {
            background: #27ae60;
            color: white;
            padding: 12px 24px;
            border-radius: 4px;
            text-align: center;
            font-weight: 600;
            margin: 20px 0;
        }
        
        .info-section {
            background: #ecf0f1;
            padding: 25px;
            border-radius: 6px;
            margin-top: 20px;
        }
        
        .info-section h2 {
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 15px;
        }
        
        .info-item {
            display: flex;
            padding: 8px 0;
            border-bottom: 1px solid #bdc3c7;
        }
        
        .info-item:last-child {
            border-bottom: none;
        }
        
        .info-label {
            font-weight: 600;
            color: #34495e;
            min-width: 120px;
        }
        
        .info-value {
            color: #7f8c8d;
        }
        
        .tech-stack {
            margin-top: 30px;
        }
        
        .tech-stack h3 {
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 12px;
        }
        
        .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .tech-tag {
            background: #3498db;
            color: white;
            padding: 6px 14px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #95a5a6;
            font-size: 0.85em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AWS 3-Tier Web Infrastructure</h1>
            <p class="subtitle">Cloud Architecture Implementation Project</p>
        </div>
        
        <div class="status-badge">
            System Status: Operational
        </div>
        
        <div class="info-section">
            <h2>Project Information</h2>
            <div class="info-item">
                <span class="info-label">Project Name</span>
                <span class="info-value">AWS 3-Tier Infrastructure Deployment</span>
            </div>
            <div class="info-item">
                <span class="info-label">Organization</span>
                <span class="info-value">SK Shields Rookies</span>
            </div>
            <div class="info-item">
                <span class="info-label">Completion Date</span>
                <span class="info-value">December 2025</span>
            </div>
            <div class="info-item">
                <span class="info-label">Environment</span>
                <span class="info-value">AWS EC2 Instance</span>
            </div>
        </div>
        
        <div class="tech-stack">
            <h3>Technology Stack</h3>
            <div class="tech-tags">
                <span class="tech-tag">Amazon VPC</span>
                <span class="tech-tag">Amazon EC2</span>
                <span class="tech-tag">Nginx</span>
                <span class="tech-tag">Linux</span>
                <span class="tech-tag">Security Groups</span>
            </div>
        </div>
        
        <div class="footer">
            <p>SK Shields Rookies AWS Cloud Training Program</p>
            <p>Infrastructure as Code Implementation</p>
        </div>
    </div>
</body>
</html>
EOF