import streamlit as st

st.set_page_config(page_title="Response", layout="wide")

st.title("Response")

response = st.session_state.get("submission_response")
document_type = st.session_state.get("submission_document_type")

if document_type:
    st.caption(f"Document type: {document_type}")

if response is None:
    st.info("No submission response available. Submit a document from the FHIR Validator page.")
else:
    if isinstance(response, (dict, list)):
        st.json(response)
    else:
        st.code(str(response))

if st.button("Back to FHIR Validator", type="secondary"):
    st.switch_page("pages/1_FHIR_Validator.py")
