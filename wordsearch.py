import numpy as np
import pandas as pd


# https://github.com/James231/Wordsearch-Solver-Python/blob/master/wordsearch_solver.py

def find_word(wordsearch, word):
    start_pos = []
    first_char = word[0]
    for i in range(0, len(wordsearch)):
        for j in range(0, len(wordsearch[i])):
            if wordsearch[i][j] == first_char:
                start_pos.append([i, j])
    for pos in start_pos:
        direction = check_start(wordsearch, word, pos)
        if direction is not None:
            return pos, direction


def check_start(wordsearch, word, start_pos):
    # directions = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]
    options = [0, 1, -1]
    directions = np.transpose([np.tile(options, len(options)), np.repeat(options, len(options))])[1:]
    for direction in directions:
        if check_dir(wordsearch, word, start_pos, direction):
            return direction


def check_dir(wordsearch, word, start_pos, dir):
    found_chars = [word[0]]
    current_pos = start_pos
    pos = [start_pos]
    while chars_match(found_chars, word):
        if len(found_chars) == len(word):
            return True
        current_pos = [current_pos[0] + dir[0], current_pos[1] + dir[1]]
        pos.append(current_pos)
        if is_valid_index(wordsearch, current_pos[0], current_pos[1]):
            found_chars.append(wordsearch[current_pos[0]][current_pos[1]])
        else:
            return


def chars_match(found, word):
    index = 0
    for i in found:
        if i != word[index]:
            return False
        index += 1
    return True


def is_valid_index(wordsearch, line_num, col_num):
    if (line_num >= 0) and (line_num < len(wordsearch)):
        if (col_num >= 0) and (col_num < len(wordsearch[line_num])):
            return True
    return False


def main():
    with open('wordsearch.txt') as f:
        lines = list(f.readlines())
        wordsearch = np.array([list(line.strip().upper()) for line in lines if line and not line.startswith('#')])

    with open('words.txt') as f:
        words = [line.strip() for line in f.readlines() if line]

    data = []
    for word in words:
        result = find_word(wordsearch, word)
        if result is None:
            print('>> not found:', word)
            continue
        pos, direction = result
        print(word, pos, direction)
        data.append(dict(word=word, x=pos[0], y=pos[1], dx=direction[0], dy=direction[1]))
    df = pd.DataFrame(data)
    df.to_csv('wordsearch_solution.csv', index=False)


if __name__ == '__main__':
    main()
