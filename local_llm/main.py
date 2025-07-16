import os
from llama_cpp import Llama

model_path = os.path.join("models", "openhermes-2.5-mistral-7b.Q4_K_M.gguf")

def llm_mistral():
    """_summary_
        gets the model from the '/models' folder and 
        use the setting to utilize the chat model (mistral)
        optimized for the low end gpu also
    Returns:
        _type_: return a llm model from the local path
    """
    llm = Llama(
        model_path=model_path,
        n_ctx=8192,
        n_gpu_layers=35,
        verbose=False
    )
    return llm


# user_input = "garam pani pine ka motape par asar batao"

# def format_prompt(user_input):
#     return f"""
#         You are an intelligent and multilingual AI assistant developed to help users with accurate, clear, and concise answers. 
#         Always respond in the **same language or tone** as the user's input, whether it's English, Hindi, Hinglish, or any other language. 
#         Adapt your reply to match the user's communication style. 
#         Answer professionally, respectfully, and helpfully at all times.

#         {user_input}
#     """

# prompt = format_prompt(user_input)


# output = llm(
#     prompt = prompt,
#     max_tokens=250
# )

# print(print(output["choices"][0]["text"].strip()))
