
arrayTest = []
arrayTest.append(["person", 2000, [100,100,200,200]])
arrayTest.append(["person", 500, [20,20,100,200]])
arrayTest.append(["cat", 50, [10,20,200,200]])
arrayTest.append(["person", 2000, [100,100,200,200]])

oque = [array[0] for array in arrayTest]
distinct = list(set(oque))
print(distinct)