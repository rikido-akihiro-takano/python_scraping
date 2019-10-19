

def recursive(a:int):------3
    print(a)---------------3
    a+= 1------------------a=4
    a= recursive(a)---------print(4), a=5, print(5), a=6, 
    return a

init= 0


recursive(init)