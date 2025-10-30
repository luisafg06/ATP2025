```
tabMeteo1 = [((2022,1,20), 2, 16, 0),((2022,1,21), 1, 13, 0.2), ((2022,1,22), 7, 17, 0.01)]

def medias(tabMeteo):
    res = []
    for dia in tabMeteo1:
        res.append((dia[0],(dia[1]+dia[2])/2))
    return res

print(medias(tabMeteo1))

def guardaTabMeteo(t, fnome):
    f=open(fnome,"w", encoding='utf-8')
    for dia in t:
        f.write(f"{dia[0][0]};{dia[0][1]};{dia[0][2]};{dia[1]};{dia[2]};{dia[3]}\n")
    f.close()
    return

guardaTabMeteo(tabMeteo1, "meteorologia.txt")

def carregaTabMeteo(fnome):
    f=open(fnome,encoding='utf-8')
    res = []
    for linha in f:
        campos=linha.split(";")
        res.append(((int(campos[0]), int(campos[1]),int(campos[2])), float(campos[3]), float(campos[4]), float(campos[5])))
    f.close()
    return res

tabMeteo2 = carregaTabMeteo("meteorologia.txt")
print(len(tabMeteo2), tabMeteo2)

def minMin(tabMeteo):
    minima=tabMeteo[0][1]
    for dia in tabMeteo[1:]:
        if dia[1]<minima:
            minima=dia[1]
    return minima

def minMin2(tabMeteo):
    minima=tabMeteo[1]
    for _,tmin,_,_ in tabMeteo[1:]:
        if tmin<minima:
            minima=tmin
    return minima

print(minMin(tabMeteo2))

def amplTerm(tabMeteo):
    res = []
    for dia in tabMeteo1:
        res.append((dia[0],(dia[2]-dia[1])))
    return res 

print(amplTerm(tabMeteo1))

def maxChuva(tabMeteo):
    max_prec=tabMeteo[0][2]
    max_data=tabMeteo[0][0]
    for data,_,_,prec in tabMeteo[1:]:
        if prec>max_prec:
            max_prec=prec
    return (max_data, max_prec)

print(maxChuva(tabMeteo1))

def diasChuvosos(tabMeteo, p):
    res=[]
    with open(tabMeteo, "r") as t:
        for linha in t:
            ano, mes, dia, tmin, tmax, prec =linha.strip().split(";")
            prec=float(prec)
            if prec>p:
                data= f"{ano}-{mes}-{dia}"
                res.append((data,prec))
    return res
print(diasChuvosos("meteorologia.txt",1.0))

def maxPeriodoCalor(tabMeteo, p):
    max_consecutivos=0
    i=0
    with open(tabMeteo, "r") as t:
        for linha in t:
            ano, mes, dia, tmin, tmax, prec =linha.strip().split(";")
            prec=float(prec)
            if prec<p:
                i=i+1
                if i>max_consecutivos:
                    max_consecutivos=i
            else:
                    i=0
    return max_consecutivos
print(maxPeriodoCalor("meteorologia.txt",1.0))

import matplotlib.pyplot as plt

def extraiTmin(t):
    res=[]
    for _,tmin,_,_ in t:
        res.append(tmin)
    return res

def extraiTmax(t):
    res=[]
    for _,_,tmax,_ in t:
        res.append(tmax)
    return res

def extraiPrecip(t):
    res=[]
    for _,_,_,precip in t:
        res.append(precip)
    return res


def grafTabMeteo(t):

    x1=list(range(1,len(t)+1))
    y1=extraiTmin(t)
    plt.plot(x1,y1,label="Temperatura Mínima")

    x2=list(range(1,len(t)+1))
    y2=extraiTmax(t)
    plt.plot(x2,y2,label="Temperatura Máxima")

    x3=list(range(1,len(t)+1))
    y3=extraiPrecip(t)
    plt.plot(x3,y3,label="Precipitação")

    plt.title('Meteorologia')
    plt.legend()
    plt.show()
    return

grafTabMeteo(tabMeteo2)
