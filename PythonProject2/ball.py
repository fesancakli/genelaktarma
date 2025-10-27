import numpy as np

balls = np.ones(12)

print(balls[0:4].sum())
a = input("a mi h mi")
b= int(input("hangi index"))

if a == "h":
    balls[b-1] = .8
elif a == "a":
    balls[b-1] = 1.2

def alg(balls : np.ndarray):
    if balls[0:4] == balls[4:8]:
        if balls[0:3] == balls[8:11]:
            if balls[11] > balls[0]:
                heavy = 1
            else :
                heavy = 0
            return 11 , heavy
        else:
            if balls[8] == balls[9]:
                if balls[10] > balls[8]:
                    heavy = 1
                else:
                    heavy = 0
                return heavy , 10
            elif balls[8] == balls[9]:




