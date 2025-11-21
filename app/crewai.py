import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Set page config
st.set_page_config(page_title="CrewAI Blog Writer", page_icon="✍️",
                   layout="wide")

# Title and description
st.title("✍️ CrewAI Blog Content Generator")
st.markdown("""
This app demonstrates a simple CrewAI workflow where AI agents collaborate to:
1. Research a topic
2. Write a blog post based on the research
3. Edit and polish the final content
""")

# Sidebar for API keys
with st.sidebar:
    st.header("⚙️ Configuration")

    openai_api_key = st.text_input("OpenAI API Key", type="password",
                                   help="Enter your OpenAI API key")
    serper_api_key = st.text_input("Serper API Key (optional)",
                                   type="password",
                                   help="For web search - get free key at serper.dev")

    st.markdown("---")
    st.markdown("### About CrewAI")
    st.markdown("""
    CrewAI enables you to create autonomous AI agents that work together.

    **Key Concepts:**
    - **Agents**: AI workers with specific roles
    - **Tasks**: Jobs assigned to agents
    - **Crew**: Team of agents working together
    - **Process**: How agents collaborate (sequential/hierarchical)
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input("📝 Blog Topic",
                          placeholder="e.g., The Future of Artificial Intelligence")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run_button = st.button("🚀 Generate Blog Post", type="primary",
                           use_container_width=True)

# Status and output area
status_container = st.container()
output_container = st.container()


def create_blog_crew(topic, openai_key, serper_key=None):
    """Create a crew of agents to write a blog post"""

    # Set environment variables
    os.environ["OPENAI_API_KEY"] = openai_key
    if serper_key:
        os.environ["SERPER_API_KEY"] = serper_key
        search_tool = SerperDevTool()
    else:
        search_tool = None

    # Define agents
    researcher = Agent(
        role='Content Researcher',
        goal=f'Research comprehensive information about {topic}',
        backstory="""You are an expert researcher with a keen eye for finding 
        relevant and accurate information. You excel at gathering facts, statistics, 
        and insights from various sources.""",
        tools=[search_tool] if search_tool else [],
        verbose=True,
        allow_delegation=False
    )

    writer = Agent(
        role='Blog Writer',
        goal=f'Write an engaging and informative blog post about {topic}',
        backstory="""You are a skilled content writer who creates compelling 
        blog posts. You know how to structure content effectively and make 
        complex topics accessible to readers.""",
        verbose=True,
        allow_delegation=False
    )

    editor = Agent(
        role='Content Editor',
        goal='Polish and refine the blog post for publication',
        backstory="""You are a meticulous editor with an eye for detail. 
        You ensure content is clear, engaging, and free of errors. You also 
        improve flow and readability.""",
        verbose=True,
        allow_delegation=False
    )

    # Define tasks
    research_task = Task(
        description=f"""Research {topic} and gather:
        - Key facts and statistics
        - Current trends and developments
        - Expert opinions or notable quotes
        - Practical applications or examples

        Provide a comprehensive research summary.""",
        agent=researcher,
        expected_output="A detailed research summary with facts, trends, and insights"
    )

    writing_task = Task(
        description=f"""Using the research provided, write a blog post about {topic}.

        The blog post should:
        - Have an engaging introduction
        - Be structured with clear sections
        - Include the key findings from research
        - Have a compelling conclusion
        - Be approximately 500-700 words
        - Use a conversational yet professional tone""",
        agent=writer,
        expected_output="A complete blog post draft with introduction, body, and conclusion"
    )

    editing_task = Task(
        description="""Review and edit the blog post to ensure:
        - Clear and engaging writing
        - Proper structure and flow
        - Correct grammar and punctuation
        - Compelling headlines and subheadings
        - A strong call-to-action at the end

        Provide the final polished version.""",
        agent=editor,
        expected_output="A polished, publication-ready blog post"
    )

    # Create and return the crew
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


# Run the workflow when button is clicked
if run_button:
    if not openai_api_key:
        st.error("⚠️ Please provide your OpenAI API key in the sidebar.")
    elif not topic:
        st.error("⚠️ Please enter a blog topic.")
    else:
        with status_container:
            with st.spinner("🤖 AI agents are working on your blog post..."):
                try:
                    # Create the crew
                    crew = create_blog_crew(topic, openai_api_key,
                                            serper_api_key)

                    # Create progress indicators
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    status_text.text(
                        "🔍 Researcher is gathering information...")
                    progress_bar.progress(33)

                    # Execute the crew
                    result = crew.kickoff()

                    progress_bar.progress(100)
                    status_text.text("✅ Blog post generated successfully!")

                    # Display the result
                    with output_container:
                        st.markdown("---")
                        st.subheader("📄 Generated Blog Post")
                        st.markdown(result)

                        # Download button
                        st.download_button(
                            label="💾 Download Blog Post",
                            data=str(result),
                            file_name=f"{topic.replace(' ', '_').lower()}_blog.txt",
                            mime="text/plain"
                        )

                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
