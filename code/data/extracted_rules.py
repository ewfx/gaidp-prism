import re
import datetime
from typing import Dict, List, Union
import pandas as pd
import ast


# ------------------------------
# Approved lists and mappings
# ------------------------------
APPROVED_RATINGS = {"AAA", "AA", "A", "BBB", "BBB-", "BB", "B", "CCC", "CC", "C", "D", "A+", "B-"}
APPROVED_BUSINESS_LINES = {"Corporate Banking", "Retail Banking", "Investment Banking", "Wealth Management"}
# For city-country, using a simple mapping for demonstration
CITY_COUNTRY_MAP = {"Paris": "FR", "London": "GB", "New York": "US", "Chicago": "US"}
VALID_INDUSTRY_CODE_TYPES = {1, 2, 3}

# ------------------------------
# 1. Field-Level Validation Functions
# ------------------------------

def validate_customer_id(customer_id: str) -> Union[None, str]:
    try:
        if re.search(r'[\n,\t\r]', customer_id):
            return "Invalid CustomerID"
        return None
    except Exception as e:
        return f"Error validating CustomerID: {e}"



def validate_internal_obligor_id(internal_obligor_id: str, seen_ids: set) -> Union[None, str]:
    try:
        if internal_obligor_id in seen_ids or re.search(r'[\n,\t\r]', internal_obligor_id):
            return "Duplicate/Invalid ObligorID"
        seen_ids.add(internal_obligor_id)
        return None
    except Exception as e:
        return f"Error validating InternalObligorID: {e}"

def validate_original_internal_obligor_id(original_id: str, internal_id: str) -> Union[None, str]:
    try:
        if original_id != internal_id:
            return "Original ID Mismatch"
        return None
    except Exception as e:
        return f"Error validating OriginalInternalObligorID: {e}"


def validate_obligor_name(obligor_name: str, tin: str) -> Union[None, str]:
    try:
        if str(obligor_name).strip() == "Individual" and str(tin).strip() not in {"", "NA"}:
            return "Name-TIN Conflict"
        if re.search(r'[^\w\s\-\.]', obligor_name):
            return "Invalid Characters in ObligorName"
        return None
    except Exception as e:
        return f"Error validating ObligorName: {e}"



def validate_city_country(city: str, country: str) -> Union[None, str]:
    try:
        mapped = CITY_COUNTRY_MAP.get(city.strip())
        if mapped and mapped != country.strip():
            return "City-Country Mismatch"
        return None
    except Exception as e:
        return f"Error validating City-Country: {e}"


def validate_country(country: str) -> Union[None, str]:
    try:
        if not re.match(r'^[A-Z]{2}$', country.strip()):
            return "Invalid Country Code"
        return None
    except Exception as e:
        return f"Error validating Country: {e}"


def validate_zip_code(zip_code: str, country: str) -> Union[None, str]:
    try:
        if country.strip() == "US" and not re.match(r'^\d{5}$', str(zip_code).strip()):
            return "Invalid ZIP/Postal Code"
        return None
    except Exception as e:
        return f"Error validating Zip Code: {e}"



def validate_industry_code(industry_code: str) -> Union[None, str]:
    try:
        if not re.match(r'^\d{4,6}$', str(industry_code).strip()):
            return "Invalid Industry Code"
        return None
    except Exception as e:
        return f"Error validating Industry Code: {e}"


def validate_industry_code_type(industry_code_type: Union[str, int]) -> Union[None, str]:
    try:
        value = int(industry_code_type)
        if value not in VALID_INDUSTRY_CODE_TYPES:
            return "Invalid Code Type"
        return None
    except Exception as e:
        return f"Error validating Industry Code Type: {e}"



def validate_internal_rating(rating: str) -> Union[None, str]:

    try:
        if rating.strip() not in APPROVED_RATINGS:
            return "Unapproved Risk Rating"
        return None
    except Exception as e:
        return f"Error validating Internal Rating: {e}"


def validate_tin(tin: str, entity_type: str = "Corporate") -> Union[None, str]:
    try:
        tin = str(tin).strip()
        if entity_type == "Individual":
            if tin not in {"", "NA"}:
                return "Invalid TIN"
            return None
        if re.match(r'^\d{2}-\d{7}$', tin) or re.match(r'^\d{9}$', tin):
            return None
        return "Invalid TIN"
    except Exception as e:
        return f"Error validating TIN: {e}"




def validate_stock_exchange_tkr(stock_exchange: str, tkr: str) -> Union[None, str]:
    try:
        if str(stock_exchange).strip() == "NA" and str(tkr).strip() not in {"", "NA"}:
            return "Exchange-TKR Conflict"
        return None
    except Exception as e:
        return f"Error validating Stock Exchange/TKR: {e}"



