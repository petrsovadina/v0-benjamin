# 🚀 Deployment Guide - Benjamin v0.3

Tento dokument popisuje postup nasazení backendu (FastAPI) a frontendu (Next.js) aplikace Benjamin.

## 📋 Prerekvizity

- **Docker** & **Docker Compose** (pro kontejnerizované nasazení)
- **Node.js 18+** (pro frontend build)
- **Python 3.11+** (pro backend manual run)
- **Supabase Project** (databáze a auth)

## 🛠️ Konfigurace prostředí

Před spuštěním je nutné nastavit proměnné prostředí. Použijte `.env.example` jako šablonu.

### Backend (`backend/.env`)
```bash
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_SERVICE_KEY=...

# Environment configuration (REQUIRED)
ENVIRONMENT=production

# CORS Configuration (REQUIRED in production)
# JSON array of allowed frontend origins
CORS_ORIGINS='["https://app.benjamin.cz","https://benjamin.cz"]'

# ... další proměnné z backend/.env.example
```

**⚠️ IMPORTANT - CORS Security**:
- In production (`ENVIRONMENT=production`), the `CORS_ORIGINS` environment variable **must be set** and **cannot be empty**.
- The application will fail to start if `CORS_ORIGINS` is empty in production to prevent security misconfigurations.
- Always use HTTPS URLs in production (e.g., `https://app.benjamin.cz`).
- Include all frontend domains that need to access the API.
- Format: JSON array of strings, e.g., `CORS_ORIGINS='["https://domain1.com","https://domain2.com"]'`

### Frontend (`.env.local` nebo `.env.production`)
```bash
NEXT_PUBLIC_SUPABASE_URL=https://xyz.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
NEXT_PUBLIC_API_URL=https://api.benjamin.cz # URL vašeho nasazeného backendu
```

---

## 🐳 Nasazení Backendu (Docker)

Backend je připraven pro nasazení v Docker kontejneru.

### 1. Build Image
V adresáři `backend/`:
```bash
docker build -t benjamin-backend:v0.3 .
```

### 2. Spuštění Kontejneru
```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name benjamin-api \
  benjamin-backend:v0.3
```

Aplikace poběží na `http://localhost:8000`.
Health check: `GET http://localhost:8000/health`

---

## 🌐 Nasazení Frontendu (Vercel/Netlify)

Frontend je standardní Next.js aplikace.

### Vercel (Doporučeno)
1. Propojte GitHub repository s Vercelem.
2. V nastavení projektu přidejte Environment Variables z `.env.production`.
3. Deploy proběhne automaticky.

### Docker (Alternativa)
Pro frontend zatím není Dockerfile optimalizován (používá se Vercel), ale lze použít standardní Next.js standalone build.

---

## 🔄 CI/CD Pipeline (Plánováno)
Projekt bude brzy obsahovat GitHub Actions workflow pro automatické testování a build.

## 📝 Poznámky k Produkci
- **Databáze:** Ujistěte se, že jste aplikovali všechny SQL migrace (`supabase/migrations`).
- **Rate Limiting:** V produkci (např. za Nginx/Traefik) může být nutné nastavit `slowapi` na použití `X-Forwarded-For` hlavičky pro správnou detekci IP adresy.

## 🔧 Troubleshooting

### Backend se nespustí v produkci s chybou "CORS_ORIGINS must not be empty"
**Problém**: Application fails to start with error about CORS_ORIGINS being empty.

**Řešení**:
1. Nastavte proměnnou prostředí `CORS_ORIGINS` s platným JSON polem URL adres:
   ```bash
   CORS_ORIGINS='["https://app.benjamin.cz","https://benjamin.cz"]'
   ```
2. Ujistěte se, že hodnota není prázdné pole `[]`.
3. Zkontrolujte, že `ENVIRONMENT=production` je správně nastaveno.

### Frontend nemůže komunikovat s backendem (CORS errors)
**Problém**: Browser console shows CORS errors when frontend tries to call API.

**Řešení**:
1. Ověřte, že frontend URL je v `CORS_ORIGINS` seznamu.
2. Zkontrolujte, že používáte správný protokol (http vs https).
3. Pro development: `CORS_ORIGINS='["http://localhost:3000","http://localhost:5173"]'`
4. Pro production: Vždy používejte HTTPS URL.
