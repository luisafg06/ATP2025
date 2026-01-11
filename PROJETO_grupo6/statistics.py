def media_ponderada_tempo(serie, tempo_final):
    m = 0.0
    if len(serie) > 0 and float(tempo_final) > 0:
        area = 0.0
        i = 0
        while i < len(serie):
            t0, v0 = serie[i]
            if i + 1 < len(serie):
                t1 = serie[i + 1][0]
            else:
                t1 = float(tempo_final)

            tt0 = float(t0)
            tt1 = float(t1)
            if tt0 < 0.0:
                tt0 = 0.0
            if tt1 < 0.0:
                tt1 = 0.0
            if tt0 > float(tempo_final):
                tt0 = float(tempo_final)
            if tt1 > float(tempo_final):
                tt1 = float(tempo_final)

            if tt1 < tt0:
                tt1 = tt0

            area = area + (tt1 - tt0) * float(v0)
            i = i + 1
        m = area / float(tempo_final)
    return m
