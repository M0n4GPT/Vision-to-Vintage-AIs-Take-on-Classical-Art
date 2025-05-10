import os
import base64
import pandas as pd
from PIL import Image
from dash import Dash, html, dcc
import plotly.express as px

# Define the data directory
DATA_DIR = "/mnt/project35"
splits = ['train', 'val', 'test']

# Initialize the Dash app
app = Dash(__name__)

def get_image_counts():
    data = []
    for split in splits:
        split_path = os.path.join(DATA_DIR, split)
        if os.path.exists(split_path):
            for artist in os.listdir(split_path):
                artist_path = os.path.join(split_path, artist)
                if os.path.isdir(artist_path):
                    count = len([f for f in os.listdir(artist_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                    data.append({'Split': split, 'Artist': artist, 'Count': count})
    return pd.DataFrame(data)

def encode_image(image_path):
    try:
        with open(image_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        return f'data:image/jpeg;base64,{encoded}'
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None

# Get image counts
df_counts = get_image_counts()

# Create bar chart
fig = px.bar(df_counts, x='Artist', y='Count', color='Split', barmode='group', title='Image Counts per Artist and Split')

# Get sample images
sample_images = []
for split in splits:
    split_path = os.path.join(DATA_DIR, split)
    if os.path.exists(split_path):
        for artist in os.listdir(split_path):
            artist_path = os.path.join(split_path, artist)
            if os.path.isdir(artist_path):
                images = [f for f in os.listdir(artist_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if images:
                    image_path = os.path.join(artist_path, images[0])
                    encoded_image = encode_image(image_path)
                    if encoded_image:
                        sample_images.append(html.Div([
                            html.H5(f'{split} - {artist}'),
                            html.Img(src=encoded_image, style={'height': '200px'})
                        ], style={'margin': '10px'}))

# Define the app layout
app.layout = html.Div([
    html.H1('Artwork Dataset Dashboard'),
    dcc.Graph(figure=fig),
    html.Div(sample_images, style={'display': 'flex', 'flexWrap': 'wrap'})
])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)
