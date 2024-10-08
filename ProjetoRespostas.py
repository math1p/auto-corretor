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
    numero_questao = input("Número da questão: ")
    alternativa = input("Alternativa: ").upper()

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
                linha = f"{num_questao} {alternativa}\n"
                alterado = True
            arquivo.write(linha)

        if not alterado:
            print(f"A questão {numero_questao} não foi encontrada no arquivo.")

def comparar_com_gabarito(nome_respostas, nome_gabarito):
    # Verifica os arquivos no diretório atual
    caminho_respostas = os.path.join(os.getcwd(), nome_respostas)
    caminho_gabarito = os.path.join(os.getcwd(), nome_gabarito)
    
    try:
        with open(caminho_respostas, 'r') as f_respostas:
            respostas = {linha.split(" - ")[0]: linha.split(" - ")[1].strip() for linha in f_respostas.readlines()}
        
        with open(caminho_gabarito, 'r') as f_gabarito:
            gabarito = [linha.strip() for linha in f_gabarito.readlines()]

        modelo_enem = input("Modelo ENEM? (s/n): ").lower()
        if modelo_enem == 's':
            dia = input("Dia 1 ou 2? (1/2): ")
            if dia == '1':
                print("\nDia 1: Linguagens e Ciências Humanas")
                categorias = [("Linguagens", 1, 45), ("Ciências Humanas", 46, 90)]
            else:
                print("\nDia 2: Ciências da Natureza e Matemática")
                categorias = [("Ciências da Natureza", 91, 135), ("Matemática", 136, 180)]

            for categoria, inicio, fim in categorias:
                corretas = 0
                erradas = 0
                print(f"\nCategoria: {categoria}")
                for i in range(inicio, fim + 1):
                    questao = str(i)
                    if questao in respostas and i <= len(gabarito):
                        if respostas[questao] == gabarito[i-1]:
                            corretas += 1
                        else:
                            erradas += 1
                print(f"Corretas: {corretas}, Erradas: {erradas}")

        else:
            corretas = 0
            erradas = 0
            for i in range(1, len(gabarito) + 1):
                questao = str(i)
                if questao in respostas:
                    if respostas[questao] == gabarito[i-1]:
                        corretas += 1
                    else:
                        erradas += 1
            print(f"\nResumo Geral: Corretas: {corretas}, Erradas: {erradas}")
    
    except FileNotFoundError as e:
        print(f"Erro: {e}")

# Loop principal
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
        
        elif opcao == '4':
            nome_gabarito = input("Digite o nome do arquivo de gabarito: ") + ".txt"
            comparar_com_gabarito(nome_arquivo, nome_gabarito)
        
        elif opcao == '5':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
    input("Pressione Enter para sair...")
