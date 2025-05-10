import os
import base64
import pandas as pd
from PIL import Image
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Path to mounted object store
DATA_DIR = "/mnt/project35"
splits = ['train', 'val', 'test']
random_splits = ['random_train', 'random_val', 'random_test']

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
                    count = len([
                        f for f in os.listdir(artist_path)
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
                    ])
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

# Bar chart for image counts
df_counts = get_image_counts()

if not df_counts.empty:
    fig = px.bar(df_counts, x='Artist', y='Count', color='Split',
                 barmode='group', title='Image Counts per Artist and Split')
else:
    fig = px.bar(title="No data available for artwork splits.")

# Layout
app.layout = html.Div([
    html.H1("Artwork Dataset Dashboard"),
    dcc.Graph(figure=fig),
    html.H3("Select Image Split to View"),
    dcc.RadioItems(
        id='split-selector',
        options=[{'label': s, 'value': s} for s in splits + random_splits],
        value='train',
        labelStyle={'display': 'inline-block', 'margin': '10px'}
    ),
    html.Div(id='image-display', style={'display': 'flex', 'flexWrap': 'wrap'})
])

@app.callback(
    Output('image-display', 'children'),
    Input('split-selector', 'value')
)
def update_images(selected_split):
    display_blocks = []

    # Adjust path depending on the split type
    if selected_split in random_splits:
        split_path = os.path.join(DATA_DIR, "random_inputs", selected_split)
    else:
        split_path = os.path.join(DATA_DIR, selected_split)

    if not os.path.exists(split_path):
        return [html.P("Selected directory does not exist.")]

    if selected_split in splits:
        # Structured by artist folders
        for artist in os.listdir(split_path):
            artist_path = os.path.join(split_path, artist)
            if os.path.isdir(artist_path):
                images = [
                    f for f in os.listdir(artist_path)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
                ]
                if images:
                    img_path = os.path.join(artist_path, images[0])
                    img_encoded = encode_image(img_path)
                    if img_encoded:
                        display_blocks.append(html.Div([
                            html.H5(f"{selected_split} - {artist}"),
                            html.Img(src=img_encoded, style={'height': '200px'})
                        ], style={'margin': '10px'}))
    else:
        # Random flat folder
        images = [
            f for f in os.listdir(split_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        for f in images[:20]:
            img_path = os.path.join(split_path, f)
            img_encoded = encode_image(img_path)
            if img_encoded:
                display_blocks.append(html.Div([
                    html.H5(f"{selected_split} - {f}"),
                    html.Img(src=img_encoded, style={'height': '200px'})
                ], style={'margin': '10px'}))

    return display_blocks


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
