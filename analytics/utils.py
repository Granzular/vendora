

def log(msg):
    try:
        with open("logs.txt",'x') as fd:
            fd.close()
    except FileExistsError:
        pass
    with open("logs.txt",'a') as fd:
        fd.write(msg)
        fd.write("\n")
        fd.close()
