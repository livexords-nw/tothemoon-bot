---

<h1 align="center">To The Moon Bot</h1>

<p align="center">Automate tasks in POP To The Moon and maximize your in-game rewards effortlessly!</p>

---

## 🚀 **About the Bot**

To The Moon Bot is a powerful automation tool designed for **POP To The Moon** that streamlines various in-game tasks such as:

- **Auto Daily Check-in:** Automatically check and claim your daily rewards.
- **Auto Task:** Execute and claim available tasks without manual input.
- **Auto Achievement:** Automatically claim achievements as soon as they're available.
- **Auto Farming:** Manage farming sessions and claim rewards seamlessly.
- **Auto Planet Exploration:** Discover new planets automatically.

Additional features include:

- **Multi-Account Support:** Manage and automate multiple accounts.
- **Threading System:** Process accounts concurrently using a configurable threading system.
- **Proxy Support:** Optionally enable proxy usage for enhanced security.
- **Customizable Delays:** Adjust delays for account switching and looping for optimal performance.

---

## 🌟 Version v1.2.9

### Updates in This Version:

1. **Remake Script:** Complete overhaul of the script for improved performance and stability.
2. **Proxy System:** Now supports proxy configuration – simply enable it in the config.
3. **Thread System:** Full support for multi-threading, allowing concurrent processing of accounts.

---

## ⚙️ **Configuration in `config.json`**

Below is an example of the configuration file. Adjust these parameters according to your needs:

```json
{
  "daily": true,
  "task": true,
  "achievement": true,
  "farming": true,
  "planet": true,
  "thread": 1,
  "proxy": false,
  "delay_account_switch": 10,
  "delay_loop": 3000
}
```

| **Function**           | **Description**                                        | **Default** |
| ---------------------- | ------------------------------------------------------ | ----------- |
| `daily`                | Automate daily reward check & claim                    | `true`      |
| `task`                 | Automate task execution and reward claims              | `true`      |
| `achievement`          | Automatically claim achievements                       | `true`      |
| `farming`              | Automate farming sessions and reward claims            | `true`      |
| `planet`               | Automatically explore planets                          | `true`      |
| `thread`               | Number of concurrent threads (accounts) to process     | `1`         |
| `proxy`                | Enable/Disable proxy usage                             | `false`     |
| `delay_account_switch` | Delay before switching accounts (in seconds)           | `10`        |
| `delay_loop`           | Delay before restarting the bot loop (in milliseconds) | `3000`      |

---

## 📥 **How to Register**

Start using To The Moon Bot by registering through the following link:

<div align="center">
  <a href="https://t.me/PoPPtothemoon_bot/moon?startapp=5438209644" target="_blank">
    <img src="https://img.shields.io/static/v1?message=POP%20To%20The%20Moon&logo=telegram&label=&color=2CA5E0&logoColor=white&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Clone the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/tothemoon-bot.git
   ```

2. **Navigate to the Project Folder**  
   Change directory to the project folder:

   ```bash
   cd tothemoon-bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Query**  
   Create a `query.txt` file and add your POP To The Moon query data.

5. **Set Up Proxy (Optional)**  
   If you wish to use a proxy, create a `proxy.txt` file and list your proxies in the following format:

   ```
   http://username:password@ip:port
   ```

   Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Execute the bot with the following command:
   ```bash
   python main.py
   ```

---

## 🚀 **Main Features**

- **Auto Daily Check-in:** Claim your daily rewards automatically.
- **Auto Task:** Complete tasks and claim rewards without manual intervention.
- **Auto Achievement:** Automatically claim achievements when eligible.
- **Auto Farming:** Handle farming sessions and reward claims with ease.
- **Auto Planet Exploration:** Explore new planets without lifting a finger.
- **Multi-Account Support:** Manage multiple accounts concurrently.
- **Threading System:** Process several accounts at once with customizable thread settings.
- **Proxy Support:** Optionally use proxies for improved security.
- **Custom Delays:** Fine-tune delay intervals for account switching and loop iterations.

---

## 🛠️ **Contributing**

This project is developed by **livexords**.  
If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
