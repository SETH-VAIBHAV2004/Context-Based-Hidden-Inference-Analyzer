# Deployment

Status: **Docker configuration provided**. Production deployment requires hosting provider selection and configuration.

## Local Development

### Without Docker

**Backend:**

```powershell
py -3.11 -m venv backend/.venv
backend\.venv\Scripts\activate
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

**Frontend:**

```powershell
cd frontend
npm install
npm run dev
```

Access at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### With Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

## Production Deployment Options

### Backend (FastAPI)

**Option 1: Railway / Render**
- Suitable for CPU-only TF-IDF baseline
- Free tier available with limitations
- Automatic HTTPS
- Easy environment variable management

**Option 2: AWS EC2 / DigitalOcean Droplet**
- Full control over resources
- Can handle larger models with appropriate instance type
- Requires manual HTTPS setup (Let's Encrypt recommended)
- More cost-effective for sustained use

**Option 3: Google Cloud Run / Azure Container Apps**
- Serverless container deployment
- Auto-scaling
- Pay-per-use

### Frontend (Next.js)

**Option 1: Vercel** (Recommended)
- Native Next.js support
- Automatic deployments from Git
- Edge network CDN
- Free tier for hobby projects
- Set `NEXT_PUBLIC_API_URL` environment variable to backend URL

**Option 2: Netlify**
- Similar to Vercel
- Good Git integration
- Free tier available

**Option 3: Cloudflare Pages**
- Fast edge network
- Generous free tier

## Environment Variables

### Backend

Required:
- `CIRCA_PATH` - Path to Circa TSV file (optional, for real dataset)

Optional:
- `CORS_ORIGINS` - Comma-separated allowed origins (default: `http://localhost:3000`)

### Frontend

Required:
- `NEXT_PUBLIC_API_URL` - Backend API URL (e.g., `https://api.yourdomain.com`)

## Security Checklist

Before production deployment:

- [ ] Set secure CORS origins (remove wildcards)
- [ ] Add rate limiting to API endpoints
- [ ] Set up HTTPS/TLS certificates
- [ ] Review file upload sizes and validation
- [ ] Add authentication if storing user data
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy for artifacts/

## Scaling Considerations

### Lightweight Demo Mode (Free Tier Compatible)
- TF-IDF + Logistic Regression only
- Synthetic fixture data
- No persistent storage
- Single instance

### Research Mode (Small VM)
- All models except LLM baseline
- Circa dataset
- File-based metrics
- 2-4 GB RAM recommended

### Full Production (Medium VM)
- All models including transformers
- Multiple datasets
- PostgreSQL for experiments
- 8+ GB RAM for transformer models

## Health Checks

Health check endpoints:
- Backend: `GET /health`
- Backend (versioned): `GET /api/v1/health`

## Cost Estimates

**Free Tier Setup:**
- Frontend: Vercel (free)
- Backend: Render free tier
- Total: $0/month
- Limitations: CPU only, cold starts, limited hours

**Basic Production:**
- Frontend: Vercel (free or Pro $20/month)
- Backend: DigitalOcean $6-12/month or Render $7/month
- Domain: $12/year
- Total: ~$10-30/month

**Research Production:**
- Frontend: Vercel Pro $20/month
- Backend: DigitalOcean $24/month (4GB)
- Database: Managed PostgreSQL $15/month
- Total: ~$60/month

## Backup Strategy

Items to back up:
- `artifacts/models/` - Trained model checkpoints
- `artifacts/metrics/` - Evaluation results
- Circa dataset (if locally stored)

Recommended: Automated daily backup to cloud storage
