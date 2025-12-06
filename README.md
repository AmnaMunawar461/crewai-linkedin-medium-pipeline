🚀 **LinkedIn & Medium Post Generator using CrewAI + Gemini Flash**

**Automated Content Generation Pipeline**

This repository contains a fully-automated content creation pipeline built using CrewAI, Google Gemini 2.5 Flash, and Serper Search API.
It generates:

✍️ LinkedIn-optimized posts

📝 Medium-ready blog posts (with Markdown formatting)

📦 A structured workflow using Agents, Tasks, Tools, and Pydantic models

📌 **Features**

**✅ 1. Multi-Agent Content Workflow**

LinkedIn Post Agent → Writes engaging LinkedIn posts using research and structure

Medium Post Generator → Researches Medium formatting rules

Code-Explainer Agent → Reads local CrewAI pipeline file and explains it in a blog format

Medium Formatter → Writes a final polished Markdown article

**✅ 2. Uses Google Gemini Flash (Fast + Cheap)**

Configured via:

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key="YOUR_API_KEY"
)

**✅ 3. Integrated Web Search (Serper API)**

Improves factual accuracy using:

web_search_tool = SerperDevTool()

**✅ 4. Pydantic Model for Structured Blog Posts**

Ensures Medium posts are structured and validated:

class BlogPost(BaseModel):
    title: str
    intro: str
    code_snippet: str
    conclusion: str

🛠️ Project Structure
├── crew_Ai_pipeline.py     # Main pipeline code (used by the tool)
├── README.md               # Documentation
└── requirements.txt        # Dependencies

⚙️ How It Works

**1️⃣ Define Agents**

A single agent performs multiple writing tasks with different instructions.

**2️⃣ Define Tasks**

writing_Task → Creates LinkedIn post

post_researcher → Learns Medium formatting

pydantic_model → Converts research + code into BlogPost model

formatting_medium_blog → Produces final Medium article

**3️⃣ Custom Tool**

Reads pipeline file for the blog explanation:

@tool("Crew AI code")
def linked_medium_code():
    with open("/content/crew_Ai_pipeline.py", "r") as f:
        return f.read()

**4️⃣ Sequential Execution**

The Crew runs tasks one-by-one:

crew = Crew(
    agents=[writing_agent],
    tasks=[writing_Task, post_researcher, pydantic_model, formatting_medium_blog],
    process=Process.sequential,
)

**5️⃣ Run Pipeline**
result_agent_centric = crew.kickoff(
    inputs={'topic': "How will be life if we don't achieve what we wanted to ?"}
)

🚀 Getting Started
1. Clone Repo
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

2. Install dependencies
pip install -r requirements.txt

3. Set environment variables
export SERPER_API_KEY="your_serper_key"
export GEMINI_API_KEY="your_gemini_key"

4. Run workflow
python crew_Ai_pipeline.py

🧪 Example Output

A 250-word LinkedIn post with emojis + structure

A Medium-ready article with title, intro, code blocks, explanation, and conclusion
