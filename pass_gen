import random
import discord


def passgen(lengy):
    characters = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    if lengy.isnumeric():
        lengy_int = int(lengy)
        for i in range(lengy_int):
            password += random.choice(characters)
        return password
    else:
        return "Please type a whole number!"
        
print(passgen(input("How many characters should the password consist of?\n")))
