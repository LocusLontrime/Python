# accepted on codewars.com
palindrome=lambda n,c:(k:=c*n)[:n//2]+k[~-n//2::-1]


print(palindrome(7, "abc"))

print(len("palindrome=p=lambda n,c:c[0]+p(n-2,c[1:])+c[0]if len(c)>1else c[0]*n"))
print(len("palindrome=p=lambda n,c:c[0]+p(n-2,c[1:])+c[0]if len(c)-1else c[0]*n"))
print(len("palindrome=lambda n,c:c[:-1]+c[len(c)//2]+c[:-1][::-1]"))
print(len("palindrome=lambda n,c:c[:-1]+c[-1:]+c[:-1][::-1]"))
print(len("ambda n,c:c[:-1]+c[-1:]+c[:-1][::-1]"))
print(len("palindrome=lambda n,c:c[:-1]+c[-1:]*(n-2*len(c)+2)+c[:-1][::-1]"))
print(len("palindrome=lambda n,s:(s*n)[:n//2]+(s*n)[~-n//2::-1]"))
print(len("palindrome=lambda n,c:(k:=c*n)[:n//2]+k[~-n//2::-1]"))

