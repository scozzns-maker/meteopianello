#!/usr/bin/env python3
"""Legge il feed Meteoalarm per l'Italia e scrive alerts.json con le allerte delle regioni scelte.

Gira dentro GitHub Actions (.github/workflows/allerte.yml). Usa solo la libreria standard.
Variabili d'ambiente:
  REGIONS  codici EMMA_ID separati da virgola (IT011 Marche, IT010 Umbria, IT013 Abruzzo, IT009 Toscana)
  OUT      file da scrivere (predefinito alerts.json)
Il file viene riscritto solo se le allerte cambiano, oppure ogni 6 ore per segnalare che il controllo è vivo.
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED = 'https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-italy'
REGIONS = [x.strip().upper() for x in os.environ.get('REGIONS', 'IT011').split(',') if x.strip()]
OUT = os.environ.get('OUT', 'alerts.json')
UA = 'meteo-pages-github-action/1.0'
ATOM = '{http://www.w3.org/2005/Atom}'
CAP = '{urn:oasis:names:tc:emergency:cap:1.2}'
HEARTBEAT_H = 6
KEEP_AFTER_EXPIRY_H = 12


def notice(title, msg):
    msg = str(msg).replace('%', '%25').replace('\r', '').replace('\n', '%0A')
    print(f'::notice title={title}::{msg[:3500]}')


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get('Content-Type', '')


def when(s):
    """ISO 8601 -> datetime UTC (None se non leggibile)."""
    if not s:
        return None
    try:
        d = dt.datetime.fromisoformat(s.strip().replace('Z', '+00:00'))
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d.astimezone(dt.timezone.utc)


def zulu(d):
    return d.strftime('%Y-%m-%dT%H:%M:%SZ') if d else None


def txt(el, path):
    x = el.find(path)
    return (x.text or '').strip() if x is not None and x.text else ''


def child(el, name):
    """Testo del primo figlio con quel nome locale, in qualunque namespace (il feed mescola Atom e CAP)."""
    for x in el:
        if x.tag.rsplit('}', 1)[-1] == name:
            return (x.text or '').strip()
    return ''


def clean(s, n=600):
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s[:n]


def read_cap(url, debug=False):
    """Testi del bollettino CAP completo: descrizione italiana e inglese, titolo, zone."""
    out = {'desc': '', 'descEn': '', 'headline': '', 'areas': [], 'zone': ''}
    try:
        raw, ctype = get(url, timeout=20)
    except Exception as e:  # noqa: BLE001
        print(f'CAP non leggibile {url}: {e}', file=sys.stderr)
        return out
    if debug:
        notice('Esempio CAP', f'{ctype}\n{raw[:2500].decode("utf-8", "replace")}')
    body = raw.lstrip()
    if body.startswith(b'{') or body.startswith(b'['):
        try:
            data = json.loads(body)
        except ValueError:
            return out
        infos = []

        def walk(o):
            if isinstance(o, dict):
                if 'description' in o or 'headline' in o:
                    infos.append(o)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)
        for i in infos:
            lang = str(i.get('language', '')).lower()
            key = 'desc' if lang.startswith('it') else 'descEn' if lang.startswith('en') else None
            if key and not out[key]:
                out[key] = clean(i.get('description', ''))
            if lang.startswith('it') and not out['headline']:
                out['headline'] = clean(i.get('headline', ''), 200)
            for a in i.get('area', []) if isinstance(i.get('area'), list) else []:
                d = clean(a.get('areaDesc', ''), 120) if isinstance(a, dict) else ''
                if d and d not in out['areas']:
                    out['areas'].append(d)
        out['zone'] = zone(out['desc']) or zone(out['descEn'])
        return out
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return out
    for info in root.iter(CAP + 'info'):
        lang = txt(info, CAP + 'language').lower()
        desc = clean(txt(info, CAP + 'description'))
        if lang.startswith('it') and not out['desc']:
            out['desc'] = desc
            out['headline'] = clean(txt(info, CAP + 'headline'), 200)
        elif lang.startswith('en') and not out['descEn']:
            out['descEn'] = desc
        elif not lang and not out['desc']:
            out['desc'] = desc
        for area in info.iter(CAP + 'area'):
            d = clean(txt(area, CAP + 'areaDesc'), 120)
            if d and d not in out['areas']:
                out['areas'].append(d)
    out['zone'] = zone(out['desc']) or zone(out['descEn'])
    return out


def zone(desc):
    """Zona scritta in maiuscolo in fondo alla descrizione, prima dell'avvertenza tra parentesi
    (es. «... di moderata intensità COSTE E APPENNINI (AVVERTENZA: ...)» -> «COSTE E APPENNINI»)."""
    head = (desc or '').split('(')[0].strip()
    m = re.search(r"([A-ZÀ-Ý][A-ZÀ-Ý '’,\-/]{2,})$", head)
    return m.group(1).strip(' ,-') if m else ''


def main():
    now = dt.datetime.now(dt.timezone.utc)
    try:
        raw, _ = get(FEED)
        root = ET.fromstring(raw)
    except Exception as e:  # noqa: BLE001
        print(f'Feed Meteoalarm non leggibile: {e}', file=sys.stderr)
        notice('Meteoalarm', f'Feed non leggibile: {e}')
        return 0  # tengo il file precedente: la pagina segnala se è troppo vecchio

    entries = root.findall(ATOM + 'entry')
    latest = None
    picked = {}
    debug_done = os.environ.get('CAP_DEBUG') != '1'
    if not debug_done:
        if entries:
            notice('Prima voce del feed', ET.tostring(entries[0], encoding='unicode')[:3000])
        rows = []
        for en in entries:
            geo = '/'.join(child(g, 'value') for g in en.findall(CAP + 'geocode'))
            rows.append(' | '.join([geo, txt(en, CAP + 'areaDesc'), txt(en, CAP + 'event'), txt(en, CAP + 'onset'),
                                    txt(en, CAP + 'expires'), txt(en, CAP + 'status'), txt(en, CAP + 'message_type')]))
        notice(f'Voci del feed ({len(entries)})', '\n'.join(rows))
        for ln in entries[0].findall(ATOM + 'link') if entries else []:
            if 'cap' in (ln.get('type') or '').lower():
                read_cap(ln.get('href'), debug=True)
                break
        debug_done = True
    for en in entries:
        sent = when(txt(en, CAP + 'sent')) or when(txt(en, ATOM + 'updated'))
        if sent and (latest is None or sent > latest):
            latest = sent
        geo = ''
        for g in en.findall(CAP + 'geocode'):
            if child(g, 'valueName').upper() == 'EMMA_ID':
                geo = child(g, 'value').upper()
        if geo not in REGIONS:
            continue
        status = txt(en, CAP + 'status').lower()
        mtype = txt(en, CAP + 'message_type').lower() or txt(en, CAP + 'msgType').lower()
        if status and status != 'actual':
            continue
        if mtype == 'cancel':
            continue
        onset = when(txt(en, CAP + 'onset')) or when(txt(en, CAP + 'effective'))
        expires = when(txt(en, CAP + 'expires'))
        if not onset or not expires or expires < now - dt.timedelta(hours=KEEP_AFTER_EXPIRY_H):
            continue
        event = txt(en, CAP + 'event')
        if not event or re.match(r'(?i)green', event):
            continue
        cap_url = ''
        for ln in en.findall(ATOM + 'link'):
            if 'cap' in (ln.get('type') or '').lower():
                cap_url = ln.get('href') or ''
        item = {
            'id': txt(en, CAP + 'identifier') or txt(en, ATOM + 'id'),
            'geo': geo,
            'region': txt(en, CAP + 'areaDesc'),
            'event': event,
            'severity': txt(en, CAP + 'severity'),
            'onset': zulu(onset),
            'expires': zulu(expires),
            'sent': zulu(sent),
            'cap': cap_url,
        }
        key = (geo, event.lower(), item['onset'], item['expires'])
        old = picked.get(key)
        if old is None or (item['sent'] or '') > (old['sent'] or ''):
            picked[key] = item

    alerts = sorted(picked.values(), key=lambda a: (a['onset'], a['geo'], a['event']))
    for a in alerts:
        url = a.pop('cap')
        info = read_cap(url, debug=not debug_done) if url else {'desc': '', 'descEn': '', 'headline': '', 'areas': [], 'zone': ''}
        debug_done = True
        a.update(info)

    doc = {
        'source': 'Meteoalarm',
        'issuer': "Servizio Meteorologico dell'Aeronautica Militare",
        'regions': REGIONS,
        'latestSent': zulu(latest),
        'checkedAt': zulu(now),
        'alerts': alerts,
    }

    try:
        with open(OUT, encoding='utf-8') as f:
            prev = json.load(f)
    except (OSError, ValueError):
        prev = None
    if prev and prev.get('alerts') == alerts and prev.get('latestSent') == doc['latestSent'] and prev.get('regions') == REGIONS:
        age = now - (when(prev.get('checkedAt')) or now - dt.timedelta(days=1))
        if age < dt.timedelta(hours=HEARTBEAT_H):
            print(f'Nessuna modifica ({len(alerts)} allerte). Ultimo salvataggio {age} fa.')
            return 0
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'Scritto {OUT}: {len(alerts)} allerte per {",".join(REGIONS)} su {len(entries)} voci del feed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
