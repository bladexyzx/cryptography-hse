import numpy as np 
import string
import math
import random

class KeyValidityError(Exception):
    pass

class BlockCiphers:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.m = len(alphabet)

    def text_to_block(self, text, block_size):
        word = [self.alphabet.index(char) for char in text]
        blocks = []
        for i in range(0, len(word), block_size):
            block = word[i:block_size + i]
            if len(block) < block_size:
                random_letters = [random.randint(0, self.m - 1) for _ in range(block_size - len(block))]
                block.extend(random_letters)
            blocks.append(block)
            
        return blocks

    def matrix_to_key(self, text):
        # Теперь функция разделяет текст по переносу строки
        lines = text.strip().split('\n')
        key = []
        for line in lines:
            # Парсим числа, введенные через пробел
            row = [int(num) for num in line.split()]
            key.append(row)
        return np.array(key)
            
    def hill_cipher_encrypt(self, text, block_size, key_text):
        key = self.matrix_to_key(key_text)
        blocks = self.text_to_block(text, block_size)

        if len(key.shape) != 2 or key.shape[0] != key.shape[1]:
            raise KeyValidityError("Матрица ключа должна быть квадратной (разное количество символов в словах).")
        
        if key.shape != (block_size, block_size):
            raise KeyValidityError(f"Ключ должен быть размера {block_size}x{block_size}.")

        det_float = np.linalg.det(key)
        det_int = int(round(det_float))
        
        if det_int == 0:
            raise KeyValidityError("Матрица ключа вырожденная (определитель равен 0).")
            
        if math.gcd(det_int % self.m, self.m) != 1:          
            raise KeyValidityError("Определитель матрицы ключа не взаимно прост с мощностью алфавита.")

        encrypted_blocks = []
        for block in blocks:
            P = np.array(block).reshape(-1, 1)
            C = np.dot(key, P) % self.m
            encrypted_block = C.flatten().tolist()
            encrypted_blocks.extend(encrypted_block)
            
        encrypted_text = ''.join([self.alphabet[idx] for idx in encrypted_blocks])
        return encrypted_text
    
    def hill_cipher_decrypt(self, encrypted_text, block_size, key_text):
        key = self.matrix_to_key(key_text)
        encrypted_blocks = self.text_to_block(encrypted_text, block_size)

        if len(key.shape) != 2 or key.shape[0] != key.shape[1]:
            raise KeyValidityError("Матрица ключа должна быть квадратной (разное количество символов в словах).")
        
        if key.shape != (block_size, block_size):
            raise KeyValidityError(f"Ключ должен быть размера {block_size}x{block_size}.")

        det_float = np.linalg.det(key)
        det_int = int(round(det_float))
        
        if det_int == 0:
            raise KeyValidityError("Матрица ключа вырожденная (определитель равен 0).")
            
        if math.gcd(det_int % self.m, self.m) != 1:          
            raise KeyValidityError("Определитель матрицы ключа не взаимно прост с мощностью алфавита.")

        det_mod = det_int % self.m
        try:
            det_inv = pow(det_mod, -1, self.m)
        except ValueError:
            raise KeyValidityError("Определитель матрицы ключа не имеет обратного по модулю (не взаимно прост с мощностью алфавита).")
        adjugate_matrix = np.round(np.linalg.inv(key) * det_float).astype(int)
        key_inv = (det_inv * adjugate_matrix) % self.m
        decrypted_blocks = []
        for block in encrypted_blocks:
            C = np.array(block).reshape(-1, 1)
            P = np.dot(key_inv, C) % self.m
            decrypted_block = P.flatten().tolist()
            decrypted_blocks.extend(decrypted_block)
            
        decrypted_text = ''.join([self.alphabet[idx] for idx in decrypted_blocks])
        return decrypted_text

    def recurrent_hill_cipher_encrypt(self, text, block_size, key_text_1, key_text_2):
            key1 = self.matrix_to_key(key_text_1)
            key2 = self.matrix_to_key(key_text_2)

            # Валидация первого ключа
            if len(key1.shape) != 2 or key1.shape[0] != key1.shape[1] or key1.shape != (block_size, block_size):
                raise KeyValidityError(f"Первый ключ должен быть квадратной матрицей {block_size}x{block_size}.")
            det1_int = int(round(np.linalg.det(key1)))
            if det1_int == 0 or math.gcd(det1_int % self.m, self.m) != 1:
                raise KeyValidityError("Определитель первого ключа вырожден или не взаимно прост с мощностью алфавита.")

            # Валидация второго ключа
            if len(key2.shape) != 2 or key2.shape[0] != key2.shape[1] or key2.shape != (block_size, block_size):
                raise KeyValidityError(f"Второй ключ должен быть квадратной матрицей {block_size}x{block_size}.")
            det2_int = int(round(np.linalg.det(key2)))
            if det2_int == 0 or math.gcd(det2_int % self.m, self.m) != 1:
                raise KeyValidityError("Определитель второго ключа вырожден или не взаимно прост с мощностью алфавитом.")

            blocks = self.text_to_block(text, block_size)
            encrypted_blocks = []

            for i, block in enumerate(blocks):
                if i == 0:
                    current_key = key1
                elif i == 1:
                    current_key = key2
                else:
                    # Рекуррентное правило: K_i = (K_i-2 * K_i-1) mod m
                    current_key = np.dot(key1, key2) % self.m
                    key1 = key2
                    key2 = current_key

                P = np.array(block).reshape(-1, 1)
                C = np.dot(current_key, P) % self.m
                encrypted_block = C.flatten().tolist()
                encrypted_blocks.extend(encrypted_block)

            encrypted_text = ''.join([self.alphabet[idx] for idx in encrypted_blocks])
            return encrypted_text
    def recurrent_hill_cipher_decrypt(self, encrypted_text, block_size, key_text_1, key_text_2):
            key1 = self.matrix_to_key(key_text_1)
            key2 = self.matrix_to_key(key_text_2)

            # Валидация первого ключа
            if len(key1.shape) != 2 or key1.shape[0] != key1.shape[1] or key1.shape != (block_size, block_size):
                raise KeyValidityError(f"Первый ключ должен быть квадратной матрицей {block_size}x{block_size}.")
            det1_int = int(round(np.linalg.det(key1)))
            if det1_int == 0 or math.gcd(det1_int % self.m, self.m) != 1:
                raise KeyValidityError("Определитель первого ключа вырожден или не взаимно прост с мощностью алфавита.")

            # Валидация второго ключа
            if len(key2.shape) != 2 or key2.shape[0] != key2.shape[1] or key2.shape != (block_size, block_size):
                raise KeyValidityError(f"Второй ключ должен быть квадратной матрицей {block_size}x{block_size}.")
            det2_int = int(round(np.linalg.det(key2)))
            if det2_int == 0 or math.gcd(det2_int % self.m, self.m) != 1:
                raise KeyValidityError("Определитель второго ключа вырожден или не взаимно прост с мощностью алфавита.")

            encrypted_blocks = self.text_to_block(encrypted_text, block_size)
            decrypted_blocks = []

            for i, block in enumerate(encrypted_blocks):
                if i == 0:
                    current_key = key1
                elif i == 1:
                    current_key = key2
                else:
                    # Ваше обновленное рекуррентное правило: K_i = (K_i-2 * K_i-1) mod m
                    current_key = np.dot(key1, key2) % self.m
                    key1 = key2
                    key2 = current_key

                # Находим обратную матрицу для текущего ключа
                det_float = np.linalg.det(current_key)
                det_int = int(round(det_float))
                det_mod = det_int % self.m
                
                try:
                    det_inv = pow(det_mod, -1, self.m)
                except ValueError:
                    raise KeyValidityError(f"На шаге {i+1} определитель ключа не имеет обратного по модулю.")
                    
                adjugate_matrix = np.round(np.linalg.inv(current_key) * det_float).astype(int)
                key_inv = (det_inv * adjugate_matrix) % self.m

                # Расшифровываем блок: P = (K^-1 * C) mod m
                C = np.array(block).reshape(-1, 1)
                P = np.dot(key_inv, C) % self.m
                decrypted_block = P.flatten().tolist()
                decrypted_blocks.extend(decrypted_block)

            decrypted_text = ''.join([self.alphabet[idx] for idx in decrypted_blocks])
            return decrypted_text
