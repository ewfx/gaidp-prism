import pandas as pd
from preprocessing import load_and_preprocess_data
from rule_extraction import extract_rules_gemini
from validation import validate_transactions
from anomaly_detection import detect_anomalies

regulatory_rules=r'D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\fed_regulations.txt'
data_meta=r'D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\fed_metadata.txt'
with open(regulatory_rules, 'r') as file:
    regulatory_rules = file.read()
with open(data_meta, 'r') as file:
    data_meta = file.read()
with open(r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\src\rules_orignal.py", "r") as file:
    python_code = file.read()
def_loan_data_path=r"D:\DataProfiling_TechnologyHackathon\data_profiling-main\data_profiling-main\data\synthetic_data.csv"
def_loan_data=pd.read_csv(def_loan_data_path)

def run_pipeline(loan_data, context):
    flag=False
    anomaly_data=pd.DataFrame()
    if loan_data.empty:
        loan_data=def_loan_data
    print("Step 1: Preprocessing Data...")
    df= load_and_preprocess_data(loan_data)

    print("Step 2: Extracting Validation Rules...")
    instruction_text = f"""
     Role: "You are an expert in financial compliance and Python programming. Your task is to Use the user context if provided to add or refine existing rules in regulatory instructions.
     Generate a Python script that enforces these the rules. only create function for validation asked in User context.

     output: only executable code WITHOUT any kind of errors.
     Instructions:
     Generate a Python function that validates corporate loan details based on the rule provided in the user context. The function should return a structured Validation Results in dictionary format containing:
     valid (Boolean): Whether the transaction passes all checks.
     flags (List): A list of detected compliance issues, append to the existing list.
     remediation (List): Suggested steps to fix or investigate flagged issues, append to the existing list.

    Corpporate Loan data fields:
    {data_meta}

    User context:
    {context}

    Example python code:
    {python_code}

     Remediation Actions:
     For flagged transactions, suggest appropriate actions, such as:
     Adjustments: Correcting discrepancies in amounts, currencies, and missing remarks.
     Explanations: Requesting additional documentation or validation from the user.
     Compliance Steps: Triggering enhanced due diligence, requesting source of funds, or blocking the transaction if risk is too high.

     Expected Output Format:
     The LLM should return a Python script with NO ERRORS that:

     Defines a validate_transaction(transaction, seen_ids, seen_facility_ids) function.
     ONLY Implements validation rules in the user context listed above.
     Uses datetime, pytz, and iso4217 for compliance checks.
     Returns a structured validation report (valid, flags, risk_score, remediation).
     Provides an example transaction and runs validation on it.
     run the generated code to check for type errors, value errors, AttributeError and other errors and rectify it for every function.
     add excpetion handling block for every function to handle type errors, value errors, AttributeError and other errors so the program doesnt stop if any occurs. THIS IS VERY IMPORTANT. continue to perform other validation.
     dont provide any comments in the code.
     """
    if context!="":
        flag=True
        extract_rules_gemini(instruction_text)
    print("Step 3: Validating Transactions...")
    validated_data=validate_transactions(df,flag)
    if df.shape[0] >= 100:
        print("Step 4: Detecting Anomalies...")
        anomaly_data=detect_anomalies(validated_data)
    if not anomaly_data.empty:
        return anomaly_data
    else:
        return validated_data

if __name__ == "__main__":
    run_pipeline()