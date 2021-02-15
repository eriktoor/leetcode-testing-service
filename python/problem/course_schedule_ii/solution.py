class Solution:
    
    def buildGraph(self, numCourses, prerequisites): 
        graph, visited = {}, {}
    
        for i in range(numCourses): 
            visited[i] = 0 
            graph[i] = set() 
            
        for p in prerequisites: 
            graph[p[1]].add(p[0])
            
        return graph, visited

    def isDagDfs(self, curr, result, graph, visited): # IS DAG 
        if visited[curr] == 1: return True
        elif visited[curr] == -1: return False
        visited[curr] = -1
        
        for child in graph[curr]:
            if self.isDagDfs(child, result, graph, visited) == False: return False
            
        visited[curr] = 1
        result.append(curr) #could also do .insert(0, curr) and not flip res at the end
        return True
    
    
    def course_schedule_ii(self, numCourses, prerequisites):
        graph, visited = self.buildGraph(numCourses, prerequisites)
        
        res = []
        
        for key in graph:
            if self.isDagDfs(key, res, graph, visited) == False: return []
        
        return res[::-1]