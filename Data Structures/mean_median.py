import math

class Solution:
    ##Complete the below codes
    # Function to find median of the array elements.
    def median(self, A, N):
        A.sort()

        if N % 2 == 0:
            idx = N // 2
            return round((A[idx - 1] + A[idx]) // 2)

        return round(A[N // 2])

        # If median is fraction then convert the median to integer and return

    # Function to find mean of the array elements.
    def mean(self, A, N):
        return round(sum(A) // N)


def main():
    T = int(input())

    while T > 0:
        N = int(input())
        a = [int(x) for x in input().strip().split()]
        ob = Solution()
        print(ob.mean(a, N), ob.median(a, N))

        T -= 1


if __name__ == "__main__":
    main()
