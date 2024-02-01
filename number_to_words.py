import inflect

def number_to_words(number):
    p = inflect.engine()
    return p.number_to_words(number)

if __name__ == "__main__":
    print(number_to_words(5))   # Outputs: five
    print(number_to_words(52))  # Outputs: fifty-two