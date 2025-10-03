import datetime as dt
import os
from typing import List, Literal, TypedDict

import streamlit as st
import requests

st.set_page_config(page_title="Chat with AI", layout="wide")


class ChatMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str
    timestamp: str


def _init_session_state() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history: List[ChatMessage] = []  # type: ignore[attr-defined]
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""
    if "clear_chat_input" not in st.session_state:
        st.session_state.clear_chat_input = False


def _append_message(role: Literal["user", "assistant"], content: str) -> None:
    st.session_state.chat_history.append(
        ChatMessage(role=role, content=content, timestamp=dt.datetime.now().isoformat())
    )


def _generate_ai_response(prompt: str) -> str:
    """Placeholder AI response; replace with real model call when available."""

    if not prompt.strip():
        return "I need some text to respond to."

    try:
        return _call_external_chat_api(prompt.strip())
    except RuntimeError as exc:
        st.warning(str(exc))

    return (
        "This is a simulated AI reply. Replace `_generate_ai_response` with an actual "
        "LLM call to enable live conversations. For now, I can reflect back your "
        f"message: {prompt.strip()}"
    )


def _call_external_chat_api(prompt: str) -> str:
    # api_url = st.secrets.get("chat_api_url") or os.getenv("CHAT_API_URL")
    api_url = "https://manuel1704.app.n8n.cloud/webhook-test/c5bcee78-e30c-43b0-9a2e-05cff3e1f28e"
    if not api_url:
        raise RuntimeError(
            "No chat API URL configured. Set `st.secrets['chat_api_url']` or the "
            "`CHAT_API_URL` environment variable."
        )

    headers = {"Content-Type": "application/json"}
    # api_key = st.secrets.get("chat_api_key") or os.getenv("CHAT_API_KEY")
    # if api_key:
    #     headers["Authorization"] = f"Bearer {api_key}"

    payload = {"message": prompt}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Chat API request failed: {exc}") from exc

    try:
        body = response.json()
    except ValueError:
        return response.text.strip()

    if isinstance(body, dict):
        for key in ("reply", "message", "response", "content"):
            value = body.get(key)
            if isinstance(value, str) and value.strip():
                return value

    return str(body)


def _render_sidebar():
    st.sidebar.header("Chat Controls")
    st.sidebar.caption("Use these options to manage the current conversation.")
    if st.sidebar.button("Clear conversation", use_container_width=True):
        st.session_state.chat_history.clear()
        st.session_state.clear_chat_input = True
        st.sidebar.success("Chat history cleared.")

    st.sidebar.subheader("Quick prompts")
    preset_prompt = st.sidebar.selectbox(
        "Insert a sample question",
        (
            "",
            "Summarize this scenario for me.",
            "List potential next steps.",
            "Provide a gentle explanation suitable for patients.",
        ),
    )
    if preset_prompt and st.sidebar.button("Use selected prompt", use_container_width=True):
        st.session_state.chat_input = preset_prompt
        st.sidebar.success("Prompt added to composer.")


def _render_chat_history():
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.info("Start the conversation by sending a message below.")
        else:
            for message in st.session_state.chat_history:
                avatar = "🧑" if message["role"] == "user" else "🤖"
                bubble_color = "#ffffff"
                border_color = "#e5e7eb" if message["role"] == "user" else "#bfdbfe"
                alignment = "flex-end" if message["role"] == "user" else "flex-start"

                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: {alignment}; margin-bottom: 0.75rem;">
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <span>{avatar}</span>
                            <div style="background-color: {bubble_color}; padding: 0.75rem 1rem; border-radius: 1rem; max-width: 65ch; border: 1px solid {border_color};">
                                <div style="font-size: 0.9rem; line-height: 1.5; color: #111827;">{message['content']}</div>
                                <div style="font-size: 0.7rem; color: #6b7280; margin-top: 0.35rem;">
                                    {dt.datetime.fromisoformat(message['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _handle_user_submission() -> None:
    user_message = st.session_state.chat_input.strip()
    if not user_message:
        st.warning("Please enter a message before sending.")
        return

    _append_message("user", user_message)
    st.session_state.clear_chat_input = True

    with st.spinner("Thinking..."):
        ai_response = _generate_ai_response(user_message)

    _append_message("assistant", ai_response)
    st.toast("Assistant replied", icon="🤖")


def main():
    st.title("Chat with AI")
    st.caption("Conversational sandbox – plug in your own LLM endpoint when ready.")

    _init_session_state()
    _render_sidebar()

    _render_chat_history()

    st.divider()

    if st.session_state.clear_chat_input:
        st.session_state.chat_input = ""
        st.session_state.clear_chat_input = False

    st.text_area(
        "Your message",
        key="chat_input",
        height=120,
        placeholder="Ask a question or paste some text...",
    )

    col_send, col_spacer = st.columns([1, 3])
    with col_send:
        if st.button("Send", type="primary", use_container_width=True):
            _handle_user_submission()

    with col_spacer:
        st.caption("Messages are stored only for this session.")


if __name__ == "__main__":
    main()
