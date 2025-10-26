

```markdown
# Shift Manager - Starter Repo


Questo repo contiene un "starter" per il progetto Shift Management (FastAPI backend + scheduler + licensing + Docker Compose).


### Cosa c'è qui
- Backend FastAPI con API CRUD minimale per `employees` e `shifts`.
- Un algoritmo greedy semplice in `scheduler.py` che genera un planning per un periodo (settimana/mese).
- Tool per generare e verificare licenze basate su firma RSA (file JWT-like semplice), per la modalità "self".
- Docker Compose per sviluppo e test locale.


### Come provarlo (locale / simulate "VPS" o "mini-PC")
1. Assicurati di avere `docker` e `docker-compose`.
2. Dal folder `shift-manager/` esegui:


```bash
docker compose up --build
```


Questo creerà due servizi principali:
- `backend` (FastAPI + Uvicorn)
- `db` (Postgres)


3. Apri http://localhost:8000/docs per vedere le API OpenAPI/Swagger.


### Generare una licenza di prova
```bash
python3 license_tools/generate_license.py --customer "ristorante-roma" --out license.json
```


Copia `license.json` nel container backend o nella cartella `backend/app` per testare la verifica licenza.


### Esempi rapidi
- Endpoint di esempio per generare schedule: `POST /generate_schedule` con payload JSON (vedi `api_examples.sh`).


### Cosa posso aggiungere dopo
- Frontend React completo
- Algoritmo OR-Tools
- Installer per mini-PC (Raspberry) + immagine
- Sistema di check periodico verso server licenze


```
```


---