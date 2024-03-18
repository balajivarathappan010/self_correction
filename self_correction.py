import sys
import g4f
import subprocess
import re

message = [{"role":"system","content":"you are an expert software developer with expertise in Python. Your task is to create creative solutions"},
           {"role":"system","content":"you are an expert in Python. Your task is to remove ALL text that is not needed to run the python code:"}]

def clean_code(code):
    clean_code = code.replace("```python","").replace("```","")
    return code if len(clean_code)==0 else clean_code.strip()

def loop(response):
    ms = ""
    for i in response:
        ms+=i
        print(i, end="", flush=True)
    return ms

def self_correct_code(code, error_message):
    message.append({"role":"system","content":f"The following Python code has an error:\n\n{code}\n\nError message:\n{error_message}\n\nPlease fix this error"})
    corrected_code = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=message
    )
    return corrected_code

def clean_self_correct_code(cleancode):
    message.append({"role":"system","content":f"Here is the Python Code{cleancode}\n\nYour task is to remove ALL text that is not needed to run the python code, only give code don't say anything:"})
    clean_corrected_code = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=message
    )
    return clean_code(clean_corrected_code)

def final_and_install_dependencies(executable_code):
    pattern = r'pip install ([^\s]+)'
    matches = re.findall(pattern, executable_code)

    for package_name in matches:
        try:
            subprocess.check_call(["pip", "install", package_name])
            print(f"Successfully installed {package_name}")
        except subprocess.CalledProcessError:
            print(f"Error installing {package_name}")

def save_code(executable_code, code_path):
    try:
        with open(code_path, 'w', encoding="utf-8") as f:
            f.write(executable_code)
        print(f"Code saved successfully to '{code_path}'")
    except Exception as e:
        print(f"Error saving code: {e}")

def execute_code(file_path):
    try:
        subprocess.run([sys.executable, file_path], check=True, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        error_message = e.stderr.strip()
        print(f"Error executing code: {error_message}")
        return False, error_message
    return True, None

def execute_code_with_self_correction(file_path):
    success, error_message = execute_code(file_path)    
    while(not success):
        with open(file_path, "r") as f:
            cur_code = f.read()
        print(f"{NEON_GREEN}Attemps failed. Trying to self-correct the code...{RESET_COLOR}")
        corrected_code = self_correct_code(cur_code, error_message)
        cleaned_corrected_code = clean_self_correct_code(corrected_code)
        executable_corrected_code = clean_code(cleaned_corrected_code)
        print(CYAN+executable_corrected_code+RESET_COLOR)
        save_code(executable_corrected_code, file_path)
        success, error_message = execute_code(file_path)
    return cur_code


if __name__=="__main__":
    goal = "simple weather monitoring website using free api"
    text = f"You are a super creative expert software developer with expertise in Python. Write a python code to {goal} with steps:"
    message.append({"role":"system","content":text})
    initial_code = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=message
    )
    print(initial_code)
    file_path = "my_path.py"
    cleaned_code = clean_self_correct_code(initial_code)
    executable_code = clean_code(cleaned_code)
    NEON_GREEN = "\033[38;2;57;255;20m"
    CYAN = "\033[96m"
    RESET_COLOR = "\033[0m"
    print(NEON_GREEN+executable_code+RESET_COLOR)
    final_and_install_dependencies(executable_code)
    save_code(executable_code, file_path)
    res, error_msg = execute_code(file_path)
    if not res:
        final_code = execute_code_with_self_correction(file_path)
        print(f"{NEON_GREEN}Successfull....{RESET_COLOR}")