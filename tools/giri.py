"""Rigenera routes.json dai giri Strava.

Uso: python3 tools/giri.py attivita.json routes.json

attivita.json: elenco di attività Ride come le restituisce il connettore Strava
(search_activities con include_polyline), con name, start_local, location_summary,
summary.distance/elevation_gain/moving_time e reduced_polyline.
Il file di ingresso contiene dati personali: non va messo nel repository.
I titoli delle attività non vengono copiati (servono solo per scartare riscaldamenti e defaticamenti).
Le tracce in uscita sono quasi complete (si tolgono solo i punti allineati, entro una decina di metri) e senza il primo e l'ultimo km.
"""
import sys
import json, math, re, random
def decode(s):
    pts=[];i=lat=lng=0
    while i<len(s):
        for k in (0,1):
            sh=r=0
            while True:
                b=ord(s[i])-63;i+=1;r|=(b&0x1f)<<sh;sh+=5
                if b<0x20:break
            d=~(r>>1) if r&1 else r>>1
            if k==0: lat+=d
            else: lng+=d
        pts.append((lat/1e5,lng/1e5))
    return pts
def hav(a,b):
    R=6371.0;la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]))
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
def cum(p):
    c=[0.0]
    for i in range(1,len(p)):c.append(c[-1]+hav(p[i-1],p[i]))
    return c
TRIM=1.0
npts=0
def at(p,c,d):
    # punto a distanza d (km) lungo la traccia
    for i in range(1,len(p)):
        if c[i]>=d:
            f=(d-c[i-1])/((c[i]-c[i-1]) or 1);return (p[i-1][0]+(p[i][0]-p[i-1][0])*f,p[i-1][1]+(p[i][1]-p[i-1][1])*f)
    return p[-1]
def enc(pts):
    # polilinea codificata alla Google, 5 decimali
    global npts;npts+=len(pts)
    out=[];pa=pb=0
    for la,lo in pts:
        a,b=int(round(la*1e5)),int(round(lo*1e5))
        for v in (a-pa,b-pb):
            v=~(v<<1) if v<0 else v<<1
            while v>=0x20:out.append(chr((0x20|(v&0x1f))+63));v>>=5
            out.append(chr(v+63))
        pa,pb=a,b
    return ''.join(out)
def trim(p,km=1.0):
    c=cum(p);L=c[-1]
    return [q for q,d in zip(p,c) if km<=d<=L-km]
def dp(p,eps):
    if len(p)<3:return p
    a,b=p[0],p[-1];dmax=0;idx=0
    for i in range(1,len(p)-1):
        x,y=p[i];x1,y1=a;x2,y2=b
        dx,dy=x2-x1,y2-y1
        if dx==dy==0:d=math.hypot(x-x1,y-y1)
        else:
            t=max(0,min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy)));d=math.hypot(x-(x1+t*dx),y-(y1+t*dy))
        if d>dmax:dmax=d;idx=i
    if dmax>eps:return dp(p[:idx+1],eps)[:-1]+dp(p[idx:],eps)
    return [a,b]
def cells(p,step=0.005):
    s=set();c=cum(p)
    # resample every ~200 m
    out=[];j=0
    for i in range(1,len(p)):
        seg=hav(p[i-1],p[i]);n=max(1,int(seg/0.2))
        for k in range(n):
            t=k/n;out.append((p[i-1][0]+(p[i][0]-p[i-1][0])*t,p[i-1][1]+(p[i][1]-p[i-1][1])*t))
    for q in out:s.add((round(q[0]/step),round(q[1]/step)))
    return s

def clusterize(acts):
    routes=[]
    for a in acts:
        d=a['summary']['distance']/1000
        if d<15:continue
        p=decode(a['reduced_polyline'])
        if len(p)<5:continue
        routes.append({'name':a['name'],'date':a['start_local'][:10],'km':round(d,1),'up':round(a['summary']['elevation_gain']),
                       'mt':a['summary']['moving_time'],'loc':a.get('location_summary','').replace(', Italy',''),'p':p,'cells':cells(p)})
    routes.sort(key=lambda r:r['date'],reverse=True)
    clusters=[]
    for r in routes:
        best=None;bj=0
        for c in clusters:
            inter=len(r['cells']&c[0]['cells']);un=len(r['cells']|c[0]['cells'])
            j=inter/un if un else 0
            if j>bj:bj=j;best=c
        if best is not None and bj>=0.55 and abs(best[0]['km']-r['km'])<=0.2*max(r['km'],best[0]['km']):best.append(r)
        else:clusters.append([r])
    return clusters
