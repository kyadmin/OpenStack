__author__ = 'andre'

def wrapper(func):    #wraper(website)
    def inner():
        print "before"
        func()
        print("after")
    return inner()
@wrapper
def website():
    print "hello world"

if __name__ == '__main__':
    website()