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
            {"role": "system", "content": f"You are tasked with generating a personalized learning roadmap for a user who wants to pursue a career in {path}. The roadmap should be customized based on the user's inputs, which include: Preferred Programming Language: {language}, Experience Level: {experience}. The user has also answered the following questions, and their responses are as follows: 1. Do you understand SQL and NoSQL databases?: {q1} 2. Do you understand object-oriented programming?: {q2} 3. Do you understand how memory management works in programming (e.g., stack vs. heap)?: {q3} 4. Do you know the concept of big-O notation in algorithm analysis?: {q4} 5. Do you understand the concept of recursion in programming?: {q5} 6. Do you know how to implement basic data structures like arrays, linked lists, and trees?: {q6} 7. Are you experienced with Git and GitHub?: {q7} 8. Do you know how to work with APIs in programming?: {q8} 9. How much time can you commit to learning coding weekly?: {q9} (Options: Less than 5 hours, 5-10 hours, 10+ hours). Based on the above inputs, generate a personalized roadmap for the user to follow, focusing on their career goals in {path}. The roadmap should start from foundational topics (if the user is a beginner or lacks knowledge in that area) and progress to advanced topics, including resume building, job preparation, and project creation. Skip topics the user already knows based on their inputs. The roadmap should be split by week, with '$&' after every week count for easy splitting. Within each week, list all tasks as bullet points in logical order of progression. Ensure each task is separated by '$&' to allow splitting between steps easily. Each task must include actionable steps and specific resources (e.g., YouTube links, websites, or platforms). For example: 'Week 1 $& - Learn Python basics (variables, data types, control structures, functions) using this YouTube tutorial: https://www.youtube.com/watch?v=_uQrJ0TkZlc $& - Practice Python basics with exercises from LeetCode: https://leetcode.com $& - Understand Git basics using GitHub's interactive guide: https://try.github.io $&'. Ensure the roadmap progresses logically, building knowledge from foundational concepts to advanced skills, tailored to the user's career goals and experience level. Output the roadmap strictly in this format with no markdown or additional symbols."}
        ],
        temperature=0.7,
    )

    result = str(completion.choices[0].message.content)

    tasks = result.split("$&")

    return tasks
