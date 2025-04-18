import os
import json
import requests
import random
import time
#from datetime import datetime
from datetime import datetime, timezone
# Configuration
CHATGPT_API_KEY = ""  # Replace with your OpenAI API Key
BSKY_USERNAME = ""  # Replace with your Bluesky username
BSKY_PASSWORD = ""  # Replace with your Bluesky password
POSTED_FILE = "posted_bsky.json"
OUTPUT_FILE = "output_bsky.txt"

# Topics array
TOPICS = [
    "Cloud Security",
    "DevSecOps Practices",
    "Zero Trust Architecture",
    "Container Security",
    "Incident Response",
    "Application Security",
    "Secure Coding"
]

# Function to load posted content
def load_posted():
    print("Loading posted content...")
    if os.path.exists(POSTED_FILE):
        try:
            with open(POSTED_FILE, "r") as f:
                data = json.load(f)
                print(f"Loaded posted content: {data}")
                return set(data) if isinstance(data, list) else set()
        except (json.JSONDecodeError, ValueError):
            print("Error decoding posted.json. Returning empty set.")
            return set()
    print("No posted.json file found. Returning empty set.")
    return set()

# Function to save posted content
def save_posted(posted):
    print(f"Saving posted content: {posted}")
    with open(POSTED_FILE, "w") as f:
        json.dump(list(posted), f, indent=4)

# Function to generate content using ChatGPT
def generate_content(topic):
    print(f"Generating content for topic: {topic}")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Define relevant hashtags for each topic
    topic_hashtags = {
        "Securing Microservices": ["#Microservices", "#CloudSecurity", "#CyberSecurity", "#DevSecOps"],
        "Phishing Attacks": ["#Phishing", "#CyberSecurity", "#InfoSec", "#DataProtection"],
        "Continuous Monitoring and Incident Response in DevSecOps": ["#DevSecOps", "#IncidentResponse", "#CyberSecurity", "#ContinuousMonitoring"],
        "Building a CyberSecurity Awareness Program for Employees": ["#CyberSecurityAwareness", "#InfoSec", "#CyberSecurity", "#EmployeeTraining"],
        "The Role of AI and Machine Learning in Enhancing CyberSecurity": ["#AI", "#MachineLearning", "#CyberSecurity", "#DataProtection"],
        "Mentoring Strategies for Remote and Hybrid Work Environments": ["#Mentorship", "#RemoteWork", "#CyberSecurity", "#HybridWork"],
        "Integrating Security into Agile Development": ["#AgileDevelopment", "#DevSecOps", "#SecureCoding", "#CyberSecurity"],
        "The Impact of Mentoring on Career Development in CyberSecurity": ["#Mentorship", "#CyberSecurityCareers", "#CareerDevelopment", "#CyberSecurity"],
        "Incident Response Planning": ["#IncidentResponse", "#CyberSecurity", "#DataBreach", "#Forensics"],
        "Creating Effective Mentoring Programs in Tech Companies": ["#Mentorship", "#TechLeadership", "#CyberSecurity", "#CareerDevelopment"],
        "Reverse Mentoring": ["#ReverseMentoring", "#Mentorship", "#DiversityAndInclusion", "#CyberSecurity"],
        "DevSecOps Culture": ["#DevSecOps", "#CyberSecurity", "#InfoSec", "#SecureDevOps"],
        "Social Engineering Attacks": ["#SocialEngineering", "#CyberSecurity", "#InfoSec", "#Phishing"],
        "Threat Modeling": ["#ThreatModeling", "#CyberSecurity", "#InfoSec", "#RiskManagement"],
        "How to Be an Effective Mentor": ["#Mentorship", "#Leadership", "#CyberSecurity", "#CareerDevelopment"],
        "Cyber Forensics": ["#CyberForensics", "#IncidentResponse", "#DataBreach", "#CyberSecurity"],
        "The Future of Quantum Computing in CyberSecurity": ["#QuantumComputing", "#CyberSecurity", "#FutureTech", "#Encryption"],
        "Kali Linux": ["#KaliLinux", "#PenetrationTesting", "#CyberSecurity", "#EthicalHacking"],
        "Building a DevSecOps Toolchain": ["#DevSecOps", "#CyberSecurity", "#SecureDevOps", "#Toolchain"],
        "Securing Remote Work": ["#RemoteWork", "#CyberSecurity", "#EndpointSecurity", "#DataProtection"],
        "Integrating Security into the DevOps Pipeline": ["#DevOps", "#DevSecOps", "#SecureCoding", "#CyberSecurity"],
        "Penetration Testing": ["#PenTesting", "#EthicalHacking", "#CyberSecurity", "#VulnerabilityAssessment"],
        "The Role of Blockchain in Enhancing CyberSecurity": ["#Blockchain", "#CyberSecurity", "#Encryption", "#DataProtection"],
        "Mentoring Women in CyberSecurity": ["#WomenInCyberSecurity", "#Mentorship", "#DiversityAndInclusion", "#CyberSecurity"],
        "Tools and Techniques for Automated Security Scanning": ["#SecurityScanning", "#Automation", "#CyberSecurity", "#DevSecOps"],
        "The Importance of Cyber Hygiene": ["#CyberHygiene", "#CyberSecurity", "#InfoSec", "#DataProtection"],
        "Using Mentoring to Foster Innovation and Creativity": ["#Mentorship", "#Innovation", "#CyberSecurity", "#CreativeThinking"],
        "Continuous Security": ["#ContinuousSecurity", "#CyberSecurity", "#DevSecOps", "#RiskManagement"],
        "Secrets Management": ["#SecretsManagement", "#CyberSecurity", "#DataProtection", "#InfoSec"],
        "Implementing Zero Trust Architecture in Modern Enterprises": ["#ZeroTrust", "#CyberSecurity", "#NetworkSecurity", "#IdentityAndAccessManagement"],
        "Bringing Security Early into the Software Development Life Cycle": ["#SecureSDLC", "#DevSecOps", "#CyberSecurity", "#SoftwareDevelopment"],
        "Measuring the Success of Mentoring Programs: Key Metrics and KPIs": ["#Mentorship", "#KPIs", "#CyberSecurity", "#Leadership"],
        "Best Practices for Cloud Security": ["#CloudSecurity", "#CyberSecurity", "#DataProtection", "#CloudComputing"],
        "Leveraging AI and Machine Learning for DevSecOps": ["#AI", "#MachineLearning", "#DevSecOps", "#CyberSecurity"],
        "Building a Mentoring Culture in CyberSecurity Teams": ["#Mentorship", "#CyberSecurity", "#Leadership", "#TeamBuilding"],
        "Ethical Hacking": ["#EthicalHacking", "#PenetrationTesting", "#CyberSecurity", "#InfoSec"],
        "Understanding and Mitigating Ransomware Threats": ["#Ransomware", "#CyberSecurity", "#IncidentResponse", "#DataProtection"],
        "CyberSecurity for IoT Devices": ["#IoTSecurity", "#CyberSecurity", "#DeviceSecurity", "#DataProtection"],
        "Overcoming Challenges in Mentor-Mentee Relationship": ["#Mentorship", "#CareerDevelopment", "#Leadership", "#CyberSecurity"]

    }

    # Select the appropriate hashtags for the topic
    hashtags = topic_hashtags.get(topic, ["#CyberSecurity", "#InfoSec", "#DevSecOps", "#DataProtection"])

    # Join hashtags into a string
    selected_hashtags = " ".join(hashtags)

    # Adjust the max content length based on the length of the hashtags
    hashtag_length = len(selected_hashtags) + 1  # Add 1 for the space before hashtags
    max_content_length = 245 - hashtag_length

    # Payload to send to OpenAI API for content generation
    payload = {
        "model": "gpt-4",
        "max_tokens": 600,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a CyberSecurity and DevSecOps expert with 20+ years of experience. "
                    "You like to communicate with people and share your knowledge with others and ask questions. "
                    "In the Bluesky platform, your goal is to share your knowledge with the audience to gain more followers and engagements to your posts."
                )
            },
            {
                "role": "user",
                "content": (
                    "Craft a post that includes engaging content related to this topic: "
                    f"{topic}\n\nConstraints:\n"
                    f"1. Just write the post, don't write anything else.\n"
                    f"2. Don't exceed {max_content_length} characters for the main content.\n"
                    "3. Don't use quotation marks.\n"
                    "4. Use relevant hashtags for the topic.\n"
                    "5. Don't use emojis.\n"
                    "6. Don't repeat what is already posted.\n"
                    "7. Don't tag YouTube and X accounts or popular Influencers.\n"
                    "8. Don't use other Content creator, names or brandings."
                )
            }
        ]
    }

    # Send request to OpenAI API
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"].strip()
        if len(content) > max_content_length:
            content = content[:max_content_length].rstrip()
        return f"{content} {selected_hashtags}"
    else:
        raise Exception(f"ChatGPT API failed: {response.status_code} {response.text}")

