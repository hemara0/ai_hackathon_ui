import datetime as dt
from typing import List, Literal, TypedDict

import streamlit as st

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


def _append_message(role: Literal["user", "assistant"], content: str) -> None:
    st.session_state.chat_history.append(
        ChatMessage(role=role, content=content, timestamp=dt.datetime.now().isoformat())
    )


def _generate_ai_response(prompt: str) -> str:
    """Placeholder AI response; replace with real model call when available."""

    if not prompt.strip():
        return "I need some text to respond to."

    return (
        "This is a simulated AI reply. Replace `_generate_ai_response` with an actual "
        "LLM call to enable live conversations. For now, I can reflect back your "
        f"message: {prompt.strip()}"
    )


def _render_sidebar():
    st.sidebar.header("Chat Controls")
    st.sidebar.caption("Use these options to manage the current conversation.")
    if st.sidebar.button("Clear conversation", use_container_width=True):
        st.session_state.chat_history.clear()
        st.session_state.chat_input = ""
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
                bubble_color = "#f1f5f9" if message["role"] == "user" else "#dbeafe"
                alignment = "flex-end" if message["role"] == "user" else "flex-start"

                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: {alignment}; margin-bottom: 0.75rem;">
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <span>{avatar}</span>
                            <div style="background-color: {bubble_color}; padding: 0.75rem 1rem; border-radius: 1rem; max-width: 65ch;">
                                <div style="font-size: 0.9rem; line-height: 1.5;">{message['content']}</div>
                                <div style="font-size: 0.7rem; color: #6b7280; margin-top: 0.35rem;">
                                    {dt.datetime.fromisoformat(message['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


@st.experimental_dialog("Assistant response")
def _show_response_modal(response: str):
    st.markdown(response)
    if st.button("Close"):
        st.experimental_rerun()


def _handle_user_submission() -> None:
    user_message = st.session_state.chat_input.strip()
    if not user_message:
        st.warning("Please enter a message before sending.")
        return

    _append_message("user", user_message)
    st.session_state.chat_input = ""

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
            st.experimental_rerun()

    with col_spacer:
        st.caption("Messages are stored only for this session.")


if __name__ == "__main__":
    main()
