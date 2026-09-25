"""
CrewAI Multi-Agent System — Myntra Trend Analysis Crew
Detection signals: crewai, Agent(), Crew(), Task()
Asset type: ai_agent_1st_party
"""
import os
from crewai import Agent, Crew, Task, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool

search_tool = SerperDevTool()
web_tool = WebsiteSearchTool()

trend_researcher = Agent(
    role="Fashion Trend Researcher",
    goal="Identify emerging fashion trends from social media and runways",
    backstory="Expert at spotting trends before they hit mainstream retail",
    tools=[search_tool, web_tool],
    verbose=True,
    llm="gpt-4o",
)

catalog_analyst = Agent(
    role="Myntra Catalog Analyst",
    goal="Map trends to available Myntra inventory and identify gaps",
    backstory="Deep knowledge of Myntra's catalog and supplier network",
    tools=[],
    verbose=True,
    llm="gpt-4o",
)

content_writer = Agent(
    role="Fashion Content Writer",
    goal="Write trend reports and buying guides for Myntra editorial",
    backstory="Fashion writer with e-commerce SEO expertise",
    tools=[],
    verbose=True,
    llm="claude-3-5-sonnet-20241022",
)

research_task = Task(
    description="Research top 5 emerging fashion trends for the upcoming season in India.",
    expected_output="A structured list of 5 trends with evidence, target demographics, and timeline.",
    agent=trend_researcher,
)

analysis_task = Task(
    description="For each identified trend, find matching Myntra products and identify inventory gaps.",
    expected_output="Trend-to-product mapping with gap analysis and sourcing recommendations.",
    agent=catalog_analyst,
    context=[research_task],
)

report_task = Task(
    description="Write an editorial trend report suitable for Myntra's homepage and email newsletter.",
    expected_output="A 500-word trend report with product recommendations and CTAs.",
    agent=content_writer,
    context=[research_task, analysis_task],
)

trend_crew = Crew(
    agents=[trend_researcher, catalog_analyst, content_writer],
    tasks=[research_task, analysis_task, report_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = trend_crew.kickoff()
    print(result)
