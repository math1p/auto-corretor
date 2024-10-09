import os

def menu():
    print("\nEscolha uma das opções:")
    print("1. Criar arquivo")
    print("2. Abrir arquivo")
    print("3. Inserir resposta")
    print("4. Comparar com gabarito")
    print("5. Sair")
    
    opcao = input("Digite o número da opção: ")
    return opcao

def criar_arquivo(nome_arquivo):
    # Pergunta se o modelo é ENEM e define o número de questões
    modelo_enem = input("Modelo ENEM? (s/n): ").lower() == 's'
    if modelo_enem:
        dia_enem = input("Dia 1 ou 2? (1/2): ")
        if dia_enem == "1":
            print("As primeiras 45 questões (1 - 45) serão de Linguagens e as últimas de Ciências Humanas.")
            start = 1
            num_questoes = 90
        elif dia_enem == "2":
            print("As primeiras 45 questões (90 - 135) serão de Ciências da Natureza e as últimas de Matemática.")
            start = 91
            num_questoes = 180
    else:
        num_questoes = int(input("Digite o número de questões: "))

    # Caminho do arquivo no diretório atual
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

    # Cria o arquivo com o layout de questões
    with open(caminho_arquivo, 'w') as f:
        for i in range(start, num_questoes + 1):
            f.write(f"{i} - \n")  # Formato: número da questão - (inicialmente vazio)

    print(f"Arquivo '{nome_arquivo}' criado, finalizando na questão {num_questoes}.")

def abrir_arquivo(nome_arquivo):
    # Verifica se o arquivo existe no diretório atual
    caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
    try:
        with open(caminho_arquivo, 'r') as f:
            conteudo = f.readlines()
            if conteudo:
                for linha in conteudo:
                    print(linha.strip())
            else:
                print(f"Arquivo '{nome_arquivo}' está vazio.")
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")

def inserir_resposta(nome_arquivo):
    alternativas_permitidas = ["A", "B", "C", "D", "E"]
    numero_questao = input("Número da questão: ")
    while True:
        alternativa = input("Alternativa: ").upper()
        if alternativa in alternativas_permitidas:
            break
        else:
            print("Alternativa inválida. A Resposta deve ser uma das alternativas: A, B, C, D ou E.")

    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    with open(nome_arquivo, "w") as arquivo:
        alterado = False
        for linha in linhas:
            #print(f"Lendo linha: '{linha.strip()}'")  # Mostra a linha que está sendo lida
            if linha.startswith(f"{numero_questao} -"):
                partes = linha.strip().split(" - ")
                if len(partes) == 2:
                    num_questao, resposta = partes
                else:
                    num_questao = partes[0]
                    resposta = None

                if resposta:
                    print(f"Questão {num_questao} já possui a alternativa {resposta}. Será atualizada para {alternativa}.")
                else:
                    print(f"Questão {num_questao} não possui resposta. Será atualizada para {alternativa}.")

                # Atualiza a linha com a nova resposta, garantindo que não fique com dois hífens
                linha = f"{num_questao} - {alternativa}\n"
                alterado = True
            arquivo.write(linha)

        if not alterado:
            print(f"A questão {numero_questao} não foi encontrada no arquivo.")

