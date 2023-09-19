# accepted on codewars.com

# Write a function that returns the longest contiguous palindromic substring in s.
# In the event that there are multiple longest palindromic substrings, return the
# first to occur.


# TODO: Complete in linear time xDD
def longest_palindrome(s):  # Manacher's algorithm
    sModified = ''

    for i in range(len(s)):
        sModified += '|' + s[i] if i != len(s) - 1 else '|' + s[i] + '|'

    print(f'sModified: {sModified}')

    maxRadii = [0] * len(sModified)

    center = 0
    maxPalindromeCenter = 0
    currentRadius = 0
    maxRadius = 0

    while center < len(sModified):

        while center - currentRadius >= 0 and center + currentRadius < len(sModified) and sModified[center - currentRadius] == sModified[center + currentRadius]:
            currentRadius += 1

        currentRadius -= 1  # one step back (we may change the cycling condition, but it will require more actions)
        maxRadii[center] = currentRadius

        if maxRadius < currentRadius:
            maxRadius = currentRadius
            maxPalindromeCenter = center
            print(f'maxRadius: {maxRadius}, maxPalindromeCenter: {maxPalindromeCenter}')

        oldCenter = center  # saved copy of center
        oldMaxRadius = currentRadius  # saved copy of maxCurrentRadius

        center += 1  # a one step to the right
        currentRadius = 0  # nullification current radius, we are now proceeding to the "mirror" section of palindrome analysis

        while center <= oldCenter + oldMaxRadius:  # the main cycling condition, while we are inside oldMaxPalindrome, we can use some previously calculated values to fasten the algo
            mirroredCenter = oldCenter - (center - oldCenter)
            maxMirroredRadius = oldCenter + oldMaxRadius - center

            if maxRadii[mirroredCenter] < maxMirroredRadius:  # if mirroredMaxPalindrome located inside oldMaxPalindrome then we can return maxRadii[mirroredCenter]
                maxRadii[center] = maxRadii[mirroredCenter]

                if maxRadius < maxRadii[mirroredCenter]:
                    maxRadius = maxRadii[mirroredCenter]
                    maxPalindromeCenter = center

                center += 1

            elif maxRadii[mirroredCenter] > maxMirroredRadius:  # if mirroredMaxPalindrome extends beyond the border of oldMaxPalindrome then we can say that maxRadius of
                # newPalindrome located around the center has maxRadius equals maxMirroredRadius, as the symbols at the edges of oldMaxPalindrome are different,
                # because it is a max possible palindrome located in the oldCenter point

                maxRadii[center] = maxMirroredRadius

                if maxRadius < maxMirroredRadius:
                    maxRadius = maxMirroredRadius
                    maxPalindromeCenter = center

                center += 1

            else:  # bottleneck point -> here we cannot predict a length of maxPalindrome located around the center, but we can continue calculating its length from maxMirroredRadius
                currentRadius = maxMirroredRadius
                break  # we can break the cycle early

    return sModified[maxPalindromeCenter - maxRadius + 1: maxPalindromeCenter + maxRadius + 1].replace("|", "")


print(longest_palindrome('ttaaftffftfaafatf'))
