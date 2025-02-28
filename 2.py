import sys
import hashlib
from colorama import Fore, Style, init

init(autoreset=True)

try:
    from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
    from aptos_sdk.account import Account
except ModuleNotFoundError as e:
    print(f"Ошибка: {e}. Установите отсутствующие модули командой: pip install bip_utils aptos-sdk")
    sys.exit(1)

# Функция для генерации адреса и приватного ключа Aptos
def generate_aptos_keys(seed_phrase):
    seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.APTOS)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    private_key = bip44_acc_ctx.PrivateKey().Raw().ToHex()
    account = Account.load_key(private_key)
    return account.address(), private_key

# Чтение сид-фраз из файла
input_file = "seed_phrases.txt"
address_file = "address.txt"
private_key_file = "privatekey.txt"
private_key_hex_file = "privatekey_hex.txt"

try:
    with open(input_file, "r", encoding="utf-8") as f:
        seed_phrases = [line.strip() for line in f if line.strip()]

    with open(address_file, "w", encoding="utf-8") as addr_f, \
         open(private_key_file, "w", encoding="utf-8") as pk_f, \
         open(private_key_hex_file, "w", encoding="utf-8") as pk_hex_f:
        
        for idx, seed_phrase in enumerate(seed_phrases, start=1):
            try:
                address, private_key = generate_aptos_keys(seed_phrase)
                addr_f.write(f"{address}\n")
                pk_f.write(f"{private_key}\n")
                pk_hex_f.write(f"0x{private_key}\n")
                first_word = seed_phrase.split()[0]
                print(f"[+] [{idx}] {first_word}...")
            except Exception as e:
                print(f"[-] Ошибка обработки сид-фразы: {seed_phrase.split()[0]}... - {e}")
except FileNotFoundError:
    print(f"Файл {input_file} не найден.")
    sys.exit(1)

print(f"{Style.BRIGHT}{Fore.GREEN}Готово! Адреса сохранены в {address_file}, приватные ключи в {private_key_file}, приватные ключи с 0x в {private_key_hex_file}")
