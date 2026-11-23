# MeteoPianello

Non ci sono scuse. Quando e dove fare un giro in bici nel weekend nelle Marche, in base al meteo.

- **Consiglio del giorno**: per sabato e domenica la pagina sceglie da sola l'orario migliore (es. 10:00–13:20) e il giro migliore tra quelli fatti nelle Marche (da Strava). La partenza è dopo l'alba e il rientro prima del tramonto; la durata è quella del giro su Strava più il 15% per le soste. Se i giri non si caricano, consiglia la località migliore per un'uscita di 3 ore.
- **Quanti km vuoi fare**: un cursore (la bici) imposta i km massimi; a meteo pari vince il giro più vicino ai km scelti.
- **Meteo lungo il percorso**: letto ogni 10 km circa su ogni giro, ora per ora; conta il punto peggiore (pioggia, strade asciutte/umide/bagnate, ghiaccio, vento, freddo).
- **Radar**: immagine dal satellite con la pioggia prevista ora per ora (da azzurro a rosso), il vento come scie in movimento e il tempo con temperatura in venti località, da Pesaro a San Benedetto. Parte da solo e si ripete in loop (tranne con "riduci movimento" attivo); si ferma con il tasto pausa o scorrendo il cursore, dalle 6 alle 20 di sabato e domenica; l'orario consigliato è segnato in verde e il giro consigliato è disegnato sulla mappa. Si ingrandisce fino a 8 volte (due dita, doppio tocco, tasti + e −, Ctrl+rotella sul computer) e si sposta trascinando; le immagini dal satellite si caricano alla risoluzione dello schermo, fino a circa 10–15 m per punto. "Guarda sul radar" inquadra il giro consigliato. È una previsione interpolata tra circa 130 punti (località, punti dei giri e una griglia), non il radar in tempo reale.
- **Tema** chiaro o scuro, con il pulsante in alto a destra (all'inizio segue quello del dispositivo).

Pagina: https://scozzns-maker.github.io/meteopianello/

La pagina si aggiorna da sola, senza interventi esterni:

- **Previsioni**: lette da [Open-Meteo](https://open-meteo.com/) nel browser a ogni apertura e poi al massimo una volta l'ora (dati CC BY 4.0). Modello ICON-2I di ItaliaMeteo-ARPAE (2 km) per i giorni che copre, altrimenti il miglior modello disponibile; probabilità di pioggia dai modelli d'insieme.
- **Allerte**: [Meteoalarm](https://www.meteoalarm.org) per le Marche (Servizio Meteorologico dell'Aeronautica Militare). Il feed non si può leggere dal browser, quindi lo legge GitHub Actions ogni 30 minuti (`.github/workflows/allerte.yml`) e lo salva in `alerts.json`, solo quando cambia o almeno ogni 6 ore.

File:

- `index.html`: la pagina.
- `alerts.json`: allerte Meteoalarm per le Marche, scritte da GitHub Actions.
- `.github/scripts/allerte.py`: lo script che legge Meteoalarm (solo libreria standard di Python).
- `routes.json`: i giri Strava, con le tracce quasi complete (un punto ogni 150 m circa, come le dà Strava) ma senza il primo e l'ultimo km, per non mostrare da dove si parte; niente titoli, link né identificativi delle attività.
- `tools/giri.py`: rigenera `routes.json` da un elenco di attività Strava. I giri nuovi non entrano da soli: per aggiungerli va rilanciato con le attività aggiornate.
- `logo.jpg`: il logo.

Immagine satellitare del radar: [Sentinel-2 cloudless - https://s2maps.eu](https://s2maps.eu) by [EOX IT Services GmbH](https://eox.at) (Contains modified Copernicus Sentinel data 2024), libera per uso non commerciale con attribuzione (CC BY-NC-SA 4.0). Se le immagini non si caricano, il radar usa una mappa disegnata (terra, mare e costa).

Nota: GitHub sospende le azioni programmate dopo 60 giorni senza attività nel repository. I salvataggi periodici di `alerts.json` contano come attività; se l'azione risultasse sospesa, si riattiva da Actions → Allerte Meteoalarm → Enable workflow.
