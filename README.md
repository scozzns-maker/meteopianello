# MeteoPianello

Non ci sono scuse. Che giro fare in bici nel weekend nelle Marche, in base al meteo (mattina 8–12 e pomeriggio 13–18).

- **Quanti km vuoi fare**: un cursore (la bici) imposta i km massimi. Tra i giri fatti nelle Marche (da Strava) entro quella lunghezza, la pagina propone per ogni giorno quello con il meteo migliore; a meteo pari, quello più vicino ai km scelti.
- **Meteo lungo il percorso**: letto ogni 10 km circa su ogni giro; conta il punto peggiore (pioggia, strade asciutte/umide/bagnate, ghiaccio, vento, freddo). Un giro del mattino che dura più di 5 ore conta anche il meteo del pomeriggio; al pomeriggio si controlla il rientro prima del tramonto. Se i giri non si caricano, la pagina consiglia la località migliore.
- **Mappa**: icone del tempo (sole, nuvole, pioggia, neve, temporale, nebbia) per venti località, da Pesaro a San Benedetto, con il giro consigliato evidenziato. Le previsioni complete per località sono in fondo, a scomparsa.
- **Tema** chiaro o scuro, con il pulsante in alto a destra (all'inizio segue quello del dispositivo).

Pagina: https://scozzns-maker.github.io/meteopianello/

La pagina si aggiorna da sola, senza interventi esterni:

- **Previsioni**: lette da [Open-Meteo](https://open-meteo.com/) nel browser a ogni apertura (dati CC BY 4.0). Modello ICON-2I di ItaliaMeteo-ARPAE (2 km) per i giorni che copre, altrimenti il miglior modello disponibile; probabilità di pioggia dai modelli d'insieme.
- **Allerte**: [Meteoalarm](https://www.meteoalarm.org) per le Marche (Servizio Meteorologico dell'Aeronautica Militare). Il feed non si può leggere dal browser, quindi lo legge GitHub Actions ogni 30 minuti (`.github/workflows/allerte.yml`) e lo salva in `alerts.json`, solo quando cambia o almeno ogni 6 ore.

File:

- `index.html`: la pagina.
- `alerts.json`: allerte Meteoalarm per le Marche, scritte da GitHub Actions.
- `.github/scripts/allerte.py`: lo script che legge Meteoalarm (solo libreria standard di Python).
- `routes.json`: i giri Strava, con tracce semplificate e senza il primo e l'ultimo tratto (da 1 a 2 km, per non mostrare da dove si parte); niente titoli, link né identificativi delle attività.
- `tools/giri.py`: rigenera `routes.json` da un elenco di attività Strava. I giri nuovi non entrano da soli: per aggiungerli va rilanciato con le attività aggiornate.
- `logo.jpg`: il logo.

Nota: GitHub sospende le azioni programmate dopo 60 giorni senza attività nel repository. I salvataggi periodici di `alerts.json` contano come attività; se l'azione risultasse sospesa, si riattiva da Actions → Allerte Meteoalarm → Enable workflow.
