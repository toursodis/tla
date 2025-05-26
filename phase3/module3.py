from phase0.FA_class import DFA
from phase2 import module2
from utils.utils import imageType


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    answer = [''] * len(json_fa_list)
    for (index, json_fa) in enumerate(json_fa_list):

        fa = DFA.deserialize_json(json_fa)
        address = {}
        for (index_image, image) in enumerate(images):
            module2.calculate_address_bit(image, '', address)
            pr = 0
            # print(address)
            for key in address.keys():
                if fa.is_accept(key) == address[key]:
                    pr += 1
            pr = (pr / len(image) ** 2) * 100
            # print(f'{pr}%')
            if pr == 100:
                answer[index] = index_image
    return answer


if __name__ == "__main__":
    ...
