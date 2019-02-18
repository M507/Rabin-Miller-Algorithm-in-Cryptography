import math
import random
import sys

debug = 0

"""
p - 1 = 2^(u)* r

This function finds r and u 
1 - r and u have to be whole numbers
2 - We need to divide (p-1) by 2 until it cannot be divided to a whole number
3 - Each time we divide by 2, we increment u
"""
def step1(p):
    r = p - 1
    u = 0
    while (r % 2 == 0):
        r /= 2
        u += 1
    r = int(r)
    u = int(u)
    return r,u


"""
Input: Prime candidate p and security parameter s 
Output: boolean, Whether it's probably prime or composite. 
"""
def is_prime(p, s):
    # First find r and u.
    r,u = step1(p)
    # 1
    for i in range(s):
        # Generate random a where 2 <= a <= (p - 2)
        a = random.randint(2,p - 1)
        # 1.2
        z = pow(a, r, p)
        # 1.3
        if ((z != 1 ) and (z != p - 1)):
            # 1.4
            for j in range(1,u):
                z = pow(z, 2, p)
                if z == 1:
                    # Found a non-trivial square root of unity so p is composite.
                    return False
                # 1.5
                if z == p - 1:
                    # Cannot proof P is composite.
                    break
            else:
                # If x is never equaled p - 1, p is composite.
                return False
    return True

"""
This function starting by creating an empty list. 
Then it starts testing the odd numbers from 105001 to 115001.
Each time it finds that a number is a prime number it increments positives, otherwise increments composite.
After it finishes each number it inputs the result into gather_information() which gather
the highest 10 probabilities and adds them to the created list in the beginning.
Finally, executes final_step() to sort the result from the list "l" and print the top 10 probabilities. 
"""
def work(fromNum,toNum):
    l=[]
    for p in range(int(fromNum), int(toNum),2):
    #for p in range(105001, 105021,2):
        composite = 0
        positives = 0
        for i in range(1, 20):
            if (is_prime(p,1)):
                positives += 1
            else:
                composite += 1
        if (composite >= 1):
            r = float(float(positives)/(float(positives+composite)))

            if debug:
                print(str(p)+" Error Probability: "+str(round(float(r),3)))
            l = gather_information(l,p,round(float(r),3))
    final_step(l)


"""
Gather the highest 10 probabilities and adds them to the created list in the beginning.
"""
def gather_information(l,p,probability):
    if len(l) >= 10:
        for i in range(len(l)):
            if probability > l[i][1]:
                l.pop(i)
                if debug:
                    print(l)
                l.append([p,probability])
                if debug:
                    print("New")
                break
    else:
        if debug:
            print("First")
        l.append([p,probability])
    return l

"""
Sort the result from the list "l" and print the top 10 probabilities.
"""
def final_step(l):
    copy_of_l = l
    print("Final results:")
    sortedList = []
    greater = l[0][1]
    greater_index = 0
    for i in range(len(l)):
        for j in range(len(l)):
            if greater < l[j][1]:
                greater = l[j][1]
                greater_index = j
        sortedList.append(l[greater_index])
        l.pop(greater_index)
        greater = 0
        greater_index = 0
    if debug:
        print(copy_of_l)
        print(sortedList)
    print("\nNumber: %d The Largest Error Probability : %f \n" % (sortedList[0][0], sortedList[0][1]))
    for element in sortedList:
        print("Number: %d Error Probability: %f" % (element[0], element[1]))
        ##print("Number: "+str(element[0])+" Error Probability: "+str(element[1]))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Arguments:"
              "RM-Algorithm.py [from] [to]"
              ""
              "Ex: RM-Algorithm.py 105001 115001")
        exit(0)
    else:
        work(sys.argv[1],sys.argv[2])
