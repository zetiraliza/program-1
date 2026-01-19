import random

number = random.randint(1, 10)
print("Selamat datang di game tebak angka!")
print("Tebak angka antara 1 sampai 10. Anda punya 3 kesempatan.")

for attempt in range(3):
    try:
        guess = int(input(f"Tebakan ke-{attempt + 1}: "))
        if guess == number:
            print("Benar! Anda menang!")
            break
        elif guess < number:
            print("Terlalu kecil!")
        else:
            print("Terlalu besar!")
    except ValueError:
        print("Masukkan angka yang valid!")
else:
    print(f"Maaf, kesempatan habis. Angka yang benar adalah {number}")

print("Terima kasih telah bermain!")