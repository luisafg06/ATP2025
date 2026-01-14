#evento = [tempo, tipo, doente]

def e_tempo(e):
    return e[0]


def e_tipo(e):
    return e[1]


def e_doente(e):
    return e[2]


#medico = [id, ocupado, doente_corrente, tempo_ocupado, inicio_consulta]

def m_id(m):
    return m[0]


def m_ocupado(m):
    return m[1]


def mOcupa(m):
    m[1] = not m[1]
    return m


def m_doente_corrente(m):
    return m[2]


def mDoenteCorrente(m, d):
    m[2] = d
    return m


def m_tempo_ocupado(m):
    return m[3]


def mSomaTempoOcupado(m, delta):
    m[3] = m[3] + float(delta)
    return m


def m_inicio_consulta(m):
    return m[4]


def mInicioConsulta(m, t):
    m[4] = float(t)
    return m