if __name__ == "__main__":
    user_alphabet = input("Пропишите '1', если по умолчанию следует использовать латинский строчный алфавит.\nВведите алфавит: ")
    if user_alphabet == '1':  
        app = BlockCiphers(string.ascii_lowercase)
    else:
        app = BlockCiphers(user_alphabet)
        
    text = input("Введите текст: ")
    block_size = int(input("Введите длину блока разбиения текста: "))
    
    cipher_type = input("Введите '1' для обычного шифра Хилла, '2' для рекуррентного: ")

    if cipher_type == '1':
        print(f"Введите матрицу ключа построчно (числа через пробел, нужно ввести {block_size} строк(и)):")
        key_rows = []
        for i in range(block_size):
            row = input(f"Строка {i + 1}: ")
            key_rows.append(row)
        key_text = "\n".join(key_rows)
        
        choice = input("Введите '1' для шифрования, '2' для расшифрования: ")
        if choice == '1':
            try:
                print("\nЗашифрованный текст:", app.hill_cipher_encrypt(text, block_size, key_text))
            except KeyValidityError as e:
                print(f"\nОшибка ключа: {e}")
        elif choice == '2':
            try:
                print("\nРасшифрованный текст:", app.hill_cipher_decrypt(text, block_size, key_text))
            except KeyValidityError as e:
                print(f"\nОшибка ключа: {e}")

    elif cipher_type == '2':
            print(f"Введите матрицу первого ключа построчно (числа через пробел, нужно ввести {block_size} строк(и)):")
            key_rows_1 = []
            for i in range(block_size):
                row = input(f"Строка {i + 1}: ")
                key_rows_1.append(row)
            key_text_1 = "\n".join(key_rows_1)

            print(f"Введите матрицу второго ключа построчно (числа через пробел, нужно ввести {block_size} строк(и)):")
            key_rows_2 = []
            for i in range(block_size):
                row = input(f"Строка {i + 1}: ")
                key_rows_2.append(row)
            key_text_2 = "\n".join(key_rows_2)

            action = input("Введите '1' для шифрования, '2' для расшифрования: ")
            try:
                if action == '1':
                    print("\nЗашифрованный текст:", app.recurrent_hill_cipher_encrypt(text, block_size, key_text_1, key_text_2))
                elif action == '2':
                    print("\nРасшифрованный текст:", app.recurrent_hill_cipher_decrypt(text, block_size, key_text_1, key_text_2))
            except KeyValidityError as e:
                print(f"\nОшибка ключа: {e}")