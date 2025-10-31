
def aaa(x):
    return x[1]

list = [[100,11],[21,1],[37,14],[245,15],[12,10000],[523,16]]

print(list)


list.sort(key=aaa)

print(list)





