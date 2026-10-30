/* Dati di MeteoPianello (previsioni 3B Meteo e allerte Meteoalarm via AccuWeather). Questo file viene riscritto ogni mattina dall'aggiornamento automatico: la pagina (index.html) non va toccata. */
window.METEO = {
  "updatedAt": "2026-10-30T14:02:00+01:00",
  "sourceNote": "sabato aggiornato alle 13:48, domenica alle 14:02; Ancona sabato alle 7:04",
  "forecasts": {
    "Osimo": {
      "2026-10-31": {"m": {"c": "pioggia", "t": 11, "p": 65, "mm": 2.5, "w": "NO 8"}, "a": {"c": "pioggia e schiarite", "t": 16, "p": 50, "mm": 2, "w": "NO 6"}},
      "2026-11-01": {"m": {"c": "pioggia e schiarite", "t": 9, "p": 90, "mm": 4.2, "w": "NNE 8"}, "a": {"c": "pioggia", "t": 10, "p": 85, "mm": 6.5, "w": "N 9"}}
    },
    "Campofilone": {
      "2026-10-31": {"m": {"c": "pioggia e schiarite", "t": 11, "p": 50, "mm": 0.3, "w": "ONO 11"}, "a": {"c": "nuvoloso", "t": 16, "p": 15, "mm": 0, "w": "NNE 13"}}
    },
    "Ostra": {
      "2026-10-31": {"m": {"c": "pioggia", "t": 10, "p": 60, "mm": 3.8, "w": "NO 11"}, "a": {"c": "nuvoloso", "t": 15, "p": 20, "mm": 0, "w": "N 16"}},
      "2026-11-01": {"m": {"c": "pioggia e schiarite", "t": 9, "p": 70, "mm": 2.8, "w": "N 12"}, "a": {"c": "rovesci", "t": 10, "p": 80, "mm": 13.2, "w": "NNE 9"}}
    },
    "Arcevia": {
      "2026-10-31": {"m": {"c": "pioggia", "t": 8, "p": 80, "mm": 3.1, "w": "N 8"}, "a": {"c": "pioggia e schiarite", "t": 13, "p": 50, "mm": 0.3, "w": "N 16"}},
      "2026-11-01": {"m": {"c": "pioggia e schiarite", "t": 7, "p": 75, "mm": 1, "w": "NNE 16"}, "a": {"c": "pioggia", "t": 9, "p": 95, "mm": 5.4, "w": "NNE 11"}}
    },
    "Sirolo": {
      "2026-11-01": {"m": {"c": "pioggia", "t": 10, "p": 80, "mm": 5.4, "w": "N 10"}, "a": {"c": "pioggia", "t": 13, "p": 80, "mm": 7.8, "w": "NO 10"}}
    },
    "Cingoli": {
      "2026-10-31": {"m": {"c": "nuvoloso", "t": 8, "p": 45, "mm": 0, "w": "NNE 7"}, "a": {"c": "pioggia debole", "t": 12, "p": 50, "mm": 0.9, "w": "N 11"}},
      "2026-11-01": {"m": {"c": "pioggia", "t": 5, "p": 95, "mm": 3.3, "w": "NNO 9"}, "a": {"c": "pioggia", "t": 6, "p": 95, "mm": 5.9, "w": "NNE 8"}}
    },
    "Ancona": {
      "2026-10-31": {"m": {"c": "pioggia e schiarite", "t": 14, "p": 50, "mm": 2.9, "w": "O 5"}, "a": {"c": "nuvoloso", "t": 15, "p": 45, "mm": 0, "w": "NO 3"}},
      "2026-11-01": {"m": {"c": "temporale", "t": 11, "p": 85, "mm": 5.3, "w": "NNE 13"}, "a": {"c": "pioggia", "t": 13, "p": 75, "mm": 4.5, "w": "NNE 14"}}
    },
    "Porto Recanati": {
      "2026-11-01": {"m": {"c": "pioggia", "t": 10, "p": 80, "mm": 5.8, "w": "NE 8"}, "a": {"c": "rovesci", "t": 12, "p": 75, "mm": 9.5, "w": "NO 11"}}
    },
    "Recanati": {
      "2026-10-31": {"m": {"c": "pioggia e schiarite", "t": 10, "p": 50, "mm": 0.3, "w": "NO 10"}, "a": {"c": "pioggia e schiarite", "t": 15, "p": 50, "mm": 0.4, "w": "NO 9"}},
      "2026-11-01": {"m": {"c": "pioggia", "t": 8, "p": 85, "mm": 3.3, "w": "NNO 7"}, "a": {"c": "rovesci", "t": 9, "p": 80, "mm": 9.5, "w": "NO 11"}}
    }
  },
  "alerts": [
    {"t": "Allerta gialla per temporali", "area": "Marche", "s": 1793491200000, "e": 1793573940000, "fino": "domenica 1 novembre"},
    {"t": "Allerta gialla per vento", "area": "Marche, zone costiere", "s": 1793318400000, "e": 1793573940000, "fino": "domenica 1 novembre"}
  ]
};
