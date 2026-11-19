import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="AI Compliance Research", page_icon="🛡️", layout="wide")

FRAMEWORKS = {
    "DPDP Act, 2023 (India)": [
        ("Purpose and lawful processing", "Is each personal-data processing activity connected to a stated lawful purpose?"),
        ("Notice and transparency", "Is a clear notice provided describing the personal data and purpose?"),
        ("Consent where applicable", "Where consent is relied upon, is it obtained through a clear affirmative action?"),
        ("Data principal requests", "Is there a process to receive and respond to applicable data principal requests?"),
        ("Security safeguards", "Are reasonable security safeguards used to protect personal data?"),
        ("Personal data breach response", "Is there a documented process to detect, manage and communicate personal data breaches as required?"),
        ("Erasure and retention", "Is personal data erased when retention is no longer necessary, subject to applicable legal requirements?"),
    ],
    "GDPR (EU) – Regulation (EU) 2016/679": [
        ("Lawfulness, fairness and transparency", "Is a lawful basis identified and is processing explained transparently?"),
        ("Purpose limitation", "Is personal data collected for specified, explicit and legitimate purposes?"),
        ("Data minimisation", "Is the personal data collected adequate, relevant and limited to what is necessary?"),
        ("Accuracy", "Are reasonable steps taken to keep personal data accurate and up to date?"),
        ("Storage limitation", "Are retention periods defined and reviewed?"),
        ("Integrity and confidentiality", "Are appropriate technical and organisational security measures applied?"),
        ("Data subject rights", "Is there a documented process for handling applicable data subject rights?"),
    ],
    "ISO/IEC 27001:2022 – ISMS basics": [
        ("ISMS scope", "Is the scope and context of the information security management system defined?"),
        ("Risk assessment", "Are information-security risks identified and assessed?"),
        ("Risk treatment", "Are risk treatment decisions, actions and owners documented?"),
        ("Access control", "Are access permissions based on business need and reviewed?"),
        ("Competence and awareness", "Are relevant personnel given information-security awareness and training?"),
        ("Operational security", "Are security processes and controls operated and reviewed?"),
        ("Incident management", "Are information-security incidents recorded, assessed and addressed?"),
    ],
}

st.title("🛡️ AI Compliance Research")
st.subheader("DPDP Act • GDPR • ISO/IEC 27001")
st.warning("Academic prototype only. This tool is an educational self-assessment aid, not legal advice, a formal audit, a certification assessment, or proof of compliance.")
st.markdown("### Organisation details")
c1,c2=st.columns(2)
with c1: organisation=st.text_input("Organisation / case-study name","Sample Organisation")
with c2: assessor=st.text_input("Assessed by","Student")
st.caption("Use fictional or non-confidential information for this demonstration.")

answers=[]
for framework, controls in FRAMEWORKS.items():
    with st.expander(framework, expanded=True):
        st.write(f"{len(controls)} introductory review questions")
        for i,(area,question) in enumerate(controls):
            key=f"{framework}_{i}"
            st.markdown(f"**{i+1}. {area}**")
            status=st.radio(question,["Yes","Partly","No"],horizontal=True,key=key)
            evidence=st.text_input("Evidence / observation (optional)",key=key+"_evidence",placeholder="Example: policy, procedure, record, or identified gap")
            answers.append({"Framework":framework,"Control area":area,"Question":question,"Status":status,"Evidence / observation":evidence})

if st.button("Generate research assessment",type="primary"):
    df=pd.DataFrame(answers)
    weights={"Yes":1.0,"Partly":0.5,"No":0.0}
    df["Indicator"]=df["Status"].map(weights)
    st.session_state["assessment"]=df
    st.session_state["org"]=organisation
    st.session_state["assessor"]=assessor

if "assessment" in st.session_state:
    df=st.session_state["assessment"]
    st.divider()
    st.header("Assessment results")
    overall=round(df["Indicator"].mean()*100,1)
    a,b,c=st.columns(3)
    a.metric("Overall indicator",f"{overall}%")
    b.metric("Questions reviewed",len(df))
    c.metric("Items needing review",int((df["Status"]!="Yes").sum()))
    summary=df.groupby("Framework")["Indicator"].mean().mul(100).round(1).reset_index(name="Indicator score (%)")
    st.subheader("Framework-wise summary")
    st.dataframe(summary,use_container_width=True,hide_index=True)
    st.bar_chart(summary.set_index("Framework"))
    gaps=df[df["Status"]!="Yes"].copy()
    st.subheader("Research findings and suggested actions")
    if gaps.empty:
        st.success("All responses are marked Yes. Confirm each answer with evidence before drawing conclusions.")
    else:
        actions=[]
        for _,r in gaps.iterrows():
            if r["Status"]=="No":
                action="Gap indicated: define the required policy or process, assign an owner, implement it, and retain evidence."
            else:
                action="Partial implementation indicated: identify missing steps, complete the process, and retain evidence of operation."
            actions.append({"Framework":r["Framework"],"Control area":r["Control area"],"Response":r["Status"],"Suggested action":action})
        st.dataframe(pd.DataFrame(actions),use_container_width=True,hide_index=True)
    st.subheader("Detailed responses")
    st.dataframe(df.drop(columns=["Indicator"]),use_container_width=True,hide_index=True)
    export=df.drop(columns=["Indicator"]).copy()
    export.insert(0,"Assessment date",date.today().isoformat())
    export.insert(1,"Organisation",st.session_state["org"])
    export.insert(2,"Assessor",st.session_state["assessor"])
    st.download_button("Download assessment as CSV",export.to_csv(index=False).encode("utf-8"),"ai_compliance_assessment.csv","text/csv")
    st.caption("Scoring is a simple educational indicator: Yes = 1, Partly = 0.5, No = 0. It is not a legal compliance score.")
