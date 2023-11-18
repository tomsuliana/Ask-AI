import subprocess

def get_answer(question):
    executable_name = "/home/uliana/lama/llama.cpp/./main"
    args = ["-m", "/home/uliana/lama/llama.cpp/models/7B/wizardlm-1.0-uncensored-llama2-13b.Q5_K_M.gguf", "-ins", '--in-prefix', '" "', "--color"]
    input_str = question
    process = subprocess.Popen([executable_name] + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    print("before communication")
    input_sent = False
    count = 0
    result = ''
    while True:
        try:
            if not input_sent:
                input_sent = True
                process.communicate(input=input_str.encode(), timeout=5)
            else:
                process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            line = process.stdout.readline()
            print(line.decode('UTF-8'))
            if ">" in line.decode('UTF-8'):
                line = line.decode('UTF-8')
                line = line.replace('> " "', ' ')
                line = line.replace('Текст', ' ')
                line = line.replace('"', ' ')
                result = result + line
                count = count + 1
                if count >= 1:
                    print("signal")
                    process.kill()
                    print("killing")
                    break
            else:
                result = result + line.decode('UTF-8')
        print("before trying")
    print("Сторонняя программа завершилась с кодом:", process.returncode)
    result = result.replace('\n', '<br>')
    print(result)
    return result


if __name__ == '__main__':
    get_answer("Привет")
