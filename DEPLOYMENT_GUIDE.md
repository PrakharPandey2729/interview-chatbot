# 🚀 Google Cloud Run Deployment Guide

## Prerequisites

### 1. Install Google Cloud CLI

**Windows:**

- Download from: https://cloud.google.com/sdk/docs/install
- Or use chocolatey: `choco install gcloudsdk`

**macOS:**

```bash
brew install --cask google-cloud-sdk
```

**Linux:**

```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 2. Setup Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or select existing one)
3. **IMPORTANT:** Enable billing (required for Cloud Run)
4. Note your `PROJECT_ID` - you'll need this!

### 3. Authentication

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR-PROJECT-ID

# Verify setup
gcloud config list
```

## Get API Keys

### 1. OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create account if needed
3. Generate new API key
4. **IMPORTANT:** Copy and save the key securely

### 2. Test Your Keys Locally (Optional)

Create a `.env` file in your project directory:

```bash
OPENAI_API_KEY=your-openai-api-key
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
BACKEND_URL=http://127.0.0.1:8000
```

## Deploy to Google Cloud Run

1. **Enable required APIs:**

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

2. **Build and deploy:**

```bash
# Build container
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/interview-chatbot

# Deploy to Cloud Run
gcloud run deploy interview-chatbot \
  --image gcr.io/YOUR-PROJECT-ID/interview-chatbot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --set-env-vars "OPENAI_API_KEY=your-key,MONGO_URI=your-mongo-uri,BACKEND_URL=http://localhost:8000"
```

## After Deployment

1. **Get your app URL:**

```bash
gcloud run services describe interview-chatbot --platform managed --region us-central1 --format 'value(status.url)'
```

2. **Test your deployment:**
   - Visit the URL provided
   - Try creating an account and starting an interview

## Troubleshooting

### Common Issues:

1. **Build fails:**

   - Check that all files are in the directory
   - Ensure Docker is running locally (if testing)

2. **MongoDB connection fails:**

   - Verify connection string format
   - Check that IP `0.0.0.0/0` is whitelisted in MongoDB Atlas
   - Ensure database user has correct permissions

3. **OpenAI API errors:**

   - Verify API key is correct
   - Check OpenAI account has credits/billing set up

4. **Environment variables not set:**
   - Use `gcloud run services update` to modify env vars
   ```bash
   gcloud run services update interview-chatbot \
     --region us-central1 \
     --set-env-vars "OPENAI_API_KEY=new-key"
   ```

### View Logs:

```bash
gcloud logs tail --service interview-chatbot
```

**The Rick Sanchez Interview Chatbot should now be live on Google Cloud!**
