import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import os
import numpy as np
import plotly.io as pio
from django.conf import settings

# Rwanda districts GeoJSON with polygon boundaries (approximate but representative)
RWANDA_DISTRICTS_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Bugesera", "district_id": 1},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [30.27, -2.13], [30.40, -2.13], [30.40, -2.35], [30.27, -2.35], [30.27, -2.13]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Burera", "district_id": 2},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.45, -1.35], [29.75, -1.35], [29.75, -1.65], [29.45, -1.65], [29.45, -1.35]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gakenke", "district_id": 3},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.60, -1.55], [29.95, -1.55], [29.95, -1.85], [29.60, -1.85], [29.60, -1.55]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gasabo", "district_id": 4},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.95, -1.80], [30.20, -1.80], [30.20, -2.10], [29.95, -2.10], [29.95, -1.80]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gatsibo", "district_id": 5},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [30.10, -1.40], [30.60, -1.40], [30.60, -1.85], [30.10, -1.85], [30.10, -1.40]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gicumbi", "district_id": 6},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.65, -1.50], [29.95, -1.50], [29.95, -1.80], [29.65, -1.80], [29.65, -1.50]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Gisagara", "district_id": 7},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.60, -2.45], [30.05, -2.45], [30.05, -2.75], [29.60, -2.75], [29.60, -2.45]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Huye", "district_id": 8},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.50, -2.50], [29.95, -2.50], [29.95, -2.75], [29.50, -2.75], [29.50, -2.50]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kamonyi", "district_id": 9},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.65, -2.20], [30.05, -2.20], [30.05, -2.50], [29.65, -2.50], [29.65, -2.20]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Karongi", "district_id": 10},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.10, -1.95], [29.55, -1.95], [29.55, -2.35], [29.10, -2.35], [29.10, -1.95]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kayonza", "district_id": 11},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [30.35, -1.75], [30.75, -1.75], [30.75, -2.05], [30.35, -2.05], [30.35, -1.75]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kicukiro", "district_id": 12},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.95, -1.90], [30.20, -1.90], [30.20, -2.10], [29.95, -2.10], [29.95, -1.90]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Kirehe", "district_id": 13},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [30.50, -2.10], [30.95, -2.10], [30.95, -2.45], [30.50, -2.45], [30.50, -2.10]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Muhanga", "district_id": 14},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.75, -2.05], [30.05, -2.05], [30.05, -2.30], [29.75, -2.30], [29.75, -2.05]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Musanze", "district_id": 15},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.45, -1.35], [29.75, -1.35], [29.75, -1.65], [29.45, -1.65], [29.45, -1.35]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Ngoma", "district_id": 16},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [30.35, -2.10], [30.65, -2.10], [30.65, -2.40], [30.35, -2.40], [30.35, -2.10]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Ngororero", "district_id": 17},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.20, -1.70], [29.55, -1.70], [29.55, -2.00], [29.20, -2.00], [29.20, -1.70]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyabihu", "district_id": 18},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.25, -1.55], [29.60, -1.55], [29.60, -1.80], [29.25, -1.80], [29.25, -1.55]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyagatare", "district_id": 19},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [30.15, -1.20], [30.55, -1.20], [30.55, -1.50], [30.15, -1.50], [30.15, -1.20]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyamagabe", "district_id": 20},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.15, -2.35], [29.60, -2.35], [29.60, -2.65], [29.15, -2.65], [29.15, -2.35]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyamasheke", "district_id": 21},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [28.90, -2.20], [29.35, -2.20], [29.35, -2.50], [28.90, -2.50], [28.90, -2.20]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyanza", "district_id": 22},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.50, -2.25], [29.95, -2.25], [29.95, -2.50], [29.50, -2.50], [29.50, -2.25]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyarugenge", "district_id": 23},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.95, -1.95], [30.15, -1.95], [30.15, -2.10], [29.95, -2.10], [29.95, -1.95]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Nyaruguru", "district_id": 24},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.05, -2.55], [29.50, -2.55], [29.50, -2.80], [29.05, -2.80], [29.05, -2.55]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rubavu", "district_id": 25},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.15, -1.55], [29.50, -1.55], [29.50, -1.85], [29.15, -1.85], [29.15, -1.55]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Ruhango", "district_id": 26},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.60, -2.15], [29.95, -2.15], [29.95, -2.35], [29.60, -2.35], [29.60, -2.15]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rulindo", "district_id": 27},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [29.65, -1.60], [30.00, -1.60], [30.00, -1.90], [29.65, -1.90], [29.65, -1.60]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rusizi", "district_id": 28},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [28.70, -2.40], [29.10, -2.40], [29.10, -2.75], [28.70, -2.75], [28.70, -2.40]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rutsiro", "district_id": 29},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [28.95, -1.75], [29.45, -1.75], [29.45, -2.05], [28.95, -2.05], [28.95, -1.75]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Rwamagana", "district_id": 30},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [30.25, -1.85], [30.60, -1.85], [30.60, -2.10], [30.25, -2.10], [30.25, -1.85]
                ]]
            }
        }
    ]
}

