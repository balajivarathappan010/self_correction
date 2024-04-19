import sys
import g4f
from g4f.client import Client
import subprocess
import re
from .searching import API_Searching

client = Client()
class SelfCorrection:
    def __init__(self):
        self.message = [{"role": "system", "content": "you are an expert software developer with expertise in Python. Your task is to create creative solutions"},
               {"role": "system", "content": "you are an expert in Python. Your task is to remove ALL text that is not needed to run the python code:"}]
        self.NEON_GREEN = "\033[38;2;57;255;20m"
        self.CYAN = "\033[96m"
        self.RESET_COLOR = "\033[0m"

    def clean_code(self, code):
        clean_code = code.replace("```python","").replace("```","")
        return code if len(clean_code)==0 else clean_code.strip()

    def loop(self, response):
        ms = ""
        for i in response:
            ms += i
            print(i, end="", flush=True)
        return ms

    def self_correct_code(self, code, error_message):
        self.message.append({"role": "system", "content": f"The following Python code has an error:\n\n{code}\n\nError message:\n{error_message}\n\nPlease fix this error"})
        corrected_code = client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message)
        response = corrected_code.choices[0].message.content
        return response

    def clean_self_correct_code(self, cleancode):
        self.message.append({"role": "system", "content": f"Here is the Python Code{cleancode}\n\nYour task is to remove ALL text that is not needed to run the python code, only give code don't say anything:"})
        clean_corrected_code = client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message)
        response = clean_corrected_code.choices[0].message.content
        return self.clean_code(response)

    def final_and_install_dependencies(self, executable_code):
        pattern = r'pip install ([^\s]+)'
        matches = re.findall(pattern, executable_code)

        for package_name in matches:
            try:
                subprocess.check_call(["pip", "install", package_name])
                print(f"Successfully installed {package_name}")
            except subprocess.CalledProcessError:
                print(f"Error installing {package_name}")

    def save_code(self, executable_code, code_path):
        try:
            with open(code_path, 'w', encoding="utf-8") as f:
                f.write(executable_code)
            print(f"Code saved successfully to '{code_path}'")
        except Exception as e:
            print(f"Error saving code: {e}")

    def execute_code(self, file_path):
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
                words = file_content.split()
            if "streamlit" in words:
                subprocess.run([sys.executable, "-m", "streamlit", "run", file_path], check=True, stderr=subprocess.PIPE, text=True)
            else:
                subprocess.run([sys.executable, file_path], check=True, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            error_message = e.stderr.strip()
            print(f"Error executing code: {error_message}")
            return False, error_message
        return True, None
    @classmethod
    def execute_code_with_self_correction(cls, file_path):
        success, error_message = cls.execute_code(file_path)    
        while not success:
            with open(file_path, "r") as f:
                cur_code = f.read()
            print(f"{cls.NEON_GREEN}Attempts failed. Trying to self-correct the code...{cls.RESET_COLOR}")
            corrected_code = cls.self_correct_code(cur_code, error_message)
            cleaned_corrected_code = cls.clean_self_correct_code(corrected_code)
            executable_corrected_code = cls.clean_code(cleaned_corrected_code)
            print(f"{cls.CYAN}{executable_corrected_code}{cls.RESET_COLOR}")
            cls.save_code(executable_corrected_code, file_path)
            success, error_message = cls.execute_code(file_path)
        return cur_code

    def main(self, goal):
        if "API" in goal or "api" in goal:
            text = f"You are a super creative expert software developer with expertise in Python. Write a Python code to {goal}, use the following API {API_Searching()} and the city is Cuddalore. Give steps first after give code"
        else:
            text = f"You are a super creative expert software developer with expertise in Python. Write a Python code to {goal}. Give steps first after give code"
        self.message.append({"role": "system", "content": text})
        initial_code = client.chat.completions.create(model="gpt-3.5-turbo", messages=self.message)
        response = initial_code.choices[0].message.content
        print(response)
        file_path = "file/my_path.py"
        cleaned_code = self.clean_self_correct_code(response)
        executable_code = self.clean_code(cleaned_code)
        print(f"{self.NEON_GREEN}{executable_code}{self.RESET_COLOR}")
        self.final_and_install_dependencies(executable_code)
        self.save_code(executable_code, file_path)
        res, error_msg = self.execute_code(file_path)
        if not res:
            final_code = self.execute_code_with_self_correction(file_path)
            print(f"{self.NEON_GREEN}Successful....{self.RESET_COLOR}")
