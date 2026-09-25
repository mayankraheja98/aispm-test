"""CrewAI fashion analysis crew."""
from crewai import Agent, Task, Crew, Process

trend_analyst = Agent(
    role="Trend Analyst",
    goal="Identify top fashion trends from social media",
    backstory="Expert fashion analyst with 10 years of experience",
    verbose=True,
)

buyer = Agent(
    role="Merchandise Buyer",
    goal="Select products aligned with identified trends",
    backstory="Senior buyer at Myntra",
    verbose=True,
)

analyze_task = Task(
    description="Analyze trending colours for upcoming season",
    agent=trend_analyst,
)

buy_task = Task(
    description="Recommend products based on trend analysis",
    agent=buyer,
)

crew = Crew(
    agents=[trend_analyst, buyer],
    tasks=[analyze_task, buy_task],
    process=Process.sequential,
)

result = crew.kickoff()
