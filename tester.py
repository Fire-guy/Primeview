# def JobScheduling(Jobs):
#       l=[[Job[1],Job[2]] for Job in Jobs]
#       maxi=float('-inf')
#       for j in l:
#         maxi=max(maxi,j[0])
#       parent=[i for i in range(maxi+1)]
#       parent[0]=-1
#       def find_parent(s):
#         if s==0 or s==-1:
#           return -1
#         if parent[s]!=s:
#           parent[s]=find_parent(parent[s])
#         return parent[s]

     
#       l.sort(key=lambda x: -x[1])
#       profit,ans=0,0
#       for j in l:
#           p=find_parent(j[0])
          
#           if p==-1:
#             continue
#           ans+=1
#           profit+=j[1]
#           parent[p]=find_parent(p-1)
          
#       return ans,profit

# Jobs=[ [1, 2, 100] , [2, 1, 19] , [3, 2, 27] , [4, 1, 25] , [5, 1, 15] ]
# print(JobScheduling(Jobs))
import collections
def get_paths(graph,colors,n):
    adj=[[] for _ in range(n+1)]
    # print("adj len is ",len(adj))
    for edge in graph:
        adj[edge[0]].append(edge[1])
        adj[edge[1]].append(edge[0])
    
    c=collections.defaultdict(int)
    for color in colors:
        c[int(color)]+=1
    
    visited=[False]*(n+1)
    ans=[0]*(n+1)
    def dfs(node):
        visited[node]=True
        my_color=int(colors[node-1])
        ones,zeroes=0,0
        for n in adj[node]:
            if not visited[n]:
                one,zero=dfs(n)
                ones+=one
                zeroes+=zero
        if my_color==1:
            ones+=1
        else:
            zeroes+=1
        ans[node]=ones*zeroes
        return ones,zeroes
        
    dfs(1)
    return ans
        
graph=[[3,1],[4,3],[5,3],[2,4]]
color="11110"
N=5

print(get_paths(graph,color,N))
