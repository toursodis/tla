from phase0.FA_class import DFA
from utils import utils
from utils.utils import imageType


def solve(image: imageType) -> 'DFA':
    dp_states = []
    dp_states.append('')
    dp_is_final = []

    dfa = DFA()
    dfa.add_state(0)
    dfa.assign_initial_state(dfa.get_state_by_id(0))
    dfa.assign_alphabet(['0', '1', '2', '3'])

    total_num_states = 1
    lentrt = len(image) ** 2

    while lentrt >= 4:
        total_num_states += lentrt
        lentrt //= 4

    for kn in range(total_num_states):
        dp_is_final.append(False)

    print(total_num_states)

    i = j = 0
    while True:
        u_i = dfa.get_state_by_id(i)
        if j < total_num_states - 1:
            print(j)
            for k in range(4):
                w = dp_states[i]
                w_k = w + str(k)
                finding = False
                # if w_k in dp_states:
                #     finding = True
                #     q = dp_states.index(w_k)
                #     dfa.add_transition(u_i, dfa.get_state_by_id(q), str(k))

                if not finding:
                    j += 1
                    dfa.add_state(j)
                    dp_states.append(calculate_w(dp_states[j - 1]))
                    dfa.add_transition(dfa.get_state_by_id(i), dfa.get_state_by_id(j), str(k))
        else:
            for jj in range(total_num_states - len(image) ** 2, total_num_states):
                for k in range(4):
                    dfa.add_transition(dfa.get_state_by_id(jj), dfa.get_state_by_id(jj), str(k))

        i += 1
        if i - 1 == j:
            break

    indexi = total_num_states - len(image) ** 2
    for i in range(0, len(image), 2):
        for j in range(0, len(image), 2):

            if image[i][j] == 0:
                dp_is_final[indexi] = True
            indexi += 1

            if image[i][j + 1] == 0:
                dp_is_final[indexi] = True
            indexi += 1

            if image[i + 1][j] == 0:
                dp_is_final[indexi] = True
            indexi += 1

            if image[i + 1][j + 1] == 0:
                dp_is_final[indexi] = True
            indexi += 1

    for indeeeeeex in range(len(dp_is_final) - 1, 0, -4):
        i1 = dp_is_final[indeeeeeex]
        i2 = dp_is_final[indeeeeeex - 1]
        i3 = dp_is_final[indeeeeeex - 2]
        i4 = dp_is_final[indeeeeeex - 3]

        dp_is_final[indeeeeeex // 4 - 1] = i1 and i2 and i3 and i4

    for xc in range(len(dp_is_final)):
        if dp_is_final[xc]:
            print(xc)
            dfa.add_final_state(dfa.get_state_by_id(xc))

    return dfa


def calculate_w(prev_state):
    if prev_state == '':
        return '0'

    n = prev_state
    lenrt = len(n)
    num = int(n[lenrt - 1])
    num += 1
    num %= 4
    while num == 0 and lenrt >= 1:
        n[lenrt - 1] = str(num)
        lenrt -= 1
        num = int(n[lenrt - 1])
        num += 1
        num %= 4
    if lenrt == 0:
        n = '0' + n

    return n


if __name__ == "__main__":
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())
