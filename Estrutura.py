import random
import time
import os  # Importado para poder limpar o terminal


# Valores constantes 

UMIDADE_MAX = 100
UMIDADE_MIN = 0
ESTRESSE_MAX = 100
ESTRESSE_MIN = 0

TEMPERATURA_LIMITE_CALOR = 30
UMIDADE_SECA_EXTREMA = 20
UMIDADE_ALAGAMENTO = 90

TURNO_REVELACAO = 5
PLANTAS_PARA_VITORIA = 15
BICHOS_PARA_VITORIA = 8


# Funções auxiliares

def limpar_tela():
    # Limpa o terminal dependendo do sistema operacional
    os.system('cls' if os.name == 'nt' else 'clear')


def limitar(valor, minimo, maximo):
    # Garante que o valor não passe do máximo nem fique abaixo do mínimo
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def mostrar_introducao():
    # Tela inicial: mostra a história e pede o nome do jogador
    limpar_tela()
    print(" A DESCOBERTA ")
    print("-" * 50)
    nome = input("Digite o seu nome para começar a aventura: ").strip()
    if not nome:
        nome = "Flora"  # Nome padrão caso o jogador aperte ENTER sem digitar nada

    print("-" * 50)
    print(f"{nome} encontra uma caixinha de música de bailarina quebrada em um beco antigo...")
    print("Ao abri-la, um brilho dourado a toca. À noite, seu quarto some e ela acorda")
    print("em um lugar vibrante, cercado por fadas e pequenas criaturas: os Lumines,")
    print("alguns seres do nosso mundo em sua versão mágica. Ela estava em uma pequena cabana quando foi até a janela,")
    print("olhou para fora e se maravilhou.")
    print(f"Para proteger esse novo mundo e achar respostas, {nome} precisa controlar a natureza!")
    print("-" * 50)
    input("\nPressione ENTER para iniciar o equilíbrio do Terrário...\n")

    return nome


def mostrar_status(nome_jogador, turno, temperatura, umidade, energia_solar, plantas, bichos, estresse_lumines):
    # Mostra o status do terrário e o menu de ações do turno
    limpar_tela()  # Limpa o turno anterior para não poluir a vista

    print(f"\n========== TURNOS NO TERRÁRIO: DIA {turno} ==========")
    print(f"Status do Ambiente: Temperatura: {temperatura}C | Umidade: {umidade}% | Energia Solar: {energia_solar}")
    print(f"População Atual:  Plantas: {len(plantas)} | Bichos: {len(bichos)} (Estresse Geral: {estresse_lumines}%)")
    print("-" * 50)

    print(f"\nO que {nome_jogador} fará neste turno?")
    print("1 - Regar o terrário (+20 Umidade, -5 Temperatura)")
    print("2 - Conjurar Luz Solar (+10 Temperatura, +15 Energia Solar, -20 Umidade)")
    print("3 - Conversar e acalmar os Lumines (-30% Estresse, ajuda a combater pragas)")
    print("4 - Usar Magia Solar no solo (-25 Energia Solar, +3 Plantas Novas)")
    print("5 - Deixar a natureza agir por si mesma")

    print("\n" + "-" * 50)
    opcao = input("Escolha uma ação (1/2/3/4/5): ")
    print("-" * 50)

    return opcao


def executar_acao(opcao, nome_jogador, umidade, temperatura, energia_solar, estresse_lumines, plantas):
    # Aplica os efeitos da ação escolhida pelo jogador
    protecao_contra_pragas = False  # Resetando a proteção contra pragas a cada turno

    if opcao == "1":
        umidade = limitar(umidade + 20, UMIDADE_MIN, UMIDADE_MAX)
        temperatura = temperatura - 5
        print(f"[ACAO] {nome_jogador} usou seus poderes de água para regar as plantas.")

    elif opcao == "2":
        temperatura = temperatura + 10
        energia_solar = energia_solar + 15
        umidade = limitar(umidade - 10, UMIDADE_MIN, UMIDADE_MAX)
        print(f"[ACAO] Uma brisa de calor e luz dourada preenche o terrário por comando de {nome_jogador}.")

    elif opcao == "3":
        estresse_lumines = limitar(estresse_lumines - 30, ESTRESSE_MIN, ESTRESSE_MAX)
        protecao_contra_pragas = True
        print(f"[ACAO] {nome_jogador} conversou com os Lumines. Eles estão felizes e alertas para proteger o jardim!")

    elif opcao == "4":
        if energia_solar >= 25:
            energia_solar = energia_solar - 25
            for _ in range(3):
                plantas.append("Planta Mágica")
            print(f"[ACAO] {nome_jogador} usou sua magia para fazer brotos mágicos crescerem.")
        else:
            print("[AVISO] Energia solar insuficiente. A natureza agiu sozinha.")

    else:
        print(f"[ACAO] {nome_jogador} decidiu apenas observar o fluxo natural hoje.")

    return umidade, temperatura, energia_solar, estresse_lumines, protecao_contra_pragas


