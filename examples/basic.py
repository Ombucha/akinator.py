# pylint: skip-file

import akinator

aki = akinator.Akinator()
aki.start_game()

while not aki.finished:
    print(f"\nQuestion: {str(aki)}")
    user_input = input(
        "Your answer ([y]es/[n]o/[i] don't know/[p]robably/[pn] probably not, [b]ack): "
    ).strip().lower()
    if user_input == "b":
        try:
            aki.back()
        except akinator.CantGoBackAnyFurther:
            print("You can't go back any further!")
    else:
        try:
            aki.answer(user_input)
        except akinator.InvalidChoiceError:
            print("Invalid answer. Please try again.")

print("\n--- Game Over ---")
print(f"Proposition: {aki.name_proposition}")
print(f"Description: {aki.description_proposition}")
print(f"Pseudo: {aki.pseudo}")
print(f"Photo: {aki.photo}")
print(f"Final Message: {aki.question}")
