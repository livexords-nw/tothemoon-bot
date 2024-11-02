from datetime import datetime
import requests
from urllib.parse import parse_qs, urlsplit
import json
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


class Display:
    """Handles display functions with color formatting."""

    @staticmethod
    def welcome_message():
        print(
            r"""
                ██╗     ██╗██╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗ ██████╗ ███████╗
                ██║     ██║██║   ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝
                ██║     ██║██║   ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝██║  ██║███████╗
                ██║     ██║╚██╗ ██╔╝██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██║  ██║╚════██║
                ███████╗██║ ╚████╔╝ ███████╗██╔╝ ██╗╚██████╔╝██║  ██║██████╔╝███████║
                ╚══════╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝
                                                                                    
        """
        )
        print(Fore.GREEN + Style.BRIGHT + "Free POP To The MOON Airdrop BOT")


class MoonBot:
    """Handles login, token retrieval, and account processing."""

    common_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
    }

    def __init__(self, init_data):
        self.init_data = init_data
        self.token = None
        self.user_data = self.parse_user_data(init_data)
    
    def print_(message, color=Fore.RESET):
        timestamp = datetime.now().strftime("[%Y:%m:%d:%H:%M:%S] |")
        print(color + timestamp + " " + message + Fore.RESET)

    @staticmethod
    def parse_user_data(init_data):
        parsed_data = {
            k: v[0] for k, v in parse_qs(urlsplit(f"/?{init_data}").query).items()
        }
        return {
            "query_id": parsed_data.get("query_id", ""),
            "user": json.loads(parsed_data.get("user", "{}")),
            "auth_date": parsed_data.get("auth_date", ""),
            "hash": parsed_data.get("hash", ""),
        }

    def login(self):
        login_url = "https://moon.popp.club/pass/login"
        payload = {"initData": self.init_data, "initDataUnSafe": self.user_data}
        response = requests.post(login_url, headers=self.common_headers, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("data", {}).get("token", None)
        return self.token

    def check_in(self):
        if self.token:
            check_in_url = "https://moon.popp.club/moon/sign/in"
            headers = {**self.common_headers, "Authorization": self.token}
            response = requests.post(check_in_url, headers=headers)
            return response.status_code == 200
        return False

    def get_asset_data(self):
        if self.token:
            asset_url = "https://moon.popp.club/moon/asset"
            headers = {**self.common_headers, "Authorization": self.token}
            response = requests.get(asset_url, headers=headers)
            return response.json() if response.status_code == 200 else None
        return None

    def claim_rewards(self):
        if not self.token:
            MoonBot.print_(color=Fore.RED, message="Token not found")
            return False

        MoonBot.print_(color=Fore.BLUE, message="======= Attempting to claim farming rewards =======")
        headers = {"Authorization": self.token, **self.common_headers}
        start_farming_url = "https://moon.popp.club/moon/farming"
        claim_farming_url = "https://moon.popp.club/moon/claim/farming"

        if self.send_request(start_farming_url, headers, "successfully started farming.", "failed to start farming"):
            return self.send_request(claim_farming_url, headers, "Successfully claimed farming results.", "failed to claim farming results")
        return False

    def send_request(self, url, headers, success_message, failure_message):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            MoonBot.print_(color=Fore.GREEN, message=success_message)
            return True
        except requests.exceptions.RequestException as e:
            MoonBot.print_(color=Fore.RED, message=f"{failure_message}: {e}")
            return False

    def explore_planets(self):
        """Initiates exploration for each planet."""
        if self.token:
            MoonBot.print_(color=Fore.BLUE, message="======= Attempting to claim farming rewards =======")
            asset_data = self.get_asset_data()
            if asset_data:
                probe = asset_data.get("data", {}).get("probe", 0)
                planets_url = "https://moon.popp.club/moon/planets"
                if probe > 0:
                    headers = {"Authorization": self.token, **self.common_headers}

                    planets_response = requests.get(planets_url, headers=headers)
                    if planets_response.status_code == 200:
                        planets_data = planets_response.json()
                        MoonBot.print_(color=Fore.GREEN, message="ID Planet:")
                        for planet in planets_data.get("data", []):
                            planet_id = planet.get("id", "N/A")
                            MoonBot.print_(color=Fore.GREEN, message=str(planet_id))

                            explorer_url = f"https://moon.popp.club/moon/explorer?plantId={planet_id}"
                            explorer_response = requests.get(explorer_url, headers=headers)

                            if explorer_response.status_code == 200:
                                explore_data = explorer_response.json().get("data", {})

                                award_data = explore_data.get("award", [{}])
                                award = award_data[0].get("award", "N/A") if award_data else "N/A"
                                amount = award_data[0].get("amount", "N/A") if award_data else "N/A"

                                MoonBot.print_(
                                    color=Fore.BLUE,
                                    message=f"{Fore.CYAN}Exploration for planet {Fore.MAGENTA}{planet_id}{Style.RESET_ALL}, "
                                            f"Award: {Fore.MAGENTA}{award}{Style.RESET_ALL}, "
                                            f"Amount: {Fore.MAGENTA}{amount}{Style.RESET_ALL}"
                                )
                            else:
                                MoonBot.print_(
                                    color=Fore.RED,
                                    message=f"Exploration request for planet {planet_id} failed with status code {explorer_response.status_code}: {explorer_response.text}"
                                )
                    else:
                        MoonBot.print_(
                            color=Fore.RED,
                            message=f"Planet request failed with status code {planets_response.status_code}: {planets_response.text}"
                        )
            else:
                MoonBot.print_(color=Fore.RED, message="Token not found")


    # Achivment Function
    def get_and_send_achievements(self):
        if not self.token:
            return

        check_task_url = "https://moon.popp.club/moon/achievement/list"
        headers = {**self.common_headers, "Authorization": self.token}

        try:
            response = requests.get(check_task_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "data" not in data:
                MoonBot.print_(color=Fore.RED, message="Response JSON does not contain 'data' key")
                return

            tasks = data["data"]

            def extract_and_send_names(data):
                if isinstance(data, dict):
                    achievement_name = data.get("name")
                    if achievement_name:
                        send_achievement_request(achievement_name)

                    # Recurse into the dictionary values
                    for value in data.values():
                        extract_and_send_names(value)
                elif isinstance(data, list):
                    # Recurse into each item in the list
                    for item in data:
                        extract_and_send_names(item)

            def send_achievement_request(achievement_name):
                try:
                    check_url = f"https://moon.popp.club/moon/achievement/check?achievementName={achievement_name}"
                    check_response = requests.get(check_url, headers=headers)
                    check_response.raise_for_status()
                    MoonBot.print_(color=Fore.BLUE, message=f"{Fore.YELLOW} Sent request for achievement: {achievement_name}, {Fore.GREEN}Status: {check_response.status_code}")
                except requests.exceptions.RequestException as e:
                    MoonBot.print_(color=Fore.RED, message=f"Failed to send request for {achievement_name}: {e}")

            # Start the extraction and request sending process
            extract_and_send_names(tasks)

        except requests.exceptions.RequestException as e:
            MoonBot.print_(color=Fore.RED, message=f"Request failed: {e}")
        except ValueError:
            MoonBot.print_(color=Fore.RED, message="Failed to decode JSON from response")

    # Task Function
    def get_tasks(self):
        if not self.token:
            return []

        check_task_url = "https://moon.popp.club/moon/task/list"
        headers = {**self.common_headers, "Authorization": self.token}

        try:
            response = requests.get(check_task_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "data" not in data:
                MoonBot.print_(color=Fore.RED, message="Response JSON does not contain 'data' key")
                return []

            tasks = data["data"]
            return [task["taskId"] for task in tasks]

        except requests.exceptions.RequestException as e:
            MoonBot.print_(color=Fore.RED, message=f"Request failed: {e}")
        except ValueError:
            MoonBot.print_(color=Fore.RED, message="Failed to decode JSON from response")

        return []
    
    def complete_task(self, task_id):
        """Starts and claims a task by task ID."""
        if not self.token:
            MoonBot.print_(color=Fore.RED, message="Token not found")
            return False

        headers = {**self.common_headers, "Authorization": self.token}
        
        # Start Task
        if not self._start_task(task_id, headers):
            return False

        # Claim Task
        return self._claim_task(task_id, headers)

    def _start_task(self, task_id, headers):
        """Starts the task and handles any request errors."""
        task_url = f"https://moon.popp.club/moon/task/visit/ss?taskId={task_id}"
        payload = {"taskId": task_id}

        try:
            response_task = requests.post(task_url, headers=headers, json=payload)
            response_task.raise_for_status()
            MoonBot.print_(color=Fore.GREEN, message=f"Successfully started task with ID: {task_id}")
            return True

        except requests.exceptions.RequestException as e:
            MoonBot.print_(color=Fore.RED, message=f"Failed to start task with ID: {task_id}. Request error: {e}")
        except ValueError:
            MoonBot.print_(color=Fore.RED, message=f"Failed to decode JSON for start task response: {response_task.text}")
        
        return False

    def _claim_task(self, task_id, headers):
        """Claims the task and handles any request errors."""
        claim_url = f"https://moon.popp.club/moon/task/claim?taskId={task_id}"

        try:
            response_claim = requests.get(claim_url, headers=headers)
            response_claim.raise_for_status()
            
            if response_claim.status_code == 200:
                MoonBot.print_(color=Fore.GREEN, message=f"Successfully claimed task with ID: {task_id}")
                return True

        except requests.exceptions.RequestException as e:
            MoonBot.print_(color=Fore.RED, message=f"Failed to claim task with ID: {task_id}. Request error: {e}")
        except ValueError:
            MoonBot.print_(color=Fore.RED, message=f"Failed to decode JSON for claim task response: {response_claim.text}")

        return False

class AccountProcessor:
    """Processes each account, handles actions like login, check-in, and asset retrieval."""

    def __init__(self, account_data_file):
        self.account_data_file = account_data_file

    def read_account_data(self):
        """Reads account data from a file, returning non-empty lines."""
        with open(self.account_data_file, "r") as file:
            return [line.strip() for line in file if line.strip()]

    def process_all_accounts(self):
        """Processes each account: logs in, performs check-in, retrieves assets, claims rewards, explores planets, and completes tasks."""
        account_list = self.read_account_data()
        total_accounts = len(account_list)

        MoonBot.print_(message=f"Total Accounts: {total_accounts}\n", color=Fore.GREEN)

        for index, account_data in enumerate(account_list, start=1):
            self.process_single_account(account_data, index, total_accounts)

    def process_single_account(self, account_data, index, total_accounts):
        """Processes a single account with actions like login, check-in, asset retrieval, and task completion."""
        MoonBot.print_(color=Fore.YELLOW, message=f"====== Processing Account {index}/{total_accounts} ======")
        bot = MoonBot(account_data)

        # Login
        if not bot.login():
            MoonBot.print_(color=Fore.RED, message="Failed to log in.")
            return
        MoonBot.print_(color=Fore.GREEN, message=f"Successfully logged in to Account {index}.")
        time.sleep(10)  # Delay after login

        # Check-in
        if bot.check_in():
            MoonBot.print_(color=Fore.GREEN, message="Check-in completed.")
        time.sleep(10)  # Delay after check-in

        # Asset retrieval and operations
        asset_data = bot.get_asset_data()
        if asset_data:
            self.display_asset_data(asset_data, bot)
            self.claim_achievements(bot)
            self.complete_tasks(bot)
            time.sleep(10)  # Delay after asset operations

        # Re-check assets after completing tasks
        bot.check_in()
        refreshed_asset_data = bot.get_asset_data()
        if refreshed_asset_data:
            self.display_asset_data(refreshed_asset_data, bot)
        time.sleep(10)  # Delay after re-checking assets

        # Final wait before processing the next account
        MoonBot.print_(color=Fore.YELLOW, message="Waiting for 10 seconds before processing the next account...")
        time.sleep(10)

    def claim_rewards(self, bot):
        """Claims farming rewards for an account."""
        result = bot.claim_rewards()
        if result:
            MoonBot.print_(color=Fore.GREEN, message="Farming rewards successfully claimed.")
        else:
            MoonBot.print_(color=Fore.RED, message="Failed to claim farming rewards.")
        time.sleep(2)


    def explore_planets(self, bot):
        """Initiates planet exploration for an account."""
        bot.explore_planets()
        time.sleep(2)

    def claim_achievements(self, bot):
        """Claims achievements for an account."""
        MoonBot.print_(color=Fore.BLUE, message="======= Claimed Achievements =======")
        bot.get_and_send_achievements()
        time.sleep(2)

    def complete_tasks(self, bot):
        """Retrieves and completes tasks for an account."""
        MoonBot.print_(color=Fore.BLUE, message="======= Claimed Tasks =======")
        task_ids = bot.get_tasks()
        for task_id in task_ids:
            success_message = f"Successfully completed the task with ID: {task_id}"
            failure_message = f"Failed to complete the task with ID: {task_id}"
            if bot.complete_task(task_id):
                MoonBot.print_(color=Fore.GREEN, message=success_message)
            else:
                MoonBot.print_(color=Fore.RED, message=failure_message)
        time.sleep(2)

    @staticmethod
    def display_asset_data(asset_data, bot):
        """Displays asset data details for an account."""
        data = asset_data.get("data", {})
        sd = data.get("sd", 0)
        probe = data.get("probe", 0)
        eth = data.get("eth", 0)

        remaining_time_ms = max(0, data.get("farmingEndTime", 0) - data.get("systemTimestamp", 0))
        hours, minutes, seconds = AccountProcessor.convert_ms_to_time(remaining_time_ms)

        # Display asset details
        MoonBot.print_(color=Fore.BLUE, message=f"{Fore.CYAN}[SD]: {Fore.MAGENTA}{sd}{Style.RESET_ALL}")
        MoonBot.print_(color=Fore.BLUE, message=f"{Fore.CYAN}[Probe]: {Fore.MAGENTA}{probe}{Style.RESET_ALL}")
        MoonBot.print_(color=Fore.BLUE, message=f"{Fore.CYAN}[ETH]: {Fore.MAGENTA}{eth}{Style.RESET_ALL}")
        MoonBot.print_(
            color=Fore.BLUE,
            message=(
                f"{Fore.CYAN}Remaining time: {Fore.YELLOW}{hours} hours, {minutes} minutes, "
                f"and {seconds} seconds{Style.RESET_ALL}"
            )
        )

        # Call bot methods instead of class methods
        if remaining_time_ms == 0:
            bot.claim_rewards()
        elif probe > 0:
            bot.explore_planets()

    @staticmethod
    def convert_ms_to_time(ms):
        """Converts milliseconds to hours, minutes, and seconds."""
        total_seconds = ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return hours, minutes, seconds

def main():
    Display.welcome_message()
    processor = AccountProcessor("query.txt")
    while True:
        processor.process_all_accounts()
        MoonBot.print_(color=Fore.GREEN,message="====== All accounts processed ======")
        MoonBot.print_(color=Fore.CYAN,message="Waiting 10 minutes before re-processing...")
        time.sleep(600)


if __name__ == "__main__":
    main()
