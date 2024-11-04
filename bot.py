from datetime import datetime
import requests
from urllib.parse import parse_qs, urlsplit
import json
import time
from colorama import init, Fore, Style

init(autoreset=True)

class Display:
    """Handles display functions with color formatting."""

    @staticmethod
    def welcome_message():
        print("             This bot created by LIVEXORDS\n")


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
    
    def print_(message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] |")
        print(Fore.LIGHTBLACK_EX + timestamp + " " + message + Fore.RESET)

    def load_config():
        """Load the configuration from config.json once at the start."""
        with open('config.json') as config_file:
            config = json.load(config_file)
        return config

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
            asset_url = "https://moon.popp.club/asset/info"
            headers = {**self.common_headers, "Authorization": self.token}
            response = requests.get(asset_url, headers=headers)
            return response.json() if response.status_code == 200 else None
        return None

    def claim_rewards(self):
        if not self.token:
            MoonBot.print_(message=f"{Fore.RED}Token not found")
            return False

        headers = {"Authorization": self.token, **self.common_headers}
        start_farming_url = "https://moon.popp.club/moon/farming"
        claim_farming_url = "https://moon.popp.club/moon/claim/farming"

        if self.send_request(claim_farming_url, headers, "successfully claim farming.", "failed to claim farming"):
            return self.send_request(start_farming_url, headers, "Successfully started farming results.", "failed to start farming results")
        return False

    def send_request(self, url, headers, success_message, failure_message):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            MoonBot.print_(message=f"{Fore.GREEN}{success_message}")
            return True
        except requests.exceptions.RequestException as e:
            MoonBot.print_(message=f"{Fore.RED}{failure_message}: {e}")
            return False

    def explore_planets(self):
        """Initiates exploration for each planet."""
        if self.token:
            asset_data = self.get_asset_data()
            if asset_data:
                probe = asset_data.get("data", {}).get("probe", 0)
                planets_url = "https://moon.popp.club/moon/planets"
                if probe > 0:
                    headers = {"Authorization": self.token, **self.common_headers}

                    planets_response = requests.get(planets_url, headers=headers)
                    if planets_response.status_code == 200:
                        planets_data = planets_response.json()
                        MoonBot.print_(message=f"{Fore.GREEN}ID Planet:")
                        for planet in planets_data.get("data", []):
                            planet_id = planet.get("id", "N/A")
                            MoonBot.print_(message=f"{Fore.GREEN}{str(planet_id)}")

                            explorer_url = f"https://moon.popp.club/moon/explorer?plantId={planet_id}"
                            explorer_response = requests.get(explorer_url, headers=headers)

                            if explorer_response.status_code == 200:
                                explore_data = explorer_response.json().get("data", {})

                                if explore_data: 
                                    award_data = explore_data.get("award", [{}])
                                    award = award_data[0].get("award", "N/A") if award_data else "N/A"
                                    amount = award_data[0].get("amount", "N/A") if award_data else "N/A"
                                else:
                                    MoonBot.print_(message=f"{Fore.RED}Error: Explore data is empty.")
                                    award = "N/A"
                                    amount = "N/A"
                                    
                                MoonBot.print_(
                                    message=f"{Fore.CYAN}Exploration for planet {Fore.MAGENTA}{planet_id}{Style.RESET_ALL}, "
                                            f"Award: {Fore.MAGENTA}{award}{Style.RESET_ALL}, "
                                            f"Amount: {Fore.MAGENTA}{amount}{Style.RESET_ALL}"
                                )
                            else:
                                MoonBot.print_(
                                    message=f"{Fore.RED}Exploration request for planet {planet_id} failed with status code {explorer_response.status_code}: {explorer_response.text}"
                                )
                    else:
                        MoonBot.print_(
                            message=f"{Fore.RED}Planet request failed with status code {planets_response.status_code}: {planets_response.text}"
                        )
            else:
                MoonBot.print_(message=f"{Fore.RED}Token not found")


    # Achievement Function
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
                MoonBot.print_(message=f"{Fore.RED}Response JSON does not contain 'data' key")
                return

            achievement = data["data"]

            awards_info = []

            def extract_and_send_names(data):
                if isinstance(data, dict):
                    achievement_name = data.get("name")
                    award = data.get("award")

                    if isinstance(award, dict):
                        award_amount = award.get("amount")
                        award_name = award.get("award")

                        if achievement_name and award_amount is not None:
                            awards_info.append((achievement_name, award_amount, award_name))
                            send_achievement_request(achievement_name, award_amount, award_name)

                    for value in data.values():
                        extract_and_send_names(value)
                elif isinstance(data, list):
                    for item in data:
                        extract_and_send_names(item)

            def send_achievement_request(achievement_name, award_amount, award_name):
                try:
                    check_url = f"https://moon.popp.club/moon/achievement/check?achievementName={achievement_name}"
                    check_response = requests.get(check_url, headers=headers)
                    check_response.raise_for_status()
                    MoonBot.print_(message=f"{Fore.GREEN}{achievement_name}{Fore.YELLOW} | Amount: {Fore.MAGENTA}{award_amount}{Fore.YELLOW} | Award: {Fore.GREEN}{award_name}{Fore.YELLOW}")
                except requests.exceptions.RequestException as e:
                    MoonBot.print_(message=f"{Fore.RED}Failed to send request for {achievement_name}: {e}")

            extract_and_send_names(achievement)

        except requests.exceptions.RequestException as e:
            MoonBot.print_(message=f"{Fore.RED}Request failed: {e}")
        except ValueError:
            MoonBot.print_(message=f"{Fore.RED}Failed to decode JSON from response")


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
                MoonBot.print_(message=f"{Fore.RED}Response JSON does not contain 'data' key")
                return []

            tasks = data["data"]
            task_details = []
            for task in tasks:
                task_id = task["taskId"]
                name = task.get("name", "N/A") 
                award_amount = task.get("award", {}).get("amount", "N/A")
                award_name = task.get("award", {}).get("award", "N/A")  
                
                task_details.append({
                    "taskId": task_id,
                    "name": name,
                    "amount": award_amount,
                    "award": award_name
                })
            return task_details

        except requests.exceptions.RequestException as e:
            MoonBot.print_(message=f"{Fore.RED}Request failed: {e}")
        except ValueError:
            MoonBot.print_(message=f"{Fore.RED}Failed to decode JSON from response")

        return []
    
    def complete_task(self, task_id, task_name, task_amount, task_award):
        """Starts and claims a task by task ID."""
        if not self.token:
            MoonBot.print_(message=f"{Fore.RED}Token not found")
            return False

        headers = {**self.common_headers, "Authorization": self.token}
        
        if not self._start_task(task_id, headers, task_name, task_amount, task_award):
            return False

        return self._claim_task(task_id, headers, task_name, task_amount, task_award)

    def _start_task(self, task_id, headers, task_name, task_amount, task_award):
        """Starts the task and handles any request errors."""
        task_url = f"https://moon.popp.club/moon/task/visit/ss?taskId={task_id}"
        payload = {"taskId": task_id}

        try:
            response_task = requests.post(task_url, headers=headers, json=payload)
            response_task.raise_for_status()
            MoonBot.print_(message=f"{Fore.GREEN}{Fore.WHITE}{task_name}{Fore.YELLOW}")
            return True

        except requests.exceptions.RequestException as e:
            MoonBot.print_(message=f"{Fore.RED}{task_name}. Request error: {e}")
        except ValueError:
            MoonBot.print_(message=f"{Fore.RED}Failed to decode JSON for start task response: {response_task.text}")
        
        return False

    def _claim_task(self, task_id, headers, task_name, task_amount, task_award):
        """Claims the task and handles any request errors."""
        claim_url = f"https://moon.popp.club/moon/task/claim?taskId={task_id}"

        try:
            response_claim = requests.get(claim_url, headers=headers)
            response_claim.raise_for_status()
            
            if response_claim.status_code == 200:
                MoonBot.print_(message=f"{Fore.GREEN}{task_name}{Fore.YELLOW} | Amount: {Fore.MAGENTA}{task_amount}{Fore.YELLOW} | Award: {Fore.GREEN}{task_award}{Fore.YELLOW}")
                return True

        except requests.exceptions.RequestException as e:
            MoonBot.print_(message=f"{Fore.RED}Failed to claim task : {Fore.WHITE}{task_name}{Fore.RED}. Request error: {e}")
        except ValueError:
            MoonBot.print_(message=f"{Fore.RED}Failed to decode JSON for claim task response: {response_claim.text}")

        return False
    
    # Claim reff
    def reff(self):
        """CLaims reff point"""
        claim_url = f"https://moon.popp.club/moon/claim/invite"
        headers = {**self.common_headers, "Authorization": self.token}

        try:
            response = requests.get(claim_url, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                MoonBot.print_(message=f"{Fore.GREEN}Successfully claim reff")
                return True
        
        except requests.exceptions.RequestException as e:
            MoonBot.print_(message=f"{Fore.RED}Failed to claim reff. Request error: {e}")
        except ValueError:
            MoonBot.print_(message=f"{Fore.RED}Failed to decode JSON for start task response: {response.text}")
        
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

        MoonBot.print_(message=f"{Fore.GREEN}Total Accounts: {total_accounts}\n")

        for index, account_data in enumerate(account_list, start=1):
            self.process_single_account(account_data, index, total_accounts)

    def process_single_account(self, account_data, index, total_accounts):
        """Processes a single account with actions like login, check-in, asset retrieval, and task completion."""
        MoonBot.print_(message=f"{Fore.GREEN}Account: {index}/{total_accounts}")
        bot = MoonBot(account_data)

        if not bot.login():
            MoonBot.print_(message=f"{Fore.RED}Failed to log in.")
            return
        MoonBot.print_(message=f"{Fore.GREEN}Successfully logged in to Account {index}.")

        if bot.check_in():
            MoonBot.print_(message=f"{Fore.GREEN}Check-in completed.")

        asset_data = bot.get_asset_data()
        config = MoonBot.load_config()
        if asset_data:
            self.display_asset_data(asset_data, bot)
            if config["reff"]:
                self.claim_reff(bot)
            else:
                MoonBot.print_(message=f"{Fore.GREEN}Reff: {Fore.RED}Off")
            if config["achievements"]:
                self.claim_achievements(bot)
            else:
                MoonBot.print_(message=f"{Fore.GREEN}Achievemtns: {Fore.RED}Off")
            if config["tasks"]:
                self.complete_tasks(bot)
            else:
                MoonBot.print_(message=f"{Fore.GREEN}Tasks: {Fore.RED}Off")

        if index == total_accounts:
            return
        
        MoonBot.print_(message=f"{Fore.WHITE}------------------------------------------------------")
        MoonBot.print_(message=f"{Fore.YELLOW} Sleep for {config["delay_change_account"]}")
        time.sleep(config["delay_change_account"])  

    def claim_rewards(self, bot):
        """Claims farming rewards for an account."""
        result = bot.claim_rewards()
        if result:
            MoonBot.print_(message=f"{Fore.GREEN}Farming rewards successfully claimed.")
        else:
            MoonBot.print_(message=f"{Fore.RED}Failed to claim farming rewards.")


    def explore_planets(self, bot):
        """Initiates planet exploration for an account."""
        bot.explore_planets()

    def claim_achievements(self, bot):
        """Claims achievements for an account."""
        MoonBot.print_(message=f"{Fore.GREEN}Achievements: On")
        bot.get_and_send_achievements()

    def complete_tasks(self, bot):
        """Retrieves and completes tasks for an account."""
        MoonBot.print_(message=f"{Fore.GREEN}Tasks: On")
        tasks = bot.get_tasks()
        for task in tasks:
            task_id = task["taskId"]
            name = task.get("name")
            award_name = task.get("award")
            award_amount = task.get("amount")
            bot.complete_task(task_id,name,award_amount,award_name)
    
    def claim_reff(self, bot):
        """Claim reff point"""
        MoonBot.print_(message=f"{Fore.GREEN}Reff: On")
        bot.reff()

    @staticmethod
    def display_asset_data(asset_data, bot):
        """Displays asset data details for an account."""
        data = asset_data.get("data", {})
        sd = data.get("sd", 0)
        probe = data.get("probe", 0)
        eth = data.get("eth", 0)

        remaining_time_ms = max(0, data.get("farmingEndTime", 0) - data.get("systemTimestamp", 0))
        hours, minutes, seconds = AccountProcessor.convert_ms_to_time(remaining_time_ms)

        MoonBot.print_(message=f"{Fore.GREEN}Status")
        MoonBot.print_(message=f"{Fore.WHITE}SD: {Fore.MAGENTA}{sd}{Style.RESET_ALL}")
        MoonBot.print_(message=f"{Fore.WHITE}Probe: {Fore.MAGENTA}{probe}{Style.RESET_ALL}")
        MoonBot.print_(message=f"{Fore.WHITE}ETH: {Fore.MAGENTA}{eth}{Style.RESET_ALL}")
        MoonBot.print_(
            message=(
                f"{Fore.WHITE}Remaining time: {Fore.YELLOW}{hours} hours, {minutes} minutes, "
                f"and {seconds} seconds{Style.RESET_ALL}"
            )
        )
        
        config = MoonBot.load_config()
        if config["farming"]:
            MoonBot.print_(message=f"{Fore.GREEN}Farming: On")
            if remaining_time_ms == 0:
                bot.claim_rewards()
        else:
            MoonBot.print_(message=f"{Fore.GREEN}Farming: {Fore.RED}Off")
        if config["planet"]:
            MoonBot.print_(message=f"{Fore.GREEN}Explore Planet: On")
            if probe > 0:
                bot.explore_planets()
        else:
            MoonBot.print_(message=f"{Fore.GREEN}Explore Planet: {Fore.RED}Off")

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
        MoonBot.print_(message=f"{Fore.WHITE}------------------------------------------------------\n")
        config = MoonBot.load_config()
        MoonBot.print_(message=f"{Fore.YELLOW}Waiting {config["delay_iteration"]} Seconds before re-processing...")
        time.sleep(config["delay_iteration"])


if __name__ == "__main__":
    main()
