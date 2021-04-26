file1 = open("../updatedmysterycodefiles/200_codes_for_mystery4_7_5.txt", "r")
codes = []
codes = file1.readlines()

code = codes[0]
# codes.remove(codes[0])
# # code.replace(" ", "")

# code = ''.join(code.split())
# code = code[0].strip()
code = code.strip()
codes.remove(codes[0])
print(code + "hi")
print("hfdg")
