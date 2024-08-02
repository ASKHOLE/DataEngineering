from datetime import datetime

color = {
    'b': 0,
    'r': 1,
    'g': 2,
    'y': 3,
    'blue': 4
}

method_lst = {
    'default': 0,
    'highlight': 1,
    'bold': 2
}

def color_print(s, method='default', front_color='blue', back_color='w'):
    print_time = str(datetime.now().strftime("%d/%m %H:%M:%S"))
    s += f' [{print_time}]'
    start = f'\033{method_lst[method]};3{color[front_color]};4{color[back_color]}m'
    end = '\033[0m'
    print(start + s + end)