def aplicar_efeito_calor(temperatura, umidade, estresse_lumines):
    # Calor: se a temperatura passar do limite, a umidade cai e o estresse sobe
    if temperatura > TEMPERATURA_LIMITE_CALOR:
        print("\n[ALERTA CLIMA] A magia solar está evaporando a água rapidamente!")
        umidade = limitar(umidade - 15, UMIDADE_MIN, UMIDADE_MAX)
        estresse_lumines = limitar(estresse_lumines + 10, ESTRESSE_MIN, ESTRESSE_MAX)

    return umidade, estresse_lumines


def aplicar_evento_aleatorio(umidade, estresse_lumines, plantas, bichos, protecao_contra_pragas):
    # Eventos e pragas aleatórios do dia
    evento = random.choice(["Chuva Forte", "Onda de Calor", "Praga", "Ventania", "Nenhum"])

    if evento == "Chuva Forte":
        print("\n[EVENTO] Chuva Forte desaba no terrário!")
        umidade = limitar(umidade + 40, UMIDADE_MIN, UMIDADE_MAX)

        if umidade >= UMIDADE_ALAGAMENTO:
            print("[CONSEQUENCIA] A umidade está alta demais! Algumas plantas se afogaram.")
            if len(plantas) > 3:
                for _ in range(3):
                    plantas.pop()
            else:
                plantas = []

    elif evento == "Onda de Calor":
        print("\n[EVENTO] Uma Onda de Calor atinge o terrário!")
        umidade = limitar(umidade - 30, UMIDADE_MIN, UMIDADE_MAX)
        estresse_lumines = limitar(estresse_lumines + 20, ESTRESSE_MIN, ESTRESSE_MAX)
        print("[CONSEQUENCIA] Os bichos estão exaustos e muito estressados para se reproduzir.")

    elif evento == "Praga":
        print("\n[EVENTO] Uma praga de insetos invadiu!")
        if protecao_contra_pragas:
            print("[DEFESA] Como os Lumines foram cuidados, eles caçaram os insetos e protegeram as plantas!")
        else:
            novas_plantas = []
            for p in plantas:
                if random.random() > 0.30:
                    novas_plantas.append(p)
            plantas = novas_plantas
            print("[CONSEQUENCIA] A praga consumiu algumas plantas do terrário.")

    elif evento == "Ventania":
        print("\n[EVENTO] Ventos fortes sopram pelo vidro!")
        if 0 < len(plantas) < 20:
            print("[CONSEQUENCIA] As sementes se espalharam! Novas plantas vão crescer.")
            plantas.append("Planta Nova")
        if len(bichos) > 0:
            print("[CONSEQUENCIA] A casa de um Lumine foi destruída! O estresse deles aumentou.")
            estresse_lumines = limitar(estresse_lumines + 25, ESTRESSE_MIN, ESTRESSE_MAX)

    return umidade, estresse_lumines, plantas, bichos, evento


def aplicar_seca_extrema(umidade, plantas):
    # Seca extrema: se a umidade ficar muito baixa, parte das plantas murcha
    if umidade < UMIDADE_SECA_EXTREMA:
        print("\n[AVISO] Seca extrema! As plantas estão murchando...")
        plantas_sobreviventes = []
        for p in plantas:
            if random.random() > 0.5:
                plantas_sobreviventes.append(p)
        plantas = plantas_sobreviventes

    return plantas


def aplicar_ciclo_de_vida(plantas, bichos, estresse_lumines, evento):
    # Ciclo de vida: fome (sem plantas) e nascimento de novos Lumines
    if len(plantas) == 0:
        print("\n[PERIGO] FOME: Não há plantas! Os bichos estão famintos.")
        bichos_sobreviventes = []
        for b in bichos:
            if random.random() > 0.8:
                bichos_sobreviventes.append(b)
        bichos = bichos_sobreviventes
    else:
        if evento != "Onda de Calor" and len(bichos) > 0 and len(plantas) > 5:
            if estresse_lumines < 50:
                bichos.append("Lumine Filhote")
                print("\n[VIDA] O ambiente está calmo e seguro. Um novo Lumine nasceu!")
            else:
                print("\n[VIDA] Os Lumines estão estressados demais para trazer novos filhotes ao mundo.")

    return bichos


