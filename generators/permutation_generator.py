from typing import Any

def generate_permutations(items: list[Any]) -> list[list[Any]]:
    """Генерирует все варианты перестановок элементов указанного множества

    :param items: список элементов
    :raise TypeError: если параметр items не является списком
    :raise ValueError: если список элементов содержит дубликаты
    :return: список перестановок, где каждая перестановка список элементов
    множества
    """
    if not isinstance(items, list):
        raise TypeError("Параметр items не является списком")
    
    if len(items) != len(set(items)):
        raise ValueError("Список элементов содержит дубликаты")
    
    if not items:
        return []
    
    if len(items) == 1:
        return [items.copy()]
    
    permutations = []
    smaller_permutations = generate_permutations(items[:-1])
    last_item = items[-1]
    
    for perm in smaller_permutations:
        for i in range(len(perm) + 1):
            new_perm = perm.copy()
            new_perm.insert(i, last_item)
            permutations.append(new_perm)
    
    return permutations


def main():
    items = [1, 2, 3]
    print(generate_permutations(items))


if __name__ == "__main__":
    main()