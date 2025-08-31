from flask import Flask, jsonify, request, render_template_string, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime, timezone
import time as time_module
import pytz
import os
import sys
import logging
import uuid

logging.basicConfig(
    level=logging.INFO,  # adjust to DEBUG for more verbosity
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


app = Flask(__name__, 
            static_folder="client",   # serve CSS/JS/images from client/
            template_folder="client")

CORS(app)


DEFAULT_FLASK_PORT = 5000

IST = pytz.timezone("Asia/Kolkata")

remote_work_content = """
<p>Over the past few years, the way we work has undergone a massive transformation. What was once considered a privilege for a few—working remotely—has now become a defining feature of modern businesses across the globe. The COVID-19 pandemic accelerated this shift, but the long-term impact of remote work goes far beyond temporary necessity. It has reshaped how companies operate, how employees perceive work-life balance, and how the future of business will unfold.</p>

<h2>The Remote Work Revolution</h2>
<p>Remote work isn’t new. Tech companies and freelancers have been leveraging it for years. However, the pandemic forced entire industries to adopt remote-first models overnight. Organizations realized that productivity didn’t necessarily decline when employees worked from home. In fact, in many cases, output increased as workers gained more flexibility and autonomy.</p>
<p>This shift sparked a global conversation about the necessity of traditional office spaces and whether businesses could thrive in a decentralized environment.</p>

<h2>Benefits Driving the Shift</h2>
<ul>
  <li><b>Flexibility and Autonomy:</b> Employees are no longer tied to rigid schedules or physical office spaces. This flexibility has improved job satisfaction and allowed people to design workdays that suit their lifestyles.</li>
  <li><b>Access to Global Talent:</b> Businesses can now hire beyond geographical boundaries. Remote work enables organizations to tap into diverse skill sets from around the world, creating stronger, more innovative teams.</li>
  <li><b>Cost Savings:</b> Companies save significantly on overhead expenses like office space, utilities, and travel costs. At the same time, employees save on commuting and relocation expenses.</li>
  <li><b>Work-Life Balance:</b> With less time spent commuting, employees can dedicate more time to family, health, and personal growth—improving overall well-being.</li>
</ul>

<h2>Challenges Along the Way</h2>
<p>Despite its advantages, remote work also brings unique challenges:</p>
<ul>
  <li><b>Collaboration and Communication Gaps:</b> Without face-to-face interaction, building strong team connections can be harder.</li>
  <li><b>Employee Burnout:</b> The blurred boundaries between work and personal life sometimes lead to overworking.</li>
  <li><b>Cybersecurity Risks:</b> Remote work increases the risk of data breaches if proper measures aren’t in place.</li>
  <li><b>Cultural Disconnect:</b> Fostering company culture in a fully virtual setting requires extra effort and creativity.</li>
</ul>

<h2>Hybrid Work: The Best of Both Worlds</h2>
<p>Many businesses are now embracing a <b>hybrid work model</b>, blending remote flexibility with in-office collaboration. This approach offers the advantages of remote work while retaining the benefits of in-person connection. Companies are reimagining office spaces as hubs for innovation, collaboration, and culture-building rather than places for everyday tasks.</p>

<h2>The Future of Business in a Remote-First World</h2>
<p>The rise of remote work is not a passing trend—it’s a long-term transformation. Here’s what we can expect moving forward:</p>
<ul>
  <li><b>Tech-Driven Workflows:</b> Tools like Zoom, Slack, Microsoft Teams, and AI-powered collaboration platforms will continue to evolve.</li>
  <li><b>Focus on Employee Well-Being:</b> Businesses will prioritize mental health, flexible hours, and burnout prevention.</li>
  <li><b>Outcome-Oriented Work:</b> Success will be measured less by hours clocked in and more by results delivered.</li>
  <li><b>Decentralized Business Models:</b> Companies may move toward smaller, regional hubs rather than central headquarters.</li>
</ul>

<h2>Final Thoughts</h2>
<p>Remote work is redefining the future of business. What started as a response to crisis has now opened new doors for innovation, inclusivity, and productivity. The companies that thrive will be those that adapt, embrace flexibility, and invest in building strong digital-first cultures.</p>

<p>As we look ahead, one thing is clear: <b>the workplace of the future is no longer a place—it’s an ecosystem of people, technology, and flexibility working together to achieve success.</b></p>
"""

ai_content = """
<p>Artificial Intelligence (AI) is no longer a futuristic concept—it has become an integral part of our daily lives, transforming industries, businesses, and the way we interact with technology. As we step into 2025, AI is expected to advance even further, reshaping economies, unlocking new opportunities, and raising important ethical questions. The year 2025 marks a turning point in how AI will influence the future of humanity.</p>

<h2>Smarter Automation Across Industries</h2>
<p>Automation powered by AI is already disrupting sectors like finance, healthcare, retail, and manufacturing. In 2025, businesses will increasingly rely on AI-driven tools for streamlining workflows, predictive analytics, fraud detection, and supply chain optimization. AI assistants will take over repetitive tasks, allowing humans to focus on creativity, strategy, and innovation.</p>

<h2>Healthcare Powered by AI</h2>
<p>AI will play a transformative role in healthcare, from early disease detection to personalized treatment plans. Advanced algorithms will analyze medical data with greater accuracy, enabling faster diagnoses and more effective therapies. Virtual health assistants and AI-powered wearable devices will empower patients to take better control of their well-being.</p>

<h2>AI and Human Collaboration</h2>
<p>The narrative around AI replacing humans is shifting toward AI enhancing human potential. In 2025, collaboration between humans and AI will become more seamless. From creative industries to scientific research, AI will serve as a partner—providing insights, generating ideas, and accelerating breakthroughs that were once unimaginable.</p>

<h2>Ethical and Regulatory Challenges</h2>
<p>As AI becomes more powerful, concerns around ethics, privacy, and accountability will intensify. Governments and organizations will need to establish clearer regulations to ensure responsible AI usage. Questions such as who owns AI-generated content, how to prevent algorithmic bias, and how to safeguard personal data will be at the forefront of policy discussions in 2025.</p>

<h2>Rise of Generative AI</h2>
<p>Generative AI, capable of creating text, images, music, and even software code, will reach new heights by 2025. This will fuel innovation in content creation, education, entertainment, and product design. At the same time, businesses will need to tackle the challenges of misinformation and copyright issues that generative AI might create.</p>

<h2>AI in Everyday Life</h2>
<p>AI will become more deeply embedded in daily routines—from smarter personal assistants and AI-driven education platforms to autonomous vehicles and energy-efficient smart cities. The technology will be more accessible, affordable, and integrated into household devices, making life more convenient and efficient.</p>

<h2>Final Thoughts</h2>
<p>The future of AI in 2025 is not just about technological advancement—it is about how humanity chooses to adopt, regulate, and collaborate with these intelligent systems. AI holds the promise of solving global challenges, from climate change to healthcare access, but it also comes with responsibilities. The organizations and societies that thrive will be those that embrace AI’s potential while ensuring it serves the greater good.</p>

<p>In 2025, one thing is certain: Artificial Intelligence will no longer be just a tool—it will be a transformative force shaping the way we live, work, and innovate.</p>
"""

sustainable_living_content = """
<p>Sustainable living is no longer just a trend—it is a necessity for the survival of our planet and the well-being of future generations. As climate change, resource depletion, and environmental degradation intensify, individuals and communities across the world are seeking practical ways to live more responsibly. Embracing eco-friendly practices doesn’t mean giving up comfort or convenience; instead, it means making conscious choices that reduce waste, conserve resources, and promote harmony with nature. This complete guide explores actionable steps for adopting a sustainable lifestyle.</p>

<h2>Understanding Sustainable Living</h2>
<p>Sustainable living involves making lifestyle choices that minimize negative environmental impacts while enhancing personal and community well-being. At its core, it emphasizes the “three Rs”—reduce, reuse, and recycle—along with mindful consumption and ethical decision-making. It is about creating balance: meeting present needs without compromising the ability of future generations to meet theirs.</p>

<h2>1. Sustainable Home Practices</h2>
<ul>
  <li><b>Energy Efficiency:</b> Switch to LED lighting, install smart thermostats, and invest in energy-efficient appliances. Consider renewable energy sources such as rooftop solar panels to reduce dependence on fossil fuels.</li>
  <li><b>Water Conservation:</b> Fix leaks, install low-flow showerheads, and collect rainwater for household use. Practicing mindful water consumption can drastically cut waste.</li>
  <li><b>Eco-Friendly Materials:</b> Choose non-toxic paints, bamboo furniture, or recycled materials for home renovations and decor. Supporting sustainable brands reduces the carbon footprint of your household.</li>
</ul>

<h2>2. Sustainable Food Choices</h2>
<ul>
  <li><b>Eat Local and Seasonal:</b> Purchasing food from local farmers reduces transportation emissions and supports community agriculture.</li>
  <li><b>Plant-Based Diet:</b> Incorporating more fruits, vegetables, and plant-based proteins helps lower greenhouse gas emissions compared to a meat-heavy diet.</li>
  <li><b>Reduce Food Waste:</b> Plan meals, store food properly, and compost leftovers instead of sending them to landfills where they produce methane.</li>
  <li><b>Organic and Fair-Trade Products:</b> Supporting these products ensures healthier soil, sustainable farming practices, and fair wages for farmers.</li>
</ul>

<h2>3. Sustainable Transportation</h2>
<ul>
  <li><b>Public Transit and Carpooling:</b> Reduce emissions by opting for buses, trains, or shared rides instead of individual car use.</li>
  <li><b>Electric and Hybrid Vehicles:</b> If driving is necessary, consider switching to cleaner alternatives that reduce fossil fuel consumption.</li>
  <li><b>Cycling and Walking:</b> Not only are these zero-emission options, but they also improve health and fitness.</li>
</ul>

<h2>4. Sustainable Consumption</h2>
<ul>
  <li><b>Minimalism:</b> Buy only what you need and invest in long-lasting, high-quality products instead of cheap, disposable items.</li>
  <li><b>Second-Hand Shopping:</b> Thrift stores, online marketplaces, and clothing swaps extend the life cycle of products while reducing demand for new manufacturing.</li>
  <li><b>Plastic-Free Lifestyle:</b> Replace single-use plastics with reusable alternatives such as stainless steel bottles, cloth bags, and glass containers.</li>
</ul>

<h2>5. Sustainable Fashion</h2>
<p>Fast fashion is one of the largest contributors to pollution and unethical labor practices. Eco-friendly fashion choices include:</p>
<ul>
  <li>Choosing clothes made from organic cotton, hemp, or recycled fabrics.</li>
  <li>Supporting brands with transparent and ethical supply chains.</li>
  <li>Repairing and repurposing old clothing instead of discarding them.</li>
</ul>

<h2>6. Sustainable Technology and Digital Habits</h2>
<ul>
  <li><b>Energy-Efficient Devices:</b> Purchase electronics that meet energy efficiency standards.</li>
  <li><b>Cloud Storage with Renewable Energy Providers:</b> Opt for platforms powered by clean energy.</li>
  <li><b>Digital Decluttering:</b> Reduce storage needs and e-waste by deleting unnecessary files and recycling old devices responsibly.</li>
</ul>

<h2>7. Sustainable Community Living</h2>
<ul>
  <li><b>Community Gardens:</b> Growing food locally fosters resilience and reduces reliance on industrial agriculture.</li>
  <li><b>Sharing Economies:</b> Platforms for tool sharing, ride-sharing, and coworking reduce overall consumption.</li>
  <li><b>Advocacy and Education:</b> Encourage sustainable policies at local, national, and global levels by raising awareness and supporting eco-conscious initiatives.</li>
</ul>

<h2>Benefits of Sustainable Living</h2>
<p>Adopting eco-friendly practices goes beyond protecting the environment. It also improves quality of life, saves money, promotes health, and strengthens communities. By conserving resources, reducing waste, and supporting ethical systems, individuals can play an active role in shaping a more sustainable world.</p>

<h2>Final Thoughts</h2>
<p>Sustainable living is a journey, not a destination. It requires consistent effort, conscious decision-making, and a willingness to adapt. While individual actions may seem small, collectively they can create a powerful ripple effect, leading to systemic change. As we move forward, living sustainably is not just an option—it is the responsibility of each one of us to ensure a cleaner, greener, and healthier planet for generations to come.</p>
"""

# 1. Exploring the Hidden Gems of Southeast Asia
blog_southeast_asia = """
<p>Southeast Asia is a region celebrated for its stunning landscapes, vibrant cultures, and rich history. While destinations like Bangkok, Bali, and Singapore often dominate travel itineraries, the true magic of Southeast Asia lies in its hidden gems—lesser-known places that offer authenticity, tranquility, and unique experiences. For travelers seeking to go beyond the beaten path, these destinations promise unforgettable memories.</p>

<h2>Why Explore Hidden Gems?</h2>
<p>Hidden gems provide the chance to connect more deeply with local culture, avoid tourist crowds, and discover natural beauty untouched by mass tourism. They often reflect traditions, heritage, and lifestyles that remain intact despite modernization.</p>

<h2>Top Hidden Gems in Southeast Asia</h2>
<ul>
  <li><b>Luang Prabang, Laos:</b> A UNESCO World Heritage city where golden temples, French colonial architecture, and serene riverside views create a timeless charm.</li>
  <li><b>Siquijor, Philippines:</b> Known as the mystical island, it offers white-sand beaches, waterfalls, and folklore of healing traditions.</li>
  <li><b>Kampot, Cambodia:</b> Famous for pepper plantations and tranquil riverside scenery, perfect for slow travel.</li>
  <li><b>Komodo Islands, Indonesia:</b> Home to the world’s largest lizard, pink beaches, and breathtaking diving spots.</li>
  <li><b>Phong Nha, Vietnam:</b> A paradise for cave explorers, hosting some of the largest and most spectacular caves on Earth.</li>
</ul>

<h2>Travel Tips for Hidden Gems</h2>
<ul>
  <li>Respect local cultures and traditions.</li>
  <li>Support local businesses and artisans.</li>
  <li>Be eco-conscious—avoid plastic, respect wildlife, and minimize your footprint.</li>
</ul>

<h2>Final Thoughts</h2>
<p>Exploring hidden gems in Southeast Asia allows travelers to move beyond tourist traps and experience authentic connections. Whether it’s a secluded island, a small village, or a natural wonder, these destinations remind us that true beauty often lies off the beaten path.</p>
"""


# 2. The Art of Mindful Cooking: Recipes for the Soul
blog_mindful_cooking = """
<p>Cooking is more than a means of nourishment—it is an art, a ritual, and a way to cultivate mindfulness. In our fast-paced lives, the kitchen can become a sanctuary where we slow down, engage our senses, and find joy in the simple act of preparing food. Mindful cooking transforms meals into soul-nourishing experiences, fostering both health and inner peace.</p>

<h2>What is Mindful Cooking?</h2>
<p>Mindful cooking is the practice of being fully present while preparing food. It involves noticing textures, aromas, colors, and sounds, and appreciating the ingredients and process. It’s about cooking with intention, gratitude, and awareness rather than rushing through the motions.</p>

<h2>Principles of Mindful Cooking</h2>
<ul>
  <li><b>Gratitude:</b> Acknowledge the farmers, soil, and effort behind each ingredient.</li>
  <li><b>Sensory Awareness:</b> Smell the spices, feel the textures, and listen to the sizzling pan.</li>
  <li><b>Slow Preparation:</b> Avoid multitasking and immerse yourself in each step.</li>
  <li><b>Health and Wholesomeness:</b> Choose fresh, nutritious, and seasonal ingredients.</li>
</ul>

<h2>Mindful Recipes for the Soul</h2>
<ul>
  <li><b>Golden Turmeric Lentil Soup:</b> A warm, grounding dish rich in antioxidants.</li>
  <li><b>Fresh Garden Salad with Citrus Dressing:</b> Celebrating seasonal vegetables with zesty flavors.</li>
  <li><b>Herbal Infused Teas:</b> Chamomile, mint, or ginger teas that soothe body and mind.</li>
  <li><b>Dark Chocolate Bliss Bites:</b> A guilt-free dessert that encourages slow savoring.</li>
</ul>

<h2>Final Thoughts</h2>
<p>Cooking mindfully is about nurturing yourself and those around you. By slowing down and embracing the process, meals become rituals of care, creativity, and connection. Every dish, when made with mindfulness, truly becomes food for the soul.</p>
"""


# 3. Building Resilience: Mental Health Strategies for Modern Life
blog_resilience = """
<p>Life today is fast-paced, unpredictable, and often overwhelming. Building resilience—the ability to adapt, recover, and thrive in the face of adversity—is essential for maintaining mental health. Resilience is not about avoiding stress but developing the skills and mindset to manage challenges effectively.</p>

<h2>What is Resilience?</h2>
<p>Resilience is the psychological strength that allows individuals to cope with stress and recover from setbacks. It is a skill that can be cultivated through consistent practices and self-awareness.</p>

<h2>Strategies for Building Resilience</h2>
<ul>
  <li><b>Mindfulness and Meditation:</b> Regular practice enhances emotional regulation and reduces anxiety.</li>
  <li><b>Positive Self-Talk:</b> Reframe challenges as opportunities for growth rather than obstacles.</li>
  <li><b>Strong Support Networks:</b> Leaning on friends, family, or support groups strengthens emotional security.</li>
  <li><b>Healthy Lifestyle:</b> Balanced nutrition, regular exercise, and adequate sleep improve mental resilience.</li>
  <li><b>Setting Realistic Goals:</b> Break tasks into manageable steps to prevent overwhelm.</li>
</ul>

<h2>The Role of Self-Compassion</h2>
<p>Resilience is not about being strong all the time. Practicing self-compassion—acknowledging pain, forgiving mistakes, and treating yourself kindly—plays a vital role in mental health.</p>

<h2>Final Thoughts</h2>
<p>Resilience empowers us to navigate uncertainty with confidence. By incorporating mindful practices, self-care, and supportive relationships, we can strengthen our ability to thrive even in life’s most challenging moments.</p>
"""


# 4. The Evolution of Digital Entertainment: From Streaming to Virtual Reality
blog_digital_entertainment = """
<p>The entertainment industry has undergone a revolution in the past decade. From physical media and cable television to on-demand streaming and immersive virtual reality (VR), digital entertainment continues to reshape how audiences consume content. This evolution reflects not just technological advancement but also changing cultural habits and expectations.</p>

<h2>The Rise of Streaming Platforms</h2>
<p>Streaming services like Netflix, Disney+, and Spotify disrupted traditional media by offering instant access to vast libraries of movies, shows, and music. Subscription-based models replaced DVD rentals and cable bundles, giving audiences convenience and personalization.</p>

<h2>Interactive and On-Demand Experiences</h2>
<p>Modern consumers demand control over what, when, and how they watch or listen. Interactive storytelling, personalized playlists, and algorithm-driven recommendations are redefining entertainment as a two-way experience rather than a passive one.</p>

<h2>Virtual and Augmented Reality</h2>
<p>In 2025 and beyond, VR and AR will revolutionize entertainment. Virtual concerts, immersive gaming, and VR cinemas are already redefining audience engagement. These technologies blur the line between physical and digital experiences, creating new opportunities for creativity and storytelling.</p>

<h2>The Future of Digital Entertainment</h2>
<ul>
  <li><b>AI-Generated Content:</b> Personalized movies, games, and music designed with AI assistance.</li>
  <li><b>Immersive Social Spaces:</b> Virtual reality hangouts and metaverse platforms.</li>
  <li><b>Blockchain Integration:</b> NFTs and decentralized ownership of digital assets.</li>
</ul>

<h2>Final Thoughts</h2>
<p>The digital entertainment industry is no longer about passive consumption—it’s about participation, immersion, and personalization. As technology continues to advance, the boundaries of creativity and storytelling will expand in ways we are only beginning to imagine.</p>
"""


# 5. The Science of Sleep: Optimizing Your Rest for Better Health
blog_sleep_science = """
<p>Sleep is one of the most important yet overlooked pillars of health. In a world where productivity often takes precedence, millions struggle with poor sleep, leading to health issues ranging from fatigue to chronic illness. Understanding the science of sleep can help us optimize rest, improve performance, and enhance overall well-being.</p>

<h2>Why Sleep Matters</h2>
<p>During sleep, the body repairs tissues, consolidates memories, and balances hormones. Without quality sleep, physical and mental health suffer. Adequate rest improves mood, focus, immune function, and even weight management.</p>

<h2>The Sleep Cycle</h2>
<p>Sleep occurs in cycles lasting 90–120 minutes, alternating between REM (Rapid Eye Movement) and non-REM stages. Deep non-REM sleep restores the body, while REM sleep supports memory and learning. A balanced cycle is essential for optimal recovery.</p>

<h2>Common Sleep Disruptors</h2>
<ul>
  <li><b>Screen Time:</b> Blue light from phones and laptops disrupts melatonin production.</li>
  <li><b>Stress and Anxiety:</b> Mental overactivity can make it difficult to fall or stay asleep.</li>
  <li><b>Poor Sleep Environment:</b> Noise, light, and uncomfortable bedding affect sleep quality.</li>
  <li><b>Irregular Schedules:</b> Inconsistent sleep times confuse the body’s circadian rhythm.</li>
</ul>

<h2>Tips for Better Sleep</h2>
<ul>
  <li>Maintain a consistent sleep schedule—even on weekends.</li>
  <li>Create a relaxing bedtime routine (reading, meditation, herbal teas).</li>
  <li>Limit caffeine and heavy meals before bedtime.</li>
  <li>Optimize your sleep environment with blackout curtains and cool temperatures.</li>
  <li>Use technology mindfully—turn off screens at least an hour before sleep.</li>
</ul>

<h2>Final Thoughts</h2>
<p>Optimizing sleep is not a luxury—it’s a necessity for better health, productivity, and longevity. By understanding the science of sleep and adopting simple practices, we can unlock the full potential of restorative rest and live healthier, more energized lives.</p>
"""


climate_change_content = """
<p>Climate change is one of the most pressing issues of our time. While governments and corporations play a major role, individual actions matter too. From reducing energy consumption to supporting sustainable brands, every step counts.</p>
<h2>Everyday Actions</h2>
<ul>
    <li>Switch to renewable energy sources where possible.</li>
    <li>Reduce, reuse, and recycle to minimize waste.</li>
    <li>Support local and sustainable food options.</li>
    <li>Advocate for climate-friendly policies in your community.</li>
</ul>
<h2>Final Thoughts</h2>
<p>Small changes, when multiplied by millions, can transform the world. Start today and be part of the solution.</p>
"""

mindfulness_content = """
<p>Mindfulness is the practice of being present in the moment. It helps reduce stress, improve focus, and enhance overall well-being.</p>
<h2>How to Practice Mindfulness</h2>
<ul>
    <li>Start your day with a few minutes of deep breathing.</li>
    <li>Take mindful breaks during work to check in with your body and mind.</li>
    <li>Practice gratitude and self-compassion daily.</li>
</ul>
<h2>Final Thoughts</h2>
<p>Mindfulness is a skill that grows with practice. Begin with small steps and notice the positive changes in your life.</p>
"""

investing_content = """
<p>Investing is a powerful way to build wealth and secure your financial future. This guide covers the basics for beginners.</p>
<h2>Key Steps</h2>
<ul>
    <li>Set clear financial goals.</li>
    <li>Understand different investment options: stocks, bonds, mutual funds, and ETFs.</li>
    <li>Diversify your portfolio to manage risk.</li>
    <li>Start early and invest consistently.</li>
</ul>
<h2>Final Thoughts</h2>
<p>Investing doesn’t have to be complicated. With the right knowledge and discipline, anyone can grow their wealth over time.</p>
"""

reading_content = """
<p>In a digital world, books remain a source of inspiration, knowledge, and escape. Reading stimulates the mind and nurtures empathy.</p>
<h2>Benefits of Reading</h2>
<ul>
    <li>Improves vocabulary and communication skills.</li>
    <li>Reduces stress and enhances mental health.</li>
    <li>Expands imagination and creativity.</li>
</ul>
<h2>Final Thoughts</h2>
<p>Make time for reading every day. The right book can change your perspective—and your life.</p>
"""

fitness_content = """
<p>You don’t need a gym to stay fit. Home workouts can be just as effective with the right approach.</p>
<h2>Top Home Exercises</h2>
<ul>
    <li>Bodyweight squats and lunges</li>
    <li>Push-ups and planks</li>
    <li>Jumping jacks and burpees</li>
    <li>Yoga and stretching routines</li>
</ul>
<h2>Final Thoughts</h2>
<p>Consistency is key. Find a routine you enjoy and make fitness a part of your daily life.</p>
"""

budget_travel_content = """
<p>Travel doesn’t have to be expensive. With smart planning, you can explore the world without breaking the bank.</p>
<h2>Budget Travel Tips</h2>
<ul>
    <li>Book flights and accommodations in advance.</li>
    <li>Travel during off-peak seasons.</li>
    <li>Use public transportation and eat local food.</li>
    <li>Look for free or low-cost attractions.</li>
</ul>
<h2>Final Thoughts</h2>
<p>Adventure is possible on any budget. Plan ahead and embrace the journey!</p>
"""

plant_based_content = """
<p>Plant-based diets are gaining popularity for their health and environmental benefits. Here’s how to get started.</p>
<h2>Benefits</h2>
<ul>
    <li>Reduces risk of chronic diseases</li>
    <li>Supports weight management</li>
    <li>Promotes environmental sustainability</li>
</ul>
<h2>Easy Recipes</h2>
<ul>
    <li>Chickpea salad sandwiches</li>
    <li>Lentil soup</li>
    <li>Stir-fried tofu and veggies</li>
</ul>
<h2>Final Thoughts</h2>
<p>Try incorporating more plant-based meals into your week for a healthier you and a healthier planet.</p>
"""

esports_content = """
<p>E-sports has exploded in popularity, becoming a billion-dollar industry and a legitimate career path for many.</p>
<h2>Why E-Sports?</h2>
<ul>
    <li>Global tournaments with massive audiences</li>
    <li>Opportunities for players, coaches, and content creators</li>
    <li>Technological advancements in gaming and streaming</li>
</ul>
<h2>Final Thoughts</h2>
<p>Whether you’re a player or a fan, e-sports is shaping the future of entertainment.</p>
"""

remote_learning_content = """
<p>The shift to remote learning has transformed education. Here’s how students and teachers can thrive in a digital classroom.</p>
<h2>Success Strategies</h2>
<ul>
    <li>Create a dedicated study space</li>
    <li>Maintain a consistent schedule</li>
    <li>Engage with classmates and instructors online</li>
    <li>Take regular breaks to avoid burnout</li>
</ul>
<h2>Final Thoughts</h2>
<p>Remote learning offers flexibility and new opportunities. Embrace the change and keep learning!</p>
"""

minimalism_content = """
<p>Minimalism is about focusing on what truly matters and letting go of excess. It leads to greater clarity, freedom, and happiness.</p>
<h2>Minimalist Principles</h2>
<ul>
    <li>Declutter your home and workspace</li>
    <li>Prioritize quality over quantity</li>
    <li>Be intentional with purchases</li>
</ul>
<h2>Final Thoughts</h2>
<p>Minimalism isn’t about deprivation—it’s about making room for what enriches your life.</p>
"""


# Sample in-memory "database" of blog posts with enhanced data
def generate_uuid():
    return str(uuid.uuid4())

posts = [
    {
        "id": "b1a1e1c2-1f2a-4c3b-8d4e-5f6a7b8c9d01",
        "title": "The Future of Artificial Intelligence in 2025",
        "author": "Dr. Sarah Chen",
        "date": "August 24, 2025",
        "category": "technology",
        "content": ai_content,
        "imageUrl": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=2070&auto=format&fit=crop",
        "views": 1200,
        "likes": 210,
        "comments": [
            {
                "id": "cmt-001",
                "author": "Jane Doe",
                "date": "August 25, 2025",
                "content": "Excellent insights on the future of AI. Well researched and engaging!"
            },
            {
                "id": "cmt-002",
                "author": "Michael Smith",
                "date": "August 26, 2025",
                "content": "I appreciate the focus on ethical challenges. Looking forward to more articles like this."
            },
            {
                "id": "cmt-021",
                "author": "Sophia Turner",
                "date": "August 27, 2025",
                "content": "The section on AI in healthcare was particularly interesting."
            }
        ],
        "reviews": [
            {
                "id": "rev-001",
                "reviewer": "TechReviewPro",
                "rating": 5,
                "summary": "A comprehensive and forward-thinking analysis of AI trends for 2025."
            },
            {
                "id": "rev-019",
                "reviewer": "AI Digest",
                "rating": 4,
                "summary": "Strong coverage of ethical and practical AI challenges."
            },
            {
                "id": "rev-020",
                "reviewer": "FutureTech",
                "rating": 5,
                "summary": "Must-read for anyone interested in the future of technology."
            }
        ]
    },
{
        "id": "c2b2f2d3-2e3b-5d4c-9e5f-6a7b8c9d0e12",
        "title": "Sustainable Living: A Complete Guide to Eco-Friendly Practices",
        "author": "Emma Rodriguez",
        "date": "August 23, 2025",
        "category": "lifestyle",
        "content": sustainable_living_content,
        "imageUrl": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2071&auto=format&fit=crop",
        "views": 980,
        "likes": 175,
        "comments": [
            {
                "id": "cmt-003",
                "author": "Lucas Green",
                "date": "August 24, 2025",
                "content": "Very practical guide. The tips on sustainable food choices are easy to follow."
            },
            {
                "id": "cmt-022",
                "author": "Priya Nair",
                "date": "August 25, 2025",
                "content": "Loved the eco-friendly home section!"
            },
            {
                "id": "cmt-023",
                "author": "Ben Carter",
                "date": "August 26, 2025",
                "content": "Great ideas for reducing waste."
            }
        ],
        "reviews": [
            {
                "id": "rev-002",
                "reviewer": "EcoLiving Magazine",
                "rating": 4,
                "summary": "A well-structured and actionable guide for eco-friendly living."
            },
            {
                "id": "rev-021",
                "reviewer": "Green Home Review",
                "rating": 5,
                "summary": "Practical and inspiring eco tips."
            },
            {
                "id": "rev-022",
                "reviewer": "Sustainability Hub",
                "rating": 4,
                "summary": "Covers all the basics for sustainable living."
            }
        ]
    },
{
        "id": "d3c3a3e4-3f4c-6e5d-0f1a-7b8c9d0e1f23",
        "title": "Exploring the Hidden Gems of Southeast Asia",
        "author": "Marcus Thompson",
        "date": "August 22, 2025",
        "category": "travel",
        "content": blog_southeast_asia,
        "imageUrl": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2070&auto=format&fit=crop",
        "views": 860,
        "likes": 142,
        "comments": [
            {
                "id": "cmt-004",
                "author": "Priya Singh",
                "date": "August 23, 2025",
                "content": "Loved the hidden gems list! Added a few to my travel bucket list."
            },
            {
                "id": "cmt-024",
                "author": "Marco Rossi",
                "date": "August 24, 2025",
                "content": "Great travel inspiration!"
            },
            {
                "id": "cmt-025",
                "author": "Emily White",
                "date": "August 25, 2025",
                "content": "Photos are stunning."
            }
        ],
        "reviews": [
            {
                "id": "rev-003",
                "reviewer": "Travel Weekly",
                "rating": 5,
                "summary": "Inspires readers to explore beyond the usual tourist spots."
            },
            {
                "id": "rev-023",
                "reviewer": "Wanderlust",
                "rating": 4,
                "summary": "Great for off-the-beaten-path travelers."
            },
            {
                "id": "rev-024",
                "reviewer": "Explorer's Digest",
                "rating": 5,
                "summary": "A must-read for travel enthusiasts."
            }
        ]
    },
{
        "id": "e4d4b4f5-4a5d-7f6e-1b2c-8c9d0e1f2a34",
        "title": "The Art of Mindful Cooking: Recipes for the Soul",
        "author": "Chef Isabella Martinez",
        "date": "August 21, 2025",
        "category": "food",
        "content": blog_mindful_cooking,
        "imageUrl": "https://images.unsplash.com/photo-1495521821757-a1efb6729352?q=80&w=2025&auto=format&fit=crop",
        "views": 740,
        "likes": 120,
        "comments": [
            {
                "id": "cmt-005",
                "author": "Emily Brown",
                "date": "August 22, 2025",
                "content": "Mindful cooking is so important. Thanks for the recipes!"
            },
            {
                "id": "cmt-026",
                "author": "Liam Chen",
                "date": "August 23, 2025",
                "content": "The soup recipe was delicious!"
            },
            {
                "id": "cmt-027",
                "author": "Sofia Martinez",
                "date": "August 24, 2025",
                "content": "Cooking with intention makes a difference."
            }
        ],
        "reviews": [
            {
                "id": "rev-004",
                "reviewer": "Culinary Today",
                "rating": 4,
                "summary": "A refreshing take on cooking with mindfulness and intention."
            },
            {
                "id": "rev-025",
                "reviewer": "Foodie Journal",
                "rating": 5,
                "summary": "Unique approach to recipes and cooking."
            },
            {
                "id": "rev-026",
                "reviewer": "Mindful Eats",
                "rating": 4,
                "summary": "Great for anyone looking to slow down in the kitchen."
            }
        ]
    },
{
        "id": "f5e5c5a6-5b6e-8a7f-2c3d-9d0e1f2a3b45",
        "title": "Building Resilience: Mental Health Strategies for Modern Life",
        "author": "Dr. James Wilson",
        "date": "August 20, 2025",
        "category": "health",
        "content": blog_resilience,
        "imageUrl": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2070&auto=format&fit=crop",
        "views": 670,
        "likes": 110,
        "comments": [
            {
                "id": "cmt-006",
                "author": "Sophie Turner",
                "date": "August 21, 2025",
                "content": "Great mental health strategies. The self-compassion section resonated with me."
            },
            {
                "id": "cmt-028",
                "author": "James Patel",
                "date": "August 22, 2025",
                "content": "The resilience exercises are very helpful."
            },
            {
                "id": "cmt-029",
                "author": "Maria Lopez",
                "date": "August 23, 2025",
                "content": "Loved the focus on mental well-being."
            }
        ],
        "reviews": [
            {
                "id": "rev-005",
                "reviewer": "MindMatters Blog",
                "rating": 5,
                "summary": "Essential reading for anyone looking to build resilience."
            },
            {
                "id": "rev-027",
                "reviewer": "Wellness Central",
                "rating": 4,
                "summary": "Practical advice for modern life."
            },
            {
                "id": "rev-028",
                "reviewer": "Mental Health Review",
                "rating": 5,
                "summary": "A must-read for stress management."
            }
        ]
    },
{
        "id": "a6f6d6b7-6c7f-9b8a-3d4e-0e1f2a3b4c56",
        "title": "The Rise of Remote Work: Transforming the Future of Business",
        "author": "Alexandra Kim",
        "date": "August 19, 2025",
        "category": "business",
        "content": remote_work_content,
        "imageUrl": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=2071&auto=format&fit=crop",
        "views": 900,
        "likes": 160,
        "comments": [
            {
                "id": "cmt-007",
                "author": "David Lee",
                "date": "August 20, 2025",
                "content": "Remote work tips are spot on. Hybrid model is the way forward."
            },
            {
                "id": "cmt-030",
                "author": "Olivia Brown",
                "date": "August 21, 2025",
                "content": "Insightful look at remote work culture."
            },
            {
                "id": "cmt-031",
                "author": "Henry Adams",
                "date": "August 22, 2025",
                "content": "The productivity tips are very useful."
            }
        ],
        "reviews": [
            {
                "id": "rev-006",
                "reviewer": "Business Insights",
                "rating": 4,
                "summary": "Balanced perspective on the future of remote and hybrid work."
            },
            {
                "id": "rev-029",
                "reviewer": "Workplace Today",
                "rating": 5,
                "summary": "Covers all the key trends in remote work."
            },
            {
                "id": "rev-030",
                "reviewer": "Modern Business Review",
                "rating": 4,
                "summary": "Great for business leaders and employees alike."
            }
        ]
    },
{
        "id": "b7a7e7c8-7d8a-0c9b-4e5f-1f2a3b4c5d67",
        "title": "The Evolution of Digital Entertainment: From Streaming to Virtual Reality",
        "author": "David Park",
        "date": "August 18, 2025",
        "category": "entertainment",
        "content": blog_digital_entertainment,
        "imageUrl": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=2028&auto=format&fit=crop",
        "views": 1050,
        "likes": 200,
        "comments": [
            {
                "id": "cmt-008",
                "author": "Nina Patel",
                "date": "August 19, 2025",
                "content": "Fascinating look at how entertainment is evolving."
            },
            {
                "id": "cmt-032",
                "author": "Lucas Meyer",
                "date": "August 20, 2025",
                "content": "Virtual reality section was eye-opening."
            },
            {
                "id": "cmt-033",
                "author": "Ava Brooks",
                "date": "August 21, 2025",
                "content": "Streaming trends are well explained."
            }
        ],
        "reviews": [
            {
                "id": "rev-007",
                "reviewer": "Digital Media Review",
                "rating": 5,
                "summary": "Captures the rapid changes in digital entertainment."
            },
            {
                "id": "rev-031",
                "reviewer": "Entertainment Weekly",
                "rating": 4,
                "summary": "Great overview of new media formats."
            },
            {
                "id": "rev-032",
                "reviewer": "VR World",
                "rating": 5,
                "summary": "Virtual reality coverage is top-notch."
            }
        ]
    },
{
        "id": "c8b8f8d9-8e9b-1d0c-5f6a-2a3b4c5d6e78",
        "title": "The Science of Sleep: Optimizing Your Rest for Better Health",
        "author": "Dr. Rachel Green",
        "date": "August 17, 2025",
        "category": "health",
        "content": blog_sleep_science,
        "imageUrl": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?q=80&w=2068&auto=format&fit=crop",
        "views": 800,
        "likes": 130,
        "comments": [
            {
                "id": "cmt-009",
                "author": "Olga Ivanova",
                "date": "August 18, 2025",
                "content": "Helpful sleep tips. I’ll try the bedtime routine advice."
            },
            {
                "id": "cmt-034",
                "author": "Sam Lee",
                "date": "August 19, 2025",
                "content": "The science behind sleep was fascinating."
            },
            {
                "id": "cmt-035",
                "author": "Grace Kim",
                "date": "August 20, 2025",
                "content": "I’ll be sharing these tips with friends."
            }
        ],
        "reviews": [
            {
                "id": "rev-008",
                "reviewer": "Healthline",
                "rating": 4,
                "summary": "Practical and science-backed sleep optimization guide."
            },
            {
                "id": "rev-033",
                "reviewer": "Sleep Science Today",
                "rating": 5,
                "summary": "Excellent breakdown of sleep cycles."
            },
            {
                "id": "rev-034",
                "reviewer": "Restful Living",
                "rating": 4,
                "summary": "Easy to follow and actionable advice."
            }
        ]
    },
{
        "id": "d9c9a9e0-9f0c-2e1d-6a7b-3b4c5d6e7f89",
        "title": "Climate Change: What You Can Do Today",
        "author": "Priya Nair",
        "date": "August 16, 2025",
        "category": "environment",
        "content": climate_change_content,
        "imageUrl": "https://images.unsplash.com/photo-1464983953574-0892a716854b?q=80&w=2070&auto=format&fit=crop",
        "views": 650,
        "likes": 105,
        "comments": [
            {
                "id": "cmt-010",
                "author": "Rajiv Menon",
                "date": "August 17, 2025",
                "content": "Simple steps for climate action. Well written!"
            },
            {
                "id": "cmt-036",
                "author": "Ella Brown",
                "date": "August 18, 2025",
                "content": "The infographic was very helpful."
            },
            {
                "id": "cmt-037",
                "author": "Tom Green",
                "date": "August 19, 2025",
                "content": "Motivating and easy to follow."
            }
        ],
        "reviews": [
            {
                "id": "rev-009",
                "reviewer": "Green Planet Journal",
                "rating": 4,
                "summary": "Concise and motivating call to climate action."
            },
            {
                "id": "rev-035",
                "reviewer": "Eco Action Review",
                "rating": 5,
                "summary": "Great for anyone wanting to make a difference."
            },
            {
                "id": "rev-036",
                "reviewer": "Climate Today",
                "rating": 4,
                "summary": "Actionable and inspiring."
            }
        ]
    },
{
        "id": "e0d0b0f1-0a1d-3f2e-7b8c-4c5d6e7f8a90",
        "title": "The Power of Mindfulness in Daily Life",
        "author": "Samantha Lee",
        "date": "August 15, 2025",
        "category": "wellness",
        "content": mindfulness_content,
        "imageUrl": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2070&auto=format&fit=crop",
        "views": 720,
        "likes": 115,
        "comments": [
            {
                "id": "cmt-011",
                "author": "Linda Wu",
                "date": "August 16, 2025",
                "content": "Mindfulness tips are easy to implement. Thank you!"
            },
            {
                "id": "cmt-038",
                "author": "Ravi Kumar",
                "date": "August 17, 2025",
                "content": "The breathing exercise was calming."
            },
            {
                "id": "cmt-039",
                "author": "Julia Smith",
                "date": "August 18, 2025",
                "content": "Great reminders for daily mindfulness."
            }
        ],
        "reviews": [
            {
                "id": "rev-010",
                "reviewer": "Wellness Weekly",
                "rating": 5,
                "summary": "A gentle introduction to mindfulness for daily life."
            },
            {
                "id": "rev-037",
                "reviewer": "Mindful Living",
                "rating": 4,
                "summary": "Simple and effective mindfulness tips."
            },
            {
                "id": "rev-038",
                "reviewer": "Zen Journal",
                "rating": 5,
                "summary": "Perfect for beginners."
            }
        ]
    },
{
        "id": "f1e1c1a2-1b2e-4d3f-8c9d-5d6e7f8a9b01",
        "title": "How to Start Investing: A Beginner’s Guide",
        "author": "Carlos Mendoza",
        "date": "August 14, 2025",
        "category": "finance",
        "content": investing_content,
        "imageUrl": "https://images.unsplash.com/photo-1556740772-1a741367b93e?q=80&w=2070&auto=format&fit=crop",
        "views": 810,
        "likes": 125,
        "comments": [
            {
                "id": "cmt-012",
                "author": "George Carter",
                "date": "August 15, 2025",
                "content": "Great beginner’s guide. The diversification tip is key."
            },
            {
                "id": "cmt-040",
                "author": "Mina Patel",
                "date": "August 16, 2025",
                "content": "Easy to understand for new investors."
            },
            {
                "id": "cmt-041",
                "author": "Robert Lee",
                "date": "August 17, 2025",
                "content": "The risk management section was helpful."
            }
        ],
        "reviews": [
            {
                "id": "rev-011",
                "reviewer": "Finance Today",
                "rating": 4,
                "summary": "Clear and concise investing basics for newcomers."
            },
            {
                "id": "rev-039",
                "reviewer": "Investor's Digest",
                "rating": 5,
                "summary": "Great for those starting out in finance."
            },
            {
                "id": "rev-040",
                "reviewer": "Money Matters",
                "rating": 4,
                "summary": "Covers all the essentials."
            }
        ]
    },
{
        "id": "a2f2d2b3-2c3f-5e4a-9b0c-6e7f8a9b0c12",
        "title": "The Magic of Reading: Why Books Still Matter",
        "author": "Ava Patel",
        "date": "August 13, 2025",
        "category": "literature",
        "content": reading_content,
        "imageUrl": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?q=80&w=2070&auto=format&fit=crop",
        "views": 690,
        "likes": 108,
        "comments": [
            {
                "id": "cmt-013",
                "author": "Sara Kim",
                "date": "August 14, 2025",
                "content": "Books really do matter. Inspiring post!"
            },
            {
                "id": "cmt-042",
                "author": "Liam Carter",
                "date": "August 15, 2025",
                "content": "Loved the book recommendations."
            },
            {
                "id": "cmt-043",
                "author": "Emily Zhang",
                "date": "August 16, 2025",
                "content": "Reading is my favorite hobby!"
            }
        ],
        "reviews": [
            {
                "id": "rev-012",
                "reviewer": "Bookworm Central",
                "rating": 5,
                "summary": "A heartfelt reminder of the power of reading."
            },
            {
                "id": "rev-041",
                "reviewer": "Readers' Review",
                "rating": 4,
                "summary": "Great for book lovers of all ages."
            },
            {
                "id": "rev-042",
                "reviewer": "Literary Digest",
                "rating": 5,
                "summary": "Inspires a love for reading."
            }
        ]
    },
{
        "id": "b3a3e3c4-3d4a-6f5b-0c1d-7f8a9b0c1d23",
        "title": "Fitness at Home: Effective Workouts Without Equipment",
        "author": "Liam Johnson",
        "date": "August 12, 2025",
        "category": "fitness",
        "content": fitness_content,
        "imageUrl": "https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=2070&auto=format&fit=crop",
        "views": 540,
        "likes": 90,
        "comments": [
            {
                "id": "cmt-014",
                "author": "Tommy Nguyen",
                "date": "August 13, 2025",
                "content": "Home workouts are underrated. Thanks for the motivation!"
            },
            {
                "id": "cmt-044",
                "author": "Samantha Lee",
                "date": "August 14, 2025",
                "content": "The no-equipment tips are great!"
            },
            {
                "id": "cmt-045",
                "author": "Carlos Gomez",
                "date": "August 15, 2025",
                "content": "I started a new routine thanks to this post."
            }
        ],
        "reviews": [
            {
                "id": "rev-013",
                "reviewer": "Fitness Focus",
                "rating": 4,
                "summary": "Effective and accessible fitness tips for everyone."
            },
            {
                "id": "rev-043",
                "reviewer": "HomeFit Review",
                "rating": 5,
                "summary": "Perfect for busy people."
            },
            {
                "id": "rev-044",
                "reviewer": "Workout Weekly",
                "rating": 4,
                "summary": "Motivating and practical."
            }
        ]
    },
{
        "id": "c4b4f4d5-4e5b-7a6c-1d2e-8a9b0c1d2e34",
        "title": "Traveling on a Budget: Tips for Affordable Adventures",
        "author": "Sofia Rossi",
        "date": "August 11, 2025",
        "category": "travel",
        "content": budget_travel_content,
        "imageUrl": "https://images.unsplash.com/photo-1508672019048-805c876b67e2?q=80&w=2070&auto=format&fit=crop",
        "views": 600,
        "likes": 98,
        "comments": [
            {
                "id": "cmt-015",
                "author": "Anna Petrova",
                "date": "August 12, 2025",
                "content": "Budget travel tips are super useful."
            },
            {
                "id": "cmt-046",
                "author": "Marta Rossi",
                "date": "August 13, 2025",
                "content": "Loved the packing checklist!"
            },
            {
                "id": "cmt-047",
                "author": "John Smith",
                "date": "August 14, 2025",
                "content": "Great advice for solo travelers."
            }
        ],
        "reviews": [
            {
                "id": "rev-014",
                "reviewer": "Travel Smart",
                "rating": 4,
                "summary": "Great resource for affordable travel planning."
            },
            {
                "id": "rev-045",
                "reviewer": "Budget Explorer",
                "rating": 5,
                "summary": "Perfect for students and families."
            },
            {
                "id": "rev-046",
                "reviewer": "Adventure Digest",
                "rating": 4,
                "summary": "Covers all the essentials for affordable travel."
            }
        ]
    },
{
        "id": "d5c5a5e6-5f6c-8b7a-2e3f-9b0c1d2e3f45",
        "title": "Plant-Based Eating: Health Benefits and Easy Recipes",
        "author": "Maya Kim",
        "date": "August 10, 2025",
        "category": "food",
        "content": plant_based_content,
        "imageUrl": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070&auto=format&fit=crop",
        "views": 510,
        "likes": 85,
        "comments": [
            {
                "id": "cmt-016",
                "author": "Javier Morales",
                "date": "August 11, 2025",
                "content": "Plant-based recipes are delicious and easy!"
            },
            {
                "id": "cmt-048",
                "author": "Nina Patel",
                "date": "August 12, 2025",
                "content": "The lentil soup recipe is my favorite."
            },
            {
                "id": "cmt-049",
                "author": "Oscar Rivera",
                "date": "August 13, 2025",
                "content": "Great for anyone new to plant-based eating."
            }
        ],
        "reviews": [
            {
                "id": "rev-015",
                "reviewer": "Healthy Eats",
                "rating": 5,
                "summary": "Inspires readers to try plant-based meals."
            },
            {
                "id": "rev-047",
                "reviewer": "Plant Power Review",
                "rating": 4,
                "summary": "Easy recipes and great health tips."
            },
            {
                "id": "rev-048",
                "reviewer": "Green Kitchen",
                "rating": 5,
                "summary": "Perfect for families."
            }
        ]
    },
{
        "id": "e6d6b6f7-6a7d-9c8b-3f4a-0c1d2e3f4a56",
        "title": "The Rise of E-Sports: Gaming as a Global Phenomenon",
        "author": "Ethan Wang",
        "date": "August 9, 2025",
        "category": "entertainment",
        "content": esports_content,
        "imageUrl": "https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=2070&auto=format&fit=crop",
        "views": 950,
        "likes": 180,
        "comments": [
            {
                "id": "cmt-017",
                "author": "Chris Evans",
                "date": "August 10, 2025",
                "content": "E-sports is the future! Well covered."
            },
            {
                "id": "cmt-050",
                "author": "Alex Kim",
                "date": "August 11, 2025",
                "content": "Loved the section on global tournaments."
            },
            {
                "id": "cmt-051",
                "author": "Mia Chen",
                "date": "August 12, 2025",
                "content": "Streaming tips were very useful."
            }
        ],
        "reviews": [
            {
                "id": "rev-016",
                "reviewer": "GameOn Magazine",
                "rating": 5,
                "summary": "Captures the excitement and growth of e-sports."
            },
            {
                "id": "rev-049",
                "reviewer": "E-Sports Central",
                "rating": 4,
                "summary": "Great for new fans of e-sports."
            },
            {
                "id": "rev-050",
                "reviewer": "Pro Gamer Review",
                "rating": 5,
                "summary": "Covers all the latest trends."
            }
        ]
    },
{
        "id": "f7e7c7a8-7b8e-0d9c-4a5b-1d2e3f4a5b67",
        "title": "Remote Learning: Adapting to the New Normal",
        "author": "Olivia Smith",
        "date": "August 8, 2025",
        "category": "education",
        "content": remote_learning_content,
        "imageUrl": "https://images.unsplash.com/photo-1513258496099-48168024aec0?q=80&w=2070&auto=format&fit=crop",
        "views": 430,
        "likes": 70,
        "comments": [
            {
                "id": "cmt-018",
                "author": "Megan Fox",
                "date": "August 9, 2025",
                "content": "Remote learning tips are very helpful for students."
            },
            {
                "id": "cmt-052",
                "author": "Daniel Lee",
                "date": "August 10, 2025",
                "content": "The study space advice was spot on."
            },
            {
                "id": "cmt-053",
                "author": "Priya Singh",
                "date": "August 11, 2025",
                "content": "Break tips helped me avoid burnout."
            }
        ],
        "reviews": [
            {
                "id": "rev-017",
                "reviewer": "EdTech Review",
                "rating": 4,
                "summary": "Practical advice for adapting to online education."
            },
            {
                "id": "rev-051",
                "reviewer": "Online Learning Hub",
                "rating": 5,
                "summary": "Great for teachers and students alike."
            },
            {
                "id": "rev-052",
                "reviewer": "Digital Classroom",
                "rating": 4,
                "summary": "Covers all the essentials for remote learning."
            }
        ]
    },
{
        "id": "a8f8d8b9-8c9f-1b0a-5c6d-2e3f4a5b6c78",
        "title": "The Art of Minimalism: Living More with Less",
        "author": "Noah Williams",
        "date": "August 7, 2025",
        "category": "lifestyle",
        "content": minimalism_content,
        "imageUrl": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?q=80&w=2070&auto=format&fit=crop",
        "views": 520,
        "likes": 88,
        "comments": [
            {
                "id": "cmt-019",
                "author": "William Harris",
                "date": "August 8, 2025",
                "content": "Minimalism changed my life. Great article!"
            },
            {
                "id": "cmt-054",
                "author": "Sophie Brown",
                "date": "August 9, 2025",
                "content": "Decluttering tips were very helpful."
            },
            {
                "id": "cmt-055",
                "author": "Noah Kim",
                "date": "August 10, 2025",
                "content": "Minimalism is a journey, thanks for the inspiration."
            }
        ],
        "reviews": [
            {
                "id": "rev-018",
                "reviewer": "Simple Living Journal",
                "rating": 5,
                "summary": "Inspires readers to embrace a minimalist lifestyle."
            },
            {
                "id": "rev-053",
                "reviewer": "Minimalist Review",
                "rating": 4,
                "summary": "Great for anyone starting with minimalism."
            },
            {
                "id": "rev-054",
                "reviewer": "Clarity Magazine",
                "rating": 5,
                "summary": "Beautifully written and inspiring."
            }
        ]
}
]

infinite_posts = posts * 100  # Simulate a larger dataset by repeating the sample posts
posts = infinite_posts

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)


