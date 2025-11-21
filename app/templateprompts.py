screener_template = """
Can you ask me some short questions that could be used to find out if I am highly likely to qualify for college financial aid, scholarships, grants and other student aid in this state?

Use intuitive, simple language. Explain the concepts as if I were new to them.

Try to stick to requirements that are as specific as possible to my background and this state.

Start with these lines: 
FROM SCREENER

### START QUESTIONS

End with this line:
### END QUESTIONS
"""

interviewer_template = """
You are a friendly interviewer. Please analyze the following questions to the best of your ability. 

For each question, if more information is needed to provide a definitive answer about college financial aid eligibility, say NOT_ENOUGH_INFO next to the question, 
but if no more information is needed to provide a definitive answer about college financial aid eligibility, 
say HAS_ENOUGH_INFO next to the question. Explain your answer. Try to use one sentence in your answers.

Use this format: 
### FROM INTERVIEWER
1. NOT_ENOUGH_INFO: More information is necessary to determine your city of residence.
2. HAS_ENOUGH_INFO: It was explicitly stated that your GPA is 3.4.
"""

reporter_template = """
You are an intelligent analyst. Given the provided information, what is a list of student aid programs that I am likely to qualify for in this state? 

Where possible, for each student aid type in your answer, try to include the names of specific programs, institutions or organizations. 

If I am highly likely to qualify, say so, otherwise say that I am not likely to qualify. 

Start with this line: 
### FROM REPORTER

When you're finished, say FINISHED.
"""

reporter_tool_prompt_template = """
Given this information, can you provide a list of relevant student aid programs that I am likely to qualify for in this state?

Include links.

Never suggest seeking information from elsewhere.

Provide links ONLY from your data, from the attached source file, if required, or if appropriate to the topic of the question.
"""