from crewai import Agent, Task, Crew, Process
from crewai import LLM
from crewai_tools import SerperDevTool
from crewai.tools import tool
import re
from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel

import os
os.environ['SERPER_API_KEY'] = '0943b574c79b13b313ab7cd49a372c5da5ab191e'

web_search_tool = SerperDevTool()

class BlogPost(BaseModel):
    title: str
    intro: str
    code_snippet: str
    conclusion: str


# Initialize the Gemini 2.5 Flash model
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key="AIzaSyDtUGWVJE19r3mNAwkBn7F6y3NaDxLy3Xc" # Or set the environment variable
)


writing_agent = Agent(
    role="LinkedIn Post Generator",
    goal="Provide exceptional linkedin post writing services by following a multi-step process to write a post based on a topic accurately.",
    backstory="""You are an AI assistant for writing LinkedIn (to show the answer) and medium post (to show the code how it was done with crew AI, what components used and etc).
    You are an expert at following instructions. You will be given a topic, you have to write it in a format that is linkedIn and medium compatible and
    in a professional manner. For each task, you will be provided with the specific tool needed to accomplish it.
    Your job is to execute each task diligently and pass the results to the next step.""",
    tools=[], # The agent is not given any tools directly
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writing_agent = Agent(
    role="LinkedIn Post Generator",
    goal="Provide exceptional linkedin post writing services by following a multi-step process to write a post based on a topic accurately.",
    backstory="""You are an AI assistant for writing LinkedIn (to show the answer) and medium post (to show the code how it was done with crew AI, what components used and etc).
    You are an expert at following instructions. You will be given a topic, you have to write it in a format that is linkedIn and medium compatible and
    in a professional manner. For each task, you will be provided with the specific tool needed to accomplish it.
    Your job is to execute each task diligently and pass the results to the next step.""",
    tools=[], # The agent is not given any tools directly
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writing_Task = Task(
    description="You are linkedIn post generator. Write a linkedIn format post on the given topic: {{topic}}. Use approriate emojis, images, fact to explain. Use proper headings and keep it to 250 words, understandable by any person and people feel the content that it touches their life",
    expected_output="A linkedIn post , created in a way that explain the topic well with fact, figures and examples",
    agent=writing_agent,
    tools=[web_search_tool]
)

post_researcher = Task(
    description="You are a medium post generator. Find how to write post on medium, what formating , MARKDOWN is used , what elements are required and use it in next task",
    expected_output="Research how to write medium post and give it in a format that is ready to use by next task",
    agent=writing_agent,
    tools=[web_search_tool],
)


@tool("Crew AI code")
def linked_medium_code() -> str:
    """
   Read this file.This contains code to create linkedIn post and to medium blog.
    """
    # Find all integers in the string
    with open("/content/crew_Ai_pipeline.py", "r") as f:  # Or paste inline
            return f.read()

pydantic_model= Task(
    description="Given tool linked_medium_code, Use a medium blog post from code given in crew_Ai_pipeline file. Explain each code snippets and wrap code in code cell.",
    expected_output="A Medium blog post in BlogPost Format",
    agent=writing_agent,
    tools=[linked_medium_code],
    context=[post_researcher],
    output_json=BlogPost
)

formatting_medium_blog = Task(
    description=(
        "You are a Medium post generator.\n"
        "Given the BlogPost object from previous task, write the FINAL Medium article.\n"
        "- Use BlogPost.title as H1 (# Title).\n"
        "- Use BlogPost.intro as intro paragraphs.\n"
        "- Insert BlogPost.code_snippet in a fenced code block: `````` and explain each code block after it.\n"
        "- Use BlogPost.conclusion as closing paragraphs.\n"
        "Return ONLY markdown text suitable for direct paste into Medium, "
        "with NO JSON, NO additional explanation, and NO surrounding backticks "
        "around the whole article. Make this post engaging with some light humor to engage the audience. Ensure all code is understandable. Post tone should be professional"
    ),
    expected_output="Markdown Medium post ready to paste.",
    agent=writing_agent,
    context=[pydantic_model, post_researcher],
)

crew = Crew(
    agents=[writing_agent],
    tasks=[writing_Task,post_researcher,pydantic_model,formatting_medium_blog],
    process=Process.sequential,
    verbose=False 
)

result_agent_centric = crew.kickoff(inputs={'topic': "How will be life if we don't achieve what we wanted to ?"})
