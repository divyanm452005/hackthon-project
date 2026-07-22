import json
import os
import shutil
from collections import Counter

REVIEWS_FILE = 'reviews.json'
IMAGES_DIR = 'images'

def load_previous_reviews():
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_reviews(reviews, user_commands):
    data = {'reviews': reviews, 'user_commands': user_commands}
    with open(REVIEWS_FILE, 'w') as f:
        json.dump(data, f)

def upload_image():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    
    image_path = input("Enter the full path to the image file to upload (e.g., /path/to/image.jpg): ").strip()
    if not image_path or not os.path.isfile(image_path):
        print("Invalid file path. Skipping upload.")
        return None
    
    filename = os.path.basename(image_path)
    dest_path = os.path.join(IMAGES_DIR, filename)
    shutil.copy(image_path, dest_path)
    print(f"Image uploaded successfully to {dest_path}")
    return dest_path

def summarize_reviews(reviews, user_commands):
    if not reviews and not user_commands:
        return "No reviews or commands provided."
    
    if user_commands:
        reviews.append(user_commands)
    
    positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'best', 'awesome', 'fantastic']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'poor', 'disappointed', 'broken']
    
    total_positive = 0
    total_negative = 0
    themes = Counter()
    
    for review in reviews:
        words = review.lower().split()
        for word in words:
            if word in positive_words:
                total_positive += 1
            if word in negative_words:
                total_negative += 1
            if len(word) > 3 and word not in positive_words and word not in negative_words:
                themes[word] += 1
    
    top_themes = themes.most_common(5)
    total_reviews = len(reviews)
    overall_sentiment = 'Positive' if total_positive > total_negative else 'Negative' if total_negative > total_positive else 'Neutral'
    
    summary = f"""
Summary:
- Total Reviews/Inputs: {total_reviews}
- Overall Sentiment: {overall_sentiment} (Positive mentions: {total_positive}, Negative mentions: {total_negative})
- Top Themes: {', '.join([f'{theme} ({count})' for theme, count in top_themes])}
"""
    return summary.strip()

if __name__ == "__main__":
    print("CheckPro - Product Reviews Summarizer")
    
    # Load and display previous reviews
    previous_data = load_previous_reviews()
    if previous_data:
        print("\nPrevious Reviews Loaded:")
        for i, review in enumerate(previous_data.get('reviews', []), 1):
            print(f"{i}. {review}")
        print(f"Previous Commands: {previous_data.get('user_commands', 'None')}")
        use_previous = input("Use previous reviews? (y/n): ").lower().strip()
        if use_previous == 'y':
            reviews = previous_data['reviews']
            user_commands = previous_data['user_commands']
        else:
            reviews = []
            user_commands = ""
    else:
        reviews = []
        user_commands = ""
    
    # Upload image
    upload_choice = input("Upload a product image? (y/n): ").lower().strip()
    if upload_choice == 'y':
        uploaded_image = upload_image()
    else:
        uploaded_image = None
    
    # Enter new reviews if not using previous
    if not reviews:
        print("Enter product reviews (one per line, press Enter twice to finish):")
        while True:
            review = input()
            if review.strip() == "":
                break
            reviews.append(review)
        
        user_commands = input("Add user commands/comments (optional, e.g., focus on 'quality'): ").strip()
    
    # Summarize
    result = summarize_reviews(reviews, user_commands)
    print(result)
    
    # Save reviews for next time
    save_reviews(reviews, user_commands)
    print("Reviews saved for future sessions.")
    
    # Feedback
    likes = 0
    dislikes = 0
    while True:
        feedback = input("Rate this summary (like/dislike/exit or press Enter to exit): ").lower().strip()
        if feedback == 'like':
            likes += 1
        elif feedback == 'dislike':
            dislikes += 1
        elif feedback == 'exit' or feedback == '':
            break
        else:
            print("Invalid input. Type 'like', 'dislike', 'exit', or press Enter to exit.")
    print(f"Feedback: Likes: {likes} | Dislikes: {dislikes}")