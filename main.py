from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

llm=ChatGroq(temperature=0,
             model_name="llama3-70b-8192",
             api_key='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')

planner = Agent(
    llm=llm,
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    llm=llm,
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're a versatile content creator who writes compelling content "
              "across different platforms while maintaining consistent messaging "
              "and brand voice.",
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    llm=llm,
   role="Content Editor",
    goal="Edit and optimize content across all formats",
    backstory="You ensure all content pieces maintain consistent quality, "
              "brand voice, and messaging while being optimized for their "
              "respective platforms.",
    allow_delegation=False,
    verbose=True
)

social_media_specialist = Agent(
    llm=llm,
    role="Social Media Specialist",
    goal="Create platform-specific social media content for {topic}",
    backstory="You specialize in crafting engaging social media content "
              "optimized for Twitter, LinkedIn, and other platforms.",
    allow_delegation=False,
    verbose=True
)

video_scriptwriter = Agent(
    llm=llm,
    role="Video Scriptwriter",
    goal="Create engaging video scripts for {topic}",
    backstory="You write compelling video scripts that maintain viewer "
              "attention while delivering valuable information.",
    allow_delegation=False,
    verbose=True
)

email_marketer = Agent(
    llm=llm,
    role="Email Marketing Specialist",
    goal="Create converting email marketing campaigns for {topic}",
    backstory="You specialize in writing email sequences that engage "
              "subscribers and drive desired actions.",
    allow_delegation=False,
    verbose=True
)

visual_prompter = Agent(
    llm=llm,
    role="Visual Content Prompter",
    goal="Create detailed image generation prompts for {topic}",
    backstory="You excel at writing detailed prompts for AI image "
              "generation tools that align with the content strategy.",
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        "1. Analyze the topic and develop a unified content strategy\n"
        "2. Identify target audiences across different platforms\n"
        "3. Create platform-specific content guidelines\n"
        "4. Develop key messaging points and SEO keywords\n"
        "5. Outline content requirements for each format"
    ),
    expected_output="A comprehensive content strategy document with "
                    "platform-specific guidelines and messaging framework.",
    agent=planner
)

write_blog = Task(
    description=(
        "1. Create an SEO-optimized blog post\n"
        "2. Include engaging headers and subheaders\n"
        "3. Incorporate relevant keywords naturally\n"
        "4. Add calls-to-action\n"
        "5. Optimize for readability"
    ),
    expected_output="A complete blog post in markdown format with "
                    "SEO optimization and proper formatting.",
    agent=writer
)

create_tweets = Task(
    description=(
        "1. Create a thread of 5-7 engaging tweets\n"
        "2. Include relevant hashtags\n"
        "3. Optimize for engagement\n"
        "4. Include call-to-actions"
    ),
    expected_output="A tweet thread with engaging content and "
                    "appropriate hashtags.",
    agent=social_media_specialist
)

create_linkedin_post = Task(
    description=(
        "1. Write a professional LinkedIn post\n"
        "2. Include relevant hashtags\n"
        "3. Optimize for B2B audience\n"
        "4. Add compelling call-to-action"
    ),
    expected_output="A LinkedIn post optimized for professional "
                    "audience engagement.",
    agent=social_media_specialist
)

create_video_script = Task(
    description=(
        "1. Write an engaging video script\n"
        "2. Include hook, main content, and call-to-action\n"
        "3. Add timestamps and scene descriptions\n"
        "4. Include b-roll suggestions"
    ),
    expected_output="A complete video script with timing, "
                    "visuals, and dialogue.",
    agent=video_scriptwriter
)

create_email_campaign = Task(
    description=(
        "1. Create email subject lines\n"
        "2. Write email body content\n"
        "3. Include personalization elements\n"
        "4. Add compelling CTAs"
    ),
    expected_output="A complete email marketing sequence "
                    "with subject lines and body content.",
    agent=email_marketer
)

create_image_prompts = Task(
    description=(
        "1. Create detailed image generation prompts\n"
        "2. Include style, mood, and composition details\n"
        "3. Specify important visual elements\n"
        "4. Add technical requirements"
    ),
    expected_output="Detailed image generation prompts for "
                    "each content piece.",
    agent=visual_prompter
)

crew = Crew(
    agents=[planner, writer, editor , social_media_specialist,video_scriptwriter,email_marketer,visual_prompter],
    tasks=[plan, write_blog , create_email_campaign,create_image_prompts,create_linkedin_post,create_video_script,create_tweets],
    verbose=2
)

result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})


from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/generate_content', methods=['POST'])
def generate_content():
     data = request.get_json()
     topic = data.get('topic')

     # Your existing code to generate content using 'crew.kickoff' goes here
     # Replace '{topic}' with 'topic' variable
     result = crew.kickoff(inputs={"topic": topic})

     return jsonify({'content': result})

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5000)