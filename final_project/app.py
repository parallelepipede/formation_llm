import streamlit as st
from utils.const import USE_SOURCES,PROMPT_MESSAGE,START_MESSAGE


st.set_page_config(
    page_title=f"Question & Answers",
    page_icon="🗨️",
    # initial_sidebar_state='collapsed'
)


model = None 
rag = None


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
        if model is not None :
            prompt = model.prompts.prompt_format_without_context.format(
                instruction=prompt)
            if USE_SOURCES:
                response = rag.query_engine.query(prompt)
                text_generator = response.response_gen
            else:
                text_generator = model.generate_response(
                    prompt)

            placeholder = st.empty()
            stop_generation = False
            for item in text_generator:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
            if USE_SOURCES:
                sources_data = response.get_formatted_sources(length=100)
                st.write(sources_data)
                
                for source in response.source_nodes: 
                    print(source.metadata["file_name"], round(source.score,2))

                message = {"role": "assistant",
                        "content": full_response,
                        "sources": sources_data}
            else : 
                message = {"role": "assistant",
                        "content": full_response}
            st.session_state.messages.append(message)
            st.session_state.is_generating = False
        assistant_must_answer = False
