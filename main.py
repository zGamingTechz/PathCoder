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
        model="meta-llama/Meta-Llama-3.1-70B-Instruct",
        messages=[
            {"role": "system", "content": f"You are tasked with generating a personalized learning roadmap for a user who wants to pursue a career in {path}. The roadmap should be customized based on the user's inputs, which include: Preferred Programming Language: {language}, Experience Level: {experience}. The user has also answered the following questions, and their responses are as follows: 1. Do you understand SQL and NoSQL databases?: {q1} 2. Do you understand object-oriented programming?: {q2} 3. Do you understand how memory management works in programming (e.g., stack vs. heap)?: {q3} 4. Do you know the concept of big-O notation in algorithm analysis?: {q4} 5. Do you understand the concept of recursion in programming?: {q5} 6. Do you know how to implement basic data structures like arrays, linked lists, and trees?: {q6} 7. Are you experienced with Git and GitHub?: {q7} 8. Do you know how to work with APIs in programming?: {q8} 9. How much time can you commit to learning coding weekly?: {q9} (Options: Less than 5 hours, 5-10 hours, 10+ hours). Based on the above inputs, generate a personalized roadmap for the user to follow, focusing on their career goals in {path}. The roadmap must: 1. Adapt to the user's time commitment. If the user has less than 5 hours per week, create a long roadmap with fewer tasks spread across multiple weeks. If the user has 10+ hours, include more tasks per week, estimating what can realistically be completed within 10 hours per week. 2. Start from foundational topics (if the user is a beginner or lacks knowledge in that area) and progressively build up to advanced concepts, skipping topics the user already knows based on their responses. 3. Include all essential topics for the user's career goals, including resume building, job preparation, and project creation. Ensure nothing critical is overlooked. 4. Provide actionable steps for each task, along with specific resources like YouTube tutorials, courses, websites, or tools. 5. Divide the roadmap by week, ensuring '$&' is placed **after every week count** (e.g., 'Week 1 $&'), and after **each task** within the week to enable easy splitting. 6. Progress logically, building on previously learned skills in a structured and clear way. Output example: 'Week 1 $& - Learn Python basics (variables, data types, control structures, functions) using this YouTube tutorial: https://www.youtube.com/watch?v=_uQrJ0TkZlc $& - Practice Python basics with exercises from LeetCode: https://leetcode.com $& - Understand Git basics using GitHub's interactive guide: https://try.github.io $& Week 2 $& - Learn basic web development using HTML/CSS with this freeCodeCamp course: https://www.freecodecamp.org $& - Practice HTML/CSS by building a simple portfolio website: https://scrimba.com/learn/htmlcss $&' Ensure the output is detailed, step-by-step, and follows this format strictly, with no markdown or additional symbols. All tasks and weeks should flow logically, leading the user towards their desired career goal in {path}."}
        ],
        temperature=0.7,
    )

    result = str(completion.choices[0].message.content)

    tasks = result.split("$&")

    return tasks


def chatbot_response(name, language, path, experience, message):
    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )

    completion = client.chat.completions.create(
        model="TheBloke/deepseek-coder-6.7B-instruct-GGUF",
        messages=[
            {"role": "system", "content": f"The user's name is {name}, he/she prefers to use {language}, they are a/an {experience} in the field of {path}. Always address the user by their name and only answwer questions related to Computer Science. If the user asks any question other than computer science tell them that you can only answer questions related to computer science. Also encourage the user to spend some time to solve the questions themselves and refer to Stackoverflow , geeks for geeks etc."},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
    )

    result = str(completion.choices[0].message.content)

    return result