def mostrar_revelacao(nome_jogador, turno):
    # Revelação do enredo: acontece uma única vez, no turno definido por TURNO_REVELACAO
    if turno == TURNO_REVELACAO:
        print("\n" + "=" * 60)
        print(" O QUE?... ")
        print(f"O céu do terrário treme violentamente. {nome_jogador} olha para cima e vê...")
        print("Dois olhos humanos GIGANTESCOS observando através das nuvens no vidro!")
        print("Vocês estão presos em um terrário na mesa de uma Bruxa Má!")
        print("Para libertar a todos, você deve cultivar a 'Flor da Luz Pureza'!")
        print("Requisito para a Flor: Manter 15 plantas e 8 bichos vivos simultaneamente.")
        print("═" * 60 + "\n")
        input("Pressione ENTER para continuar após esta revelação...")


def verificar_fim_de_jogo(nome_jogador, turno, plantas, bichos):
    # Condições de vitória ou derrota
    # Retorna True se o jogo deve terminar, False se ainda continua
    if len(bichos) == 0 and len(plantas) == 0:
        print("\n" + "=" * 50)
        print("FIM DE JOGO: Todo o ecossistema foi extinto. A bruxa descartou o terrário...")
        print("=" * 50)
        return True

    if turno > TURNO_REVELACAO and len(plantas) >= PLANTAS_PARA_VITORIA and len(bichos) >= BICHOS_PARA_VITORIA:
        print("\n" + "=" * 50)
        print(" VITÓRIA INDISCUTÍVEL! ")
        print("Uma luz radiante emana do centro do ecossistema... Nasceu a Flor da Luz Pureza!")
        print(f"{nome_jogador} ergue a flor em direção ao topo do vidro. A Bruxa Má a toca e começa a chorar.")
        print("O coração seco da Bruxa se enche de amor. O feitiço se quebra!")
        print(f"Ela abre o terrário, liberta {nome_jogador} e todas as criaturinhas. FIM FELIZ!")
        print("=" * 50)
        return True

    return False


# Código principal

def main():
    # Introdução e coleta do nome
    nome_jogador = mostrar_introducao()

    # Quantidades iniciais
    umidade = 50
    temperatura = 25
    energia_solar = 60
    turno = 1
    jogo_ativo = True

    estresse_lumines = 0

    plantas = ["Planta" for _ in range(10)]
    bichos = ["Lumine" for _ in range(5)]

    while jogo_ativo:
        # Mostra o status atual e pede a ação do jogador
        opcao = mostrar_status(
            nome_jogador, turno, temperatura, umidade,
            energia_solar, plantas, bichos, estresse_lumines
        )

        print("\n" + "~" * 60)
        print(f"  ACONTECIMENTOS DO DIA {turno}:")
        print("~" * 60 + "\n")

        # Ação do jogador
        umidade, temperatura, energia_solar, estresse_lumines, protecao_contra_pragas = executar_acao(
            opcao, nome_jogador, umidade, temperatura, energia_solar, estresse_lumines, plantas
        )

        # Efeito do calor extremo
        umidade, estresse_lumines = aplicar_efeito_calor(temperatura, umidade, estresse_lumines)

        # Evento aleatório do dia
        umidade, estresse_lumines, plantas, bichos, evento = aplicar_evento_aleatorio(
            umidade, estresse_lumines, plantas, bichos, protecao_contra_pragas
        )

        # Seca extrema
        plantas = aplicar_seca_extrema(umidade, plantas)

        # Ciclo de vida (fome e nascimento)
        bichos = aplicar_ciclo_de_vida(plantas, bichos, estresse_lumines, evento)

        # Revelação do enredo
        mostrar_revelacao(nome_jogador, turno)

        # Condições de vitória ou derrota
        if verificar_fim_de_jogo(nome_jogador, turno, plantas, bichos):
            jogo_ativo = False

        print("\n" + "~" * 60)

        # Avançar turno se o jogo ainda continuar
        if jogo_ativo:
            turno = turno + 1
            print("\n")
            input("Pressione ENTER para passar para o próximo dia...")


if __name__ == "__main__":
    main()
    
