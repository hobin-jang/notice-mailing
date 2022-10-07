def test(num):
    num.append(123)
    num.append(456)

def reset(num) : 
    num.clear()

num = []
test(num)
print(num)

reset(num)
print(num)

# 위 두 개는 모두 call by reference