# MeteoPianello

Non ci sono scuse. Meteo del weekend (mattina 8–12 e pomeriggio 13–18) per dieci località delle Marche, con mappa, dettaglio per località e allerte.

La pagina ha due parti:

- **Che giro fare**: per ogni giorno del weekend, il giro (tra quelli fatti nelle Marche, da Strava) con il meteo migliore lungo tutto il percorso, con la scelta tra giri sotto i 50 km e da 50 km in su. Per ogni giro conta il punto del percorso con il meteo peggiore (pioggia, strade asciutte/umide/bagnate, ghiaccio, vento, freddo); al pomeriggio la pagina controlla anche se si rientra prima del tramonto. Se i giri non si caricano, consiglia la località migliore.
- **Mappa**: probabilità di pioggia e vento nelle dieci località, con il giro consigliato evidenziato per il giorno e la fascia scelti. Le previsioni complete per località sono in fondo, a scomparsa.

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
