from services.code_executor import run_code

code = """
print("Hello World")
"""

result = run_code(code, "python")
print(result)
