import os
import requests
from pathlib import Path
from urllib.parse import urlparse

# Create directories if they don't exist
directories = [
    '../Some web/assets/images/team',
    '../Some web/assets/images/events',
    '../Some web/assets/images/gallery',
    '../Some web/assets/images/activities',
    '../Some web/assets/images/about',
    '../Some web/assets/images/features',
    '../Some web/assets/images/contact'
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)

# Image URLs (using Unsplash images)
images = {
    # Hero and Logo
    '../Some web/assets/images/hero-bg.jpg': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=1920&q=80',  # Engineering background
    '../Some web/assets/images/logo.png': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=200&q=80',  # Engineering logo
    
    # Team Members
    '../Some web/assets/images/team/chairperson.jpg': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&q=80',  # Professional engineer
    '../Some web/assets/images/team/secretary.jpg': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&q=80',  # Professional female engineer
    '../Some web/assets/images/team/treasurer.jpg': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80',  # Professional engineer
    
    # Events
    '../Some web/assets/images/events/workshop.jpg': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&q=80',  # Engineering workshop
    '../Some web/assets/images/events/conference.jpg': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80',  # Engineering conference
    '../Some web/assets/images/events/competition.jpg': 'https://images.unsplash.com/photo-1523580846011-d3a5bc25702b?w=800&q=80',  # Engineering competition
    
    # Gallery - Engineering Projects and Activities
    '../Some web/assets/images/gallery/robotics.jpg': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=80',  # Robotics project
    '../Some web/assets/images/gallery/solar.jpg': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800&q=80',  # Solar project
    '../Some web/assets/images/gallery/coding.jpg': 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&q=80',  # Programming
    '../Some web/assets/images/gallery/electronics.jpg': 'https://images.unsplash.com/photo-1580706483913-b6ea7db483a0?w=800&q=80',  # Electronics
    '../Some web/assets/images/gallery/workshop1.jpg': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&q=80',  # Workshop
    '../Some web/assets/images/gallery/design.jpg': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800&q=80',  # Design
    '../Some web/assets/images/gallery/research.jpg': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800&q=80',  # Research
    '../Some web/assets/images/gallery/presentation.jpg': 'https://images.unsplash.com/photo-1558008258-3256797b43f3?w=800&q=80',  # Presentation
    '../Some web/assets/images/gallery/teamwork.jpg': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&q=80',  # Team collaboration
    '../Some web/assets/images/gallery/field_trip.jpg': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&q=80',  # Field trip
    '../Some web/assets/images/gallery/competition.jpg': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&q=80',  # Competition
    '../Some web/assets/images/gallery/community.jpg': 'https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?w=800&q=80',  # Community service
    
    # Activities/Services page images - Optimized sizes
    '../Some web/assets/images/activities/workshop1.jpg': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=600&q=80',  # CAD Workshop
    '../Some web/assets/images/activities/workshop2.jpg': 'https://images.unsplash.com/photo-1542831371-32f555c86880?w=600&q=80',  # Programming
    '../Some web/assets/images/activities/workshop3.jpg': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&q=80',  # AI/ML & Robotics
    '../Some web/assets/images/activities/project1.jpg': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&q=80',  # Renewable Energy
    '../Some web/assets/images/activities/project2.jpg': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=600&q=80',  # Smart Agriculture
    '../Some web/assets/images/activities/project3.jpg': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600&q=80',  # Design Projects
    '../Some web/assets/images/activities/mentorship.jpg': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&q=80',  # Mentorship
    '../Some web/assets/images/activities/peer-tutoring.jpg': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&q=80',  # Peer Tutoring
    '../Some web/assets/images/activities/competition.jpg': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600&q=80',  # Competition Teams
    
    # About Section
    '../Some web/assets/images/about/mission.jpg': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=80',  # Engineering mission
    '../Some web/assets/images/about/vision.jpg': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=80',  # Engineering vision
    
    # Features Section
    '../Some web/assets/images/features/academic.jpg': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=600&q=80',  # Academic excellence
    '../Some web/assets/images/features/networking.jpg': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&q=80',  # Networking
    '../Some web/assets/images/features/practical.jpg': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600&q=80',  # Practical skills
    '../Some web/assets/images/features/leadership.jpg': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600&q=80',  # Leadership
    
    # Contact Section
    '../Some web/assets/images/contact/map.jpg': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&q=80',  # Campus map
    '../Some web/assets/images/contact/office.jpg': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&q=80',  # Office location
}

def download_image(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

# Download all images
for file_path, url in images.items():
    download_image(url, file_path) 