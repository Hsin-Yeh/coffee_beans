#!/usr/bin/env python3

import folium
import json

# Create a world map
world_map = folium.Map(location=[0, 0], zoom_start=2)

# Load country data
with open('countries.geojson') as f:
    countries = json.load(f)

# Add clickable polygons for each country
folium.GeoJson(
    countries,
    style_function=lambda feature: {
        'fillColor': 'lightgreen',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['ADMIN'], aliases=['Country']),
    popup=folium.GeoJsonPopup(fields=['ADMIN'], aliases=['Country'])
).add_to(world_map)

# Add custom JavaScript for interactivity
custom_js = """
<script>
document.addEventListener('DOMContentLoaded', (event) => {
    const map = document.querySelector('.folium-map');
    map.addEventListener('click', function(e) {
        if (e.target.classList.contains('leaflet-interactive')) {
            const country = e.target.querySelector('.leaflet-popup-content').textContent.trim();
            showCoffeeInfo(country);
        }
    });
});

function showCoffeeInfo(country) {
    fetch(`/get_coffee/${country}`)
        .then(response => response.json())
        .then(data => {
            let content = `<h3>Coffee Beans from ${country}</h3>`;
            if (data.length > 0) {
                data.forEach(bean => {
                    content += `<p><strong>${bean[0]}</strong>: ${bean[1]}</p>`;
                });
            } else {
                content += '<p>No coffee beans recorded for this country yet.</p>';
            }

            const popup = L.popup()
                .setLatLng(map.getCenter())
                .setContent(content)
                .openOn(map);
        });
}

// Update the click event listener
map.addEventListener('click', function(e) {
    if (e.target.classList.contains('leaflet-interactive')) {
        const country = e.target.querySelector('.leaflet-popup-content').textContent.trim();
        showCoffeeInfo(country);
    }
});

function submitCoffeeData(country) {
    const data = {
        country: country,
        bean_name: document.getElementById('beanName').value,
        roast_level: document.getElementById('roastLevel').value,
        notes: document.getElementById('notes').value
    };
    fetch('/add_coffee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Coffee added successfully!');
            map.closePopup();
        } else {
            alert('Error adding coffee: ' + data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while submitting the data.');
    });
}
</script>
"""

# Add the custom JavaScript to the map
world_map.get_root().html.add_child(folium.Element(custom_js))

# Save the map as an HTML file
world_map.save("templates/coffee_map.html")
