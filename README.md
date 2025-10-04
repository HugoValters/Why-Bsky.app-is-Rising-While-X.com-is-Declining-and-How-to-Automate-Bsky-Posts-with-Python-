As of 2025, X.com is slowly dying due to poor decisions, spam overload, AI-generated noise, and widespread disinformation. However, that’s not necessarily bad news — Bsky.app has been gaining more and more former X.com users every day. Not only are people signing up, but they are actively engaging, communicating with brands, and creating a lively atmosphere. Brands, too, have started opening accounts and posting actively.

Of course, as Bsky.app grows, it will also eventually face challenges like bots, fake accounts, and misinformation. Growth always brings new issues. But why are so many users currently migrating to Bsky.app?

From my perspective, the main reasons are:
* **Trust**: Co-founded by Twitter’s original creator Jack Dorsey
* **Simplicity**: It reminds users of the early Twitter experience — clean and user-friendly.
* **Independence**: The platform is not tied to any government, unlike X.com, where Elon Musk is now heavily involved in U.S. and even global politics. In my opinion, that’s a mistake. Platforms like Starlink and X should remain politically neutral and focus on improving service quality — fixing fake engagement, bot issues, spam, misinformation, and creating better programs for content creators.

Still, that’s just my opinion. X is a private business and can operate however it wants.

Meanwhile, Bsky.app is starting to feel like “home” for many users, including myself. That’s why I decided to automate my Bsky.app activity — by creating a Python script that can post AI-generated messages. This could be very useful for companies to maintain an active profile without manual effort.

I’ve made a video guide available here:
https://www.youtube.com/watch?v=bbT2FtokMmY

Last year, I created a tutorial on automating X.com posts using Make.com, but since Make.com does not support Bsky.app directly, I decided to build a Python solution.

This is Version 1 of the script: it posts messages to Bsky.app. In the future, I plan to:
* Dockerize the project
* Add database support.
* Expand it to support X.com, LinkedIn.com, and more.
* Allow users to select different AI providers.

## Getting Started: Requirements
* OpenAI account (needs to be topped up with around 10 USD/EUR; it should last 4–6 months at low usage rates)
* A VPS server (or your own PC/laptop/server)

Personally, I use a VPS from [Zone.eu](https://www.zone.eu). They offer secure hosting, real 24/7 human support (no chatbots or AI), and competitive pricing. I highly recommend trying them!

## Step 1: Setting Up the Server

Login to your server: On MacOS: open Terminal. On Windows: open CMD.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mc366o03j4enqf9vikhe.webp)

Update your package list:

```
sudo apt-get update
```

Install Python and related packages:

```
sudo apt install -y python-is-python3 python3-venv python3-pip
```

Install Git (if not already installed):

```
sudo apt-get install -y git
```

Create a project directory:

```
mkdir /srv/socialmedia && cd /srv/socialmedia
```

Clone the [GitHub](https://github.com/HugoValters/social-media-automation) repository:

```
git clone https://github.com/ValtersIT/social-media-automation.git
```

## Step 2: Setting Up OpenAI API Key
Go to [OpenAI Login](https://auth.openai.com/log-in)
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/u4wsprvocxpufyhdkw9o.webp)

Log in or create an account (no credit card required to start).
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2vvq0yow46xginwdlobk.webp)

Click the gear icon (top right) → API Keys.
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4laebeybv788h385nvt9.webp)

Create a new secret key and save it safely.
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y908hnltc1qo8s8wb71p.webp)


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/048ynrioh6mbhsicwt2p.webp)


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kwljlot7151j3figkdw7.webp)

You will also need to add credit (around 10 USD/EUR) to your account under the Billing section.

## Step 3: Setting Up Bsky.app Credentials
If you don’t have a Bsky.app account yet, create one here: [Bsky Signup](https://bsky.app).
You will need your email and password for the script (note: if you have Two-Factor Authentication enabled, the script might not work yet).

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rrtskt1u17mrvgyzjiq1.webp)

## Step 4: Configuring the Python Script
Open the script for editing:

```
nano /srv/socialmedia/social-media-automation/bsky.py
```

Replace the placeholders in the script:
* **OPENAI_API_KEY** → your OpenAI secret key (starting with sk-…)
* **BSKY_USERNAME** → your Bsky.app email.
* **BSKY_PASSWORD** → your Bsky.app password


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kcrkko2vvu0lpocirsf6.webp)

**Topics**: Add a list of topics you want your AI posts to be about. Example:


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vvnii1mejk11jushyf6g.webp)

```
TOPICS = [
  "Cloud Security",
  "DevSecOps Practices",
  "Zero Trust Architecture",
  "Incident Response"
]
```

> Hashtags: For each topic, define related hashtags. Example:
“Incident Response”: [“#IncidentResponse”, “#CyberSecurity”, “#InfoSec”, “#DevSecOps”]
You can generate topics and hashtags easily by asking ChatGPT:

* “**Give me 20 topics about CyberSecurity.**”
* “**Give me 30 hashtags for Network Security.**”


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/659stnjz8opbonz3np52.webp)

## Step 5: Running the Script
Make the script executable:
```
chmod +x /srv/socialmedia/social-media-automation/bsky.py
```

Run the script manually:
```
python3 /srv/socialmedia/social-media-automation/bsky.py
```

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3ulj7mpkfvlj8lc2sr9g.webp)

It will:
* Randomly select a topic.
* Ask ChatGPT to generate a post.
* Add relevant hashtags.
* Post to Bsky.app.

It also saves the generated messages to output_bsky.txt and a JSON file posted_bsky.json to avoid reposting the same content.


![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n294ci6wwcvimgtkc25q.webp)

## Step 6: Automating with Cron
If you want to post automatically every 30 minutes, set up a cron job:

Edit the crontab:
```
crontab -e
```

At the end of the file, add:
```
*/30 * * * * python3 /srv/socialmedia/social-media-automation/bsky.py
```

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vuis3vk9f0ybrhpuodnt.webp)

Save and exit.
Now your server will post automatically every 30 minutes!

## Final Words
That’s it! Now you have a fully working Bsky.app auto-poster powered by ChatGPT.
If you found this guide useful, don’t forget to follow me:

Follow for more:<br>
X.com: https://x.com/hugovalters<br>
bsky.app: https://bsky.app/profile/hugovalters.bsky.social<br>
YouTube: https://www.youtube.com/@hugovalters<br>
Homepage: https://www.valters.eu<br>
GitHub: https://github.com/hugovalters<br>
GitLab: [https://gitlab.com/hugovalters](https://gitlab.com/hugovalters)<br>
Medium: https://blog.valters.eu

Thank you for reading!
(Disclaimer: This post reflects my personal opinions and experiences.)

By Hugo Valters
