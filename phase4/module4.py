from math import log2

from phase0.FA_class import DFA
from utils.utils import imageType


def solve(json_str: str, resolution: int) -> imageType:
    address = {}
    image = [[''] * resolution for b in range(resolution)]
    fa = DFA.deserialize_json(json_str)
    len_bit_address = log2(resolution)

    for i in range(resolution ** 2):
        a = ''
        q = i % 4
        m = i // 4
        a += str(q)
        while m > 0:
            q = m % 4
            m = m // 4
            a = str(q) + a

        while len(a) < len_bit_address:
            a = '0' + a
        address[a] = int(fa.is_accept(a))

    for key in address.keys():
        i = j = 0
        for (index, letter) in enumerate(key):
            tool = resolution // 2 ** (index + 1)

            if letter == '1':
                j += tool
            elif letter == '2':
                i += tool
            elif letter == '3':
                i += tool
                j += tool
            if tool == 1:
                image[i][j] = address[key]
    return image


if __name__ == "__main__":
    pic_arr = solve(
        '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
        '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
        '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
        '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
        '"3": "q_4"}}',
        4
    )
    print(pic_arr)
