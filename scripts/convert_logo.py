import cairosvg
import os

# Create assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

# SVG content
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <!-- Background -->
  <rect width="400" height="400" fill="#000000"/>

  <!-- Standard English letter S -->
  <text x="200" y="300" 
        text-anchor="middle"
        font-family="Arial Black, Arial, sans-serif"
        font-size="300"
        font-weight="bold"
        fill="#E50914">
    S
  </text>
</svg>'''

# Save SVG file
with open('assets/logo.svg', 'w') as f:
    f.write(svg_content)

# Convert SVG to PNG
cairosvg.svg2png(url='assets/logo.svg', write_to='assets/logo.png', output_width=400, output_height=400) 