#!/usr/bin/python3

def result2steps(r, graph, good):
	if r in graph:
		good.add(graph[r][0])
		for nr in graph[r][1]:
			result2steps(nr, graph, good)



def filter_tasks(tasks, result):
	graph = {}
	for task in tasks:
		for o in task[2]:
			graph[o] = (task[0], task[1])

	good = set()
	for r in result:
		result2steps(r, graph, good)

	return good



def main():
	fin = open('log.txt', 'r')
	tasks = []
	for line in fin:
		task, inf, outf = line.strip().split(';')
		tasks.append((task, inf.split(' '), outf.split(' ')))

	good = filter_tasks(tasks, ['5',])
	for task in tasks:
		if task[0] in good:
			print(task)

if __name__ == '__main__':
	main()