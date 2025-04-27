import pandas as pd
import re
import os


def ler_input():
    print("\nCole abaixo TODO o conteúdo das questões.")
    print("Quando terminar, digite FIM sozinho na linha e pressione Enter:")
    linhas = []
    while True:
        linha = input()
        if linha.strip().upper() == "FIM":
            break
        linhas.append(linha)
    return "\n".join(linhas)


def processar_questoes(texto, origem):
    questoes = []
    blocos = re.split(r'Question \d+', texto)

    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco:
            continue

        linhas = bloco.split("\n")
        pergunta = ""
        opcoes = []
        respostas_corretas = []
        explicacao = ""
        captura_explicacao = False
        encontrou_true_false = False

        for i, linha in enumerate(linhas):
            linha = linha.strip()

            if i == 0 and linha.lower() == 'skipped':
                continue

            if i == 1 and linha != '':
                pergunta = linha
                continue

            if linha.lower() in [
                'choose the correct answer.',
                'there are two correct answers.',
                'there are three correct answers.',
                'there are four correct answers.',
                'there are five correct answers.'
            ]:
                continue

            if linha.lower().startswith('correct answer') or linha.lower().startswith('correct selection'):
                try:
                    resposta = linhas[i+1].strip()
                    if resposta:
                        respostas_corretas.append(resposta)
                except:
                    pass

            elif linha.lower().startswith('overall explanation'):
                captura_explicacao = True

            elif captura_explicacao:
                explicacao += linha + " "

            else:
                if linha and not linha.lower().startswith('note') and not linha.lower().startswith('skipped'):
                    if linha.lower() in ['true', 'false']:
                        encontrou_true_false = True
                    opcoes.append(linha)

        if encontrou_true_false and not opcoes:
            opcoes = ["True", "False"]

        while len(opcoes) < 5:
            opcoes.append("")

        pergunta_formatada = pergunta
        if len(respostas_corretas) > 1:
            pergunta_formatada += f" ({len(respostas_corretas)} correct)"

        questoes.append({
            "Pergunta": pergunta_formatada,
            "Opção A": opcoes[0],
            "Opção B": opcoes[1],
            "Opção C": opcoes[2],
            "Opção D": opcoes[3],
            "Opção E": opcoes[4],
            "Resposta(s) Correta(s)": "; ".join(respostas_corretas),
            "Explicação": explicacao.strip(),
            "Origem": origem
        })

    return questoes


def salvar_arquivos(questoes, nome_base):
    df = pd.DataFrame(questoes)

    print("\nEm qual formato você deseja exportar?")
    print("1 - Excel (.xlsx)")
    print("2 - CSV (.csv)")
    print("3 - Ambos")

    formato = input("Escolha uma opção (1, 2 ou 3): ").strip()

    if formato in ['1', '3']:
        nome_xlsx = nome_base + ".xlsx"
        df.to_excel(nome_xlsx, index=False)
        print(f"✅ Arquivo Excel '{nome_xlsx}' gerado com sucesso!")

    if formato in ['2', '3']:
        csv_data = []
        for questao in questoes:
            csv_data.append({
                "Question": questao["Pergunta"],
                "Answer 1": questao["Opção A"],
                "Answer 2": questao["Opção B"],
                "Answer 3": questao["Opção C"],
                "Answer 4": questao["Opção D"],
                "Answer 5": questao["Opção E"],
                "Correct Answer(s)": questao["Resposta(s) Correta(s)"],
                "Explanation": questao["Explicação"]
            })

        df_csv = pd.DataFrame(csv_data)
        nome_csv = nome_base + ".csv"
        df_csv.to_csv(nome_csv, index=False, encoding='utf-8-sig')
        print(f"✅ Arquivo CSV '{nome_csv}' gerado com sucesso!")

    print(f"📊 Total de questões processadas: {len(questoes)}")


def agregar_planilhas():
    quantidade = int(input("Quantas planilhas você deseja agregar? "))
    arquivos = []
    for i in range(quantidade):
        nome = input(f"Digite o nome da planilha {i+1} (ex: planilha.xlsx): ").strip()
        if not os.path.exists(nome):
            print(f"\n🚫 Arquivo '{nome}' não encontrado! Abortando.")
            return
        arquivos.append(nome)

    frames = []
    for arquivo in arquivos:
        df = pd.read_excel(arquivo)
        frames.append(df)

    df_final = pd.concat(frames, ignore_index=True)

    nome_saida = input("Digite o nome do novo arquivo final (ex: todas_questoes.xlsx): ").strip()
    if not nome_saida.endswith('.xlsx'):
        nome_saida += '.xlsx'

    df_final.to_excel(nome_saida, index=False)
    print(f"\n✅ Arquivo agregado '{nome_saida}' gerado com sucesso!")
    print(f"📊 Total de questões agregadas: {len(df_final)}")


def gerar_nome_base(origem):
    return origem.lower().replace("practice test", "practice").replace(" ", "")


def menu_principal():
    print("\n=== Gerenciador de Questões Udemy ===")
    print("1 - Gerar nova planilha")
    print("2 - Agregar planilhas existentes")
    opcao = input("Escolha uma opção (1 ou 2): ").strip()

    if opcao == '1':
        origem = input("Digite de qual Practice Test essas questões pertencem (ex: Practice Test 1): ").strip()
        texto = ler_input()
        questoes = processar_questoes(texto, origem)
        nome_base = gerar_nome_base(origem)
        salvar_arquivos(questoes, nome_base)

    elif opcao == '2':
        agregar_planilhas()

    else:
        print("\nOpção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()
