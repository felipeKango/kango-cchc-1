# kango-cchc-1

Sitio estático de una página que resume la **Clase #1 "IA para la construcción en Chile"** de KangoLab para socios CChC.

- **Stack:** HTML + CSS + JS vanilla en un solo `index.html` (excepción explícita al stack canónico; ver PRD §8).
- **URL objetivo:** https://kangocchc-1.vercel.app

## Estructura

```
index.html          Página completa (9 secciones, formulario, script de leads)
public/img/         Imágenes del deck (logo Kango, relatores, LAB10, Ras Mic)
public/og.png       Imagen Open Graph 1200×630
public/qr.png       QR 1000×1000 apuntando a la URL final (para la lámina de cierre)
content/*.json      Contenido textual extraído del deck Faces h1tkw3pi (fuente de verdad)
vercel.json         Headers de cache para /public
```

## Configuración (constantes públicas en `index.html`)

Al inicio del `<script>` de `index.html`:

```js
var MOCK_MODE = true;        // true: el submit solo hace console.log y muestra confirmación
var SUPABASE_URL = "";       // https://xxxx.supabase.co
var SUPABASE_ANON_KEY = "";  // anon key (pública por diseño; RLS solo permite INSERT)
var WHATSAPP_NUMBER = "";    // 569XXXXXXXX — si está vacío, el botón de WhatsApp se oculta
```

Para pasar a producción: `MOCK_MODE = false` y completar las tres constantes.
El switch de envío vive en **una sola función**: `submitLead()`.

### Tabla Supabase

```sql
create table cchc_leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  nombre text not null,
  empresa text not null,
  cargo text not null,
  whatsapp text not null,
  fuente text default 'cchc_clase_1',
  user_agent text,
  utm_source text
);
alter table cchc_leads enable row level security;
create policy "anon insert only" on cchc_leads
  for insert to anon with check (true);
-- Sin política de select para anon: el formulario escribe, nadie lee desde el cliente.
```

## Desarrollo local

```bash
python3 -m http.server 8080
# abrir http://localhost:8080
```

## Deploy

1. Crear repo GitHub `kango-cchc-1` (cuenta de Felipe), rama `main`, y hacer push.
2. En Vercel: **Import Project** → seleccionar el repo → framework "Other" (estático, sin build).
3. Nombre de proyecto en Vercel: `kangocchc-1` → publica en `https://kangocchc-1.vercel.app`.
4. Dominio propio opcional después: CNAME `cchc.getkango.com` → proyecto Vercel (fuera de alcance del día 1).

## Regenerar OG y QR

```bash
python3 -m venv .venv && .venv/bin/pip install pillow qrcode
.venv/bin/python scripts/gen_assets.py
```

## Notas

- Todas las imágenes se descargaron del CDN del deck y se optimizaron localmente (sin placeholders; las 5 descargas funcionaron).
- Todo el contenido textual proviene del deck (Anexo A del PRD + `content/*.json`). Las cifras que no están en el deck se omitieron.
