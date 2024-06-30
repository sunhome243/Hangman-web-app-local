from flask import Flask, jsonify, send_from_directory, render_template, request
import random
import json

app = Flask(__name__)

# Word pool for the game
words = ['house', 'car', 'book', 'computer', 'phone', 'table', 'chair', 'lamp', 'desk', 'bed', 'door', 'window', 'mirror', 'clock', 'television', 'radio', 'guitar', 'piano', 'drums', 'microwave', 'refrigerator', 'oven', 'sink', 'toilet', 'shower', 'bathtub', 'towel', 'soap', 'shampoo', 'toothbrush', 'toothpaste', 'hairbrush', 'comb', 'hairdryer', 'cosmetics', 'perfume', 'deodorant', 'toilet paper', 'tissue', 'trash', 'dustbin', 'broom', 'mop', 'vacuum', 'bucket', 'sponge', 'dish', 'plate', 'bowl', 'fork', 'knife', 'spoon', 'glass', 'cup', 'mug', 'jug', 'bottle', 'can', 'pan', 'pot', 'kettle', 'cutting board', 'oven mitts', 'apron', 'dishwasher', 'mixer', 'blender', 'whisk', 'ovenware', 'cooking', 'utensils', 'scale', 'measuring', 'cup', 'rolling pin', 'food', 'processor', 'coffee', 'maker', 'coffee', 'grinder', 'toaster', 'bread', 'maker', 'juicer', 'tupperware', 'storage', 'container', 'cutlery', 'sharpener', 'ladle', 'strainer', 'colander', 'thermometer', 'timer', 'kitchen', 'timer', 'corkscrew', 'bottle', 'opener', 'peeler', 'grater', 'scissors', 'ruler', 'tape', 'glue', 'pencil', 'pen', 'marker', 'highlighter', 'eraser', 'sharpener', 'notebook', 'journal', 'diary', 'folder', 'file', 'stapler', 'staples', 'hole', 'punch', 'paper', 'clip', 'rubber', 'band', 'envelope', 'calendar', 'planner', 'bulletin', 'board', 'corkboard', 'whiteboard', 'chalkboard', 'eraser', 'clipboard', 'note', 'pad', 'sticky', 'notes', 'post', 'it', 'bookshelf', 'shelf', 'drawer', 'cabinet', 'wardrobe', 'closet', 'hanger', 'hook', 'peg', 'rack', 'clothes', 'hanger', 'clothes', 'peg', 'coat', 'hanger', 'shoe', 'rack', 'umbrella', 'walking', 'stick', 'bag', 'suitcase', 'backpack', 'briefcase', 'wallet', 'purse', 'handbag', 'handkerchief', 'scarf', 'hat', 'cap', 'bonnet', 'gloves', 'mittens', 'socks', 'stockings', 'tights', 'shoes', 'sandals', 'boots', 'sneakers', 'slippers', 'belt', 'tie', 'bow', 'ribbon', 'lanyard', 'necklace', 'bracelet', 'earrings', 'ring', 'watch', 'brooch', 'button', 'zipper', 'lace', 'buckle', 'safety', 'pin', 'sewing', 'needle', 'thread', 'cushion', 'thimble', 'sewing', 'machine', 'scrapbook', 'knitting', 'needles', 'crochet', 'hook', 'yarn', 'wool', 'fabric', 'tapestry', 'patchwork', 'quilting', 'embroidery', 'cross', 'stitch', 'beading', 'pendant', 'hair', 'pin']

DATA_FILE = 'player_data.json'

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

@app.route('/start', methods=['GET'])
def start():
    word = random.choice(words)
    return jsonify({'word': word})

# Route to handle player data
@app.route('/player', methods=['POST'])
def player():
    data = request.get_json()
    name = data.get('name')
    if name:
        try:
            with open(DATA_FILE, 'r') as f:
                player_data = json.load(f)
        except FileNotFoundError:
            player_data = {}
        if name in player_data:
            # Player exists, update data
            player_data[name]['score'] = player_data[name].get('score', 0)
            player_data[name]['win_streak'] = player_data[name].get('win_streak', 0)
        else:
            # New player
            player_data[name] = {'score': 0, 'win_streak': 0}
        with open(DATA_FILE, 'w') as f:
            json.dump(player_data, f)
        return jsonify(player_data[name])  # Return player data as JSON
    return jsonify({'message': 'Invalid player name'})

# Route to handle game win
@app.route('/win', methods=['POST'])
def win():
    data = request.get_json()
    name = data.get('name')
    if name:
        try:
            with open(DATA_FILE, 'r') as f:
                player_data = json.load(f)
        except FileNotFoundError:
            player_data = {}
        if name in player_data:
            player_data[name]['score'] += 1
            player_data[name]['win_streak'] += 1
            with open(DATA_FILE, 'w') as f:
                json.dump(player_data, f)
            return jsonify({'message': 'Player score and win streak updated'})
    return jsonify({'message': 'Invalid player name'})

# Route to handle game loss
@app.route('/loss', methods=['POST'])
def loss():
    data = request.get_json()
    name = data.get('name')
    if name:
        try:
            with open(DATA_FILE, 'r') as f:
                player_data = json.load(f)
        except FileNotFoundError:
            player_data = {}
        if name in player_data:
            player_data[name]['win_streak'] = 0
            with open(DATA_FILE, 'w') as f:
                json.dump(player_data, f)
            return jsonify({'message': 'Player win streak reset'})
    return jsonify({'message': 'Invalid player name'})

# Serve static files (including JavaScript and CSS)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5200)