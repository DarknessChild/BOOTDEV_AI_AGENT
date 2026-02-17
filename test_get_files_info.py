from functions.get_files_info import get_files_info

print("Result for current directory:")
result_1 = get_files_info("calculator", ".")
for line in result_1.split("\n"):
    print(f"    {line}")
print("Result for 'pkg' directory:")
result_2 = get_files_info("calculator", "pkg")
for line in result_2.split("\n"):
    print(f"    {line}")
print("Result for '/bin' directory:")
result_3 = get_files_info("calculator", "/bin")
print(f"    {result_3}")
print("Result for '../' directory:")
result_4 = get_files_info("calculator", "../")
print(f"    {result_4}")
