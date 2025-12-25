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
# ... další proměnné z backend/.env.example
```

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
