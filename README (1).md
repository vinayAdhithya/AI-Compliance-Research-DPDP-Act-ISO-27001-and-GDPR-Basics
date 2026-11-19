# AI Compliance Research: DPDP Act, ISO 27001 and GDPR Basics

**Student:** VINAY ADHITHYA A  
**Register Number:** 410724149036  
**Project Number:** 13

## Project purpose
An educational, rule-based self-assessment prototype covering selected introductory topics from India's Digital Personal Data Protection Act, 2023, the EU GDPR, and ISO/IEC 27001:2022.

## Features
- Three framework-wise checklists
- Yes / Partly / No responses and optional evidence notes
- Explainable rule-based gap suggestions
- Framework-wise and overall indicator summaries
- CSV export

## Run on Windows
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/app.py
```
Open the local address shown in the terminal, usually http://localhost:8501.

## Scoring
Yes = 1.0; Partly = 0.5; No = 0.0. The average is only an educational indicator, not a legal compliance percentage.

## Important legal note
The DPDP Act, 2023 and DPDP Rules, 2025 have phased commencement provisions. The Act's commencement notification specifies different dates for different provisions. This prototype is not an interpretation of which provisions apply to a particular organisation. Check current official Gazette notifications and obtain qualified legal advice.

## Limitations
This is a rule-based academic prototype, not a machine-learning legal expert system, legal opinion, formal audit, or certification tool. It does not validate evidence or inspect systems. Use sample data only.
