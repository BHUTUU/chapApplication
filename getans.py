for i in range(0, 100000):
    if((1+i)**i + i**(1+i) == 17):
        print("The value of a is {}, and b is {}".format(str(i+1), str(i)))