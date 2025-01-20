from openai import OpenAI
from keys import ai_key

def retrieve_answers(request):
    q1 = request.form['q1']
    q2 = request.form['q2']
    q3 = request.form['q3']
    q4 = request.form['q4']
    q5 = request.form['q5']
    q6 = request.form['q6']
    q7 = request.form['q7']
    q8 = request.form['q8']        
    q9 = request.form['q9']

    return q1, q2, q3, q4, q5, q6, q7, q8, q9

def ai_response(request):
    q1, q2, q3, q4, q5, q6, q7, q8, q9 = retrieve_answers(request=request)

    client = OpenAI(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key=ai_key
    )

    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": ""}
        ],
        temperature=0.7,
    )

    result = str(completion.choices[0].message.content)

    tasks = result.split("$&")

    return tasks
