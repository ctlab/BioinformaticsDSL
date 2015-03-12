#!/usr/bin/python3

def g(task, inp, out):
	text = ''
	text += task + ';'
	text += ' '.join(inp) + ';'
	text += ' '.join(out) + '\n'
	return text

def gen():
	text = ''
	text += g('a', ('1',), ('2',))
	text += g('b', ('1',), ('3',))
	text += g('c', ('3',), ('4',))
	text += g('d', ('2',), ('5',))
	return text


def main():
	fout = open('log.txt', 'w')
	fout.write(gen())
	print(gen())Aeyrwbb

if __name__ == '__main__':
	main()