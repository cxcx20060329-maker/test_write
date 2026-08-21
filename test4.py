# 方法1:
nums = [3, 1, 2, 3, 4, 1, 2]

result = []

for num in nums:
    if num not in result:
        result.append(num)

print(result)

# 方法二:
nums = [3, 1, 2, 3, 4, 1, 2]

result = list(dict.fromkeys(nums))

print(result)


# 方法3:
nums = [3, 1, 2, 3, 4, 1, 2]

seen = set()
result = []

for num in nums:

    if num not in seen:
        seen.add(num)
        result.append(num)

print(result)