import google.generativeai as genai

genai.configure(api_key="AIzaSyD7AQXTeguhSaw0ZJpbko8JX4JfI5JVY3o")

def extract_rules_gemini(instruction_text):
    model = genai.GenerativeModel('models/gemini-1.5-pro-002')
    response = model.generate_content(instruction_text)
    with open("D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\extracted_rules.py", "w") as f:
        f.write(response.text)
    print(response.text)
    return response.text
