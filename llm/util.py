
SYSTEM_PROMPT = '''
You are a Car Expert, specifically for Audi. You will advice the User.
'''

def create_prompt(user_car:str, context:str) -> str:
    '''
    Create the User prompt with the Context.
    '''
    return f'''
    Determine if the price is jsutifeid based on the other cars and their prices.
    Justifiy your Answer, solely based in the context given. If you are unsure on a topic, then say so.

    The Car in question: 
    {user_car}

    Similar cars:
    {context}
    '''

