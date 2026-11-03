# MeteoPianello

Non ci sono scuse. Meteo del weekend (mattina 8–12 e pomeriggio 13–18) per dieci località delle Marche, con mappa, dettaglio per località e allerte.

In cima, **Dove uscire in bici**: per ogni giorno la località e la fascia migliori per un giro in bici da corsa (meno pioggia, strade asciutte, vento debole, temperature più miti), con lo stato stimato delle strade: asciutte, umide o bagnate in base alla pioggia prevista prima e durante l'uscita, più l'avviso di ghiaccio o brina quando le minime scendono vicino a 0 °C.

Pagina: https://scozzns-maker.github.io/meteopianello/

La pagina si aggiorna da sola, senza interventi esterni:

- **Previsioni**: lette da [Open-Meteo](https://open-meteo.com/) nel browser a ogni apertura (dati CC BY 4.0). Modello ICON-2I di ItaliaMeteo-ARPAE (2 km) per i giorni che copre, altrimenti il miglior modello disponibile; probabilità di pioggia dai modelli d'insieme.
- **Allerte**: [Meteoalarm](https://www.meteoalarm.org) per le Marche (Servizio Meteorologico dell'Aeronautica Militare). Il feed non si può leggere dal browser, quindi lo legge GitHub Actions ogni 30 minuti (`.github/workflows/allerte.yml`) e lo salva in `alerts.json`, solo quando cambia o almeno ogni 6 ore.

File:

- `index.html`: la pagina.
- `alerts.json`: allerte Meteoalarm per le Marche, scritte da GitHub Actions.
- `.github/scripts/allerte.py`: lo script che legge Meteoalarm (solo libreria standard di Python).
- `logo.jpg`: il logo.

Nota: GitHub sospende le azioni programmate dopo 60 giorni senza attività nel repository. I salvataggi periodici di `alerts.json` contano come attività; se l'azione risultasse sospesa, si riattiva da Actions → Allerte Meteoalarm → Enable workflow.
