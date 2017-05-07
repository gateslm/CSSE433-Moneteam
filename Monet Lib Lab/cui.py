import os

if __name__ == "__main__":
    # main()
    print "Library system has been brought online"
    while 1:
        myinput = raw_input("\nPlease type in your command: \n")
        if (myinput == "exit"):
            break
        myinput = "python library.py -fn "+myinput
        print myinput
        os.system(myinput)
    print " Library system has shut down"
