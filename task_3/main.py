"""Module for comparing the performance of search alghorithms."""

from pathlib import Path
import timeit
import pandas as pd


def kmp_search(main_string, pattern):
    """Implementation of the Knuth-morris search algorithm."""

    def compute_lps(pattern):
        """Computes the longest prefix suffix array for the pattern."""
        lps = [0] * len(pattern)
        length = 0
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    m = len(pattern)
    n = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < n:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == m:
            return i - j

    return -1  # якщо підрядок не знайдено


def boyer_moore_search(text, pattern):
    """Implementation of the Boyer-Moore search algorithm."""

    def build_shift_table(pattern):
        """Builds the shift table for the pattern."""
        table = {}
        length = len(pattern)
        # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
        for index, char in enumerate(pattern[:-1]):
            table[char] = length - index - 1
        # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
        table.setdefault(pattern[-1], length)
        return table

    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


def rabin_karp_search(main_string, substring):
    """Implementation of the Rabin-Karp search algorithm."""

    def polynomial_hash(s, base=256, modulus=101):
        """Hash function that returns the hash value of the string."""
        n = len(s)
        hash_value = 0
        for i, char in enumerate(s):
            power_of_base = pow(base, n - i - 1) % modulus
            hash_value = (hash_value + ord(char) * power_of_base) % modulus
        return hash_value

    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def read_file(file_path):
    """Reads the content of the file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def main():
    """Main function."""

    texts = {"text_1": "", "text_2": ""}

    base_path = Path(__file__).resolve().parent

    # Зчитуємо вміст файлів
    try:
        texts["text_1"] = read_file(Path(base_path, "text_1.txt"))
        texts["text_2"] = read_file(Path(base_path, "text_2.txt"))
    except FileNotFoundError as e:
        print(f"Error: {e.strerror}")

    # Substrings
    existing_substrings = [
        "розподілених у структурі",
        "формування рекомендацій аналогічно",
    ]
    non_existing_substrings = ["пошук неможливий", "пошук неможливий"]

    # Functions to test
    functions = {
        "Boyer-Moore": boyer_moore_search,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp_search,
    }

    # Measure time
    results = []

    for key, existing_substring, non_existing_substring in zip(
        texts.keys(), existing_substrings, non_existing_substrings
    ):
        for name, func in functions.items():
            time_existing = timeit.timeit(
                lambda: func(texts[key], existing_substring), number=1000
            )
            time_non_existing = timeit.timeit(
                lambda: func(texts[key], non_existing_substring), number=1000
            )
            
            results.append((name, key, time_existing, time_non_existing))

    # Visualize the results
    df = pd.DataFrame(results, columns=["Algorithm", "Text", "Time Existing", "Time Non-Existing"])
    print(df)


if __name__ == "__main__":
    main()
