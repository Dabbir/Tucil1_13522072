import main

def save_to_file(buffer_size, matrix, num_sequences, sequences, filename):
    with open(filename, "w") as file:
        file.write(str(buffer_size) + "\n")
        file.write(str(len(matrix)) + ' ' + str(len(matrix[0])) + "\n")
        for row in matrix:
            file.write(" ".join(row) + "\n")

        file.write(str(num_sequences) + '\n')
        for sequence, reward in sequences.items():
            file.write(" ".join(sequence) + "\n")
            file.write(str(reward) + "\n")

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            buffer_size = int(file.readline())
            matrix_width, matrix_height = map(int, file.readline().split())
            matrix = [file.readline().split() for _ in range(matrix_height)]
            number_of_sequences = int(file.readline())

            sequence_reward = {}
            for _ in range(number_of_sequences):
                sequence = tuple(file.readline().split())
                reward = int(file.readline())
                sequence_reward[sequence] = reward

        return buffer_size, matrix_width, matrix_height, matrix, sequence_reward

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

def write_file(matrix, max_reward, max_path, time_ms, filename):
    with open(filename, "w") as file:
        file.write(str(max_reward) + '\n')
        file.write(' '.join(main.coordinates_to_elements(matrix, max_path))  + '\n')
        for x, y in max_path:
            file.write(f'{y+1}, {x+1}\n')
        file.write(f'\n{str(time_ms)} ms\n')