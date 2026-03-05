import os
import re

# folder_a = r'/home/mxjtufeigmail/桌面/tmp/controller_2024-03-17-10-39-07/Camera0/controller_2024-03-17-10-59-34/Camera0/images'
# folder_b = r'/home/mxjtufeigmail/桌面/tmp/controller_2024-03-17-10-39-07/Camera0/controller_2024-03-17-10-59-34/Camera6/images'

def extract_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    else:
        return None


def main():
    folder_a = r'D:\新桌面\glew-2.1.0\backup\controller_2024-04-19-06-30-28/Camera0/images/'
    folder_b = r'D:\新桌面\glew-2.1.0\backup\controller_2024-04-19-06-30-28/Camera6/images/'
    threshold = 9000000

    files_a = os.listdir(folder_a)
    files_b = os.listdir(folder_b)

    for file_a in files_a:
        number_a = extract_number(file_a)
        if number_a is None:
            continue

        for file_b in files_b:
            number_b = extract_number(file_b)
            if number_b is None:
                continue

            diff = abs(number_a - number_b)
            if diff <= threshold:
                print(f"File pair: {file_a}, {file_b}, Difference: {diff}")


if __name__ == "__main__":
    main()



   # """
   # 1982919806668 - 1982918951312 = 855356
   #  24、31 | 12、20、


   # 693573033058 - 693568142962 = 4890096
   # 21、20

# """