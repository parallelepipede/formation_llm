import streamlit as st
from const import USE_SOURCES
import rag


START_MESSAGE = f'Veuillez poser une question : '
PROMPT_MESSAGE = "Veuillez poser une question et appuyer sur Entrée..."


st.set_page_config(
    page_title=f"Question & Answers",
    page_icon="🗨️",
    # initial_sidebar_state='collapsed'
)


query_engine =  None ### declare rag engine here 


assistant_must_answer = True
if 'messages' not in st.session_state:
    assistant_must_answer = False
    st.session_state['messages'] = [
        {"role": "assistant", "content": START_MESSAGE}]

if st.session_state['messages'][-1]['role'] == 'assistant':
    assistant_must_answer = False

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            # with st.expander('Question'):
            st.write(message["content"])
        elif message["role"] == 'assistant':
            st.write(message["content"])
            if 'sources' in message:
                with st.expander('Source'):
                    st.write(message['sources'])

prompt = st.chat_input(PROMPT_MESSAGE)

# If the user hits enter
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    assistant_must_answer = True

if assistant_must_answer:
    with st.chat_message("assistant"):
        full_response = ''
        sources_data = ''
        with st.expander("Réponse"):
            if USE_SOURCES:
                response = None #   rag.generate_response(query_engine, prompt)
                text_generator = response.response_gen
            placeholder = st.empty()
            stop_generation = False
            for item in text_generator:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
        with st.expander("Sources"):
            if USE_SOURCES:
                sources_data = response.get_formatted_sources(length=100)
                sources_text  = ""
                for source in response.source_nodes: 
                    if "page_label" in source.metadata:
                        sources_text += f"""{source.metadata["file_name"]}, page {source.metadata["page_label"]} : {str(round(source.score,2))} 
    """

                st.markdown(sources_text)
                message = {"role": "assistant",
                        "content": full_response,
                        "sources": sources_text}
            else : 
                message = {"role": "assistant",
                        "content": full_response}
            st.session_state.messages.append(message)
            st.session_state.is_generating = False
        assistant_must_answer = False