from Touch_the_fish.name_function import get_formatted

print("Enter 'q' at any time to quit.")
while True:
    first = input("\n Please give me a first name: ")
    if first == "q":
        break
    last = input("Please give me a last name: ")
    if last == "q":
        break
    formatted_name = get_formatted(first, last)
    print("\t Heatly formatted name : " + formatted_name + ".")

