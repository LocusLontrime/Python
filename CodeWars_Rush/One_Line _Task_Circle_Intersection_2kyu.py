from numpy import*;circleIntersection=lambda a,b,r:r*r*(lambda l:l<1and arccos(l)-l*(1-l*l)**.5)(hypot(*subtract(b,a))/r/2)//.5

print(circleIntersection([0, 0],[0, 10],10))
print(circleIntersection([-12, 20],[43, -49],23))

print(hypot(*subtract([3, 4], [1, 2])/2/2))

