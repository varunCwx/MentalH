import streamlit as st
import datetime
from typing import Dict, List
import time

# Configure page
st.set_page_config(
    page_title="MindSpace - Mental Health Community",
    page_icon="💙",
    layout="wide"
)

# Initialize session state
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {
            'id': 1,
            'author': 'Sarah M.',
            'timestamp': datetime.datetime.now() - datetime.timedelta(hours=2),
            'content': 'Feeling overwhelmed with work stress lately. Anyone else dealing with similar feelings?',
            'tags': ['stress', 'work'],
            'replies': [
                {
                    'author': 'Mike K.',
                    'timestamp': datetime.datetime.now() - datetime.timedelta(hours=1),
                    'content': 'I completely understand. Taking short breaks throughout the day has helped me manage work stress better.'
                },
                {
                    'author': 'Lisa R.',
                    'timestamp': datetime.datetime.now() - datetime.timedelta(minutes=30),
                    'content': 'Have you tried the 5-4-3-2-1 grounding technique? It really helps when I feel overwhelmed.'
                }
            ]
        },
        {
            'id': 2,
            'author': 'Alex T.',
            'timestamp': datetime.datetime.now() - datetime.timedelta(hours=5),
            'content': 'Started therapy last week and feeling hopeful for the first time in months. Just wanted to share some positivity!',
            'tags': ['therapy', 'hope', 'positivity'],
            'replies': [
                {
                    'author': 'Emma D.',
                    'timestamp': datetime.datetime.now() - datetime.timedelta(hours=3),
                    'content': 'That\'s wonderful! Taking that first step is always the hardest. Proud of you! 💪'
                }
            ]
        },
        {
            'id': 3,
            'author': 'Jordan P.',
            'timestamp': datetime.datetime.now() - datetime.timedelta(days=1),
            'content': 'Having trouble sleeping again. Any natural remedies that have worked for you?',
            'tags': ['sleep', 'insomnia'],
            'replies': []
        }
    ]

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I'm here to provide mental health support and resources. How are you feeling today?"}
    ]

# Sidebar navigation
st.sidebar.title("🧠 MindSpace")
st.sidebar.markdown("*A safe space for mental health support*")

page = st.sidebar.selectbox("Navigate", ["Community Feed", "Create Post", "Support Chat", "Resources"])

