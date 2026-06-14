# ESAME-FINALE-1-ANNO-INFOBASIC


## DESCRIZIONE:
Il seguente progetto simula un gestionale di spedizione che puo essere utilizzato da tre tipi di utenti, ognuno con diverse operazioni:

1) UTENTE: 
    - Accedere alla propria area utente
    - Salvare e visualizzare i pacchi che si vuole vedere

2) CORRIERE:
    - Accedere alla propria area corriere:
    - Visualizzare i pacchi che deve consegnare
    - Visualizzare le tappe da percorrere
    - Cambiare lo stato dei pacchi assegnatigli 

3) ADMIN:
    - Accedere alla propria area admin
    - Visualizzare tutti i pacchi esistenti (anche filtrati)
    - Creare nuovi pacchi (assegnati automaticamente al corriere piu libero)
    - Visualizzare tutti i corrieri
    - Creare un nuovo Corriere  
    
Inoltre nella home del sito tutti possono visualizzare un pacco esistente tramite codice e registrarsi come utente    



## Passaggi per fa funzionare il progetto:

### Installazioni:

1) Aprire "pgadmin" (o un altro programma cheutlizza PostgreSQL) e creare un database chiamato "GESTORE_SPEDIZIONI"

2) Aprire il terminale e creare un ambiente virtuale e attivarlo:
    - python -m venv .venv     (per crearlo)
    - .venv\Scripts\activate.bat  (per avviarlo)

3) Installare i requirements (preferibilmente dentro un venv)
    - pip install -r requirements.txt 

4) Aprire il file "db_config.py" dentro la cartella "persistence" dentro la cartella "Back-end" e cambiare configurazione:
    - "postgresql://[nome_utente]:[password]@localhost:5432/GESTORE_SPEDIZIONI"

5) Cambiare directory su "Front-end" e isntallare tutte le dipendenze:
    - npm i

### Per avviare il Programma:

6) Avviare il file "app.py" dentro la cartella "back-end"

7) Cambiare directory su "Front-end" e avviare il sito con "npm run dev"