def validate_tkr(tkr: str) -> Union[None, str]:

    try:
        tkr = str(tkr).strip()
        if tkr in {"", "NA"}:
            return None
        if not re.match(r'^[A-Z0-9]{1,5}$', tkr):
            return "Invalid Ticker"
        return None
    except Exception as e:
        return f"Error validating TKR: {e}"


def validate_cusip(cusip: str) -> Union[None, str]:
    try:
        cusip = str(cusip).strip()
        if cusip in {"", "NA"}:
            return None
        if not re.match(r'^[A-Z0-9]{6}$', cusip):
            return "Invalid CUSIP"
        return None
    except Exception as e:
        return f"Error validating CUSIP: {e}"


def validate_internal_credit_facility_id(facility_id: str, seen_facility_ids: set) -> Union[None, str]:
    try:
        if facility_id in seen_facility_ids or re.search(r'[^A-Za-z0-9]', facility_id):
            return "Duplicate/Invalid FacilityID"
        seen_facility_ids.add(facility_id)
        return None
    except Exception as e:
        return f"Error validating InternalCreditFacilityID: {e}"


def validate_original_internal_credit_facility_id(orig_facility_id: str, facility_id: str) -> Union[None, str]:

    try:
        if orig_facility_id != facility_id:
            return "Original FacilityID Mismatch"
        return None
    except Exception as e:
        return f"Error validating OriginalInternalCreditFacilityID: {e}"



def validate_origination_date(origination_date: str) -> Union[None, str]:
    try:
        dt = datetime.datetime.strptime(origination_date.strip(), "%Y-%m-%d")
        if dt > datetime.datetime.today():
            return "Future Origination Date"
        return None
    except Exception as e:
        return f"Error validating OriginationDate: {e}"




def validate_maturity_date(maturity_date: str, origination_date: str) -> Union[None, str]:
    try:
        orig_dt = datetime.datetime.strptime(origination_date.strip(), "%Y-%m-%d")
        mat_dt = datetime.datetime.strptime(maturity_date.strip(), "%Y-%m-%d")
        if maturity_date.strip() != "9999-01-01" and mat_dt <= orig_dt:
            return "Invalid Maturity Date"
        return None
    except Exception as e:
        return f"Error validating MaturityDate: {e}"


def validate_facility_type(facility_type: str) -> Union[None, str]:
    try:
        val = int(facility_type)
        if not (0 <= val <= 19):
            return "Invalid Facility Type"
        return None
    except Exception as e:
        return f"Error validating FacilityType: {e}"


def validate_other_facility_type(other_facility_type: str, facility_type: str) -> Union[None, str]:
    try:
        ft = int(facility_type)
        if ft == 0:
            if not str(other_facility_type).strip():
                return "Missing Other Facility Type Description"
        else:
            if str(other_facility_type).strip():
                return "Unnecessary Facility Description"
        return None
    except Exception as e:
        return f"Error validating OtherFacilityType: {e}"


def validate_credit_facility_purpose(purpose: str) -> Union[None, str]:
    try:
        val = int(purpose)
        if not (0 <= val <= 33):
            return "Invalid Purpose Code"
        return None
    except Exception as e:
        return f"Error validating CreditFacilityPurpose: {e}"



def validate_other_credit_facility_purpose(other_purpose: str, purpose: str) -> Union[None, str]:

    try:
        p = int(purpose)
        if p == 0:
            if not str(other_purpose).strip():
                return "Missing Other Purpose Description"
        else:
            if str(other_purpose).strip():
                return "Unnecessary Purpose Description"
        return None
    except Exception as e:
        return f"Error validating OtherFacilityPurpose: {e}"



def validate_committed_exposure(committed: str) -> Union[None, str]:
    try:
        val = int(committed)
        if val < 0:
            return "Invalid Exposure Amount"
        return None
    except Exception as e:
        return f"Error validating CommittedExposure: {e}"


def validate_utilized_exposure(utilized: str, committed: str) -> Union[None, str]:
    try:
        used = int(utilized)
        comm = int(committed)
        if used > comm:
            return "Overutilized Facility"
        return None
    except Exception as e:
        return f"Error validating UtilizedExposure: {e}"


def validate_reporting_line(report_line: str) -> Union[None, str]:
    try:
        val = int(report_line)
        if not (1 <= val <= 11):
            return "Invalid Reporting Line"
        return None
    except Exception as e:
        return f"Error validating LineReportedOnFRY9C: {e}"


def validate_line_of_business(lob: str) -> Union[None, str]:

    try:
        if lob.strip() not in APPROVED_BUSINESS_LINES:
            return "Unapproved Line of Business"
        return None
    except Exception as e:
        return f"Error validating LineOfBusiness: {e}"



