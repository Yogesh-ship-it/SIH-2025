from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

'''Activities dataset:
 6 categories, 
 4 days, 
 with budget classification'''

activities = {
    "nature": {
        1: [
            {"name": "Tsomgo Lake Visit", "desc": "Scenic lake in the mountains.", "location": "Tsomgo Lake", "budget": "medium"},
            {"name": "Baba Mandir", "desc": "Pilgrimage site near lake.", "location": "Gangtok Area", "budget": "low"}
        ],
        2: [
            {"name": "Kanchenjunga Viewpoint Trek", "desc": "Short trek to view Kanchenjunga.", "location": "Gangtok", "budget": "medium"},
            {"name": "Namgyal Institute of Tibetology Garden", "desc": "Peaceful botanical gardens.", "location": "Gangtok", "budget": "low"}
        ],
        3: [
            {"name": "Trekking in Khangchendzonga National Park", "desc": "Nature trekking in Himalayas.", "location": "Yuksom", "budget": "high"},
            {"name": "Ravangla Nature Walk", "desc": "Relaxed forest walk.", "location": "Ravangla", "budget": "low"}
        ],
        4: [
            {"name": "Tashi Viewpoint Visit", "desc": "Panoramic view of mountains.", "location": "Gangtok", "budget": "medium"},
            {"name": "Banjhakri Falls Park", "desc": "Waterfalls with garden park.", "location": "Gangtok", "budget": "low"}
        ],
    },
    "culture": {
        1: [
            {"name": "Rumtek Monastery", "desc": "Largest monastery of Sikkim.", "location": "Gangtok", "budget": "medium"},
            {"name": "MG Marg Cultural Walk", "desc": "Explore local shops and traditions.", "location": "Gangtok", "budget": "low"}
        ],
        2: [
            {"name": "Handicraft Workshop", "desc": "Learn local crafts.", "location": "Namchi", "budget": "medium"},
            {"name": "Traditional Dance Performance", "desc": "Folk cultural show.", "location": "Gangtok", "budget": "low"}
        ],
        3: [
            {"name": "Namgyal Institute of Tibetology", "desc": "Museum of Buddhist artifacts.", "location": "Gangtok", "budget": "medium"},
            {"name": "Local Village Tour", "desc": "Experience Bhutia & Lepcha culture.", "location": "Ravangla", "budget": "low"}
        ],
        4: [
            {"name": "Yuksom Heritage Walk", "desc": "Old town with historic significance.", "location": "Yuksom", "budget": "low"},
            {"name": "Cultural Market Visit", "desc": "Explore local handicrafts.", "location": "Gangtok", "budget": "medium"}
        ],
    },
    "adventure": {
        1: [
            {"name": "Paragliding", "desc": "Soar over Gangtok valleys.", "location": "Gangtok", "budget": "high"},
            {"name": "Mountain Trek", "desc": "Short trek for beginners.", "location": "Ravangla", "budget": "medium"}
        ],
        2: [
            {"name": "River Rafting", "desc": "Thrill on Teesta River.", "location": "Rangit River", "budget": "high"},
            {"name": "Rock Climbing", "desc": "Beginner-friendly rocks.", "location": "Gangtok", "budget": "medium"}
        ],
        3: [
            {"name": "Zip Lining Adventure", "desc": "Adventure over valleys.", "location": "Namchi Hills", "budget": "high"},
            {"name": "Cycling Tour", "desc": "Explore hilly terrain on bike.", "location": "Pelling", "budget": "medium"}
        ],
        4: [
            {"name": "Camping Night", "desc": "Overnight under the stars.", "location": "Ravangla", "budget": "medium"},
            {"name": "ATV Ride", "desc": "All-terrain adventure ride.", "location": "Pelling", "budget": "high"}
        ],
    },
    "spiritual": {
        1: [
            {"name": "Morning Prayer at Rumtek Monastery", "desc": "Attend monastery prayers.", "location": "Gangtok", "budget": "low"},
            {"name": "Meditation Session", "desc": "Guided meditation in serene spot.", "location": "Enchey Monastery", "budget": "low"}
        ],
        2: [
            {"name": "Yoga Retreat", "desc": "Morning yoga in nature.", "location": "Ravangla", "budget": "medium"},
            {"name": "Pilgrimage Walk", "desc": "Sacred route exploration.", "location": "Yuksom", "budget": "low"}
        ],
        3: [
            {"name": "Chanting Ceremony", "desc": "Experience local rituals.", "location": "Phodong Monastery", "budget": "low"},
            {"name": "Monk Blessing", "desc": "Receive spiritual blessings.", "location": "Lingdum Monastery", "budget": "medium"}
        ],
        4: [
            {"name": "Prayer Flags Walk", "desc": "Learn about Buddhist symbols.", "location": "Gangtok Hills", "budget": "low"},
            {"name": "Sound Healing Session", "desc": "Relax with Tibetan bowls.", "location": "Ravangla Retreat", "budget": "medium"}
        ],
    },
    "food": {
        1: [
            {"name": "Momo Tasting", "desc": "Try Sikkimese dumplings.", "location": "Gangtok Market", "budget": "low"},
            {"name": "Local Brewery Visit", "desc": "Taste millet beer.", "location": "Gangtok", "budget": "medium"}
        ],
        2: [
            {"name": "Cooking Class", "desc": "Learn Sikkimese recipes.", "location": "Namchi", "budget": "medium"},
            {"name": "Street Food Walk", "desc": "Explore local snacks.", "location": "MG Marg, Gangtok", "budget": "low"}
        ],
        3: [
            {"name": "Tea Garden Visit", "desc": "Temi Tea Estate tour and tasting.", "location": "Ravangla", "budget": "medium"},
            {"name": "Yak Cheese Tasting", "desc": "Sample local cheese.", "location": "Farmhouse", "budget": "low"}
        ],
        4: [
            {"name": "Local Dessert Sampling", "desc": "Try Sikkim sweets.", "location": "Gangtok", "budget": "low"},
            {"name": "Fine Dining Experience", "desc": "Modern Sikkimese cuisine.", "location": "5-Star Restaurant", "budget": "high"}
        ],
    },
    "heritage": {
        1: [
            {"name": "Tsuklakhang Palace", "desc": "Historic palace visit.", "location": "Gangtok", "budget": "medium"},
            {"name": "Gangtok Heritage Museum", "desc": "Ancient artifacts on display.", "location": "Gangtok", "budget": "low"}
        ],
        2: [
            {"name": "Pemayangtse Monastery", "desc": "Ancient Buddhist monastery.", "location": "Pelling", "budget": "medium"},
            {"name": "Rabdentse Ruins", "desc": "Historic ruins of Sikkim royalty.", "location": "Pelling", "budget": "medium"}
        ],
        3: [
            {"name": "Namgyal Fort Ruins", "desc": "Explore historic fort remains.", "location": "Namchi", "budget": "low"},
            {"name": "Village Heritage Walk", "desc": "Old houses and local stories.", "location": "Rural Sikkim", "budget": "low"}
        ],
        4: [
            {"name": "Traditional Bridge Visit", "desc": "Historic trade route bridge.", "location": "Dentam Bridge", "budget": "low"},
            {"name": "Folk Museum", "desc": "Cultural artifacts and heritage.", "location": "Namchi", "budget": "medium"}
        ],
    }
}

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/plan", methods=["POST"])
def plan():
    data = request.get_json()
    days = min(int(data.get("days", 1)), 4)  # max 4 days
    category = data.get("category", "nature")
    budget = data.get("budget", "low")

    itinerary = {}
    for day in range(1, days + 1):
        day_activities = activities.get(category, {}).get(day, [])
        # Filter by budget
        filtered = [act for act in day_activities if act.get("budget") == budget]
        itinerary[day] = filtered

    return jsonify({"itinerary": itinerary})

if __name__ == "__main__":
    app.run(debug=True)