# Main content area
if page == "Community Feed":
    st.title("💬 Community Feed")
    st.markdown("Connect with others and share your mental health journey in a supportive environment.")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search posts...", placeholder="Search by content or tags")
    with col2:
        sort_by = st.selectbox("Sort by", ["Recent", "Most Replies"])
    
    # Tag filter
    all_tags = set()
    for post in st.session_state.posts:
        all_tags.update(post['tags'])
    
    selected_tags = st.multiselect("Filter by tags", list(all_tags))
    
    st.divider()
    
    # Display posts
    filtered_posts = st.session_state.posts
    
    # Apply filters
    if search_term:
        filtered_posts = [p for p in filtered_posts if search_term.lower() in p['content'].lower()]
    
    if selected_tags:
        filtered_posts = [p for p in filtered_posts if any(tag in p['tags'] for tag in selected_tags)]
    
    # Sort posts
    if sort_by == "Recent":
        filtered_posts.sort(key=lambda x: x['timestamp'], reverse=True)
    else:
        filtered_posts.sort(key=lambda x: len(x['replies']), reverse=True)
    
    for post in filtered_posts:
        with st.container():
            st.markdown(f"**{post['author']}** • {post['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown(post['content'])
            
            # Tags
            if post['tags']:
                tag_html = " ".join([f"<span style='background-color: #e1f5fe; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; color: #01579b;'>#{tag}</span>" for tag in post['tags']])
                st.markdown(tag_html, unsafe_allow_html=True)
            
            # Reply section
            if post['replies']:
                with st.expander(f"💬 {len(post['replies'])} replies", expanded=len(post['replies']) <= 2):
                    for reply in post['replies']:
                        st.markdown(f"**{reply['author']}** • {reply['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                        st.markdown(f"↳ {reply['content']}")
                        st.markdown("---")
            
            # Add reply form
            with st.form(f"reply_form_{post['id']}"):
                reply_content = st.text_area("Add a supportive reply...", key=f"reply_{post['id']}", height=80)
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.form_submit_button("💙 Reply"):
                        if reply_content:
                            new_reply = {
                                'author': 'You',
                                'timestamp': datetime.datetime.now(),
                                'content': reply_content
                            }
                            post['replies'].append(new_reply)
                            st.success("Reply added!")
                            st.rerun()
            
            st.divider()

elif page == "Create Post":
    st.title("✍️ Create New Post")
    st.markdown("Share your thoughts, feelings, or ask for support from the community.")
    
    with st.form("new_post_form"):
        st.markdown("### Your Post")
        
        # Anonymous option
        is_anonymous = st.checkbox("Post anonymously")
        
        # Post content
        post_content = st.text_area(
            "What's on your mind?",
            height=150,
            placeholder="Share your thoughts, feelings, or ask for support. Remember, this is a safe space."
        )
        
        # Tags
        st.markdown("### Tags (optional)")
        col1, col2 = st.columns(2)
        with col1:
            tag_input = st.text_input("Add tags (comma-separated)", placeholder="stress, anxiety, support")
        
        # Mood selector
        with col2:
            mood = st.selectbox("Current mood", ["😊 Good", "😐 Okay", "😔 Struggling", "😰 Anxious", "😴 Tired"])
        
        # Submit button
        submitted = st.form_submit_button("🚀 Share Post", use_container_width=True)
        
        if submitted:
            if post_content:
                # Parse tags
                tags = [tag.strip() for tag in tag_input.split(',') if tag.strip()]
                
                # Create new post
                new_post = {
                    'id': len(st.session_state.posts) + 1,
                    'author': 'Anonymous' if is_anonymous else 'You',
                    'timestamp': datetime.datetime.now(),
                    'content': post_content,
                    'tags': tags,
                    'replies': []
                }
                
                st.session_state.posts.insert(0, new_post)
                st.success("Post shared successfully! 🎉")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please write something before posting.")

elif page == "Support Chat":
    st.title("🤖 AI Support Chat")
    st.markdown("*Note: This is a UI mockup. In a real application, this would connect to a mental health support AI.*")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI Support:** {message['content']}")
        
        st.divider()
    
    # Chat input
    with st.form("chat_form"):
        user_input = st.text_area("Type your message...", height=80, placeholder="Share what's on your mind...")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.form_submit_button("Send 💙"):
                if user_input:
                    # Add user message
                    st.session_state.chat_messages.append({"role": "user", "content": user_input})
                    
                    # Simulate AI response (mock responses)
                    mock_responses = [
                        "I understand this must be difficult for you. Can you tell me more about what you're experiencing?",
                        "It sounds like you're going through a challenging time. Remember that seeking support is a sign of strength.",
                        "Thank you for sharing that with me. Have you considered speaking with a mental health professional?",
                        "Your feelings are valid. Here are some coping strategies that might help...",
                        "I'm here to listen. Sometimes talking through our thoughts can provide clarity."
                    ]
                    
                    import random
                    ai_response = random.choice(mock_responses)
                    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                    
                    st.rerun()
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🆘 Crisis Resources"):
            st.info("🚨 **Emergency:** 911\n📞 **988 Suicide & Crisis Lifeline:** Call or text 988\n💬 **Crisis Text Line:** Text HOME to 741741\n📞 **NAMI HelpLine:** 1-800-950-6264\n\n[More crisis resources](https://988lifeline.org/)")
    with col2:
        if st.button("🧘 Breathing Exercise"):
            st.info("**4-7-8 Breathing Technique:**\n• Inhale through nose for 4 counts\n• Hold breath for 7 counts\n• Exhale through mouth for 8 counts\n• Repeat 3-4 times\n\n[Watch Dr. Weil's Tutorial](https://www.drweil.com/videos-features/videos/breathing-exercises-4-7-8-breath/)")
    with col3:
        if st.button("🌟 Grounding Technique"):
            st.info("**5-4-3-2-1 Grounding:**\n• 5 things you can see\n• 4 things you can touch\n• 3 things you can hear\n• 2 things you can smell\n• 1 thing you can taste\n\n[Complete Guide](https://www.verywellmind.com/5-4-3-2-1-grounding-technique-8639390)")

elif page == "Resources":
    st.title("📚 Mental Health Resources")
    
    # Crisis resources
    st.markdown("## 🆘 Crisis Resources")
    crisis_col1, crisis_col2 = st.columns(2)
    
    with crisis_col1:
        st.markdown("""
        **Immediate Help:**
        - 🔴 **Emergency:** 911
        - 💬 **Crisis Text Line:** Text HOME to 741741
        - 📞 **988 Suicide & Crisis Lifeline:** Call or text 988 (24/7)
        - 📞 **NAMI HelpLine:** 1-800-950-6264 (M-F, 10 AM-10 PM ET)
        - 📞 **National Mental Health Hotline:** 1-866-903-3787
        """)
    
    with crisis_col2:
        st.markdown("""
        **Text Options:**
        - Text "NAMI" to 62640 (NAMI)
        - Text "TalkWithUs" to 66746 (Disaster Distress)
        - Text "HELLO" to 741741 (Crisis Text Line)
        
        **International:**
        - 🇬🇧 **UK:** 116 123 (Samaritans)
        - 🇨🇦 **Canada:** 1-833-456-4566
        - 🇦🇺 **Australia:** 13 11 14 (Lifeline)
        """)
    
    st.divider()
    
    # Self-care tools
    st.markdown("## 🧘 Self-Care Tools & Techniques")
    
    tool_col1, tool_col2, tool_col3 = st.columns(3)
    
    with tool_col1:
        st.markdown("""
        **Breathing Exercises:**
        - [4-7-8 Breathing Guide](https://www.drweil.com/videos-features/videos/breathing-exercises-4-7-8-breath/) - Dr. Weil's original technique
        - [4-7-8 Technique Tutorial](https://www.healthline.com/health/4-7-8-breathing) - Step-by-step guide
        - [Box Breathing Animation](https://lassebomh.github.io/box-breathing/) - Visual breathing guide
        - [10 Breathing Techniques](https://www.healthline.com/health/breathing-exercise) - Various methods
        """)
    
    with tool_col2:
        st.markdown("""
        **Grounding Techniques:**
        - [5-4-3-2-1 Grounding Guide](https://www.verywellmind.com/5-4-3-2-1-grounding-technique-8639390) - Complete tutorial
        - [Grounding Techniques Worksheet](https://www.therapistaid.com/therapy-worksheet/grounding-techniques) - Printable resource
        - [18 Grounding Methods](https://www.calm.com/blog/grounding-techniques) - Various techniques
        - [Anxiety Grounding Guide](https://www.urmc.rochester.edu/behavioral-health-partners/bhp-blog/april-2018/5-4-3-2-1-coping-technique-for-anxiety) - University resource
        """)
    
    with tool_col3:
        st.markdown("""
        **Relaxation & Mindfulness:**
        - [Progressive Muscle Relaxation](https://www.helpguide.org/mental-health/meditation/progressive-muscle-relaxation-meditation) - Complete guide
        - [PMR Script](https://www.therapistaid.com/worksheets/progressive-muscle-relaxation-script) - Guided script
        - [Mindfulness Meditation](https://www.headspace.com/meditation) - Guided sessions
        - [Calm App](https://www.calm.com/) - Meditation & sleep stories
        """)
    
    st.divider()
    
    # Professional help
    st.markdown("## 👩‍⚕️ Professional Help")
    
    prof_col1, prof_col2 = st.columns(2)
    
    with prof_col1:
        st.markdown("""
        **Finding a Therapist:**
        - [Psychology Today](https://www.psychologytoday.com/us/therapists) - Therapist directory
        - [GoodTherapy.org](https://www.goodtherapy.org/) - Therapist finder
        - [988lifeline.org](https://988lifeline.org/) - Crisis support & resources
        - [NAMI.org](https://www.nami.org/) - Mental health support
        - Your insurance provider's website
        - Community mental health centers
        - Employee assistance programs (EAP)
        """)
    
    with prof_col2:
        st.markdown("""
        **Types of Therapy:**
        - **Cognitive Behavioral Therapy (CBT)** - Thought patterns
        - **Dialectical Behavior Therapy (DBT)** - Emotional regulation
        - **Acceptance and Commitment Therapy (ACT)** - Mindfulness-based
        - **EMDR** - Trauma processing
        - **Interpersonal Therapy (IPT)** - Relationship focus
        - **Psychodynamic Therapy** - Unconscious patterns
        """)
    
    st.divider()
    
    # Educational resources
    st.markdown("## 📖 Educational Resources & Online Tools")
    
    with st.expander("🧠 Mental Health Apps & Online Resources"):
        st.markdown("""
        **Crisis Support:**
        - [988lifeline.org](https://988lifeline.org/) - 24/7 crisis support
        - [Crisis Text Line](https://www.crisistextline.org/) - Text-based crisis support
        - [NAMI](https://www.nami.org/) - Mental health education & support
        
        **Self-Help & Coping:**
        - Headspace, Calm, Insight Timer (meditation apps)
        - Youper, Sanvello, MindShift (mood tracking apps)
        - DBT Coach, CBT Thought Record (therapy skill apps)
        """)
    
    with st.expander("📚 Understanding Mental Health Conditions"):
        st.markdown("""
        - **Anxiety Disorders:** Excessive worry, fear, or panic attacks
        - **Depression:** Persistent sadness, loss of interest, hopelessness
        - **PTSD:** Trauma-related flashbacks, nightmares, hypervigilance
        - **Bipolar Disorder:** Alternating mood episodes (mania/depression)
        - **OCD:** Obsessive thoughts and compulsive behaviors
        - **ADHD:** Attention difficulties, hyperactivity, impulsivity
        """)
    
    with st.expander("🛠️ Coping Strategies & Techniques"):
        st.markdown("""
        **Immediate Coping:**
        - **5-4-3-2-1 Grounding:** [Complete Guide](https://www.verywellmind.com/5-4-3-2-1-grounding-technique-8639390) - Identify 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste
        - **Box Breathing:** [Visual Guide](https://lassebomh.github.io/box-breathing/) - 4-4-4-4 pattern (inhale-hold-exhale-hold)
        - **Progressive Muscle Relaxation:** [Tutorial](https://www.helpguide.org/mental-health/meditation/progressive-muscle-relaxation-meditation) - Tense and release muscle groups
        - **Cold Water Technique:** Run cold water on wrists/face for instant calm
        
        **Daily Management:**
        - **Sleep Hygiene:** [Sleep Foundation Guide](https://www.sleepfoundation.org/sleep-hygiene) - 7-9 hours, consistent schedule
        - **Physical Activity:** [Exercise for Mental Health](https://www.mayoclinic.org/diseases-conditions/depression/in-depth/depression-and-exercise/art-20046495) - Even 10-minute walks help
        - **Mindfulness:** [Headspace](https://www.headspace.com/) or [Calm](https://www.calm.com/) apps for guided meditation
        - **Journaling:** [Mental Health Journaling Guide](https://www.helpguide.org/mental-health/wellbeing/journaling-for-mental-health-and-wellness) - Track thoughts and feelings
        - **Social Support:** Regular check-ins with trusted friends/family
        """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🔒 Your privacy and safety are our priority")
st.sidebar.markdown("💙 Remember: You're not alone")
st.sidebar.markdown("⚠️ This is a UI mockup for demonstration purposes")