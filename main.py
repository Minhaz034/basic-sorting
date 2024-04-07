from flask import Flask, render_template, request
from random import randint
import time

app = Flask(__name__)

def merge(left, right):
    """Merge two sorted lists into a single sorted list."""
    result, left_index, right_index = [], 0, 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result

def merge_sort(arr):
    """Sort an array using the merge sort algorithm."""
    if len(arr) < 2:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def heapify(arr, n, i):
    """Helper function to maintain the heap property."""
    largest, left, right = i, 2 * i + 1, 2 * i + 2
    if left < n and arr[largest] < arr[left]:
        largest = left
    if right < n and arr[largest] < arr[right]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapsort(arr):
    """Sort an array using the heap sort algorithm."""
    start_time = time.time()
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    execution_time = time.time() - start_time
    return arr, execution_time

def partition_last_elem(arr, start, end):
    """Partition the array using the last element as the pivot."""
    pivot_index = start - 1
    pivot = arr[end]
    for j in range(start, end):
        if arr[j] < pivot:
            pivot_index += 1
            arr[pivot_index], arr[j] = arr[j], arr[pivot_index]
    arr[pivot_index + 1], arr[end] = arr[end], arr[pivot_index + 1]
    return pivot_index + 1

def quicksort(arr, start, end):
    """Sort an array using the quick sort algorithm."""
    if start < end:
        pivot_index = partition_last_elem(arr, start, end)
        quicksort(arr, start, pivot_index - 1)
        quicksort(arr, pivot_index + 1, end)

def partition_3_median(arr, start, end):
    """Partition using the median of three methodology."""
    indices = [start, end, (start + end) // 2]
    values = [arr[i] for i in indices]
    median_value = sorted(values)[1]
    median_index = indices[values.index(median_value)]
    arr[median_index], arr[end] = arr[end], arr[median_index]
    return partition_last_elem(arr, start, end)

def quicksort_3M(arr, start, end):
    """Sort an array using the quick sort algorithm with a 3-median pivot."""
    if start < end:
        pivot_index = partition_3_median(arr, start, end)
        quicksort_3M(arr, start, pivot_index - 1)
        quicksort_3M(arr, pivot_index + 1, end)

def insertion_sort(arr):
    """Sort an array using the insertion sort algorithm."""
    start_time = time.time()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    execution_time = time.time() - start_time
    return arr, execution_time

def selection_sort(arr):
    """Sort an array using the selection sort algorithm."""
    start_time = time.time()
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    execution_time = time.time() - start_time
    return arr, execution_time

def bubble_sort(arr):
    """Sort an array using the bubble sort algorithm."""
    start_time = time.time()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    execution_time = time.time() - start_time
    return arr, execution_time

def generate_random_array(size):
    """Generate a list of random integers."""
    return [randint(10, 600) for _ in range(size)]

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home_f():
    if request.method == 'POST':
        size = int(request.form.get("alen_", 0))
        algorithm = request.form.get("algo")
        arr = generate_random_array(size)
        start_time = time.time()
        
        if algorithm == "Mergesort":
            sorted_arr = merge_sort(arr)
        elif algorithm == "Heapsort":
            sorted_arr, _ = heapsort(arr[:])
        elif algorithm == "Quicksort":
            quicksort(arr, 0, len(arr) - 1)
            sorted_arr = arr
        elif algorithm == "Quicksort3":
            quicksort_3M(arr, 0, len(arr) - 1)
            sorted_arr = arr
        elif algorithm == "Insertionsort":
            sorted_arr, _ = insertion_sort(arr[:])
        elif algorithm == "Selectionsort":
            sorted_arr, _ = selection_sort(arr[:])
        elif algorithm == "Bubblesort":
            sorted_arr, _ = bubble_sort(arr[:])
        else:
            sorted_arr = []
        
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return render_template('home.html', algo=algorithm, alen_=size, sort=sorted_arr, arr=arr, extime=execution_time)

    return render_template('home.html')

@app.route("/compare", methods=['GET', 'POST'])
def comp_f():
    if request.method == 'POST':
        size = int(request.form.get("alen_", 0))
        arr = generate_random_array(size)
        algorithms = {
            "Mergesort": lambda x: merge_sort(x),
            "Heapsort": lambda x: heapsort(x[:])[0],
            "Quicksort": lambda x: quicksort(x[:], 0, len(x) - 1) or x,
            "Quicksort3": lambda x: quicksort_3M(x[:], 0, len(x) - 1) or x,
            "Insertionsort": lambda x: insertion_sort(x[:])[0],
            "Selectionsort": lambda x: selection_sort(x[:])[0],
            "Bubblesort": lambda x: bubble_sort(x[:])[0],
        }
        data = []
        
        for name, func in algorithms.items():
            copy_arr = arr[:]
            start_time = time.perf_counter()
            func(copy_arr)
            execution_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
            data.append([name, execution_time])
        
        return render_template('chart.html', data_for_chart=data, input_size_string=f"Length of Input array is {size}.")

    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug=True)
