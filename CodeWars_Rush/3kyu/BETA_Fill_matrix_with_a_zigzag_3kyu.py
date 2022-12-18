# accepted on codewars.com

def determinate_value(j,i,n):
    d=j+i+1
    return n**2-c(n-1-j,n-1-i,2*n-d)+1 if d>n else c(j,i,d)
def c(j,i,d):
    return d*(d-1)//2+(i+1 if d%2 else j+1)