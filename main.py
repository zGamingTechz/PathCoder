from openai import OpenAI
from keys import ai_key

def retrieve_answers(questions):
    q1 = questions[0]
    q2 = questions[1]
    q3 = questions[2]
    q4 = questions[3]
    q5 = questions[4]
    q6 = questions[5]
    q7 = questions[6]
    q8 = questions[7]        
    q9 = questions[8]

    return q1, q2, q3, q4, q5, q6, q7, q8, q9

def ai_response(questions, language, path, experience):
    q1, q2, q3, q4, q5, q6, q7, q8, q9 = retrieve_answers(questions=questions)

    client = OpenAI(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key=ai_key
    )

    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": f"You are tasked with generating a personalized learning roadmap for a user who wants to pursue a career in {path}. The roadmap should be customized based on the user's inputs, which include: Preferred Programming Language: {language}, Experience Level: {experience}. The user has also answered the following questions, and their responses are as follows: 1. Do you understand SQL and NoSQL databases?: {q1} 2. Do you understand object-oriented programming?: {q2} 3. Do you understand how memory management works in programming (e.g., stack vs. heap)?: {q3} 4. Do you know the concept of big-O notation in algorithm analysis?: {q4} 5. Do you understand the concept of recursion in programming?: {q5} 6. Do you know how to implement basic data structures like arrays, linked lists, and trees?: {q6} 7. Are you experienced with Git and GitHub?: {q7} 8. Do you know how to work with APIs in programming?: {q8} 9. How much time can you commit to learning coding weekly?: {q9} (Options: Less than 5 hours, 5-10 hours, 10+ hours). Now, based on the above inputs, generate a personalized roadmap for the user to follow, focusing on their career goals in {path}. The roadmap should not only pick relevant topics but also provide detailed step-by-step instructions. For example: If the user is new to SQL, include an introductory lesson to SQL. If the user is already experienced with Git and GitHub, skip basic Git tutorials and include more advanced Git features. Focus on the topics most relevant to the user's career path and provide clear, actionable steps that build up from foundational concepts to advanced knowledge in a structured manner. Ensure the roadmap progresses in a logical sequence, taking into account the user's experience and knowledge gaps. The roadmap should be broken into steps, separated by '$&'. You are only strictly allowed to output the roadmap steps separated by '$&' and nothing else."}
        ],
        temperature=0.7,
    )

    result = str(completion.choices[0].message.content)

    tasks = result.split("$&")

    return tasks
