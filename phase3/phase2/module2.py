from phase0.FA_class import DFA
from utils.utils import imageType


def solve(json_str: str, image: imageType) -> bool:
    address = {}
    fa = DFA.deserialize_json(json_str)

    calculate_address_bit(image,'',address)
    pr = 0
    # print(address)
    for key in address.keys():
        if fa.is_accept(key) == address[key]:
            pr += 1
    pr = (pr / len(image) ** 2)*100
    # print(f'{pr}%')
    if pr == 100:
        return True
    return False


def calculate_address_bit(image: imageType, bit_address='',address={}):
    tool = len(image)
    if tool == 1:
        address[bit_address] = image[tool - 1][tool - 1]
        return

    h_tool = tool // 2
    i_sm = 0
    j_sm = 0

    for k in range(4):
        new_image = [[''] * h_tool for b in range(h_tool)]

        for i in range(i_sm, h_tool + i_sm):
            for j in range(j_sm, h_tool + j_sm):
                x = i - i_sm
                y = j - j_sm
                new_image[x][y] = image[i][j]

        calculate_address_bit(new_image, bit_address + str(k),address)

        if i_sm == h_tool:
            j_sm = h_tool

        elif j_sm == h_tool:
            i_sm = h_tool
            j_sm = 0

        else:
            j_sm = h_tool


if __name__ == "__main__":

    print(
        solve(
            '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}',
            [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
        )
    )
