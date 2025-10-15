# Cinema = [Sala]
# Sala = [nlugares, Vendidos, filme]
# nlugares = Int
# filme = String 
# Vendidos = [Int]

sala1 = [150, [55,70,66,23,70], "Soul"]
sala2 = [200, [55,70,66,23,70], "Eternal Sunshine"]
sala3 = [200, [55,70,66,23,70], "Before sunsrise"]
cinema = [sala1, sala2 , sala3]

def listar(cinema):
     print("CARTAZ")
     for sala in cinema:
          print(f"filme: {sala[2]} , exibido na sala: {sala[0]}")

def disponivel(cinema, filme, lugar):
    for sala in cinema:
        if filme == sala[2]:
            if lugar in sala[1]:   
                print(f"o lugar {lugar} para o filme {filme} não está disponível") 
                return False
            else:
                print(f"o lugar {lugar} para o filme {filme} está disponível")
                return True
    print("filme não encontrado")
    return False

def vendebilhete(cinema, filme, lugar):
    for sala in cinema:
        if filme == sala[2]:
            if lugar not in sala[1]:
                sala[1].append(lugar)
                print(f"o seu bilhete com o lugar {lugar} para o filme {filme} foi comprado")
                return cinema
            else:
                print("não pode comprar este bilhete, o lugar já se encontra ocupado") 
                return cinema
    print("filme não encontrado")
    return cinema


def listardisponibilidade(cinema):   
    print("bilhetes disponiveis")
    for sala in cinema:
        lugares_disponiveis = int(sala[0]) - len(sala[1])
        print(f"para {sala[2]} existem {lugares_disponiveis} lugares disponíveis")


def existesala(cinema, nome_sala):
    for sala in cinema:
        if sala[2] == nome_sala:
            print("a sala já existe")
            return True
    print("pode adicionar esta sala")
    return False


def inserirsala(cinema, nome_sala, nlugares, filme):
    if not existesala(cinema, nome_sala):
        nova_sala = [nlugares, [], filme]
        cinema.append(nova_sala)
        print(f"a sala {nome_sala} foi adicionada ao cinema, com o filme {filme} e {nlugares} lugares disponíveis")
    return cinema

print("""Opção 1: consutar o cartaz e o nº de lugares das salas"
Opção 2: verificar a disponibiliade de lugares"
Opção 3: comprar bilhetes"
Opção 4: ver a disponbilidade para o filme"
Opção 5: ver se existe a sala: "
Opção 6: se não existir a sala, adicione! juntamente com o filme e o número de lugares disponíveis"
Opção 0: sair""")

opção = input("Introduza a opção a que quer aceder:")

while opção != "0":
    if opção == "1":
        listar(cinema)
        opção = input("introduza a opção a que quer aceder:")

    elif opção == "2":
        filme = input("nome do filme: ")
        lugar = int(input("lugar:"))
        disponivel(cinema, filme, lugar)
        opção = input("introduza a opção a que quer aceder:")

    elif opção == "3":
        filme = input("nome do filme: ")
        lugar = int(input("lugar:"))
        vendebilhete(cinema, filme, lugar)
        opção = input("introduza a opção a que quer aceder:")

    elif opção == "4":
        listardisponibilidade(cinema)
        opção = input("introduza a opção a que quer aceder:")

    elif opção == "5":
        nome_sala = input("nome da sala: ")
        existesala(cinema, nome_sala)
        opção = input("introduza a opção a que quer aceder:")

    elif opção == "6":
        nome_sala = input("nome da sala: ")
        nlugares = int(input("número de lugares da sala:"))
        filme = input("nome do filme: ")
        inserirsala(cinema, nome_sala, nlugares, filme)
        opção = input("introduza a opção a que quer aceder:")

    elif opção not in ["1","2","3","4","5","6"]:
        print("opção invalida")
        opção = input("introduza a opção a que quer aceder:")

