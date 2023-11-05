import time

start_timer = time.mktime(time.localtime())

big_number = range(10000000)
for i in big_number:
    print(i, end=" ")

total_time = time.mktime(time.localtime()) - start_timer

print("Total time:", total_time, "seconds")
