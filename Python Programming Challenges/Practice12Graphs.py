#PRACTICE CODE FOR GRAPHS

class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.graph:
            self.graph[vertex1].append(vertex2)
        else:
            self.graph[vertex1] = [vertex2]

        #Comment out the lines below for a directed graph
        if vertex2 in self.graph:
            self.graph[vertex2].append(vertex1)
        else:
            self.graph[vertex2] = [vertex1]

    def DFS(self, start_vertex):
        visited = set()
        output = []

        def dfs(vertex):
            if vertex not in visited:
                visited.add(vertex)
                output.append(vertex)
                for neighbor in self.graph[vertex]:
                    dfs(neighbor)

        dfs(start_vertex)
        return output
    
    def BFS(self, start_vertex):
        visited = set()
        queue = [start_vertex]
        output = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                output.append(vertex)
                queue.extend()


#Functions
def create_adjacency_list():
    a_graph = Graph()
    a_graph.add_vertex("A")
    a_graph.add_vertex("B")
    a_graph.add_vertex("C")
    a_graph.add_vertex("D")
    a_graph.add_vertex("E")

    a_graph.add_edge("A", "B")
    a_graph.add_edge("A", "C")
    a_graph.add_edge("B", "D")
    a_graph.add_edge("D", "E")

    return a_graph.graph

def convert_graph_to_matrix(graph):
    print("", end="\t")
    for g in graph:
        print (g, end="\t")
    print("--")
    for g in graph:
        print (g, end="\t")
        for h in graph:
            if h in graph[g]:
                print (1, end="\t")
            else:
                print (0, end="\t")
            # print(graph[g][0], end="\t")
            # print (f"Ind: {index}", end="\t")
        print("--")

def add_vertex_and_edge_to_list(vertex, edge1, edge2):
    b_graph = Graph()
    b_graph.graph = create_adjacency_list()
    b_graph.add_vertex(vertex)
    b_graph.add_edge(vertex, edge1)
    b_graph.add_edge(vertex, edge2)

    return b_graph.graph

def find_one_degree_vertices(c_graph):
    one_degree_vertices = []
    for a in c_graph.graph:
        if len(c_graph.graph[a]) == 1:
            one_degree_vertices.append(a)
    return one_degree_vertices

#Executions
a_graph = Graph() 
a_graph.graph = create_adjacency_list()
print(f"Adjacency list: {a_graph.graph}") #Solution 1 simple
print(f"One degree vertices: {find_one_degree_vertices(a_graph)}") #Solution 1 expert
convert_graph_to_matrix(a_graph.graph) #Solution 1 intermediate
b_graph = Graph()
b_graph.graph = add_vertex_and_edge_to_list('F', 'A', 'E')
print(f"Updated Adjacency list: {a_graph.graph}") #Solution 1 advanced
print(f"One degree vertices: {find_one_degree_vertices(b_graph)}") #Solution 1 expert