# Function to authenticate with Bluesky
def authenticate_bsky():
    print("Authenticating with Bluesky...")
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    payload = {
        "identifier": BSKY_USERNAME,
        "password": BSKY_PASSWORD
    }
    
    while True:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("Authentication successful.")
            return response.json()["accessJwt"]
        elif response.status_code == 401 and "AuthFactorTokenRequired" in response.text:
            print("Sign-in code required. Check your email.")
            code = input("Enter the sign-in code sent to your email: ").strip()
            
            # Add the MFA code to the payload
            payload["code"] = code
        else:
            raise Exception(f"Bluesky authentication failed: {response.status_code} {response.text}")



# Function to post content to Bluesky
# Function to post content to Bluesky
def post_to_bsky(content, auth_token):
    print(f"Posting content to Bluesky: {content}")
    
    # Ensure the handle format for Bluesky username is correct (e.g., "@username.bsky.social")
    repo_handle = f"hugovalters.bsky.social"  # Assuming the format is "@username.bsky.social"
    
    # Check if there are hashtags at the end and make sure they're formatted correctly
    # Ensure no leading space before the hashtags
    if content.endswith(" "):
        content = content.strip()

    url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    # Ensure the timestamp is in UTC and correctly formatted
    created_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')  # RFC-3339 format

    # Prepare the payload with correct timestamp and repo handle
    payload = {
        "collection": "app.bsky.feed.post",
        "repo": repo_handle,  # Use the correctly formatted repo handle here
        "record": {
            "text": content,
            "createdAt": created_at
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Content posted successfully.")
    else:
        raise Exception(f"Bluesky post failed: {response.status_code} {response.text}")

# Main script logic
def main():
    try:
        posted = load_posted()
        attempts = 0
        max_attempts = 10
        unique_content_found = False

        while attempts < max_attempts and not unique_content_found:
            topic = random.choice(TOPICS)
            print(f"Selected topic: {topic}")
            content = generate_content(topic)

            if content not in posted:
                unique_content_found = True
            else:
                print("Content already posted. Regenerating...")
                attempts += 1

        if not unique_content_found:
            print("Failed to generate unique content after multiple attempts.")
            return

        with open(OUTPUT_FILE, "a") as f:
            f.write(f"\n{datetime.now()}\n{topic}\n{content}\n")

        # Authenticate and post to Bluesky
        auth_token = authenticate_bsky()
        time.sleep(5)  # Wait 5 seconds before posting

        post_to_bsky(content, auth_token)
        posted.add(content)
        save_posted(posted)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()