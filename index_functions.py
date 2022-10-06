from re import compile, finditer

functions_directory = './/utils//functions.py'
pattern = compile("def (.*)\(")

index = {}
for i, line in enumerate(open(functions_directory)):
    for match in finditer(pattern, line):
        name_function = match.groups()[0]
        
        print(name_function)
        print(name_function.__doc__)
        print('\n\n')