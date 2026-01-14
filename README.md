Recipes MVP – Sustav za razmjenu i pretraživanje recepata

## Opis projekta
Ova aplikacija predstavlja MVP sustava za razmjenu i pretraživanje recepata.  
Sustav omogućuje registraciju korisnika, objavu recepata te njihovo pretraživanje prema različitim kriterijima.

##  Autori
- Moira Grozdanić
- Matea Kenđel

##  1. faza – Osnovna funkcionalnost
U prvoj fazi implementirane su sljedeće funkcionalnosti:

- Registracija korisnika
- Prijava korisnika u sustav
- Objavljivanje recepata koji sadrže:
  - naziv jela
  - popis sastojaka
  - postupak pripreme
  - kategoriju (npr. predjelo, glavno jelo, desert)
- Prikaz korisnikovih i svih objavljenih recepata
- Jednostavno korisničko sučelje (HTML + CSS)

### Tehnologije:
- **Flask** – web poslužitelj
- **MongoDB (NoSQL)** – pohrana korisnika i recepata
- **Docker** 
---

##  Arhitektura sustava
Sustav se sastoji od:
- web aplikacije pokrenute u Docker okruženju (localhost)
- NoSQL baze podataka (MongoDB)
- Traefik load balancera
- replikacije MongoDB baze radi veće pouzdanosti i skalabilnosti

##  2. faza – Napredna pretraga
U drugoj fazi proširene su mogućnosti pretrage:

- Pretraživanje recepata po:
  - sastojcima
  - tekstualnom sadržaju (naziv, opis, postupak)
  - kategoriji
 - Uveden je full-text search sustav – Elasticsearch
- Brža i učinkovitija pretraga nad velikom količinom podataka

## 3. faza – Planirane funkcionalnosti (NIJE IMPLEMENTIRANO)
uključuje:

- Ocjenjivanje recepata (1–5 zvjezdica)
- Pohranu ocjena u postojeću NoSQL bazu
- Praćenje popularnih recepata u stvarnom vremenu (npr. Kafka)
- Keširanje često pregledanih recepata (npr. Redis)


##  Pokretanje aplikacije
Aplikacija se pokreće lokalno pomoću Dockera:

```bash
docker compose up --build
