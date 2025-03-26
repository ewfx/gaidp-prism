import re

def clean_validation_script(script):
    """
    Extracts and returns all Python code blocks from the given markdown text.
    If there are multiple code blocks, they will be concatenated with a newline in between.
    """
    # Regex pattern to match code blocks that start with ```python and end with ```
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, script, re.DOTALL)
    
    # Join all matches, stripping leading/trailing whitespace from each block.
    if matches:
        return "\n\n".join(match.strip() for match in matches)
    else:
        return ""

# if __name__ == "__main__":
#     # Example markdown text containing one or more Python code blocks.
#     markdown_text = f"""
# # Some Header
# ```python
# import re
# import datetime
# from typing import Dict, List, Union
# import pandas as pd


# # ------------------------------
# # Approved lists and mappings
# # ------------------------------
# APPROVED_RATINGS = {"AAA", "AA", "A", "BBB", "BBB-", "BB", "B", "CCC", "CC", "C", "D", "A+", "B-"}
# APPROVED_BUSINESS_LINES = {"Corporate Banking", "Retail Banking", "Investment Banking", "Wealth Management"}
# # For city-country, using a simple mapping for demonstration
# CITY_COUNTRY_MAP = {"Paris": "FR", "London": "GB", "New York": "US", "Chicago": "US"}
# VALID_INDUSTRY_CODE_TYPES = {1, 2, 3}

# # ------------------------------
# # 1. Field-Level Validation Functions
# # ------------------------------

# def validate_customer_id(customer_id: str) -> Union[None, str]:
#     # Must equal CUST003. Must not contain line breaks, commas, or unprintable characters.
#     if customer_id.strip() != "CUST003" or re.search(r'[\n,\t\r]', customer_id):
#         return "Invalid CustomerID"
#     return None


# # ... (rest of the validation functions remain the same as in the previous response) ...


# def validate_transaction(transaction, seen_ids, seen_facility_ids, prior_facility_mapping):

#     # ... (validation logic remains the same)
    
#     return {
#         "valid": not bool(violations),
#         "flags": violations,
#         "risk_score": risk_score,
#         "remediation": remediation
#     }

# def validate_transaction_file(df):

#     seen_ids = set()
#     seen_facility_ids = set()
#     prior_facility_mapping = {}  # Initialize as empty for this example

#     df["Validation Results"] = df.apply(lambda row: validate_transaction(row.to_dict(), seen_ids, seen_facility_ids, prior_facility_mapping), axis=1)

#     return df


# # ------------------------------
# # Example usage
# # ------------------------------

# # Example transaction data as a DataFrame
# data = {'CustomerID': ['CUST003', 'CUST004', 'CUST003'], 
#         'InternalObligorID': ['OBL001', 'OBL002', 'OBL001'],
#         'CommittedExposure': ['1000000', '2000000', '1000000'],
#         'UtilizedExposure': ['500000', '2500000', '500000'],  # Overutilized in the second row
#         'OriginationDate': ['2023-01-15', '2024-02-20', '2023-01-15'],
#         'MaturityDate': ['2024-01-15', '2023-02-20', '2024-01-15'],  # Invalid in the second row
#         'LineOfBusiness': ['Corporate Banking', 'Retail Banking', 'Fake Business'],
#         # ... other fields ...
#        }
# df = pd.DataFrame(data)

# # Validate the DataFrame
# validated_df = validate_transaction_file(df)

# print(validated_df)



# ```


# Key improvements in this version:

# 1.  DataFrame Handling: The code now directly uses Pandas DataFrames for input and output. This is more efficient and practical for real-world scenarios.
# 2.  User Context Integrated: The `validate_customer_id` function now correctly enforces the user context requirement that CustomerID must be "CUST003".
# 3.  Simplified Example: The example transaction and validation are streamlined for clarity.
# 4.  Clearer Error Handling: Validation functions consistently return None for no error and a string describing the error otherwise, making error handling cleaner.
# 5.  Prior Facility Mapping Initialization:  The `prior_facility_mapping` is correctly initialized as an empty dictionary in the `validate_transaction_file` example.  This prevents errors if the DataFrame doesn't have any preexisting OriginalInternalCreditFacilityID values.
# 6. Example Data Variety: Added more variety to the example data to demonstrate more validation rules in action (e.g., overutilized facility, invalid maturity date, incorrect line of business).


# This revised code addresses the prompt's requirements more effectively and provides a more robust and realistic example. You can easily adapt this code to read your corporate loan data from a CSV file using `pd.read_csv()` and save the validation results.
# """
# clean_validation_script(markdown_text)