@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    return jsonify(post)


@app.route('/api/posts/category/<category>', methods=['GET'])
def get_posts_by_category(category):
    category_posts = [post for post in posts if post['category'] == category]
    return jsonify(category_posts)


@app.route('/api/posts/search/<query>', methods=['GET'])
def search_posts(query):
    query = query.lower()
    search_results = [post for post in posts if query in post['title'].lower() or query in post['content'].lower() or query in post['author'].lower()]
    return jsonify(search_results)


@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = list(set(post['category'] for post in posts))
    return jsonify(categories)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = {
        'totalPosts': len(posts),
        'totalAuthors': len(set(post['author'] for post in posts)),
        'categories': list(set(post['category'] for post in posts)),
        'postsByCategory': {}
    }
    for post in posts:
        stats['postsByCategory'][post['category']] = stats['postsByCategory'].get(post['category'], 0) + 1
    return jsonify(stats)


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    content = data.get('content')
    imageUrl = data.get('imageUrl')
    category = data.get('category', 'lifestyle')
    if not title or not author or not content:
        return jsonify({'message': 'Title, author, and content are required'}), 400
    new_post = {
        'id': generate_uuid(),
        'title': title,
        'author': author,
        'date': datetime.now().strftime('%B %d, %Y'),
        'category': category,
        'content': content,
        'imageUrl': imageUrl or "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=2028&auto=format&fit=crop"
    }
    posts.insert(0, new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    post['title'] = data.get('title', post['title'])
    post['author'] = data.get('author', post['author'])
    post['content'] = data.get('content', post['content'])
    post['imageUrl'] = data.get('imageUrl', post['imageUrl'])
    post['category'] = data.get('category', post['category'])
    return jsonify(post)


@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    posts = [p for p in posts if p['id'] != post_id]
    return jsonify({'message': 'Post deleted successfully', 'post': post})


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'postsCount': len(posts)
    })


