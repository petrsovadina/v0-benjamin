# Deployment Guide

## Docker Deployment (Production)

The project includes a `docker-compose.prod.yml` file for orchestrating the frontend and backend services in a production environment.

### Prerequisites
- Docker Engine
- Docker Compose

### Configuration
Create a `.env` file in the root directory (or ensure your environment variables are set in your CI/CD or hosting provider).

**Required Environment Variables:**
```env
# Backend & AI
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000 # Or your production backend URL
```

### Running the Application

1.  **Build and Start**:
    ```bash
    docker-compose -f docker-compose.prod.yml up --build -d
    ```

2.  **Verify Status**:
    ```bash
    docker-compose -f docker-compose.prod.yml ps
    ```

3.  **Logs**:
    ```bash
    docker-compose -f docker-compose.prod.yml logs -f
    ```

## Cloud Deployment

### General Strategy
- **Frontend**: Can be deployed to Vercel, Netlify, or as a standalone Docker container.
- **Backend**: Can be deployed to any container orchestration service (AWS ECS, Google Cloud Run, DigitalOcean App Platform) or a VPS.

### Vercel (Frontend only)
1.  Link your GitHub repository.
2.  Configure Environment Variables (`NEXT_PUBLIC_API_URL`).
3.  Deploy.

### VPS (Docker)
1.  Clone the repository to your server.
2.  Set up the `.env` file.
3.  Run the Docker Compose commands listed above.
