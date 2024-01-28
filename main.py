def main():
	print("Hello World")

# Find the all factors of x using a loop and the operator %
# % means find remainder,forexample 10%2=0;10%3=1
n = 52633
def get_all_factors(x):
    factors = []
    for i in range(1,x+1):
        if x%i == 0:
            factors.append(i)
    return factors

# Write a function that prints all factors of the given parameter x
def print_factor(x):
	print(x)


# your code here
if __name__ == '__main__':
	main()
	fac = get_all_factors(n)
	print_factor(fac)

	# Write a program that be able to find all factors of the numbers in the list l
	l = [52633, 8137, 1024, 999]
	for i in l:
		fac = get_all_factors(i)
		print_factor(fac)