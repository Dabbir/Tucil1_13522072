import time
import random
import utils

# ==================================== GENERATE CLI  ====================================
def input_cli():
    num_tokens = int(input("Jumlah token [5] : ") or "5")
    tokens = input("Token (dipisah spasi) [BD 1C 7A 55 E9] : ").split() or ["BD", "1C", "7A", "55", "E9"]
    buffer_size = int(input("Ukuran Buffer [7] : ") or "7")
    matrix_size = list(map(int, input("Ukuran Matriks (dipisah spasi) [6 6] : ").split())) or [6, 6]
    num_sequences = int(input("Jumlah Sekuens [3] : ") or "3")
    max_sequence_size = int(input("Ukuran Maksimal Sekuens [4] : ") or "4")

    return num_tokens, tokens, buffer_size, matrix_size, num_sequences, max_sequence_size

def generate_matrix(matrix_size, tokens):
    matrix = []
    for _ in range(matrix_size[0]):
        row = [random.choice(tokens) for _ in range(matrix_size[1])]
        matrix.append(row)
    return matrix

def generate_sequences(num_sequences, max_sequence_size, tokens):
    sequences = {}
    for _ in range(num_sequences):
        size = random.randint(1, max_sequence_size)
        sequence = tuple(random.choice(tokens) for _ in range(size))
        sequences[sequence] = random.randint(-100, 100)
    return sequences

def generate_cli():
    num_tokens, tokens, buffer_size, matrix_size, num_sequences, max_sequence_size = input_cli()

    print(buffer_size)
    print(f'{matrix_size[0]} {matrix_size[1]}')
    matrix = generate_matrix(matrix_size, tokens)
    for row in matrix:
        print(' '.join(row))
    
    print(num_sequences)
    sequences = generate_sequences(num_sequences, max_sequence_size, tokens)
    for sequence, reward in sequences.items():
        print(' '.join(sequence))
        print(reward)

    main(buffer_size, matrix, sequences)

    is_write = input("\nApakah ingin menyimpan Matriks & sekuens permainan (beserta dengan bobot hadiahnya)? (y/n) ")
    if is_write == 'y' or is_write == 'Y':
        file_name = input('Masukkan nama file untuk disimpan: ')
        utils.save_to_file(buffer_size, matrix, num_sequences, sequences, 'test/' + file_name + '.txt')

# ==================================== INPUT FILE ====================================
def coordinates_to_elements(matrix, coordinates):
    elements_combination = []
    for row, col in coordinates:
        elements_combination.append(matrix[row][col])
    return elements_combination

def breach_protocol(buffer_size, matrix, sequences):
    rows = len(matrix)
    cols = len(matrix[0])
    sequence = {tuple(key): value for key, value in sequences.items()}

    def is_subarray(arr, subarr):
        subarr_length = len(subarr)
        for i in range(len(arr) - subarr_length + 1):
            if arr[i:i+subarr_length] == subarr:
                return True
        return False

    def generate_combinations(matrix_height, matrix_width, buffer_size):
        def backtrack(combination, buffer_size):
            valid_combinations = []
            if len(combination) >= 1 and combination[0][0] == 0:
                valid_combinations.append(combination[:])
            if len(combination) == buffer_size:
                return valid_combinations
            for row in range(matrix_height):
                for col in range(matrix_width):
                    if not any(row == r and col == c for r, c in combination):
                        if not combination or row == combination[-1][0] or col == combination[-1][1]:
                            if len(combination) < 2 or (len(combination) >= 2 and combination[0][1] == combination[1][1] and combination[-2][0] != row and combination[-2][1] != col):
                                valid_combinations.extend(backtrack(combination + [(row, col)], buffer_size))
            return valid_combinations

        return backtrack([], buffer_size)

    def calculate_reward(combination, sequence):
        reward = 0
        for key in sequence:
            if is_subarray(combination, key):
                reward += sequence[key]
        return reward

    def search_optimal_path(combinations, sequence, matrix):
        paths = {}
        max_reward = 0
        max_path = []

        for combination in combinations:
            path = tuple(matrix[row][col] for row, col in combination)
            reward = calculate_reward(path, sequence)
            paths[tuple(matrix[row][col] for row, col in combination)] = reward
            if reward > max_reward or (reward == max_reward and len(combination) < len(max_path)):
                max_reward = reward
                max_path = combination

        return paths, max_reward, max_path

    start_time = time.time()
    combinations = generate_combinations(rows, cols, buffer_size)
    time_ms = round((time.time() - start_time) * 1000)

    paths, max_reward, max_path = search_optimal_path(combinations, sequence, matrix)

    return paths, max_reward, max_path, time_ms

def main(buffer_size, matrix, sequences):
    print('\n============= RESULT =============\n')
    paths, max_reward, max_path, time_ms = breach_protocol(buffer_size, matrix, sequences)
    print(max_reward)
    print(' '.join(coordinates_to_elements(matrix, max_path)))
    for x, y in max_path:
        print(f'{y+1}, {x+1}')
    print(f'\n{time_ms} ms\n')

    is_write = input("Apakah ingin menyimpan solusi? (y/n) ")
    if is_write == 'y' or is_write == 'Y':
        file_name = input("\nMasukkan nama file (.txt): ")
        utils.write_file(matrix, max_reward, max_path, time_ms, f'test/{file_name}.txt')

if __name__ == "__main__":
    print('\n==================================')
    print('  CYBERPUNK 2077 BREACH PROTOCOL  ')
    print('==================================')
    print('Pilih input:')
    print('1. Input File')
    print('2. Generate Matrix & Sequence')
    print('3. Exit')
    method = int(input('Input: '))

    while method < 3 and method > 0:
        while method != 1 and method != 2:
            print('Pilih input:')
            print('1. Input File')
            print('2. Generate Matrix & Sequence')
            method = int(input('Masukkan input yang benar: '))

        if method == 1:
            file_path = input("Masukkan nama file input: ")
            data = utils.read_file(f'test/{file_path}.txt')
            main(data[0], data[3], data[4])
        elif method == 2:
            generate_cli()

        print('==================================')
        print('  CYBERPUNK 2077 BREACH PROTOCOL  ')
        print('==================================')
        print('Pilih input:')
        print('1. Input File')
        print('2. Generate Matrix & Sequence')
        print('3. Exit')
        method = int(input('Input: '))

        print()

    print('THANK YOU ^_^\n')