def validate_chargeoffs(chargeoffs: str, committed: str) -> Union[None, str]:
    try:
        if str(chargeoffs).strip() in {"NA", ""}:
            return None
        co = int(chargeoffs)
        comm = int(committed)
        if co < 0 or co > comm:
            return "Invalid Charge-off Amount"
        return None
    except Exception as e:
        return f"Error validating CumulativeChargeoffs: {e}"


def validate_asc31010(asc: str) -> Union[None, str]:
    try:
        val = int(asc)
        if val < 0:
            return "Invalid Reserve Amount"
        return None
    except Exception as e:
        return f"Error validating ASC31010: {e}"

# ------------------------------
# Dynamic Risk Scoring
# ------------------------------
def calculate_risk_score(violations: List[str]) -> int:
    weights = {
        "Invalid CustomerID": 5,
        "Duplicate/Invalid ObligorID": 10,
        "Original ID Mismatch": 10,
        "Name-TIN Conflict": 8,
        "City-Country Mismatch": 8,
        "Invalid Country Code": 5,
        "Invalid ZIP/Postal Code": 5,
        "Invalid Industry Code": 5,
        "Invalid Code Type": 5,
        "Unapproved Risk Rating": 5,
        "Invalid TIN": 8,
        "Exchange-TKR Conflict": 8,
        "Invalid Ticker": 5,
        "Invalid CUSIP": 10,
        "Duplicate/Invalid FacilityID": 10,
        "Original FacilityID Mismatch": 10,
        "Future Origination Date": 5,
        "Invalid Origination Date Format": 5,
        "Invalid Maturity Date": 10,
        "Invalid Maturity Date Format": 5,
        "Invalid Facility Type": 8,
        "Missing Other Facility Type Description": 5,
        "Unnecessary Facility Description": 5,
        "Invalid Purpose Code": 8,
        "Missing Other Purpose Description": 5,
        "Unnecessary Purpose Description": 5,
        "Invalid Exposure Amount": 8,
        "Overutilized Facility": 10,
        "Invalid Reporting Line": 5,
        "Unapproved Line of Business": 8,
        "Invalid Charge-off Amount": 5,
        "Invalid Reserve Amount": 5, "CustomerID Mismatch": 10,
    }
    score = sum(weights.get(v, 0) for v in violations)
    return score

def extract_violation(row):
    try:
        validation_data = row.get("Validation Results", "")

        if isinstance(validation_data, dict):
            return validation_data.get("flags", [])

        if not isinstance(validation_data, str) or pd.isna(validation_data):
            return []

        if validation_data.startswith("\"{") and validation_data.endswith("}\""):
            validation_data = validation_data[1:-1]
        
        validation_dict = ast.literal_eval(validation_data)
        return validation_dict.get("flags", [])
    
    except (SyntaxError, ValueError, TypeError, AttributeError):  # More specific exception handling
        return []

def extract_remediation(row):
    try:
        validation_data = row.get("Validation Results", "")

        if isinstance(validation_data, dict):
            return validation_data.get("remediation", [])

        if not isinstance(validation_data, str) or pd.isna(validation_data):
            return []

        if validation_data.startswith("\"{") and validation_data.endswith("}\""):
            validation_data = validation_data[1:-1]
        
        validation_dict = ast.literal_eval(validation_data)
        return validation_dict.get("remediation", [])
    
    except (SyntaxError, ValueError, TypeError, AttributeError):  # More specific exception handling
        return []

def extract_risk_score(row):
    try:
        validation_data = row.get("Validation Results", "")

        if isinstance(validation_data, dict):
            return validation_data.get("risk_score", 0)

        if not isinstance(validation_data, str) or pd.isna(validation_data):
            return 0

        if validation_data.startswith("\"{") and validation_data.endswith("}\""):
            validation_data = validation_data[1:-1]
        
        validation_dict = ast.literal_eval(validation_data)
        return validation_dict.get("risk_score", 0)
    
    except (SyntaxError, ValueError, TypeError, AttributeError):  # More specific exception handling
        return 0


def validate_customer_id_filter(customer_id: str) -> Union[None, str]:
    try:
        if customer_id != "CUST003":
            return "CustomerID Mismatch"  # Changed flag name
        return None
    except Exception as e:
        return f"Error in Customer ID filter: {e}"


