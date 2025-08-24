from flask import Flask, jsonify, request, render_template_string, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime, timezone
import time as time_module
import pytz
import os
import sys
import logging

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

# Sample in-memory "database" of blog posts with enhanced data
posts = [
    {
        "id": 1,
        "title": "The Future of Artificial Intelligence in 2025",
        "author": "Dr. Sarah Chen",
        "date": "August 24, 2025",
        "category": "technology",
        "content": "Artificial Intelligence has evolved dramatically over the past decade, and 2025 marks a pivotal year in its development. From autonomous vehicles navigating our streets to AI-powered healthcare systems revolutionizing patient care, the integration of AI into our daily lives has become seamless and indispensable.\n\nMachine learning algorithms are now capable of processing vast amounts of data in real-time, enabling breakthroughs in fields ranging from climate science to financial markets. The emergence of quantum computing has further accelerated AI capabilities, allowing for complex problem-solving that was previously impossible.\n\nHowever, with great power comes great responsibility. As AI systems become more sophisticated, questions about ethics, privacy, and job displacement become increasingly important. It's crucial that we develop AI with human values at its core, ensuring that these powerful tools serve to enhance human potential rather than replace it.\n\nThe next decade promises even more remarkable advancements, with AI becoming an integral part of how we work, learn, and interact with the world around us.",
        "imageUrl": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=2070&auto=format&fit=crop"
    },
    {
        "id": 2,
        "title": "Sustainable Living: A Complete Guide to Eco-Friendly Practices",
        "author": "Emma Rodriguez",
        "date": "August 23, 2025",
        "category": "lifestyle",
        "content": "In today's world, sustainable living isn't just a trend—it's a necessity. As we face the challenges of climate change and environmental degradation, adopting eco-friendly practices has become more important than ever.\n\nThis comprehensive guide explores practical ways to reduce your environmental footprint while improving your quality of life. From simple changes like switching to reusable water bottles and shopping bags, to more significant commitments like installing solar panels or starting a home garden, every action counts.\n\nWe'll dive into sustainable food choices, energy conservation, waste reduction, and ethical consumerism. You'll discover how small daily decisions can create meaningful impact when multiplied across communities and generations.\n\nRemember, sustainability isn't about perfection—it's about progress. Every step toward a more eco-friendly lifestyle is a step toward a healthier planet for future generations.",
        "imageUrl": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2071&auto=format&fit=crop"
    },
    {
        "id": 3,
        "title": "Exploring the Hidden Gems of Southeast Asia",
        "author": "Marcus Thompson",
        "date": "August 22, 2025",
        "category": "travel",
        "content": "Southeast Asia is a treasure trove of cultural diversity, stunning landscapes, and unforgettable experiences. While popular destinations like Bangkok and Bali attract millions of visitors, the region's true magic lies in its lesser-known destinations.\n\nFrom the pristine beaches of the Philippines' Palawan Island to the ancient temples of Myanmar's Bagan, Southeast Asia offers adventures for every type of traveler. The region's rich history, diverse cuisines, and warm hospitality create experiences that stay with you long after you return home.\n\nThis journey takes us through hidden villages in Vietnam's mountains, traditional markets in Laos, and untouched islands in Indonesia. We'll explore local customs, sample authentic street food, and connect with communities that have preserved their traditions for generations.\n\nTraveling off the beaten path not only provides more authentic experiences but also helps support local economies and promotes sustainable tourism practices.",
        "imageUrl": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2070&auto=format&fit=crop"
    },
    {
        "id": 4,
        "title": "The Art of Mindful Cooking: Recipes for the Soul",
        "author": "Chef Isabella Martinez",
        "date": "August 21, 2025",
        "category": "food",
        "content": "Cooking is more than just preparing food—it's a form of meditation, creativity, and love. In our fast-paced world, taking time to cook mindfully can be a powerful way to reconnect with ourselves and nourish both body and soul.\n\nThis collection of recipes goes beyond simple instructions. Each dish is designed to engage all your senses, from the vibrant colors of fresh vegetables to the aromatic spices that fill your kitchen. We'll explore techniques that transform cooking from a chore into a joyful ritual.\n\nFrom simple weeknight meals that can be prepared in under 30 minutes to elaborate weekend feasts that bring families together, these recipes celebrate the connection between food, culture, and community.\n\nRemember, the best ingredient in any dish is the love and intention you bring to the cooking process. Let's create meals that feed not just our bodies, but our spirits as well.",
        "imageUrl": "https://images.unsplash.com/photo-1495521821757-a1efb6729352?q=80&w=2025&auto=format&fit=crop"
    },
    {
        "id": 5,
        "title": "Building Resilience: Mental Health Strategies for Modern Life",
        "author": "Dr. James Wilson",
        "date": "August 20, 2025",
        "category": "health",
        "content": "In our increasingly complex and fast-paced world, mental health has become a critical component of overall wellness. Building resilience—the ability to adapt and thrive in the face of adversity—is essential for navigating life's challenges.\n\nThis comprehensive guide explores evidence-based strategies for strengthening mental health and developing emotional resilience. We'll examine the science behind stress, anxiety, and depression, and learn practical techniques for managing these common challenges.\n\nFrom mindfulness practices and cognitive behavioral techniques to the importance of social connections and physical activity, we'll discover how to build a strong foundation for mental wellness.\n\nRemember, seeking help is a sign of strength, not weakness. Whether through professional therapy, support groups, or self-care practices, there are many paths to mental health and resilience.",
        "imageUrl": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2070&auto=format&fit=crop"
    },
    {
        "id": 6,
        "title": "The Rise of Remote Work: Transforming the Future of Business",
        "author": "Alexandra Kim",
        "date": "August 19, 2025",
        "category": "business",
        "content": "The remote work revolution has fundamentally changed how we think about employment, productivity, and work-life balance. What began as a necessity during global challenges has evolved into a preferred way of working for millions of people worldwide.\n\nCompanies are discovering that remote work can lead to increased productivity, reduced overhead costs, and access to a global talent pool. Employees are enjoying greater flexibility, reduced commute times, and the ability to work from anywhere in the world.\n\nHowever, this shift also presents new challenges: maintaining team cohesion, ensuring work-life boundaries, and creating inclusive virtual environments. We'll explore best practices for both employers and employees in this new work landscape.\n\nThe future of work is hybrid, flexible, and human-centered. Organizations that adapt to these changes will thrive in the evolving business landscape.",
        "imageUrl": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=2071&auto=format&fit=crop"
    },
    {
        "id": 7,
        "title": "The Evolution of Digital Entertainment: From Streaming to Virtual Reality",
        "author": "David Park",
        "date": "August 18, 2025",
        "category": "entertainment",
        "content": "The entertainment industry has undergone a remarkable transformation in the digital age. From the rise of streaming platforms to the emergence of virtual reality experiences, how we consume and interact with entertainment has changed dramatically.\n\nStreaming services have democratized content creation, allowing independent artists and creators to reach global audiences. The traditional barriers to entry have been lowered, leading to an explosion of diverse voices and stories.\n\nVirtual reality and augmented reality are creating entirely new forms of entertainment, from immersive gaming experiences to virtual concerts and art exhibitions. These technologies are blurring the lines between the digital and physical worlds.\n\nAs we look to the future, the integration of AI, blockchain, and other emerging technologies promises to further revolutionize how we create, distribute, and experience entertainment.",
        "imageUrl": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=2028&auto=format&fit=crop"
    },
    {
        "id": 8,
        "title": "The Science of Sleep: Optimizing Your Rest for Better Health",
        "author": "Dr. Rachel Green",
        "date": "August 17, 2025",
        "category": "health",
        "content": "Sleep is one of the most fundamental aspects of human health, yet it's often overlooked in our busy lives. Quality sleep is essential for physical recovery, cognitive function, emotional regulation, and overall well-being.\n\nRecent research has revealed the complex relationship between sleep and various health outcomes, from immune function to mental health. We'll explore the science behind sleep cycles, circadian rhythms, and the factors that influence sleep quality.\n\nPractical strategies for improving sleep hygiene include creating optimal sleep environments, establishing consistent routines, and managing stress and anxiety that can interfere with rest.\n\nBy prioritizing sleep and implementing evidence-based strategies, we can enhance our health, performance, and quality of life. Remember, good sleep isn't a luxury—it's a necessity for thriving in our modern world.",
        "imageUrl": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?q=80&w=2068&auto=format&fit=crop"
    }
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>', methods=['GET'])
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
        'id': len(posts) + 1,
        'title': title,
        'author': author,
        'date': datetime.now().strftime('%B %d, %Y'),
        'category': category,
        'content': content,
        'imageUrl': imageUrl or "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?q=80&w=2028&auto=format&fit=crop"
    }
    posts.insert(0, new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
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


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", DEFAULT_FLASK_PORT))
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)
    logger.info(f"Flask started at (port={port})")
