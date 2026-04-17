from functions.get_file_content import get_file_content

print(
    f'lorem.txt >> length: {len(get_file_content('calculator', 'lorem.txt'))} \n last line: {get_file_content('calculator', 'lorem.txt')[-60:]} \n')
print(
    f'main.py >> length: {len(get_file_content('calculator', 'main.py'))} \n content: {get_file_content('calculator', 'main.py')} \n')
print(
    f'/bin/cat >> length: {len(get_file_content('calculator', '/bin/cat'))} \n content: {get_file_content('calculator', '/bin/cat')} \n')
print(
    f'pkg/does_not_exist.py >> length: {len(get_file_content('calculator', 'pkg/does_not_exist.py'))} \n content: {get_file_content('calculator', 'pkg/does_not_exist.py')} \n')
print(
    f'pkg/calculator >> length: {len(get_file_content('calculator', 'pkg/calculator.py'))} \n content: {get_file_content('calculator', 'pkg/calculator.py')} \n')