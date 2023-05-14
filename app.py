
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは熱意溢れる教員が集う専門学校のグループのAIパートナーです。
さまざまな学科の国家試験、各種資格合格のために、学生の要望に合わせて学習、合格のためのアドバイスを行って下さい。
あなたの役割は生徒の合格力を向上させることなので、例えば以下のような関係のないことを聞かれても絶対に答えないでください。

*芸能人
*音楽
*演芸
＊映画
"""
# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは熱意溢れる教員が集う専門学校のグループのAIパートナーです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)
    
    response = openai.ChatCompletion.create(
        model="gpt-plus",
        messages=messages,
        temperature=0.0
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("Your AI Partner『合格 honki 応援くん』")
st.image("5_basicschoool")
st.write("AI Partner helps you to go get the licenses.")

user_input = st.text_input("なんでも質問を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
