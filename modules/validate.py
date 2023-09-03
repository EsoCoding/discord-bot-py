person_fields = {
    "name": {"pretty": "first name", "validation": str.isalpha},
    "lastname": {"pretty": "last name", "validation": str.isalpha},
    "fathers_name": {"pretty": "father's name", "validation": str.isalpha},
    "age": {"pretty": "age", "validation": str.isdigit},
    "class": {"pretty": "class", "validation": str.isdigit},
}

for field, info in person_fields.items():
    while True:
        user_input = input(f"Please enter your {info['pretty']}: ")
        if info["validation"](user_input):
            break
        print("Invalid input. ", end="")