def validate_transaction(transaction, seen_ids, seen_facility_ids):

    violations = extract_violation(transaction)
    remediation = extract_remediation(transaction)
    risk_score= extract_risk_score(transaction)
    

    try:
        err = validate_customer_id_filter(transaction.get("CustomerID"))
        if err:
            violations.append(err)
            remediation.append("CustomerID does not match CUST003, skipping record.")

        # If CustomerID Mismatch, stop further validations:
        if "CustomerID Mismatch" in violations:
            risk_score += calculate_risk_score(violations)
            return {
                "valid": not bool(violations),
                "flags": violations,
                "risk_score": risk_score,
                "remediation": remediation
            }

        err = validate_customer_id(transaction.get("CustomerID", ""))
        if err: violations.append(err)

        err = validate_internal_obligor_id(transaction.get("InternalObligorID", ""), seen_ids)
        if err: violations.append(err)
        

        err = validate_original_internal_obligor_id(transaction.get("OriginalInternalObligorID", ""), transaction.get("InternalObligorID", ""))
        if err: violations.append(err)
        

        err = validate_obligor_name(transaction.get("ObligorName", ""), transaction.get("TIN", ""))
        if err: violations.append(err)
        

        err = validate_city_country(transaction.get("City", ""), transaction.get("Country", ""))
        if err: violations.append(err)
        
        err = validate_country(transaction.get("Country", ""))
        if err: violations.append(err)
    

        err = validate_zip_code(transaction.get("ZipCodeForeignMailingCode", ""), transaction.get("Country", ""))
        if err: violations.append(err)


        err = validate_industry_code(transaction.get("IndustryCode", ""))
        if err: violations.append(err)


        err = validate_industry_code_type(transaction.get("IndustryCodeType", ""))
        if err: violations.append(err)


        err = validate_internal_rating(transaction.get("InternalRating", ""))
        if err: violations.append(err)
    
        err = validate_tin(transaction.get("TIN", ""), transaction.get("EntityType", "Corporate"))
        if err: violations.append(err)


        err = validate_stock_exchange_tkr(transaction.get("StockExchange", ""), transaction.get("TKR", ""))
        if err: violations.append(err)


        err = validate_tkr(transaction.get("TKR", ""))
        if err: violations.append(err)


        err = validate_cusip(transaction.get("CUSIP", ""))
        if err: violations.append(err)


        err = validate_internal_credit_facility_id(transaction.get("InternalCreditFacilityID", ""), seen_facility_ids)
        if err: violations.append(err)


        err = validate_original_internal_credit_facility_id(transaction.get("OriginalInternalCreditFacilityID", ""), transaction.get("InternalCreditFacilityID", ""))
        if err: violations.append(err)


        err = validate_origination_date(transaction.get("OriginationDate", ""))
        if err: violations.append(err)


        err = validate_maturity_date(transaction.get("MaturityDate", ""), transaction.get("OriginationDate", ""))
        if err: violations.append(err)



        err = validate_facility_type(transaction.get("FacilityType", ""))
        if err: violations.append(err)


        err = validate_other_facility_type(transaction.get("OtherFacilityType", ""), transaction.get("FacilityType", ""))
        if err: violations.append(err)
        

        err = validate_credit_facility_purpose(transaction.get("CreditFacilityPurpose", ""))
        if err: violations.append(err)
        

        err = validate_other_credit_facility_purpose(transaction.get("OtherFacilityPurpose", ""), transaction.get("CreditFacilityPurpose", ""))
        if err: violations.append(err)
       

        err = validate_committed_exposure(transaction.get("CommittedExposure", ""))
        if err: violations.append(err)


        err = validate_utilized_exposure(transaction.get("UtilizedExposure", ""), transaction.get("CommittedExposure", ""))
        if err: violations.append(err)

        err = validate_reporting_line(transaction.get("LineReportedOnFRY9C", ""))
        if err: violations.append(err)
        

        err = validate_line_of_business(transaction.get("LineOfBusiness", ""))
        if err: violations.append(err)


        err = validate_chargeoffs(transaction.get("CumulativeChargeoffs", ""), transaction.get("CommittedExposure", ""))
        if err: violations.append(err)


        err = validate_asc31010(transaction.get("ASC31010", ""))
        if err: violations.append(err)
        

        try:
            committed = int(transaction["CommittedExposure"])
            utilized = int(transaction["UtilizedExposure"])
            if utilized > committed:
                violations.append("Overutilized Facility")
        except (ValueError, TypeError, KeyError):
            violations.append("Invalid Exposure Amount")

        seen_ids.add(transaction["CustomerID"])
        seen_facility_ids.add(transaction["InternalCreditFacilityID"])

    except Exception as e: # this block is not used in output since each function has exception handling block, but this is the ideal code as asked in question prompt.
        violations.append(f"An unexpected error occurred: {e}")


    risk_score += calculate_risk_score(violations)


    if risk_score > 30:
        remediation.append("Trigger enhanced compliance review and request additional documentation.")
    elif violations:
        remediation.append("Correct the flagged issues as indicated.")
    else:
        remediation.append("No remediation needed.")


    return {
        "valid": not bool(violations),
        "flags": violations,
        "risk_score": risk_score,
        "remediation": remediation
    }

def validate_transaction_file(df):

    seen_ids = set()
    seen_facility_ids = set()

    df["Validation Results"] = df.apply(lambda row: validate_transaction(row.to_dict(), seen_ids, seen_facility_ids), axis=1)

    return df