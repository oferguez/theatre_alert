# Culture Officer - Automated Cultural Event Curator

The Culture Officer is a serverless Google Cloud Function that queries OpenAI's GPT to discover and curate relevant cultural events happening in London. It runs on a scheduled basis and emails personalized recommendations based on specific taste preferences.

## 🎭 What It Does

The Culture Officer is designed as a cultural curator for users interested in:
- Queer, emotionally raw, and politically charged cinema
- Offbeat, sharp, and socially conscious content
- Bold, experimental, and activist-led art
- Independent film screenings and festivals
- Political or experimental talks and lectures
- Anything unusual, challenging, poetic, or thought-provoking

### Key Features
- **AI-Powered Curation**: Uses OpenAI GPT-4o to discover and filter cultural events
- **Personalized Recommendations**: Tailored to specific artistic and cultural preferences
- **Automated Scheduling**: Runs twice weekly (Monday & Friday at 10:00 AM)
- **Email Delivery**: Sends beautifully formatted HTML reports via Mailjet
- **Date-Aware**: Focuses on events in the next 10 days from execution
- **Debug Mode**: Saves raw GPT responses for development purposes

## 🏗️ Architecture

```
Cloud Scheduler ---> Cloud Function ---> OpenAI API
  (Cron Jobs)        (culture_officer)     (GPT-4o)
                            |
                            v
                     HTML Formatter ---> Mailjet API
                      (Beautifier)       (Email Sender)
```

## 📋 Configuration

### Environment Variables

#### Required (Sensitive - stored in Google Secret Manager)
- `OPENAI_API_KEY`: OpenAI API key for GPT access
- `MAILJET_API_KEY`: Mailjet API key for email sending
- `MAILJET_SECRET_KEY`: Mailjet secret key for authentication

#### Required (Non-sensitive - stored in container)
- `EMAIL_RECIPIENT`: Primary recipient email address
- `EMAIL_SENDER`: Sender email address (must be verified in Mailjet)

#### Optional
- `EMAIL_RECIPIENT_2`: Secondary recipient email address
- `OPENAI_MODEL`: OpenAI model to use (default: "gpt-4o")
- `OPENAI_MAX_TOKENS`: Maximum tokens for GPT response (default: 1000)
- `OPENAI_TEMPERATURE`: GPT creativity level (default: 0.7)
- `OPENAI_TOP_P`: GPT nucleus sampling parameter (default: 1.0)
- `DEBUG`: Enable debug mode to save GPT responses (default: false)
- `CULTURE_OFFICER_USER_PROMPT`: Custom user prompt for GPT (optional)

### Configuration Files

#### `.env.local` (Local Development)
Contains all environment variables including sensitive API keys for local testing.

#### `.env.docker` (Containerization)
Contains only non-sensitive environment variables. Sensitive keys are passed at runtime.

## 🐳 Containerization

### Dockerfile Features
- **Base Image**: Python 3.12 slim for optimal performance
- **Multi-stage Configuration**: Separates build dependencies from runtime
- **Environment Hardcoding**: Non-sensitive variables baked into image
- **Test Integration**: Runs unit tests during build process
- **Security**: No sensitive data stored in image layers

### Build Process
```bash
# Non-sensitive environment variables are hardcoded in env.docker file
ENV EMAIL_RECIPIENT=aeyal.gross@gmail.com
ENV EMAIL_RECIPIENT_2=nachush2000@gmil.com
ENV EMAIL_SENDER=guez.ofer@gmail.com
ENV DEBUG=true

# Sensitive API keys passed, when debugging locally, at runtime via -e flags
```

## 🧪 Local Testing

### Prerequisites
Create .env.local with all required environment variables, including API keys 

### Automated Testing Script
Use the provided shell script for easy local testing:

```bash
./run_docker_local.sh
```

**What the script does:**
1. Loads API keys from `.env.local`
2. Builds Docker image with non-sensitive environment variables
3. Runs unit tests on that image
4. Stops any existing containers
5. Starts new container with API keys passed as environment variables
6. Waits 5 seconds for startup
7. Automatically triggers the function endpoint
8. Shows response and provides log access commands

### Manual Testing Options

#### Option 1: Functions Framework (Local)
```bash
# Load environment variables
export $(cat .env.local | xargs)
# Start functions framework
functions-framework --target=handler --source=culture_officer.py --debug
# Test endpoint
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{}'
```

#### Option 2: Direct Docker Commands
```bash
# Build image
docker build -t culture-officer .

# Run with API keys
docker run -p 8080:8080 \
  -e MAILJET_API_KEY="your-key" \
  -e MAILJET_SECRET_KEY="your-secret" \
  -e OPENAI_API_KEY="your-openai-key" \
  culture-officer

# Test endpoint
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{}'
```

#### Option 3: Unit Tests
```bash
# Run unit tests
python -m pytest tests/unittests/
python -m pytest tests/inttests/
```

## ☁️ Google Cloud Deployment

