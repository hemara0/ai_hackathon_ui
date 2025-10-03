import json
import os
from typing import Any, Optional, Tuple

import streamlit as st
import requests

from json_validator import validate_json


def _decode_bytes(file_bytes: bytes) -> Tuple[Optional[str], Optional[str]]:
    """Attempt to decode *file_bytes* using common UTF encodings."""

    for encoding in ("utf-8-sig", "utf-8", "utf-16", "utf-16le", "utf-16be"):
        try:
            return file_bytes.decode(encoding), None
        except UnicodeDecodeError:
            continue
    return None, "Unable to decode file. Supported encodings: UTF-8 or UTF-16."


def _submit_json_to_api(payload: Any) -> Any:
    #api_url = st.secrets.get("fhir_submit_url") or os.getenv("FHIR_SUBMIT_URL")
    api_url = "https://manuel1704.app.n8n.cloud/webhook-test/c5bcee78-e30c-43b0-9a2e-05cff3e1f28e"
    if not api_url:
        raise RuntimeError(
            "No submission endpoint configured. Set `st.secrets['fhir_submit_url']` or "
            "the `FHIR_SUBMIT_URL` environment variable."
        )

    headers = {"Content-Type": "application/json"}
    # api_key = st.secrets.get("fhir_submit_api_key") or os.getenv("FHIR_SUBMIT_API_KEY")
    # if api_key:
    #     headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Submission request failed: {exc}") from exc

    try:
        return response.json()
    except ValueError:
        return response.text.strip()

st.set_page_config(page_title="FHIR Validator", layout="wide")

st.markdown(
    """
    <style>
    main[data-testid="stAppViewContainer"] {
        padding: 0;
    }
    .header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    .textarea-block {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .textarea-block .stTextArea {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .textarea-block textarea {
        flex: 1;
        resize: none;
        width: 100%;
        min-height: 100%;
        font-family: "Courier New", monospace;
        font-size: 0.95rem;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #d1d5db;
        background-color: #fff;
    }
    .bottom-bar {
        margin-top: auto;
        padding-top: 0.5rem;
    }
    .bottom-bar [data-testid="column"]:nth-child(n+3) {
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .bottom-bar [data-testid="column"]:nth-child(3),
    .bottom-bar [data-testid="column"]:nth-child(4) {
        padding-right: 0.5rem;
    }
    .bottom-bar .stButton button {
        background-color: #1d4ed8;
        color: #ffffff;
        border: none;
        min-width: 120px;
        height: 3rem;
        border-radius: 0.5rem;
        font-weight: 600;
        white-space: nowrap;
        padding: 0 1.5rem;
    }
    .bottom-bar .stButton button:hover {
        background-color: #1e40af;
    }
    .bottom-bar .stButton button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3);
    }
    .bottom-bar [data-testid="column"]:nth-child(2) {
        flex: 1;
    }
    .browse-uploader [data-testid="stFileUploaderDropzone"] {
        border: none;
        background-color: transparent;
        padding: 0;
    }
    .browse-uploader [data-testid="stFileUploaderDropzone"] section {
        padding: 0;
    }
    .browse-uploader [data-testid="stFileUploaderDropzone"] button {
        width: 100%;
        background-color: #1d4ed8;
        color: transparent;
        border-radius: 0.5rem;
        border: none;
        height: 3rem;
        font-weight: 600;
        position: relative;
    }
    .browse-uploader [data-testid="stFileUploaderDropzone"] button::after {
        content: "Browse";
        color: #ffffff;
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .browse-uploader [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #1e40af;
    }
    .browse-uploader [data-testid="stFileUploaderDropzone"] div:nth-child(1) {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="full-page">', unsafe_allow_html=True)

title_col, browse_col = st.columns([8, 2])

with title_col:
    st.markdown("### PAPAA - PriorAuth Patient Access API")

with browse_col:
    st.markdown('<div class="browse-uploader">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Browse",
        type=["json"],
        label_visibility="collapsed",
        key="json_file_picker",
    )
    st.markdown('</div>', unsafe_allow_html=True)

if "json_payload" not in st.session_state:
    st.session_state["json_payload"] = ""

file_status: Optional[Tuple[str, str]] = None

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    signature = (uploaded_file.name, uploaded_file.size)
    last_signature = st.session_state.get("last_uploaded_file_signature")
    is_new_upload = signature != last_signature

    decoded_text, decode_error = _decode_bytes(file_bytes)

    if decode_error:
        file_status = ("error", decode_error)
    else:
        file_validation = validate_json(decoded_text)
        if file_validation.is_valid:
            pretty_payload = json.dumps(file_validation.payload, indent=2)
            st.session_state["json_payload"] = pretty_payload
            file_status = ("success", "Loaded JSON from file.")
        else:
            file_status = ("error", file_validation.message)

    st.session_state["last_uploaded_file_signature"] = signature

    if not is_new_upload:
        file_status = None

st.markdown('<div class="textarea-block">', unsafe_allow_html=True)
json_payload = st.text_area(
    "PAPAA - PriorAuth Patient Access API",
    placeholder="Paste or type your JSON here...",
    height=500,
    label_visibility="collapsed",
    key="json_payload",
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
left_col, spacer_col, validate_col, submit_col = st.columns([2, 5, 2, 1])

with left_col:
    document_type = st.selectbox(
        "Document Type",
        ("Claim", "ClaimResponse"),
    )

spacer_col.empty()

with validate_col:
    validate_clicked = st.button("Beauty and Validate", use_container_width=True)

with submit_col:
    submit_clicked = st.button("Submit", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

feedback_container = st.container()

st.markdown('</div>', unsafe_allow_html=True)

if file_status:
    status, message = file_status
    with feedback_container:
        if status == "success":
            st.success(message)
            st.toast("JSON loaded from file", icon="📂")
        else:
            st.error(message)
            st.toast("File could not be decoded", icon="⚠️")

if validate_clicked:
    validation_result = validate_json(json_payload)
    with feedback_container:
        if validation_result.is_valid:
            st.success(validation_result.message)
            st.json(validation_result.payload)
            st.toast("JSON validated successfully", icon="✅")
        else:
            st.error(validation_result.message)
            st.toast("JSON validation failed", icon="⚠️")

if submit_clicked:
    if not json_payload.strip():
        st.warning("Please provide JSON before submitting.")
    else:
        try:
            structured_payload = json.loads(json_payload)
        except json.JSONDecodeError as exc:
            st.error(f"Invalid JSON: {exc}")
            st.toast("Submission failed — invalid JSON", icon="⚠️")
        else:
            with st.spinner("Submitting to external API..."):
                try:
                    response_body = _submit_json_to_api(structured_payload)
                except RuntimeError as exc:
                    st.error(str(exc))
                    st.toast("Submission failed", icon="⚠️")
                else:
                    st.session_state["submission_response"] = response_body
                    st.session_state["submission_payload"] = structured_payload
                    st.session_state["submission_document_type"] = document_type
                    st.toast("Submission sent", icon="🚀")
                    st.switch_page("pages/Response.py")
