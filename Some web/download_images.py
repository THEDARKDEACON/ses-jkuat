import os
import requests
import shutil
import time

# Create necessary directories
def create_directories():
    directories = [
        'assets/images',
        'assets/images/portfolio',
        'assets/images/blog',
        'assets/images/team',
        'assets/images/testimonials',
        'assets/images/about'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

# Image URLs (using Unsplash images)
image_urls = {
    # Logo and branding
    'assets/images/logo.png': 'https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=200&h=80&fit=crop',
    'assets/images/favicon.ico': 'https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=32&h=32&fit=crop',
    
    # Hero and background
    'assets/images/hero-bg.jpg': 'https://images.unsplash.com/photo-1562408590-e32931084e23?w=1600&h=900&fit=crop',  # Engineering students working
    'assets/images/about-bg.jpg': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=1600&h=900&fit=crop',  # Technology background
    
    # Portfolio/Events images
    'assets/images/portfolio/event1.jpg': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&h=600&fit=crop',  # Tech workshop
    'assets/images/portfolio/event2.jpg': 'https://images.unsplash.com/photo-1573497620053-ea5300f94f21?w=800&h=600&fit=crop',  # Women in tech
    'assets/images/portfolio/event3.jpg': 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800&h=600&fit=crop',  # Community service
    
    # Team/Committee images
    'assets/images/team/mentorship.jpg': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=400&fit=crop',  # Mentorship
    'assets/images/team/editorial.jpg': 'https://images.unsplash.com/photo-1542744094-3a31f272c490?w=400&h=400&fit=crop',  # Editorial/Writing
    'assets/images/team/projects.jpg': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=400&fit=crop',  # Engineering projects
    'assets/images/team/wit.jpg': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop',  # Women in tech
    
    # Testimonial images (professional headshots)
    'assets/images/testimonials/testimonial1.jpg': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop',
    'assets/images/testimonials/testimonial2.jpg': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=200&h=200&fit=crop',
    'assets/images/testimonials/testimonial3.jpg': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop',
    
    # Admin images
    'assets/images/admin-avatar.jpg': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200&h=200&fit=crop'  # Professional admin avatar
}

def download_image(url, filepath, retries=3):
    for attempt in range(retries):
        try:
            print(f"\nDownloading {filepath}")
            print(f"From URL: {url}")
            
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            
            print(f"✓ Successfully downloaded: {filepath}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{retries} failed:")
            print(f"Error: {str(e)}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"❌ Failed to download {filepath} after {retries} attempts")
                return False

def main():
    print("=== SES JKUAT Image Downloader ===")
    print("\nCreating directories...")
    create_directories()
    
    print("\nDownloading images...")
    success_count = 0
    total_images = len(image_urls)
    
    for filepath, url in image_urls.items():
        if download_image(url, filepath):
            success_count += 1
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded: {success_count}/{total_images} images")
    
    if success_count < total_images:
        print("Some images failed to download. Please check the error messages above.")

if __name__ == "__main__":
    main() 