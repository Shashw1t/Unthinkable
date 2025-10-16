# Deployment Guide

This guide covers deploying the Knowledge Base Search Engine to production environments.

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended for Beginners)
### Option 2: Heroku
### Option 3: AWS EC2
### Option 4: Google Cloud Run
### Option 5: Azure App Service
### Option 6: Docker Deployment

---

## 🐳 Docker Deployment

### Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploaded_documents chroma_db

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "setup_and_run.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LLM_PROVIDER=openai
      - LLM_MODEL=gpt-3.5-turbo
    volumes:
      - ./uploaded_documents:/app/uploaded_documents
      - ./chroma_db:/app/chroma_db
    restart: unless-stopped
```

### Build and Run

```bash
# Build the image
docker build -t knowledge-base-search .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/uploaded_documents:/app/uploaded_documents \
  -v $(pwd)/chroma_db:/app/chroma_db \
  knowledge-base-search

# Or use docker-compose
docker-compose up -d
```

---

## ☁️ Railway Deployment

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Create `railway.json`**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python setup_and_run.py",
    "healthcheckPath": "/health"
  }
}
```

4. **Create `Procfile`**
```
web: python setup_and_run.py
```

5. **Deploy**
```bash
railway init
railway up
```

6. **Set Environment Variables** in Railway Dashboard:
- `OPENAI_API_KEY`
- `LLM_PROVIDER=openai`
- `LLM_MODEL=gpt-3.5-turbo`

---

## 🔧 Heroku Deployment

1. **Create `Procfile`**
```
web: python setup_and_run.py
```

2. **Create `runtime.txt`**
```
python-3.11.0
```

3. **Deploy**
```bash
heroku login
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key_here
git push heroku main
```

---

## 🌐 AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. Launch Ubuntu 22.04 instance (t2.medium recommended)
2. Configure security group:
   - Port 22 (SSH)
   - Port 8000 (Application)
   - Port 80 (HTTP) - optional with Nginx
   - Port 443 (HTTPS) - optional with SSL

### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3-pip python3-venv -y

# Clone repository
git clone <your-repo-url>
cd Unthinkable1

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API key
```

### Step 3: Setup as Service

Create `/etc/systemd/system/knowledge-base.service`:

```ini
[Unit]
Description=Knowledge Base Search Engine
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Unthinkable1
Environment="PATH=/home/ubuntu/Unthinkable1/venv/bin"
ExecStart=/home/ubuntu/Unthinkable1/venv/bin/python setup_and_run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable knowledge-base
sudo systemctl start knowledge-base
sudo systemctl status knowledge-base
```

### Step 4: Setup Nginx (Optional)

```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/knowledge-base
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/knowledge-base /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 SSL/HTTPS Setup with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

---

## 📊 Production Considerations

### 1. Environment Variables

**Never commit `.env` to Git!**

Set these in your deployment platform:
```bash
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
HOST=0.0.0.0
PORT=8000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

### 2. Security

**API Key Protection:**
- Use environment variables
- Rotate keys regularly
- Monitor usage for anomalies

**CORS Configuration:**
Edit `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

**File Upload Security:**
- Validate file types strictly
- Implement file size limits
- Scan for malware (production)
- Use signed URLs for uploads

### 3. Database & Storage

**Vector Database:**
- ChromaDB data persists in `chroma_db/`
- Mount this as a volume in production
- Consider managed vector DB for scale:
  - Pinecone
  - Weaviate
  - Qdrant Cloud

**File Storage:**
- Local: Use persistent volumes
- Cloud: Use S3, GCS, or Azure Blob Storage

### 4. Monitoring

**Application Monitoring:**
```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Health Checks:**
Already implemented at `/health` endpoint

**Metrics:**
Consider adding:
- Prometheus for metrics
- Grafana for visualization
- Sentry for error tracking

### 5. Performance Optimization

**Caching:**
```python
# Add Redis for query caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="kb-cache")
```

**Async Processing:**
- Use Celery for background document processing
- Queue uploads for large batches

**Load Balancing:**
- Use multiple instances behind load balancer
- Nginx/HAProxy for load balancing
- Kubernetes for orchestration

### 6. Scaling Considerations

**Horizontal Scaling:**
- Separate vector DB from app instances
- Use shared storage (S3/GCS)
- Load balance across instances

**Database Scaling:**
- Use managed vector DB services
- Implement database replication
- Consider sharding for large datasets

### 7. Backup Strategy

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz chroma_db/ uploaded_documents/
aws s3 cp backup_$DATE.tar.gz s3://your-backup-bucket/
```

### 8. Cost Optimization

**LLM Costs:**
- Use GPT-3.5-turbo instead of GPT-4
- Implement caching for common queries
- Set token limits appropriately
- Monitor API usage

**Infrastructure:**
- Use spot instances where possible
- Auto-scaling groups
- Schedule shutdown for dev/test environments

---

## 🔍 Monitoring & Logging

### Application Logs

```python
# Enhanced logging in config.py
import logging.handlers

handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics to Track

- Request count
- Response time
- Error rate
- Document processing time
- LLM API latency
- Vector search performance
- Storage usage

---

## 🧪 Testing in Production

```bash
# Health check
curl https://your-domain.com/health

# Upload test
curl -X POST https://your-domain.com/upload \
  -F "files=@test.pdf"

# Query test
curl -X POST https://your-domain.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test question"}'
```

---

## 🆘 Troubleshooting Production

**High Memory Usage:**
- Reduce embedding model size
- Limit concurrent requests
- Increase instance size

**Slow Queries:**
- Optimize chunk size
- Reduce TOP_K_RESULTS
- Add caching layer

**API Rate Limits:**
- Implement request queuing
- Add rate limiting middleware
- Use backup LLM provider

---

## 📝 Production Checklist

✅ Environment variables configured
✅ API keys secured
✅ CORS properly configured
✅ HTTPS/SSL enabled
✅ Monitoring in place
✅ Backup strategy implemented
✅ Error tracking configured
✅ Rate limiting enabled
✅ Health checks working
✅ Documentation updated
✅ Load testing completed
✅ Security audit performed

---

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/production-best-practices)

---

**Good luck with your deployment! 🚀**
