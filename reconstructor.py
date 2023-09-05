def reader(count):
    with open('0_output.txt') as f:
        lines = f.readlines()
        parce_def = lines[count].strip('[]').replace(' ', '').replace(']\n', '').split(',')
        with open('output.txt', 'a') as f1:
            f1.write(str(parce_def) + '\n')
            print('Выход: ' + str(parce_def))
    return None


def reconstuctor(file, file_copy):
    counter = 0
    for row in file:
        counter += 1
        parce = row.strip('[]').replace(' ', '').replace(']\n', '').split(',')
        for row_new in file_copy:
            parce_copy = row_new.strip('[]').replace(' ', '').replace(']\n', '').split(',')
            if parce[8] == parce_copy[0]:
                for i in range(6):
                    parce.append(parce_copy[i + 1])
        if len(parce) > 10:
            with open('input.txt', 'a') as f:
                parce.pop(0)
                parce.pop(7)
                parce.pop(2)
                parce.pop(8)
                parce[2] = str(float(parce[4]) / float(parce[2]))
                parce[8] = str(float(parce[10]) / float(parce[8]))
                parce.pop(3)
                parce.pop(8)
                parce.pop(3)
                parce.pop(7)
                f.write(str(parce) + "\n")
                print('Вход: ' + str(parce))

            reader(counter - 1)
        file_copy.seek(0)
    return None


if __name__ == "__main__":
    reconstuctor(open('0_input.txt'), open('1_input.txt'))