### Deployment Pipeline
The application uses Google Cloud Build with the following pipeline:

### Useful links:
1. [Build page](https://console.cloud.google.com/cloud-build/builds?referrer=search&hl=en-au&inv=1&invt=Ab50Sg&project=theatre-alert)
2. [Schdeule page](https://console.cloud.google.com/cloudscheduler/jobs/edit/europe-west2/trigger-culture-officer?hl=en-au&inv=1&invt=Ab50Sg&project=theatre-alert)

#### Build Steps:
1. **Build**: Creates Docker image with commit SHA tag 
2. **Push**: Pushes image to Google Artifact Registry
3. **Deploy**: Updates Cloud Run service with new image
4. **Schedule**: Creates/updates Cloud Scheduler job

### Cloud Build Configuration
```yaml
# Build and push Docker image
- name: gcr.io/cloud-builders/docker
  args: [build, --no-cache, -t, IMAGE_URL, ., -f, Dockerfile]

# Deploy to Cloud Run with secrets
- name: gcr.io/google.com/cloudsdktool/cloud-sdk:slim
  args:
    - run services update culture-officer
    - --image=IMAGE_URL
    - --update-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest
    - --update-secrets=MAILJET_API_KEY=MAILJET_API_KEY:latest
    - --update-secrets=MAILJET_SECRET_KEY=MAILJET_SECRET_KEY:latest
```

### Secrets Management
Sensitive environment variables are stored in Google Secret Manager:
- `OPENAI_API_KEY`: Latest version mounted to Cloud Run
- `MAILJET_API_KEY`: Latest version mounted to Cloud Run  
- `MAILJET_SECRET_KEY`: Latest version mounted to Cloud Run

Non-sensitive variables are baked into the Docker image during build.

### Deployment Configuration
- **Project**: `theatre-alert`
- **Service Name**: `culture-officer`
- **Region**: `europe-west1`
- **Platform**: Cloud Run (managed)

## ⏰ Cloud Scheduler Configuration

### Schedule Details
- **Job Name**: `culture-officer-scheduler`
- **Schedule**: `0 10 * * 1,5` (Monday and Friday at 10:00 AM UTC)
- **Target**: HTTPS endpoint of the deployed Cloud Run service
- **Method**: POST request
- **Authentication**: OIDC service account authentication

### Schedule Customization
The CRON schedule can be customized via the `_CRON_SCHEDULE` substitution variable:
- Current: `"0 10 * * 1,5"` (Mon/Fri at 10 AM)
- Daily: `"0 10 * * *"` (Every day at 10 AM)
- Weekly: `"0 10 * * 1"` (Mondays only at 10 AM)

## 🔧 Development

### Code Structure
```
culture_officer.py              # Main function handler
├── handler()                   # Cloud Function entry point
├── call_gpt()                 # OpenAI API integration
└── send_email()               # Mailjet email sending

config.py                      # Configuration management
├── Config class               # Singleton configuration loader
├── load_and_validate()       # Environment variable validation
└── _validate()               # Required field checking

cultural_officer_system_prompt.py  # GPT system prompt
├── get_system_prompt()        # Dynamic prompt generation
└── system_prompt              # Exported prompt string

format_culture_html.py         # HTML formatting
└── parse_and_format_culture_html()  # GPT response to HTML
```

### Adding New Features
1. **Update configuration** in `config.py` for new environment variables
2. **Modify system prompt** in `cultural_officer_system_prompt.py` for different curation
3. **Enhance HTML formatting** in `format_culture_html.py` for better emails
4. **Update tests** in `tests/` directory
5. **Rebuild and test** using `./run_docker_local.sh`

### Debugging
- Enable `DEBUG=true` to save raw GPT responses to `culture_officer_debug.txt`
- Check Cloud Function logs via Google Cloud Console
- Use `docker logs culture-officer-container` for local debugging

## 🚀 Quick Start

1. **Set up environment**:
   Edit .env.local with your API keys

2. **Test locally**:
   ```bash
   chmod +x run_docker_local.sh
   ./run_docker_local.sh
   ```

3. **Deploy to Google Cloud**:
   - Push to repository with Cloud Build trigger
   - Or use `gcloud run deploy` manually

4. **Verify scheduler**:
   ```bash
   gcloud scheduler jobs list --location=europe-west1
   ```

## 📚 Dependencies

- `functions-framework`: Google Cloud Functions runtime
- `mailjet-rest`: Email sending via Mailjet API
- `requests`: HTTP requests to OpenAI API

## 🛡️ Security Best Practices

- ✅ Sensitive API keys stored in Google Secret Manager
- ✅ No secrets in Docker image layers
- ✅ OIDC authentication for Cloud Scheduler
- ✅ Minimal container with only required dependencies
- ✅ Input validation in configuration loader
- ✅ Structured logging for audit trails

---

*This is a learning project demonstrating serverless functions running on floating cloud infrastructure with proper security, containerization, and automation practices.*