import meteorologia as m
def menu():
    print("\n===MENU Meteorologia===")
    print("1: Calcular médias diárias")
    print("2: Guardar tabela no fichiero")
    print("3: Carregar tabel do ficheiro")
    print("4: Mostrar temperatuira mínima mais baixa")
    print("5: Mostrar dias chuvosos")
    print("6: Mostrar amplitude média diária")
    print("7: Mostrar o dia de máxima precipitação")
    print("8: Mostrar o maior período seco")
    print("9: Mostrar gráfico")
    print("0: Sair")

def main():
    tab=m.tabMeteo1
    ficheiro="meteorologia.txt"
    while True:
        menu()
        op=input("Introduza a opção que deseja executar:")

        if op=="0":
            break
        elif op=="1":
            print(m.medias(tab))
        elif op=="2":
            m.guardaTabMeteo(tab,ficheiro)
            print(f"Tabela guardada em {ficheiro}")
        elif op=="3":
            tab=m.carregaTabMeteo(ficheiro)
            print("Tabela carregada do ficheiro")
        elif op=="4":
            print("A temperatura mais baixa foi:", m.minMin(tab))
        elif op=="5":
            p=float(input("Limite p:"))
            print(m.diasChuvosos(ficheiro,p))
        elif op=="6":
            print(m.amplTerm(tab))
        elif op=="7":
            print(m.maxChuva(tab))
        elif op=="8":
            p=float(input("Limite p:"))
            print("Maior período seco:", m.maxPeriodoCalor(ficheiro,p))
        elif op=="9":
            m.grafTabMeteo(tab)
        else:
            print("Opção inválida!")
if __name__=="__main__":
    main()
