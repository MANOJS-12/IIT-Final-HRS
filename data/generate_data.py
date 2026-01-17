import pandas as pd
import random
import uuid

def generate_data():
    # 1. Emotions
    emotions = [
        {'id': 'E001', 'name': 'Anxiety'},
        {'id': 'E002', 'name': 'Stress'},
        {'id': 'E003', 'name': 'Sadness'},
        {'id': 'E004', 'name': 'Joy'},
        {'id': 'E005', 'name': 'Anger'},
        {'id': 'E006', 'name': 'Loneliness'}
    ]
    df_emotions = pd.DataFrame(emotions)
    df_emotions.to_csv('emotions.csv', index=False)
    print("Generated emotions.csv")

    # 2. Activities
    activities = [
        {'id': 'A001', 'name': 'Deep Breathing', 'type': 'Meditation', 'target_emotion_id': 'E001'},
        {'id': 'A002', 'name': 'Yoga Flow', 'type': 'Exercise', 'target_emotion_id': 'E002'},
        {'id': 'A003', 'name': 'Journaling', 'type': 'Writing', 'target_emotion_id': 'E003'},
        {'id': 'A004', 'name': 'Nature Walk', 'type': 'Exercise', 'target_emotion_id': 'E002'},
        {'id': 'A005', 'name': 'Gratitude List', 'type': 'Writing', 'target_emotion_id': 'E004'},
        {'id': 'A006', 'name': 'Boxing', 'type': 'Exercise', 'target_emotion_id': 'E005'},
        {'id': 'A007', 'name': 'Call a Friend', 'type': 'Social', 'target_emotion_id': 'E006'},
        {'id': 'A008', 'name': 'Progressive Muscle Relaxation', 'type': 'Meditation', 'target_emotion_id': 'E001'}
    ]
    df_activities = pd.DataFrame(activities)
    df_activities.to_csv('activities.csv', index=False)
    print("Generated activities.csv")

    # 3. Content
    content_list = [
        {'id': 'C001', 'title': 'Understanding Anxiety', 'type': 'Article', 'category': 'Educational', 'related_emotion_id': 'E001'},
        {'id': 'C002', 'title': '5 Minute Stress Relief', 'type': 'Video', 'category': 'Guided', 'related_emotion_id': 'E002'},
        {'id': 'C003', 'title': 'Coping with Loss', 'type': 'Article', 'category': 'Support', 'related_emotion_id': 'E003'},
        {'id': 'C004', 'title': 'The Science of Happiness', 'type': 'Podcast', 'category': 'Educational', 'related_emotion_id': 'E004'},
        {'id': 'C005', 'title': 'Managing Anger Constructively', 'type': 'Article', 'category': 'Educational', 'related_emotion_id': 'E005'},
        {'id': 'C006', 'title': 'Community Connection', 'type': 'Video', 'category': 'Social', 'related_emotion_id': 'E006'},
        {'id': 'C007', 'title': 'Calming Music Mix', 'type': 'Audio', 'category': 'Relaxation', 'related_emotion_id': 'E001'},
        {'id': 'C008', 'title': 'Work-Life Balance Tips', 'type': 'Article', 'category': 'Productivity', 'related_emotion_id': 'E002'}
    ]
    df_content = pd.DataFrame(content_list)
    df_content.to_csv('content.csv', index=False)
    print("Generated content.csv")

    # 4. Users
    users = []
    for i in range(1, 21): # 20 users
        users.append({'id': f'U{i:03d}', 'name': f'User_{i}'})
    df_users = pd.DataFrame(users)
    df_users.to_csv('users.csv', index=False)
    print("Generated users.csv")

    # 5. Interactions (Synthetic)
    interactions = []
    for user in users:
        # Each user has interacted with 2-5 content items
        num_interactions = random.randint(2, 5)
        viewed_content = random.sample(content_list, num_interactions)
        
        for c in viewed_content:
            interactions.append({
                'user_id': user['id'],
                'content_id': c['id'],
                'rating': random.randint(3, 5), # Mostly positive for now
                'timestamp': '2023-10-27T10:00:00'
            })
    
    df_interactions = pd.DataFrame(interactions)
    df_interactions.to_csv('interactions.csv', index=False)
    print("Generated interactions.csv")

if __name__ == '__main__':
    generate_data()