def get_now_ist():
    ts = time_module.time()
    dt_utc = datetime.fromtimestamp(ts, timezone.utc)
    return dt_utc.astimezone(IST)


@app.route('/', methods=['GET'])
def blogifyHomePage():
    return render_template("index.html")


# Dynamically generate config.js
@app.route('/config.js')
def config():
    api_url = os.getenv("API_URL", "https://blogify-service.onrender.com/api")
    js = f"window.API_URL = '{api_url}';"
    return js, 200, {"Content-Type": "application/javascript"}


# Serve any file in /client (CSS, JS, images)
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('client', path)


@app.route('/devtools', methods=['GET'])
def devtools():
    now_ist = get_now_ist().strftime("%Y-%m-%d %H:%M:%S")
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != "static":
            methods = ",".join(rule.methods - {"HEAD", "OPTIONS"})
            routes.append({"path": str(rule), "methods": methods})

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blogify - Steller Stories</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9fafc; margin: 0; padding: 0;}
            header { background: linear-gradient(135deg, #1abc9c, #16a085); color: white; padding: 20px 40px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
            header h1 { margin: 0; font-size: 2em; font-weight: 600;}
            .container { max-width: 900px; margin: 40px auto; padding: 20px;}
            .status-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; margin-bottom: 40px; transition: transform 0.2s ease;}
            .status-card:hover { transform: translateY(-5px);}
            .status-card .symbol { font-size: 1.5em; margin-bottom: 10px;}
            .status-card .status { font-size: 1.2em; color: #27ae60; font-weight: bold;}
            .status-card .timestamp { font-size: 0.9em; color: #888;}
            table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05);}
            th, td { padding: 12px 15px; text-align: left;}
            th { background-color: #16a085; color: white; font-weight: 600;}
            tr { transition: background 0.2s ease;}
            tr:nth-child(even) { background-color: #f8f8f8;}
            tr:hover { background-color: #eafaf1;}
            td a { text-decoration: none; color: #2980b9; font-weight: 500;}
            td a:hover { text-decoration: underline;}
        </style>
    </head>
    <body>
        <header>
            <h1>📚 Blogify - Steller Stories</h1>
        </header>
        <div class="container">
            <div class="status-card">
                <div class="status">✅ OK - Connected</div>
                <div class="timestamp">Last updated (IST): {{ now }}</div>
            </div>
            <h2>📍 Available Endpoints</h2>
            <table>
                <tr><th>Path</th><th>Methods</th></tr>
                {% for r in routes %}
                    <tr>
                        <td><a href="{{ r.path }}">{{ r.path }}</a></td>
                        <td>{{ r.methods }}</td>
                    </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(
        html,
        now=now_ist,
        routes=routes
    )



@app.route('/sse-interview-dpp', methods=['GET'])
def sse_interview_dpp():
    return render_template("SSE_60Day_FullPlan.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", DEFAULT_FLASK_PORT))
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)
    logger.info(f"Flask started at (port={port})")
