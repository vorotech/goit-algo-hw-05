"""Mdodule contains binary search function."""

def binary_search(arr, target):
    """Performs binary search on a sorted array."""
    low, high = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = low + (high - low) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            upper_bound = arr[mid]

    return (iterations, upper_bound)

def main():
    """Main function."""
    sorted_array = [1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8]
    target = 4.0
    result = binary_search(sorted_array, target)
    print(result)  # Виведе (3, 4.5)

if __name__ == "__main__":
    main()
