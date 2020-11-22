# Avaliando se CPF é real
# Esse aplicativo testa se o CPF é real pelos critérios matemáticos.
# No final, se o cpf for válido, mostra também em qual estado foi emitido.

def main():
    cpf = input("\nDigite o CPF: ")

    #retira os espaços
    cpf = cpf.strip()

    # Retira os caracteres errados/desnecessários.
    for char in cpf:
        try:
            char = int(char)+1
        except:
            cpf = cpf.replace(char, "")

    print("O CPF digitado foi: ", cpf)


    # esse é o algoritmo:
    if len(cpf) != 11:
        print("CPF inválido : quantidade errada de dígitos")
    else:
        # transformando cada dígito em uma variável int.
        cpf1 = int(cpf[0])
        cpf2 = int(cpf[1])
        cpf3 = int(cpf[2])
        cpf4 = int(cpf[3])
        cpf5 = int(cpf[4])
        cpf6 = int(cpf[5])
        cpf7 = int(cpf[6])
        cpf8 = int(cpf[7])
        cpf9 = int(cpf[8])
        cpfx = int(cpf[9])
        cpfy = int(cpf[10])

        # testando soma dos dígitos
        list_cpf = [int(i) for i in str(cpf)]
        sum_cpf = (sum(list_cpf))
        possible_cpf_sum = [10, 11, 12, 21, 22, 23, 32, 33, 34, 43, 44, 45, 54, 55, 56, 65, 66, 67, 76, 77, 78, 87, 88]

        if sum_cpf not in possible_cpf_sum:
            print("Inválido pela soma de dígitos")
        else:
            # testando primeiro dígito verificador (X)
            obtendo_x = cpf1 * 10 + cpf2 * 9 + cpf3 * 8 + cpf4 * 7 + cpf5 * 6 + cpf6 * 5 + cpf7 * 4 + cpf8 * 3 + cpf9 * 2
            resto_x = obtendo_x % 11
            x_calc = 11 - resto_x
            if x_calc >= 10:
                x_calc = 0

            if x_calc != cpfx:
                print("CPF inválido - critério X")
            else:
                # Testando o segundo dígito verificador (Y)
                obtendo_y = cpf1 * 11 + cpf2 * 10 + cpf3 * 9 + cpf4 * 8 + cpf5 * 7 + cpf6 * 6 + cpf7 * 5 + cpf8 * 4 + cpf9 * 3 + cpfx * 2
                resto_y = obtendo_y % 11
                y_calc = 11 - resto_y
                if y_calc >= 10:
                    y_calc = 0

                if y_calc != cpfy:
                    print("CPF inválido - critério Y")
                else:
                    # se passou em todos os testes até aqui: é válido

                    print("\t --- CPF matematicamente válido --- ")
                    estado_dic = {
                        0: "Rio Grande do Sul",
                        1: "Distrito Federal, Goiás, Mato Grosso, Mato Grosso do Sul ou Tocantins",
                        2: "Amazonas, Pará, Roraima, Amapá, Acre ou Rondônia",
                        3: "Ceará, Maranhão ou Piauí",
                        4: "Paraíba, Pernambuco, Alagoas ou Rio Grande do Norte",
                        5: "Bahia ou Sergipe",
                        6: "Minas Gerais",
                        7: "Rio de Janeiro ou Espírito Santo",
                        8: "São Paulo",
                        9: "Paraná ou Santa Catarina"
                    }

                    estado = cpf[-3]
                    estado = int(estado)
                    print("Esse CPF foi emitido em: ", estado_dic[estado])


while True:
    main()