clusters=clusterize(json.load(open(sys.argv[1])))
TOWNS={'Ancona':(43.617,13.517),'Osimo':(43.482,13.488),'San Biagio':(43.455,13.444),'Camerano':(43.528,13.553),'Sirolo':(43.522,13.615),'Numana':(43.512,13.622),
'Loreto':(43.441,13.607),'Recanati':(43.403,13.548),'Porto Recanati':(43.433,13.659),'Castelfidardo':(43.464,13.546),'Filottrano':(43.435,13.352),'Jesi':(43.523,13.243),
'Cingoli':(43.374,13.208),'Apiro':(43.392,13.131),'Arcevia':(43.500,12.941),'Ostra':(43.613,13.158),'Senigallia':(43.716,13.217),'Montemarciano':(43.640,13.309),
'Falconara':(43.627,13.397),'Chiaravalle':(43.600,13.326),'Corinaldo':(43.649,13.048),'Fabriano':(43.336,12.906),'Sassoferrato':(43.432,12.857),'Pergola':(43.563,12.836),
'Fano':(43.839,13.019),'Pesaro':(43.910,12.913),'Gradara':(43.940,12.771),'Urbino':(43.726,12.636),'Fossombrone':(43.689,12.808),'Cagli':(43.547,12.649),'Gubbio':(43.352,12.577),
'Macerata':(43.300,13.453),'Tolentino':(43.209,13.285),'San Severino Marche':(43.229,13.177),'Treia':(43.312,13.312),'Montecassiano':(43.364,13.436),
'Civitanova Marche':(43.307,13.729),'Porto Sant\'Elpidio':(43.257,13.758),'Fermo':(43.160,13.718),'Porto San Giorgio':(43.183,13.794),'Pedaso':(43.098,13.840),
'Campofilone':(43.082,13.825),'Montegiorgio':(43.130,13.538),'Amandola':(42.980,13.356),'Comunanza':(42.957,13.414),'Lago di Gerosa':(42.945,13.395),
'San Benedetto del Tronto':(42.949,13.883),'Grottammare':(42.990,13.867),'Cupra Marittima':(43.025,13.858),'Ripatransone':(43.000,13.762),'Offida':(42.935,13.693),
'Montefiore dell\'Aso':(43.050,13.750),'Monterubbiano':(43.083,13.718),'Staffolo':(43.433,13.186),'Cupramontana':(43.445,13.116),'Serra San Quirico':(43.444,13.019),
'Genga':(43.429,12.934),'Polverigi':(43.531,13.392),'Agugliano':(43.543,13.388),'Offagna':(43.526,13.440),'Santa Maria Nuova':(43.497,13.311),'Montefano':(43.410,13.437),
'Camerata Picena':(43.578,13.351),'Monte San Vito':(43.601,13.271),'Montelupone':(43.344,13.568),'Potenza Picena':(43.366,13.621),'Morrovalle':(43.315,13.582),
'Montecosaro':(43.316,13.635),'Sant\'Elpidio a Mare':(43.230,13.686),'Altidona':(43.107,13.795),'Montegranaro':(43.233,13.632),'Monte Urano':(43.205,13.672)}
def town(q,exclude=()):
    best=min((hav(q,v),k) for k,v in TOWNS.items() if k not in exclude);return best[1],best[0]
CELL=0.08
cellix={};cells=[];out=[]
for c in clusters:
    c=[r for r in c if not re.search(r'warm ?up|cool ?down',r['name'],re.I)]
    if not c:continue
    r=c[0];p=[tuple(x) for x in r['p']]
    # privacy: tolgo esattamente il primo e l'ultimo km (con un punto interpolato a 1 km da ciascun capo)
    c0=cum(p);L0=c0[-1];a=b=TRIM
    tp=[at(p,c0,a)]+[q for q,d in zip(p,c0) if a<d<L0-b]+[at(p,c0,L0-b)]
    if len(tp)<5:continue
    cu=cum(tp);L=cu[-1]
    start=p[0];far=max(p,key=lambda q:hav(start,q))
    st=r['loc'] or town(start)[0]
    ft,fd=town(far,exclude=(st,))
    loop=hav(p[0],p[-1])<3
    label=(st+' – '+ft) if loop else (st+' → '+town(p[-1],exclude=())[0])
    if not loop and town(p[-1])[0]==st: label=st+' – '+ft
    w=[]
    nw=max(4,round(L/10))  # un punto meteo ogni 10 km circa
    for f in [(j+0.5)/nw for j in range(nw)]:
        tgt=f*L;i=next(i for i,d in enumerate(cu) if d>=tgt)
        k=(round(tp[i][0]/CELL),round(tp[i][1]/CELL))
        if k not in cellix:cellix[k]=len(cells);cells.append([round(tp[i][0],2),round(tp[i][1],2)])
        if cellix[k] not in w:w.append(cellix[k])
    sp=dp(tp,0.00012)
    out.append({'id':'r'+str(len(out)),'label':label,'km':r['km'],'up':r['up'],'n':len(c),
                'start':st,'h':round(r['mt']/3600,1),'line':enc(sp),'w':w})
print(len(out),'routes',len(cells),'weather cells',npts,'points')
json.dump({'note':'Giri in bici nelle Marche da Strava: tracce senza il primo e l\'ultimo km; line = polilinea codificata (precisione 1e-5).','trimKm':TRIM,'cells':cells,'routes':out},open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))
import os;print(os.path.getsize(sys.argv[2]),'bytes')