def create_rwanda_districts_geojson():
    """Create a basic GeoJSON structure for Rwanda districts"""
    # This is a simplified GeoJSON with approximate district boundaries
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Bugesera"},
                "geometry": {"type": "Point", "coordinates": [30.15, -2.23]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Burera"},
                "geometry": {"type": "Point", "coordinates": [29.62, -1.48]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Gakenke"},
                "geometry": {"type": "Point", "coordinates": [29.77, -1.68]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Gasabo"},
                "geometry": {"type": "Point", "coordinates": [30.06, -1.95]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Gatsibo"},
                "geometry": {"type": "Point", "coordinates": [30.34, -1.62]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Gicumbi"},
                "geometry": {"type": "Point", "coordinates": [29.85, -1.68]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Gisagara"},
                "geometry": {"type": "Point", "coordinates": [29.85, -2.61]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Huye"},
                "geometry": {"type": "Point", "coordinates": [29.74, -2.60]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Kamonyi"},
                "geometry": {"type": "Point", "coordinates": [29.86, -2.34]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Karongi"},
                "geometry": {"type": "Point", "coordinates": [29.34, -2.14]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Kayonza"},
                "geometry": {"type": "Point", "coordinates": [30.55, -1.89]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Kicukiro"},
                "geometry": {"type": "Point", "coordinates": [30.08, -1.97]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Kirehe"},
                "geometry": {"type": "Point", "coordinates": [30.75, -2.27]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Muhanga"},
                "geometry": {"type": "Point", "coordinates": [29.75, -2.08]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Musanze"},
                "geometry": {"type": "Point", "coordinates": [29.63, -1.50]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Ngoma"},
                "geometry": {"type": "Point", "coordinates": [30.55, -2.23]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Ngororero"},
                "geometry": {"type": "Point", "coordinates": [29.45, -1.85]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Nyabihu"},
                "geometry": {"type": "Point", "coordinates": [29.45, -1.67]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Nyagatare"},
                "geometry": {"type": "Point", "coordinates": [30.33, -1.34]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Nyamagabe"},
                "geometry": {"type": "Point", "coordinates": [29.37, -2.47]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Nyamasheke"},
                "geometry": {"type": "Point", "coordinates": [29.11, -2.35]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Nyanza"},
                "geometry": {"type": "Point", "coordinates": [29.75, -2.35]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Nyarugenge"},
                "geometry": {"type": "Point", "coordinates": [30.05, -1.97]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Nyaruguru"},
                "geometry": {"type": "Point", "coordinates": [29.28, -2.65]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Rubavu"},
                "geometry": {"type": "Point", "coordinates": [29.32, -1.70]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Ruhango"},
                "geometry": {"type": "Point", "coordinates": [29.79, -2.23]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Rulindo"},
                "geometry": {"type": "Point", "coordinates": [29.87, -1.73]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Rusizi"},
                "geometry": {"type": "Point", "coordinates": [28.90, -2.57]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Rutsiro"},
                "geometry": {"type": "Point", "coordinates": [29.10, -1.87]}
            },
            {
                "type": "Feature",
                "properties": {"name": "Rwamagana"},
                "geometry": {"type": "Point", "coordinates": [30.43, -1.95]}
            }
        ]
    }
    return geojson

def rwanda_vehicle_map_with_boundaries():
    """Map showing vehicle clients by district with proper geographic boundaries"""
    try:
        df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
        
        # Count clients per district
        district_counts = df.groupby("district").size().reset_index(name="clients")
        
        # Get GeoJSON data
        geojson_data = get_rwanda_geojson()
        
        # Create choropleth map using district centroids and client data
        fig = go.Figure(data=go.Scattergeo(
            locations=district_counts['district'],
            mode='text+markers',
            marker=dict(size=10),
            text=district_counts['clients'],
            textposition="middle center"
        ))
        
        # Alternative: Use scatter mapbox with boundary visualization
        # Create a more visually distinct map with colored regions
        district_coords = {
            'Bugesera': (-2.23, 30.15), 'Burera': (-1.48, 29.62), 'Gakenke': (-1.68, 29.77),
            'Gasabo': (-1.95, 30.06), 'Gatsibo': (-1.62, 30.34), 'Gicumbi': (-1.68, 29.85),
            'Gisagara': (-2.61, 29.85), 'Huye': (-2.60, 29.74), 'Kamonyi': (-2.34, 29.86),
            'Karongi': (-2.14, 29.34), 'Kayonza': (-1.89, 30.55), 'Kicukiro': (-1.97, 30.08),
            'Kirehe': (-2.27, 30.75), 'Muhanga': (-2.08, 29.75), 'Musanze': (-1.50, 29.63),
            'Ngoma': (-2.23, 30.55), 'Ngororero': (-1.85, 29.45), 'Nyabihu': (-1.67, 29.45),
            'Nyagatare': (-1.34, 30.33), 'Nyamagabe': (-2.47, 29.37), 'Nyamasheke': (-2.35, 29.11),
            'Nyanza': (-2.35, 29.75), 'Nyarugenge': (-1.97, 30.05), 'Nyaruguru': (-2.65, 29.28),
            'Rubavu': (-1.70, 29.32), 'Ruhango': (-2.23, 29.79), 'Rulindo': (-1.73, 29.87),
            'Rusizi': (-2.57, 28.90), 'Rutsiro': (-1.87, 29.10), 'Rwamagana': (-1.95, 30.43)
        }
        
        district_counts['lat'] = district_counts['district'].map(lambda x: district_coords.get(x, (-1.94, 29.87))[0])
        district_counts['lon'] = district_counts['district'].map(lambda x: district_coords.get(x, (-1.94, 29.87))[1])
        
        # Create choropleth-style map with boundaries shown as density regions
        fig = go.Figure()
        
        # Add Voronoi diagram effect by using larger semi-transparent circles for each district
        max_clients = district_counts['clients'].max()
        
        for _, row in district_counts.iterrows():
            # Size circles based on number of clients
            circle_size = 60 + (row['clients'] / max_clients) * 40
            
            # Add semi-transparent colored circle to show district area
            fig.add_trace(go.Scattermapbox(
                lat=[row['lat']],
                lon=[row['lon']],
                mode='markers',
                marker=dict(
                    size=circle_size,
                    color='rgba(255, 140, 0, 0.2)',  # Light orange with transparency
                    sizemode='diameter'
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Add the actual data points on top
        fig.add_trace(go.Scattermapbox(
            lat=district_counts['lat'],
            lon=district_counts['lon'],
            color=district_counts['clients'],
            colorscale="YlOrRd",
            mode='markers+text',
            marker=dict(
                size=district_counts['clients'].apply(lambda x: max(12, min(40, x/2.5))),
                sizemode='diameter',
                opacity=0.8
            ),
            text=[f"<b>{row['district']}</b><br>{row['clients']}" for _, row in district_counts.iterrows()],
            textposition="middle center",
            textfont=dict(size=8, color='white'),
            hovertemplate='<b>%{text}</b><br>Clients: %{marker.size:,}<extra></extra>',
            showlegend=False,
            colorbar=dict(
                title="<b>Clients</b>",
                thickness=20,
                len=0.7,
                x=1.02,
                tickformat=','
            )
        ))
        
        # Add district boundary outlines using polygon traces
        for _, row in district_counts.iterrows():
            # Create a circle outline for district boundaries
            fig.add_trace(go.Scattermapbox(
                lat=[row['lat']],
                lon=[row['lon']],
                mode='markers',
                marker=dict(
                    size=(60 + (row['clients'] / max_clients) * 40) * 1.1,
                    color='rgba(26, 71, 42, 0)',  # Transparent
                    sizemode='diameter'
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(lat=-1.9403, lon=29.8739),
                zoom=7.2
            ),
            title={
                'text': "<b>Rwanda Vehicle Clients Distribution by District</b><br><sub>Circle size and color represent client count per district</sub>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1a472a'}
            },
            height=800,
            margin={"r": 20, "t": 100, "l": 0, "b": 0},
            hovermode='closest',
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': True, 'responsive': True, 'scrollZoom': True})
    
    except Exception as e:
        print(f"Error creating Rwanda map with boundaries: {str(e)}")
        import traceback
        traceback.print_exc()
        return f'<div class="alert alert-danger">Error loading map: {str(e)}</div>'


def rwanda_vehicle_map_with_labels():
    """Map with district boundary lines and client counts using choropleth"""
    try:
        df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
        
        # Count clients per district
        district_counts = df.groupby("district").size().reset_index(name="clients")
        district_counts = district_counts.sort_values("clients", ascending=False)
        
        # Create a mapping of district names to client counts
        district_to_clients = dict(zip(district_counts['district'], district_counts['clients']))
        
        # Create figure with plotly graph objects for more control
        fig = go.Figure()
        
        # Add the GeoJSON polygon boundaries as choropleth
        locations = []
        z_values = []
        
        for feature in RWANDA_DISTRICTS_GEOJSON['features']:
            district_name = feature['properties']['name']
            locations.append(district_name)
            # Get client count, default to 0 if not found
            z_values.append(district_to_clients.get(district_name, 0))
        
        # Add choropleth layer with district boundaries
        fig.add_trace(go.Choroplethmapbox(
            geojson=RWANDA_DISTRICTS_GEOJSON,
            locations=locations,
            z=z_values,
            featureidkey="properties.name",
            colorscale="YlOrRd",
            showscale=True,
            marker_line_width=2.5,
            marker_line_color='#008B8B',  # Teal boundary lines
            hovertemplate='<b>%{location}</b><br>Clients: %{z:,}<extra></extra>',
            colorbar=dict(
                title="<b>Number of<br>Clients</b>",
                thickness=20,
                len=0.7,
                x=1.02,
                tickformat=','
            ),
            name='Districts'
        ))
        
        # Add district name labels at centroids
        for feature in RWANDA_DISTRICTS_GEOJSON['features']:
            district_name = feature['properties']['name']
            coords = feature['geometry']['coordinates'][0]
            
            # Calculate centroid of polygon
            lons = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            centroid_lon = sum(lons) / len(lons)
            centroid_lat = sum(lats) / len(lats)
            
            # Get client count
            clients = district_to_clients.get(district_name, 0)
            
            # Add text label
            fig.add_trace(go.Scattermapbox(
                lon=[centroid_lon],
                lat=[centroid_lat],
                mode='text',
                text=f"<b>{district_name}</b><br>{clients}",
                textposition="middle center",
                textfont=dict(
                    size=9,
                    color='white',
                    family='Arial, sans-serif'
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Update layout
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(lat=-1.9403, lon=29.8739),
                zoom=7.2
            ),
            title={
                'text': "<b>Rwanda Vehicle Clients by District</b><br><sub>District boundaries clearly marked with client counts</sub>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1a472a'}
            },
            height=850,
            margin={"r": 20, "t": 100, "l": 0, "b": 0},
            hovermode='closest',
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': True, 'responsive': True, 'scrollZoom': True})
    
    except Exception as e:
        print(f"Error creating Rwanda map with boundaries: {str(e)}")
        import traceback
        traceback.print_exc()
        return f'<div class="alert alert-danger">Error loading map: {str(e)}</div>'


        df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")

        # Count clients per district
        district_counts = df.groupby("district").size().reset_index(name="clients")
        district_counts = district_counts.sort_values("clients", ascending=False)
        
        # Approximate coordinates for Rwanda districts (lat, lon)
        district_coords = {
            'Bugesera': (-2.23, 30.15),
            'Burera': (-1.48, 29.62),
            'Gakenke': (-1.68, 29.77),
            'Gasabo': (-1.95, 30.06),
            'Gatsibo': (-1.62, 30.34),
            'Gicumbi': (-1.68, 29.85),
            'Gisagara': (-2.61, 29.85),
            'Huye': (-2.60, 29.74),
            'Kamonyi': (-2.34, 29.86),
            'Karongi': (-2.14, 29.34),
            'Kayonza': (-1.89, 30.55),
            'Kicukiro': (-1.97, 30.08),
            'Kirehe': (-2.27, 30.75),
            'Muhanga': (-2.08, 29.75),
            'Musanze': (-1.50, 29.63),
            'Ngoma': (-2.23, 30.55),
            'Ngororero': (-1.85, 29.45),
            'Nyabihu': (-1.67, 29.45),
            'Nyagatare': (-1.34, 30.33),
            'Nyamagabe': (-2.47, 29.37),
            'Nyamasheke': (-2.35, 29.11),
            'Nyanza': (-2.35, 29.75),
            'Nyarugenge': (-1.97, 30.05),
            'Nyaruguru': (-2.65, 29.28),
            'Rubavu': (-1.70, 29.32),
            'Ruhango': (-2.23, 29.79),
            'Rulindo': (-1.73, 29.87),
            'Rusizi': (-2.57, 28.90),
            'Rutsiro': (-1.87, 29.10),
            'Rwamagana': (-1.95, 30.43)
        }
        
        # Add coordinates to the dataframe
        district_counts['lat'] = district_counts['district'].map(lambda x: district_coords.get(x, (-1.94, 29.87))[0])
        district_counts['lon'] = district_counts['district'].map(lambda x: district_coords.get(x, (-1.94, 29.87))[1])
        
        # Create scatter mapbox with enhanced styling
        fig = px.scatter_mapbox(
            district_counts,
            lat="lat",
            lon="lon",
            size="clients",
            color="clients",
            color_continuous_scale="YlOrRd",  # Yellow to Orange to Red for better visibility
            hover_name="district",
            hover_data={"district": False, "clients": ":,", "lat": False, "lon": False},
            labels={"clients": "Number of Clients"},
            mapbox_style="carto-positron",
            center={"lat": -1.9403, "lon": 29.8739},
            zoom=7,
            size_max=50,
            opacity=0.85
        )
        
        # Add district boundary circles (visual district boundaries) using colored rings
        for _, row in district_counts.iterrows():
            # Add circle boundary around each district using color markers
            fig.add_trace(go.Scattermapbox(
                lat=[row['lat']],
                lon=[row['lon']],
                mode='markers',
                marker=dict(
                    size=45,
                    color='#1a472a',  # Dark green boundary
                    opacity=0.3
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Add text labels showing district names and client counts
        fig.add_trace(go.Scattermapbox(
            lat=district_counts['lat'],
            lon=district_counts['lon'],
            mode='text',
            text=[f"<b>{row['district']}</b><br>{row['clients']}" 
                  for _, row in district_counts.iterrows()],
            textposition="middle center",
            textfont=dict(
                size=8,
                color='white',
                family='Arial, sans-serif'
            ),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Update traces to show district markers more clearly
        fig.update_traces(
            hovertemplate='<b>%{hovertext}</b><br>Clients: %{marker.color:,}<extra></extra>',
            selector=dict(type='scattermapbox', mode='markers')
        )
        
        # Update layout for better appearance
        fig.update_layout(
            title={
                'text': "<b>Vehicle Clients Distribution Across Rwanda Districts</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 22, 'color': '#1a472a', 'family': 'Arial, sans-serif'}
            },
            height=750,
            margin={"r": 20, "t": 80, "l": 0, "b": 0},
            coloraxis_colorbar={
                'title': {"text": "<b>Number of<br>Clients</b>", "side": "right"},
                'thickness': 25,
                'len': 0.7,
                'x': 1.02,
                'tickformat': ',',
                'tickfont': {'size': 12}
            },
            hovermode='closest'
        )

        return fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': True, 'responsive': True, 'scrollZoom': True})
    
    except Exception as e:
        print(f"Error creating Rwanda map: {str(e)}")
        import traceback
        traceback.print_exc()
        return f'<div class="alert alert-danger">Error loading map: {str(e)}<br>Check server console for details.</div>'

def rwanda_district_summary():
    df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
    
    # Count clients per district and sort by count
    district_counts = df.groupby("district").size().reset_index(name="Number of Clients")
    district_counts = district_counts.rename(columns={"district": "District"})
    district_counts = district_counts.sort_values("Number of Clients", ascending=False)
    
    # Add rank
    district_counts.insert(0, "Rank", range(1, len(district_counts) + 1))
    
    return district_counts.to_html(
        classes="table table-bordered table-striped table-hover table-sm",
        index=False,
        justify="center"
    )


def rwanda_district_bar_chart():
    """Fallback visualization if map doesn't work"""
    try:
        df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
        
        # Count clients per district
        district_counts = df.groupby("district").size().reset_index(name="clients")
        district_counts = district_counts.sort_values("clients", ascending=True)
        
        fig = px.bar(
            district_counts,
            x="clients",
            y="district",
            orientation='h',
            title="Vehicle Clients by District",
            labels={"clients": "Number of Clients", "district": "District"},
            color="clients",
            color_continuous_scale="Viridis",
            text="clients"
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            height=800,
            showlegend=False,
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            }
        )
        
        return fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': True})
    except Exception as e:
        return f'<div class="alert alert-danger">Error: {str(e)}</div>'


def rwanda_vehicle_map_with_labels():
    """Enhanced map with district boundaries and labels showing district names and client counts"""
    try:
        df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")

        # Count clients per district
        district_counts = df.groupby("district").size().reset_index(name="clients")
        district_counts = district_counts.sort_values("clients", ascending=False)
        
        # Approximate coordinates for Rwanda districts (lat, lon) - centroids
        district_coords = {
            'Bugesera': (-2.23, 30.15),
            'Burera': (-1.48, 29.62),
            'Gakenke': (-1.68, 29.77),
            'Gasabo': (-1.95, 30.06),
            'Gatsibo': (-1.62, 30.34),
            'Gicumbi': (-1.68, 29.85),
            'Gisagara': (-2.61, 29.85),
            'Huye': (-2.60, 29.74),
            'Kamonyi': (-2.34, 29.86),
            'Karongi': (-2.14, 29.34),
            'Kayonza': (-1.89, 30.55),
            'Kicukiro': (-1.97, 30.08),
            'Kirehe': (-2.27, 30.75),
            'Muhanga': (-2.08, 29.75),
            'Musanze': (-1.50, 29.63),
            'Ngoma': (-2.23, 30.55),
            'Ngororero': (-1.85, 29.45),
            'Nyabihu': (-1.67, 29.45),
            'Nyagatare': (-1.34, 30.33),
            'Nyamagabe': (-2.47, 29.37),
            'Nyamasheke': (-2.35, 29.11),
            'Nyanza': (-2.35, 29.75),
            'Nyarugenge': (-1.97, 30.05),
            'Nyaruguru': (-2.65, 29.28),
            'Rubavu': (-1.70, 29.32),
            'Ruhango': (-2.23, 29.79),
            'Rulindo': (-1.73, 29.87),
            'Rusizi': (-2.57, 28.90),
            'Rutsiro': (-1.87, 29.10),
            'Rwamagana': (-1.95, 30.43)
        }
        
        # Add coordinates to the dataframe
        district_counts['lat'] = district_counts['district'].map(lambda x: district_coords.get(x, (-1.94, 29.87))[0])
        district_counts['lon'] = district_counts['district'].map(lambda x: district_coords.get(x, (-1.94, 29.87))[1])
        
        # Create figure
        fig = go.Figure()
        
        # Add scatter points with size and color based on client count
        fig.add_trace(go.Scattermapbox(
            lat=district_counts['lat'],
            lon=district_counts['lon'],
            mode='markers',
            marker=dict(
                size=district_counts['clients'].apply(lambda x: max(15, min(50, x/2))),  # Scale size by client count
                color=district_counts['clients'],
                colorscale="YlOrRd",  # Yellow to Orange to Red for better visibility
                showscale=True,
                colorbar=dict(
                    title="<b>Number of<br>Vehicle Clients</b>",
                    thickness=20,
                    len=0.7,
                    x=1.02,
                    tickformat=','
                ),
                opacity=0.85
            ),
            text=district_counts['district'],
            hovertemplate='<b>%{text}</b><br>Clients: %{marker.color:,}<extra></extra>',
            showlegend=False,
            name='Districts'
        ))
        
        # Add district boundary circles for clear visualization
        for _, row in district_counts.iterrows():
            fig.add_trace(go.Scattermapbox(
                lat=[row['lat']],
                lon=[row['lon']],
                mode='markers',
                marker=dict(
                    size=50,
                    color='#1a472a',  # Dark green boundary
                    opacity=0.3
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Add text labels (district names and client counts) at each district center
        fig.add_trace(go.Scattermapbox(
            lat=district_counts['lat'],
            lon=district_counts['lon'],
            mode='text',
            text=[f"<b>{row['district']}</b><br><i>{row['clients']} clients</i>" 
                  for _, row in district_counts.iterrows()],
            textposition="middle center",
            textfont=dict(
                size=9,
                color='white',
                family='Arial, sans-serif'
            ),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Update layout to focus on Rwanda
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(lat=-1.9403, lon=29.8739),
                zoom=7.2
            ),
            title={
                'text': "<b>Vehicle Clients Distribution Across Rwanda Districts</b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#1a472a', 'family': 'Arial, sans-serif'},
                'y': 0.98,
                'yanchor': 'top'
            },
            height=850,
            width=None,
            margin={"r": 20, "t": 80, "l": 0, "b": 0},
            showlegend=False,
            hovermode='closest',
            paper_bgcolor='rgba(240, 245, 250, 1)',
            plot_bgcolor='rgba(240, 245, 250, 1)'
        )

        return fig.to_html(include_plotlyjs='cdn', config={'displayModeBar': True, 'responsive': True, 'scrollZoom': True})
    
    except Exception as e:
        print(f"Error creating labeled Rwanda map: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback to regular map
        return rwanda_vehicle_map()


def generate_rwanda_map(df):
    """Generate a high-quality Mapbox choropleth with static text labels for each district."""
    BASE_DIR = settings.BASE_DIR
    
    # Aggregating client counts per district
    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']
    district_counts['district'] = district_counts['district'].str.strip()

    # Absolute path to GeoJSON
    geojson_path = os.path.join(BASE_DIR, "dummy-data", "rwanda_districts.geojson")
    
    if os.path.exists(geojson_path):
        with open(geojson_path, "r") as f:
            rwanda_geojson = json.load(f)
            
        # 1. Prepare GeoJSON and calculate centroids for labels
        centroids = []
        for feature in rwanda_geojson['features']:
            name = feature['properties']['shapeName'].strip()
            feature['id'] = name
            
            # Simple centroid calculation for polygon
            coords = feature['geometry']['coordinates']
            # Coordinates can be nested if Polygon or MultiPolygon
            all_lons = []
            all_lats = []
            
            def extract_coords(c_list):
                for item in c_list:
                    if isinstance(item[0], (int, float)):
                        all_lons.append(item[0])
                        all_lats.append(item[1])
                    else:
                        extract_coords(item)
            
            extract_coords(coords)
            if all_lons and all_lats:
                centroids.append({
                    'district': name,
                    'lat': np.mean(all_lats),
                    'lon': np.mean(all_lons)
                })
        
        centroid_df = pd.DataFrame(centroids)
        # Merge counts with centroids
        label_df = pd.merge(centroid_df, district_counts, on='district', how='left')
        label_df['client_count'] = label_df['client_count'].fillna(0).astype(int)
        # Formatted label text
        label_df['text'] = label_df['district'] + "<br>" + label_df['client_count'].astype(str)

        # 2. Base Choropleth Map
        fig = px.choropleth_mapbox(
            district_counts,
            geojson=rwanda_geojson,
            locations='district',
            color='client_count',
            color_continuous_scale="Reds", 
            mapbox_style="carto-positron", 
            center={"lat": -1.94, "lon": 30.06}, 
            zoom=7.8, # Slightly tighter zoom
            opacity=0.6,
            title="Vehicle Clients per District in Rwanda",
            labels={'client_count': 'Total Clients'}
        )
        
        # 3. Add Static Text Layer (ScatterMapbox)
        fig.add_trace(
            go.Scattermapbox(
                lat=label_df['lat'],
                lon=label_df['lon'],
                mode='text',
                text=label_df['text'],
                textfont={'size': 10, 'color': 'black', 'weight': 'bold'},
                hoverinfo='none', # Disable hover on the text trace so it doesn't block polygon hover
                showlegend=False
            )
        )
        
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=700, # Taller map for better label visibility
            dragmode="zoom",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_mapboxes(
            center={"lat": -1.94, "lon": 30.06},
            zoom=7.8
        )
        
        fig.update_traces(marker_line_width=1, marker_line_color="darkred", selector=dict(type='choropleth_mapbox'))
        
        return pio.to_html(
            fig, 
            full_html=False, 
            include_plotlyjs=False,
            config={'scrollZoom': True}
        )
    else:
        return f"<div class='alert alert-danger'>GeoJSON not found at {geojson_path}.</div>"

