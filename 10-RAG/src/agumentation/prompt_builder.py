def build_prompt(query:str,context:str)->str:
    prompt = f"""

you are a helpful universiy assistant 
Anser the user's question using only the provided context.
If the answer cannot be found in the context , say that you do not have enough information.

Context:
{context}

Question:
{query}


Answer:

"""
    return prompt