def comparar_com_gabarito(nome_arquivo_respostas, nome_arquivo_gabarito, modelo_enem=False, dia_prova=None):
    try:
        with open(nome_arquivo_respostas, "r") as f_respostas:
            respostas = {}
            for linha in f_respostas.readlines():
                partes = linha.split(" - ")
                if len(partes) >= 2:
                    respostas[partes[0]] = partes[1].strip()
                else:
                    print(f"Formato inválido na linha: '{linha.strip()}'")  # Para depuração

        with open(nome_arquivo_gabarito, "r") as f_gabarito:
            gabarito = {}
            for linha in f_gabarito.readlines():
                partes = linha.split(" - ")
                if len(partes) >= 2:
                    gabarito[partes[0]] = partes[1].strip()
                else:
                    print(f"Formato inválido na linha do gabarito: '{linha.strip()}'")  # Para depuração

        pontos = 0
        total_questoes = len(gabarito)
        
        # Resumo por categoria (caso seja o modelo ENEM)
        if modelo_enem:
            resumod1 = {
                "Linguagens": {"corretas": 0, "erradas": 0, "em_branco": 0},
                "Ciências Humanas": {"corretas": 0, "erradas": 0, "em_branco": 0},
            }

            resumod2 = {
                "Ciências da Natureza": {"corretas": 0, "erradas": 0, "em_branco": 0},
                "Matemática": {"corretas": 0, "erradas": 0, "em_branco": 0},
            }

        for questao, resposta in gabarito.items():
            questao_num = int(questao)  # Convertendo a chave da questão para um número
            
            if questao in respostas:
                if respostas[questao] == resposta:
                    print(f"Questão {questao}: Correta")
                    pontos += 1
                    
                    if modelo_enem:
                        if dia_prova == 1:
                            if questao_num <= 45:
                                resumod1["Linguagens"]["corretas"] += 1
                            elif 46 <= questao_num <= 90:
                                resumod1["Ciências Humanas"]["corretas"] += 1
                        elif dia_prova == 2:
                            if questao_num <= 135:
                                resumod2["Ciências da Natureza"]["corretas"] += 1
                            elif 136 <= questao_num <= 180:
                                resumod2["Matemática"]["corretas"] += 1

                elif respostas[questao] == "Anulado":
                    print(f"Questão {questao}: Anulado. Você recebeu 1 ponto.")
                    pontos += 1
                    
                    if modelo_enem:
                        if dia_prova == 1:
                            if questao_num <= 45:
                                resumod1["Linguagens"]["corretas"] += 1
                            elif 46 <= questao_num <= 90:
                                resumod1["Ciências Humanas"]["corretas"] += 1
                        elif dia_prova == 2:
                            if questao_num <= 135:
                                resumod2["Ciências da Natureza"]["corretas"] += 1
                            elif 136 <= questao_num <= 180:
                                resumod2["Matemática"]["corretas"] += 1

                elif respostas[questao] == "":
                    print(f"Questão {questao}: Não respondida.")
                    
                    if modelo_enem:
                        if dia_prova == 1:
                            if questao_num <= 45:
                                resumod1["Linguagens"]["em_branco"] += 1
                            elif 46 <= questao_num <= 90:
                                resumod1["Ciências Humanas"]["em_branco"] += 1
                        elif dia_prova == 2:
                            if questao_num <= 135:
                                resumod2["Ciências da Natureza"]["em_branco"] += 1
                            elif 136 <= questao_num <= 180:
                                resumod2["Matemática"]["em_branco"] += 1

                else:
                    print(f"Questão {questao}: Errada. Sua resposta: {respostas[questao]}, Gabarito: {resposta}")
                    
                    if modelo_enem:
                        if dia_prova == 1:
                            if questao_num <= 45:
                                resumod1["Linguagens"]["erradas"] += 1
                            elif 46 <= questao_num <= 90:
                                resumod1["Ciências Humanas"]["erradas"] += 1
                        elif dia_prova == 2:
                            if questao_num <= 135:
                                resumod2["Ciências da Natureza"]["erradas"] += 1
                            elif 136 <= questao_num <= 180:
                                resumod2["Matemática"]["erradas"] += 1

            else:
                print(f"Questão {questao} não respondida.")

        print(f"\nTotal de pontos: {pontos} de {total_questoes}")
        
        # Mostrar o resumo se for o modelo ENEM
        if modelo_enem:
            if dia_prova == 1:
                print("\nResumo da correção (Modelo ENEM):")
                for categoria, resultados in resumod1.items():
                    print(f"{categoria}: Corretas: {resultados['corretas']}, Erradas: {resultados['erradas']}, Em branco: {resultados['em_branco']}")

            elif dia_prova == 2:
                print("\nResumo da correção (Modelo ENEM):")
                for categoria, resultados in resumod2.items():
                    print(f"{categoria}: Corretas: {resultados['corretas']}, Erradas: {resultados['erradas']}, Em branco: {resultados['em_branco']}")
            
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        
def main():
    nome_arquivo = input("Digite o nome do arquivo de respostas: ") + ".txt"

    while True:
        opcao = menu()
        
        if opcao == '1':
            alterar_arquivo = input("Alterar nome do arquivo? (s/n)").lower()
            if alterar_arquivo == 's':
                nome_arquivo = input("Digite o nome do arquivo de respostas: ") + ".txt"
            else:
                criar_arquivo(nome_arquivo)
        
        elif opcao == '2':
            abrir_arquivo(nome_arquivo)
        
        elif opcao == '3':
            inserir_resposta(nome_arquivo)
        
        elif opcao == "4":
            nome_arquivo = input("Digite o nome do arquivo de respostas: ") + ".txt"
            nome_gabarito = input("Digite o nome do arquivo de gabarito: ") + ".txt"
            
            modelo_enem = input("A correção será no modelo ENEM? (S/N): ").strip().lower()
            
            if modelo_enem == 's':
                dia_prova = int(input("Qual o dia da prova? (1 ou 2): "))
                comparar_com_gabarito(nome_arquivo, nome_gabarito, modelo_enem=True, dia_prova=dia_prova)
            else:
                comparar_com_gabarito(nome_arquivo, nome_gabarito, modelo_enem=False)

        
        elif opcao == '5':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
    input("Pressione Enter para sair...")
