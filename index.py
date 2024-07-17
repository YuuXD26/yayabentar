from flask import Flask, request, render_template_string
import itertools

app = Flask(__name__)

def is_solution(words, result, mapping, operation):
    for word in words:
        if mapping[word[0]] == '0':
            return False
    if mapping[result[0]] == '0':
        return False

    words_int = [int(''.join(str(mapping[c]) for c in word)) for word in words]
    result_int = int(''.join(str(mapping[c]) for c in result))

    if operation == 'tambah': 
        return sum(words_int) == result_int
    elif operation == 'kurang':  
        return words_int[0] - sum(words_int[1:]) == result_int
    elif operation == 'kali': 
        prod = 1
        for num in words_int:
            prod *= num
        return prod == result_int
    elif operation == 'bagi':  
        try:
            div = words_int[0]
            for num in words_int[1:]:
                div /= num
            return div == result_int
        except ZeroDivisionError:
            return False
    return False

def solve_cryptarithm(words, result, operation):
    unique_chars = set(''.join(words) + result)
    if len(unique_chars) > 10:
        return "Too many unique characters!"

    digits = '0123456789'
    for perm in itertools.permutations(digits, len(unique_chars)):
        mapping = dict(zip(unique_chars, perm))
        if is_solution(words, result, mapping, operation):
            words_int = [''.join(mapping[c] for c in word) for word in words]
            result_int = ''.join(mapping[c] for c in result)
            operator = {'tambah': '+', 'kurang': '-', 'kali': '*', 'bagi': '/'}[operation]
            return f"{' '.join(words_int[:-1])} {operator} {words_int[-1]} = {result_int}"
    
    return "No solution found."

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        words = request.form['words'].split()
        result_word = request.form['result']
        operation = request.form['operation']
        result = solve_cryptarithm(words, result_word, operation)

    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cryptarithm Solver</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="flex items-center justify-center min-h-screen -mt-20 p-4">
        <form method="post" class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
            <div class="mb-7 w-full text-center">
                <h1 class="text-3xl font-semibold text-blue-500">Cryptarithm Solver</h1>
                <p class="text-xs text-gray-500 font-semibold">by ItsBayy</p>
            </div>
            <div class="mb-4">
                <label class="block text-gray-700 mb-2">Masukkan kata</label>
                <input type="text" name="words" placeholder="Masukkan kata..." class="w-full px-4 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <p class="text-sm mt-1 text-gray-500">&#x2139; Gunakan spasi untuk memisahkan kata!</p>
            </div>
            <hr class="text-gray-500 mb-4 mt-4">
            <div class="mb-4">
                <label class="block text-gray-700 mb-2">Masukkan kata hasil</label>
                <input type="text" name="result" placeholder="Masukkan kata hasil..." class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div class="mb-4 w-full flex flex-wrap justify-between">
                <div class="flex items-center mb-2">
                    <input type="radio" id="tambah" name="operation" value="tambah" class="mr-2">
                    <label for="tambah" class="text-gray-700">Tambah</label>
                </div>
                <div class="flex items-center mb-2">
                    <input type="radio" id="kurang" name="operation" value="kurang" class="mr-2">
                    <label for="kurang" class="text-gray-700">Kurang</label>
                </div>
                <div class="flex items-center mb-2">
                    <input type="radio" id="kali" name="operation" value="kali" class="mr-2">
                    <label for="kali" class="text-gray-700">Kali</label>
                </div>
                <div class="flex items-center mb-2">
                    <input type="radio" id="bagi" name="operation" value="bagi" class="mr-2">
                    <label for="bagi" class="text-gray-700">Bagi</label>
                </div>
            </div>
            <div class="text-center">
                <button type="submit" class="w-full font-semibold px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">Cryptarithm</button>
            </div>
        </form>
    </div>
    <div class="bg-gray-100 flex items-center justify-center -mt-40 p-4">
        <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md text-center">
            <p class="text-md font-semibold">Hasil Cryptarithm</p>
            <p class="text-2xl font-semibold">{{ result }}</p>
        </div>
    </div>
</body>
</html>''', result=result)

if __name__ == '__main__':
    app.run(debug=True)
