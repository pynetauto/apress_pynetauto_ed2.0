import timeit

# Method 1: String Concatenation
method1_time = timeit.timeit("'Around ' + 'the ' + 'World ' + 'in ' + '100 ' + 'days.'", number=1000000)

# Method 2: String Formatting
method2_time = timeit.timeit("('{} {} {} {} {} {}'.format('Around', 'the', 'World', 'in', '100', 'days.'))", number=1000000)

# Method 3: String Join
method3_time = timeit.timeit("' '.join(['Around', 'the', 'World', 'in', '100', 'days.'])", number=1000000)

# Method 4: f-Strings
method4_time = timeit.timeit("'Around' + ' the' + ' World' + ' in' + ' 100' + ' days.'", number=1000000)

# Method 5: String Literal with Spaces
method5_time = timeit.timeit("'Around the World in 100 days.'", number=1000000)

# Print the execution times in microseconds
print("Method 1 Time:", method1_time * 1e6, "microseconds")
print("Method 2 Time:", method2_time * 1e6, "microseconds")
print("Method 3 Time:", method3_time * 1e6, "microseconds")
print("Method 4 Time:", method4_time * 1e6, "microseconds")
print("Method 5 Time:", method5_time * 1e6, "microseconds")