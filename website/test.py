# split '⠃⠗⠁⠊⠇⠇⠑⠠⠑⠙'
# into 'char 1' 'char 1 char 2' etc
splitted = [c for c in '⠃⠗⠁⠊⠇⠇⠑⠠⠑⠙']
splitted = [''.join(splitted[:i+1]) for i in range(len(splitted))]
print(splitted)
