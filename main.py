from datetime import datetime
import requests
from urllib.parse import parse_qs, urlsplit
import json
import time
from colorama import init, Fore, Style
import random
from fake_useragent import UserAgent
import asyncio


class tothemoon:
    BASE_URL = "https://moons.popp.club/"
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.config = self.load_config()

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 ToTheMoon Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔐 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        self.log(f"📋 Using token: {token[:10]}... (truncated for security)", Fore.CYAN)

        # Parse token data (integrating parse_user_data logic)
        try:
            self.log("📡 Parsing token data...", Fore.CYAN)
            parsed_qs = parse_qs(urlsplit(f"/?{token}").query)
            parsed_data = {k: v[0] for k, v in parsed_qs.items()}
            user_data_parsed = {
                "query_id": parsed_data.get("query_id", ""),
                "user": json.loads(parsed_data.get("user", "{}")),
                "auth_date": parsed_data.get("auth_date", ""),
                "hash": parsed_data.get("hash", ""),
            }
            self.log("✅ Token data parsed successfully", Fore.GREEN)
        except Exception as e:
            self.log(f"❌ Failed to parse token data: {e}", Fore.RED)
            return

        # Send login request using BASE_URL
        login_url = f"{self.BASE_URL}pass/login"
        payload = {"initData": token, "initDataUnSafe": user_data_parsed}
        self.log("📡 Sending login request...", Fore.CYAN)
        try:
            response = requests.post(login_url, headers=self.HEADERS, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send login request: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during login: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception:
                pass
            return

        if response.status_code == 200:
            data = response.json().get("data", None)
            if data is None:
                self.log("❌ Token Expired", Fore.RED)
                return
            self.token = data.get("token", None)
            self.log("✅ Login successful! Token retrieved", Fore.GREEN)
        else:
            self.log(
                f"❌ Login request failed with status code {response.status_code}",
                Fore.RED,
            )
            return

        # Fetch asset data after login
        asset_url = f"{self.BASE_URL}asset/info"
        headers = {**self.HEADERS, "Authorization": self.token}
        self.log("📡 Fetching asset data...", Fore.CYAN)
        try:
            asset_response = requests.get(asset_url, headers=headers)
            asset_response.raise_for_status()
            asset_data = asset_response.json()
            self.log("✅ Asset data retrieved successfully", Fore.GREEN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch asset data: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {asset_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error while fetching asset data: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {asset_response.text}", Fore.RED)
            except Exception:
                pass
            return

        # Display only the important asset data in a user-friendly format
        asset_info = asset_data.get("data", {})
        balance = asset_info.get("sd", "N/A")
        time_val = asset_info.get("time", "N/A")
        wallet_address = asset_info.get("address", "N/A")
        invite_count = asset_info.get("inviteCount", "N/A")
        first_name = asset_info.get("firstName", "N/A")
        equipped_ship = asset_info.get("equippedShip", {})

        self.log("💰 Important Asset Data:", Fore.CYAN)
        self.log(f"    • Balance (sd): {balance}", Fore.CYAN)
        self.log(f"    • Time: {time_val}", Fore.CYAN)
        self.log(f"    • Wallet Address: {wallet_address}", Fore.CYAN)
        self.log(f"    • Invite Count: {invite_count}", Fore.CYAN)
        self.log(f"    • First Name: {first_name}", Fore.CYAN)

        if equipped_ship:
            ship_name = equipped_ship.get("name", "N/A")
            ship_type = equipped_ship.get("type", "N/A")
            ship_level = equipped_ship.get("level", "N/A")
            self.log("    • Equipped Ship:", Fore.CYAN)
            self.log(f"         - Name: {ship_name}", Fore.CYAN)
            self.log(f"         - Type: {ship_type}", Fore.CYAN)
            self.log(f"         - Level: {ship_level}", Fore.CYAN)

    def daily(self) -> bool:
        if not self.token:
            self.log("❌ No token found. Please login first.", Fore.RED)
            return False

        daily_url = f"{self.BASE_URL}moon/sign/in"
        headers = {**self.HEADERS, "Authorization": self.token}
        self.log("📡 Sending daily check-in request...", Fore.CYAN)
        try:
            response = requests.post(daily_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Daily check-in request error: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception:
                pass
            return False

        if response.status_code == 200:
            self.log("✅ Daily check-in successful!", Fore.GREEN)
            return True
        else:
            self.log(
                f"❌ Daily check-in failed with status code: {response.status_code}",
                Fore.RED,
            )
            return False

    def farming(self) -> bool:
        """
        Attempts to claim farming rewards and then start farming.
        This function first sends a POST request to claim farming rewards.
        If successful, it then sends another POST request to start farming.
        Returns True if both requests succeed; otherwise, returns False.
        """
        if not self.token:
            self.log("❌ Token not found. Please login first.", Fore.RED)
            return False

        headers = {**self.HEADERS, "Authorization": self.token}

        # Claim farming rewards
        claim_farming_url = f"{self.BASE_URL}moon/claim/farming"
        self.log("📡 Sending request to claim farming rewards...", Fore.CYAN)
        try:
            response_claim = requests.post(claim_farming_url, headers=headers)
            response_claim.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error claiming farming rewards: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {response_claim.text}", Fore.RED)
            except Exception:
                pass
            return False

        if response_claim.status_code == 200:
            self.log("✅ Successfully claimed farming rewards.", Fore.GREEN)
        else:
            self.log(
                f"❌ Failed to claim farming rewards: Status {response_claim.status_code}",
                Fore.RED,
            )
            return False

        # Start farming
        start_farming_url = f"{self.BASE_URL}moon/farming"
        self.log("📡 Sending request to start farming...", Fore.CYAN)
        try:
            response_start = requests.post(start_farming_url, headers=headers)
            response_start.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error starting farming: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {response_start.text}", Fore.RED)
            except Exception:
                pass
            return False

        if response_start.status_code == 200:
            self.log("✅ Successfully started farming.", Fore.GREEN)
            return True
        else:
            self.log(
                f"❌ Failed to start farming: Status {response_start.status_code}",
                Fore.RED,
            )
            return False

    def planet(self) -> None:
        """
        Initiates planet exploration if probes are available.
        It fetches asset data from the asset API, then the planet list,
        and for each planet sends an exploration request. Key results
        (award and amount) are logged in a user-friendly format.
        """
        if not self.token:
            self.log("❌ No token found. Please login first.", Fore.RED)
            return

        # Fetch asset data directly from the asset API
        asset_url = f"{self.BASE_URL}asset/info"
        headers = {**self.HEADERS, "Authorization": self.token}
        self.log("📡 Fetching asset data...", Fore.CYAN)
        try:
            asset_response = requests.get(asset_url, headers=headers)
            asset_response.raise_for_status()
            asset_data = asset_response.json()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch asset data: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {asset_response.text}", Fore.RED)
            except Exception:
                pass
            return

        # Check if there are probes available for exploration
        probe = asset_data.get("data", {}).get("probe", 0)
        if probe <= 0:
            self.log("ℹ️ No probe available for planet exploration.", Fore.YELLOW)
            return

        # Fetch planet list
        planets_url = f"{self.BASE_URL}moon/planets"
        self.log("📡 Fetching planet data...", Fore.CYAN)
        try:
            planets_response = requests.get(planets_url, headers=headers)
            planets_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Planet request error: {e}", Fore.RED)
            return

        if planets_response.status_code == 200:
            planets_data = planets_response.json()
            self.log("✅ Planet IDs:", Fore.GREEN)
            for planet in planets_data.get("data", []):
                planet_id = planet.get("id", "N/A")
                self.log(f"🌍 Planet ID: {planet_id}", Fore.GREEN)

                # Send exploration request for each planet
                explorer_url = f"{self.BASE_URL}moon/explorer?plantId={planet_id}"
                self.log(f"📡 Exploring planet {planet_id}...", Fore.CYAN)
                try:
                    explorer_response = requests.get(explorer_url, headers=headers)
                    explorer_response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    self.log(
                        f"❌ Exploration request for planet {planet_id} error: {e}",
                        Fore.RED,
                    )
                    continue

                if explorer_response.status_code == 200:
                    explore_data = explorer_response.json().get("data", {})
                    if explore_data:
                        award_data = explore_data.get("award", [{}])
                        award = (
                            award_data[0].get("award", "N/A") if award_data else "N/A"
                        )
                        amount = (
                            award_data[0].get("amount", "N/A") if award_data else "N/A"
                        )
                    else:
                        self.log("❌ Error: Exploration data is empty.", Fore.RED)
                        award = "N/A"
                        amount = "N/A"

                    self.log(
                        f"🌌 Exploration for planet {planet_id}: Award: {Fore.MAGENTA}{award}{Fore.CYAN}, "
                        f"Amount: {Fore.MAGENTA}{amount}",
                        Fore.CYAN,
                    )
                else:
                    self.log(
                        f"❌ Exploration request for planet {planet_id} failed with status code "
                        f"{explorer_response.status_code}: {explorer_response.text}",
                        Fore.RED,
                    )
                    time.sleep(5)
        else:
            self.log(
                f"❌ Planet request failed with status code {planets_response.status_code}: "
                f"{planets_response.text}",
                Fore.RED,
            )

    def achievement(self) -> None:
        """
        Retrieves achievement data from the API and checks each achievement.
        For each achievement in the achievementMap, if it is not yet claimed (claimStatus == 0)
        and the current value meets or exceeds the threshold, a claim request is sent.
        Logs the outcome for each achievement in a user-friendly format.
        """
        if not self.token:
            self.log("❌ No token found. Please login first.", Fore.RED)
            return

        achievements_url = f"{self.BASE_URL}moon/achievement/list"
        headers = {**self.HEADERS, "Authorization": self.token}
        self.log("📡 Fetching achievements...", Fore.CYAN)

        try:
            response = requests.get(achievements_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch achievements: {e}", Fore.RED)
            return

        data = response.json()
        if "data" not in data:
            self.log("❌ Response JSON does not contain 'data' key.", Fore.RED)
            return

        achievement_map = data["data"].get("achievementMap", {})
        if not achievement_map:
            self.log("ℹ️ No achievements found.", Fore.YELLOW)
            return

        # Process each achievement in the achievementMap
        for key, ach in achievement_map.items():
            name = ach.get("name", "N/A")
            award_info = ach.get("award", {})
            amount = award_info.get("amount", "N/A")
            award_name = award_info.get("award", "N/A")
            threshold = ach.get("threshold", 0)
            current = ach.get("current", 0)
            claim_status = ach.get("claimStatus", 0)

            if claim_status == 0 and current >= threshold:
                self.log(
                    f"📡 Claiming achievement: {name} (Current: {current}, Threshold: {threshold})...",
                    Fore.CYAN,
                )
                check_url = (
                    f"{self.BASE_URL}moon/achievement/check?achievementName={name}"
                )
                try:
                    check_response = requests.get(check_url, headers=headers)
                    check_response.raise_for_status()
                    self.log(
                        f"✅ {name} | Amount: {Fore.MAGENTA}{amount}{Fore.RESET} | Award: {Fore.GREEN}{award_name}{Fore.RESET}",
                        Fore.GREEN,
                    )
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to claim achievement {name}: {e}", Fore.RED)
            else:
                if claim_status != 0:
                    self.log(
                        f"ℹ️ Achievement {name} already claimed (Claim Status: {claim_status}).",
                        Fore.YELLOW,
                    )
                else:
                    self.log(
                        f"ℹ️ Achievement {name} not eligible (Current: {current}, Threshold: {threshold}).",
                        Fore.YELLOW,
                    )

    def task(self) -> None:
        """
        Retrieves the task list and processes active tasks.
        For each active task (where "junzi" is True), the function first starts the task
        by sending two requests:
        1. A POST request to the original start endpoint.
        2. A GET request to the new check endpoint.
        If both calls are successful, the task is considered started.
        After starting all tasks, the function waits 5 seconds before claiming them.
        Logs the outcome of each step in a user-friendly manner.
        """
        if not self.token:
            self.log("❌ No token found. Please login first.", Fore.RED)
            return

        tasks_url = f"{self.BASE_URL}moon/task/list"
        headers = {**self.HEADERS, "Authorization": self.token}
        self.log("📡 Fetching task list...", Fore.CYAN)

        try:
            response = requests.get(tasks_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch tasks: {e}", Fore.RED)
            return

        data = response.json()
        if "data" not in data:
            self.log("❌ Task response JSON does not contain 'data' key.", Fore.RED)
            return

        tasks = data["data"]
        if not tasks:
            self.log("ℹ️ No tasks available.", Fore.YELLOW)
            return

        # List to store details of tasks that are started and ready to claim
        started_tasks = []

        self.log("🚀 Starting tasks...", Fore.CYAN)
        for task in tasks:
            # Process only tasks that are active (junzi: true means still available to work on)
            if task.get("junzi", False):
                task_id = task.get("taskId")
                name = task.get("name", "N/A")
                award_info = task.get("award", {})
                amount = award_info.get("amount", "N/A")
                award_name = award_info.get("award", "N/A")

                self.log(f"📡 Starting task: {name} (ID: {task_id})", Fore.CYAN)

                # First, send the old start API (POST request)
                old_start_url = f"{self.BASE_URL}moon/task/visit/ss?taskId={task_id}"
                payload = {"taskId": task_id}
                try:
                    old_start_response = requests.post(
                        old_start_url, headers=headers, json=payload
                    )
                    old_start_response.raise_for_status()
                    self.log(f"✅ Old start succeeded for task: {name}", Fore.GREEN)
                except requests.exceptions.RequestException as e:
                    self.log(
                        f"❌ Failed to start task {name} (old API) [ID: {task_id}]: {e}",
                        Fore.RED,
                    )
                    continue

                # Then, call the new start/check API (GET request)
                new_start_url = f"{self.BASE_URL}moon/task/check?taskId={task_id}"
                try:
                    new_start_response = requests.get(new_start_url, headers=headers)
                    new_start_response.raise_for_status()
                    new_data = new_start_response.json()
                    if new_data.get("code") == "200":
                        self.log(f"✅ New check succeeded for task: {name}", Fore.GREEN)
                    else:
                        self.log(
                            f"❌ New check failed for task: {name} with response: {new_data}",
                            Fore.RED,
                        )
                        continue
                except requests.exceptions.RequestException as e:
                    self.log(
                        f"❌ Failed to check task {name} (new API) [ID: {task_id}]: {e}",
                        Fore.RED,
                    )
                    continue

                # If both start calls are successful, add the task to the list for claiming later
                started_tasks.append((task_id, name, amount, award_name))

        if not started_tasks:
            self.log("ℹ️ No active tasks were started.", Fore.YELLOW)
            return

        self.log("⏳ Waiting 5 seconds before claiming tasks...", Fore.CYAN)
        time.sleep(5)

        self.log("🚀 Claiming tasks...", Fore.CYAN)
        for task_id, name, amount, award_name in started_tasks:
            claim_url = f"{self.BASE_URL}moon/task/claim?taskId={task_id}"
            try:
                claim_response = requests.get(claim_url, headers=headers)
                claim_response.raise_for_status()
                if claim_response.status_code == 200:
                    self.log(
                        f"✅ {name} | Amount: {Fore.MAGENTA}{amount}{Fore.RESET} | Award: {Fore.GREEN}{award_name}{Fore.RESET}",
                        Fore.GREEN,
                    )
                else:
                    self.log(
                        f"❌ Claiming task {name} failed with status code {claim_response.status_code}",
                        Fore.RED,
                    )
            except requests.exceptions.RequestException as e:
                self.log(
                    f"❌ Failed to claim task {name} (ID: {task_id}): {e}", Fore.RED
                )

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        import random

        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


async def process_account(account, original_index, account_label, tothe, config):
    # Set a random fake User-Agent for this account
    ua = UserAgent()
    tothe.HEADERS["User-Agent"] = ua.random

    display_account = account[:10] + "..." if len(account) > 10 else account
    tothe.log(f"👤 Processing {account_label}: {display_account}", Fore.YELLOW)

    # Override proxy if enabled
    if config.get("proxy", False):
        tothe.override_requests()
    else:
        tothe.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

    # Login (blocking call executed in a thread) using the account's index
    await asyncio.to_thread(tothe.login, original_index)

    tothe.log("🛠️ Starting task execution...", Fore.CYAN)
    tasks_config = {
        "daily": "Daily Reward Check & Claim 🎁",
        "task": "Automatically solving tasks 🤖",
        "achievement": "Auto claim achievement",
        "farming": "Automatic farming for abundant harvest 🌾",
        "planet": "Auto planet exploration 🚀",
    }

    for task_key, task_name in tasks_config.items():
        task_status = config.get(task_key, False)
        color = Fore.YELLOW if task_status else Fore.RED
        tothe.log(
            f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
            color,
        )
        if task_status:
            tothe.log(f"🔄 Executing {task_name}...", Fore.CYAN)
            await asyncio.to_thread(getattr(tothe, task_key))

    delay_switch = config.get("delay_account_switch", 10)
    tothe.log(
        f"➡️ Finished processing {account_label}. Waiting {Fore.WHITE}{delay_switch}{Fore.CYAN} seconds before next account.",
        Fore.CYAN,
    )
    await asyncio.sleep(delay_switch)


async def worker(worker_id, tothe, config, queue):
    """
    Each worker takes one account from the queue and processes it sequentially.
    A worker will not take a new account until the current one is finished.
    """
    while True:
        try:
            original_index, account = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        account_label = f"Worker-{worker_id} Account-{original_index+1}"
        await process_account(account, original_index, account_label, tothe, config)
        queue.task_done()
    tothe.log(
        f"Worker-{worker_id} finished processing all assigned accounts.", Fore.CYAN
    )


async def main():
    tothe = tothemoon()  # Initialize your ToTheMoon instance
    config = tothe.load_config()
    all_accounts = tothe.query_list
    num_workers = config.get("thread", 1)  # Number of concurrent workers (threads)

    tothe.log(
        "🎉 [LIVEXORDS] === Welcome to ToTheMoon Automation === [LIVEXORDS]",
        Fore.YELLOW,
    )
    tothe.log(f"📂 Loaded {len(all_accounts)} accounts from query list.", Fore.YELLOW)

    if config.get("proxy", False):
        proxies = tothe.load_proxies()

    while True:
        # Create a new asyncio Queue and add all accounts (with their original index)
        queue = asyncio.Queue()
        for idx, account in enumerate(all_accounts):
            queue.put_nowait((idx, account))

        # Create worker tasks according to the number of threads specified
        workers = [
            asyncio.create_task(worker(i + 1, tothe, config, queue))
            for i in range(num_workers)
        ]

        # Wait until all accounts in the queue are processed
        await queue.join()

        # Cancel workers to avoid overlapping in the next loop
        for w in workers:
            w.cancel()

        tothe.log("🔁 All accounts processed. Restarting loop.", Fore.CYAN)
        delay_loop = config.get("delay_loop", 30)
        tothe.log(
            f"⏳ Sleeping for {Fore.WHITE}{delay_loop}{Fore.CYAN} seconds before restarting.",
            Fore.CYAN,
        )
        await asyncio.sleep(delay_loop)


if __name__ == "__main__":
    asyncio.run(main())
