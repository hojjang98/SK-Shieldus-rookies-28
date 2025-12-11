#!/bin/bash
yum update -y
yum install -y nginx
systemctl start nginx
systemctl enable nginx

INSTANCE_ID=$(ec2-metadata --instance-id | cut -d " " -f 2)
AZ=$(ec2-metadata --availability-zone | cut -d " " -f 2)

cat > /usr/share/nginx/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>3-Tier Architecture</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 20px; }
        .info { background: #f0f0f0; padding: 20px; border-radius: 5px; margin-top: 20px; }
        .label { font-weight: bold; color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AWS 3-Tier Architecture</h1>
        <p>Successfully deployed with Auto Scaling!</p>
        <div class="info">
            <p><span class="label">Instance ID:</span> INSTANCE_ID_PLACEHOLDER</p>
            <p><span class="label">Availability Zone:</span> AZ_PLACEHOLDER</p>
            <p><span class="label">Organization:</span> SK Shields Rookies</p>
        </div>
    </div>
</body>
</html>
EOF

sed -i "s/INSTANCE_ID_PLACEHOLDER/$INSTANCE_ID/g" /usr/share/nginx/html/index.html
sed -i "s/AZ_PLACEHOLDER/$AZ/g" /usr/share/nginx/html/index.html