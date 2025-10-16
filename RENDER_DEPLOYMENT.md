# 🚀 Deployment Guide - Render

This guide will help you deploy the Knowledge Base Search Engine to Render.

## Prerequisites

- [x] GitHub account with the repository pushed
- [x] Render account (sign up at https://render.com)
- [x] Google Gemini API key

## Step-by-Step Deployment

### Option 1: Deploy Using Render Dashboard (Recommended)

#### 1. Sign Up / Log In to Render
- Go to https://render.com
- Sign up or log in with your GitHub account

#### 2. Create a New Web Service
1. Click **"New +"** button in the dashboard
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect GitHub"** if not already connected
   - Search for your repository: `Shashw1t/Unthinkable`
   - Click **"Connect"**

#### 3. Configure the Web Service

Fill in the following details:

**Basic Settings:**
- **Name:** `knowledge-base-search-engine` (or any name you prefer)
- **Region:** Choose the closest region to you
- **Branch:** `main`
- **Root Directory:** Leave empty
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:** 
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **Free** tier (or paid if you prefer)

#### 4. Add Environment Variables

Click on **"Advanced"** and add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `GOOGLE_API_KEY` | `AIzaSyBowh3JsGa6UlL_Af5LA_tPLvIj37kznDw` | Your Google Gemini API Key |
| `LLM_PROVIDER` | `google` | LLM provider to use |
| `LLM_MODEL` | `models/gemini-2.0-flash` | Gemini model name |
| `SIMILARITY_THRESHOLD` | `0.0` | Minimum similarity for search results |
| `PYTHON_VERSION` | `3.12` | Python version |

**Important:** Keep your API key secure! Consider using Render's secret environment variables.

#### 5. Deploy
1. Click **"Create Web Service"**
2. Render will start building your application
3. Wait 5-10 minutes for the initial build
4. Once deployed, you'll get a URL like: `https://knowledge-base-search-engine.onrender.com`

---

### Option 2: Deploy Using render.yaml (Blueprint)

If you want automated deployment configuration:

1. The `render.yaml` file is already in your repository
2. Go to Render Dashboard → **"Blueprints"**
3. Click **"New Blueprint Instance"**
4. Select your repository
5. Render will read the `render.yaml` and configure everything automatically
6. Add your `GOOGLE_API_KEY` in the environment variables (not in render.yaml for security)
7. Click **"Apply"**

---

## Post-Deployment

### 1. Test Your Deployment

Once deployed, test your application:

1. Visit your Render URL (e.g., `https://your-app.onrender.com`)
2. The frontend should load with the upload and query interface
3. Try uploading a document
4. Ask a question

### 2. Monitor Your Application

- Go to Render Dashboard → Your Service
- Check **"Logs"** tab for any errors
- Monitor **"Metrics"** for performance

### 3. Custom Domain (Optional)

To add a custom domain:
1. Go to your service settings
2. Click **"Custom Domain"**
3. Follow Render's instructions to configure DNS

---

## Important Notes

### Free Tier Limitations

⚠️ **Render Free Tier:**
- Application **sleeps after 15 minutes** of inactivity
- First request after sleep takes **30-60 seconds** to wake up
- **750 hours/month** of runtime

**Solution:** 
- Upgrade to paid tier ($7/month) for always-on service
- Or use a ping service to keep it awake

### File Storage

⚠️ **Ephemeral Storage:**
- Uploaded documents are stored in memory/disk
- **Files are lost on restart** or redeploy
- ChromaDB data is also ephemeral

**Solutions:**
1. **For persistent storage:** Use Render Disks (paid feature)
2. **Or use cloud storage:** AWS S3, Google Cloud Storage, or Cloudflare R2
3. **For this demo:** Ephemeral storage is acceptable

### Environment Variables

Never commit sensitive data like API keys to GitHub! Always use environment variables.

---

## Troubleshooting

### Build Fails

**Issue:** ChromaDB or other dependencies fail to install

**Solution:** 
```bash
# In render.yaml, add system dependencies
buildCommand: |
  apt-get update && apt-get install -y build-essential
  pip install -r requirements.txt
```

### Application Doesn't Start

**Issue:** Port binding error

**Solution:** Make sure start command uses `--host 0.0.0.0 --port $PORT`

### Cold Start (Free Tier)

**Issue:** First request takes too long

**Solution:** 
- Upgrade to paid tier
- Or accept the cold start behavior

### API Key Not Working

**Issue:** Google Gemini API returns errors

**Solution:**
- Check if API key is correctly set in environment variables
- Verify the API key has proper permissions
- Check Render logs for detailed error messages

---

## Updating Your Deployment

When you push changes to GitHub:

1. **Automatic Deploy:** Render auto-deploys on git push (if enabled)
2. **Manual Deploy:** Go to Render Dashboard → Click "Manual Deploy" → Select branch
3. **Check logs** after deployment to ensure no errors

---

## Cost Estimate

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/month | 750 hrs, sleeps after 15min, 512MB RAM |
| **Starter** | $7/month | Always-on, 512MB RAM, custom domain |
| **Standard** | $25/month | 2GB RAM, better performance |

For a demo project, **Free tier is sufficient**.

---

## Next Steps

1. ✅ Deploy to Render using steps above
2. ✅ Test your application
3. ✅ Share the deployed URL
4. ✅ (Optional) Add custom domain
5. ✅ (Optional) Set up monitoring

---

## Support

- **Render Docs:** https://render.com/docs
- **Community:** https://community.render.com
- **Status:** https://status.render.com

**Deployed by:** Shashwat
**Repository:** https://github.com/Shashw1t/Unthinkable

---

**Happy Deploying! 🚀**
