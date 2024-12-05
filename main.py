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
        """
        The `welcome_message` function prints a welcome message with the creator's name and Telegram
        contact information.
        """
        print("             This bot created by LIVEXORDS")
        print("             Telegram: t.me/livexordsscript\n")


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
        """
        The function initializes an object with initial data and parses user data from the initial data.
        
        :param init_data: The `init_data` parameter in the `__init__` method of a class is typically
        used to initialize the object with some initial data or configuration. In your code snippet, the
        `init_data` parameter is being assigned to the `init_data` attribute of the class instance
        """
        self.init_data = init_data
        self.token = None
        self.user_data = self.parse_user_data(init_data)
    
    def print_(self):
        """
        The function `print_` prints a given string with a timestamp in a specific format using color
        formatting.
        """
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] |")
        print(Fore.LIGHTBLACK_EX + timestamp + " " + self + Fore.RESET)

    def load_config():
        """Load the configuration from config.json once at the start."""
        with open('config.json') as config_file:
            config = json.load(config_file)
        return config

    @staticmethod
    def parse_user_data(init_data):
        """
        The function `parse_user_data` parses user data from an initial data string and returns specific
        attributes in a dictionary format.
        
        :param init_data: The `init_data` parameter in the `parse_user_data` function is expected to be
        a string containing user data that will be parsed and processed within the function. This data
        is typically in the form of query parameters that are part of a URL query string
        :return: The `parse_user_data` function returns a dictionary with the following keys and values:
        """
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
        """
        The `login` function sends a POST request to a login URL with payload data and retrieves a token
        if the response status code is 200.
        :return: The `login` method is returning the `self.token` value.
        """
        login_url = "https://moon.popp.club/pass/login"
        payload = {"initData": self.init_data, "initDataUnSafe": self.user_data}
        response = requests.post(login_url, headers=self.common_headers, json=payload)
        if response.status_code == 200:
            data = response.json().get("data", None)
            if data is None:
                MoonBot.print_(f"{Fore.RED}Token Expired")
                return None
            self.token = data.get("token", None)
        return self.token

    def check_in(self):
        """
        The function `check_in` sends a POST request to a specific URL with authorization headers and
        returns a boolean based on the response status code.
        :return: The `check_in` method is returning a boolean value indicating whether the POST request
        to the specified URL (`https://moon.popp.club/moon/sign/in`) was successful (status code 200) or
        not. If the `self.token` is truthy, the method sends a POST request with the token in the
        headers and returns `True` if the response status code is 200. Otherwise
        """
        if self.token:
            check_in_url = "https://moon.popp.club/moon/sign/in"
            headers = {**self.common_headers, "Authorization": self.token}
            response = requests.post(check_in_url, headers=headers)
            return response.status_code == 200
        return False

    def get_asset_data(self):
        """
        The function `get_asset_data` retrieves asset information from a specified URL using an
        authorization token.
        :return: The `get_asset_data` method returns the JSON response from the asset URL if the status
        code of the response is 200 (OK). Otherwise, it returns `None`.
        """
        if self.token:
            asset_url = "https://moon.popp.club/asset/info"
            headers = {**self.common_headers, "Authorization": self.token}
            response = requests.get(asset_url, headers=headers)
            return response.json() if response.status_code == 200 else None
        return None

    def claim_rewards(self):
        """
        This Python function `claim_rewards` checks for a token, makes a request to claim farming
        rewards, and then starts farming if successful.
        :return: The `claim_rewards` method returns a boolean value. If the token is not found, it
        returns `False`. If the request to claim farming is successful, it then makes a request to start
        farming and returns the result of that request (either `True` for success or `False` for
        failure). If the request to claim farming fails, it also returns `False`.
        """
        if not self.token:
            MoonBot.print_(f"{Fore.RED}Token not found")
            return False

        headers = {"Authorization": self.token, **self.common_headers}
        claim_farming_url = "https://moon.popp.club/moon/claim/farming"

        if self.send_request(claim_farming_url, headers, "successfully claim farming.", "failed to claim farming"):
            start_farming_url = "https://moon.popp.club/moon/farming"
            return self.send_request(start_farming_url, headers, "Successfully started farming results.", "failed to start farming results")
        return False

    def send_request(self, url, headers, success_message, failure_message):
        """
        The function `send_request` sends a GET request to a specified URL with headers and prints
        success or failure messages based on the response.
        
        :param url: The `url` parameter in the `send_request` method is the URL to which the HTTP GET
        request will be sent. It specifies the location of the resource that you want to retrieve or
        interact with
        :param headers: The `headers` parameter in the `send_request` method is used to pass any
        additional HTTP headers that need to be included in the request. These headers can contain
        information such as authentication tokens, content type, user-agent, etc. They are typically
        provided as a dictionary where the keys are the header
        :param success_message: The `success_message` parameter is a message that will be displayed when
        the request is successful. It is a string that typically provides feedback to the user or
        developer that the request was successful
        :param failure_message: The `failure_message` parameter in the `send_request` method is a
        message that will be displayed if an exception occurs during the request. It is used to provide
        feedback to the user about the failure that occurred
        :return: The `send_request` method returns a boolean value - `True` if the request was
        successful and `False` if there was an exception during the request.
        """
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            MoonBot.print_(f"{Fore.GREEN}{success_message}")
            return True
        except requests.exceptions.RequestException as e:
            MoonBot.print_(f"{Fore.RED}{failure_message}: {e}")
            return False

    def explore_planets(self):
        """Initiates exploration for each planet."""
        if not self.token:
            return
        if asset_data := self.get_asset_data():
            probe = asset_data.get("data", {}).get("probe", 0)
            if probe > 0:
                headers = {"Authorization": self.token, **self.common_headers}

                planets_url = "https://moon.popp.club/moon/planets"
                planets_response = requests.get(planets_url, headers=headers)
                if planets_response.status_code == 200:
                    planets_data = planets_response.json()
                    MoonBot.print_(f"{Fore.GREEN}ID Planet:")
                    for planet in planets_data.get("data", []):
                        planet_id = planet.get("id", "N/A")
                        MoonBot.print_(f"{Fore.GREEN}{str(planet_id)}")

                        explorer_url = f"https://moon.popp.club/moon/explorer?plantId={planet_id}"
                        explorer_response = requests.get(explorer_url, headers=headers)

                        if explorer_response.status_code == 200:
                            if explore_data := explorer_response.json().get(
                                "data", {}
                            ):
                                award_data = explore_data.get("award", [{}])
                                award = award_data[0].get("award", "N/A") if award_data else "N/A"
                                amount = award_data[0].get("amount", "N/A") if award_data else "N/A"
                            else:
                                MoonBot.print_(f"{Fore.RED}Error: Explore data is empty.")
                                award = "N/A"
                                amount = "N/A"

                            MoonBot.print_(
                                f"{Fore.CYAN}Exploration for planet {Fore.MAGENTA}{planet_id}{Style.RESET_ALL}, "
                                        f"Award: {Fore.MAGENTA}{award}{Style.RESET_ALL}, "
                                        f"Amount: {Fore.MAGENTA}{amount}{Style.RESET_ALL}"
                            )
                        else:
                            MoonBot.print_(
                                f"{Fore.RED}Exploration request for planet {planet_id} failed with status code {explorer_response.status_code}: {explorer_response.text}"
                            )
                            time.sleep(5)
                else:
                    MoonBot.print_(
                        f"{Fore.RED}Planet request failed with status code {planets_response.status_code}: {planets_response.text}"
                    )
        else:
            MoonBot.print_(f"{Fore.RED}Token not found")

    # Achievement Function
    def get_and_send_achievements(self):
        """
        The function `get_and_send_achievements` retrieves achievement data from an API, processes it,
        and sends requests for each achievement.
        :return: The `get_and_send_achievements` function returns either a success message with
        achievement details or error messages if there are any issues during the process.
        """
        if not self.token:
            return

        check_task_url = "https://moon.popp.club/moon/achievement/list"
        headers = {**self.common_headers, "Authorization": self.token}

        try:
            response = requests.get(check_task_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "data" not in data:
                MoonBot.print_(f"{Fore.RED}Response JSON does not contain 'data' key")
                return

            achievement = data["data"]

            awards_info = []

            def extract_and_send_names(data):
                """
                The function `extract_and_send_names` recursively extracts achievement names and award
                information from a nested dictionary structure and sends a request with this
                information.
                
                :param data: The `data` parameter in the `extract_and_send_names` function is expected
                to be a dictionary or a list containing information about achievements and awards. The
                function recursively extracts the names and amounts of awards from the dictionary and
                sends a request with this information. If the data is a dictionary, it looks
                """
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
                """
                The function `send_achievement_request` sends a request to check for an achievement and
                prints information about the achievement if successful.
                
                :param achievement_name: The `achievement_name` parameter is the name of the achievement
                for which you want to send a request
                :param award_amount: The `award_amount` parameter in the `send_achievement_request`
                function represents the amount of the award associated with the achievement. It is a
                numerical value that specifies how much of the award will be given upon achieving the
                specified achievement
                :param award_name: The `award_name` parameter in the `send_achievement_request` function
                is the name of the award associated with the achievement. It is used to display the
                award name when printing the achievement details
                """
                try:
                    check_url = f"https://moon.popp.club/moon/achievement/check?achievementName={achievement_name}"
                    check_response = requests.get(check_url, headers=headers)
                    check_response.raise_for_status()
                    MoonBot.print_(f"{Fore.GREEN}{achievement_name}{Fore.YELLOW} | Amount: {Fore.MAGENTA}{award_amount}{Fore.YELLOW} | Award: {Fore.GREEN}{award_name}{Fore.YELLOW}")
                except requests.exceptions.RequestException as e:
                    MoonBot.print_(f"{Fore.RED}Failed to send request for {achievement_name}: {e}")

            extract_and_send_names(achievement)

        except requests.exceptions.RequestException as e:
            MoonBot.print_(f"{Fore.RED}Request failed: {e}")
        except ValueError:
            MoonBot.print_(f"{Fore.RED}Failed to decode JSON from response")


    # Task Function
    def get_tasks(self):
        """
        This Python function retrieves tasks using a token for authorization and handles exceptions for
        failed requests and JSON decoding errors.
        :return: An empty list is being returned if the `self.token` is not set. Otherwise, the function
        makes a request to the specified URL with the headers containing the authorization token. If the
        request is successful, the function returns the result of `_extracted_from_get_tasks_9` method.
        If there is a `requests.exceptions.RequestException`, it prints a message indicating the request
        failure. If there is
        """
        if not self.token:
            return []

        check_task_url = "https://moon.popp.club/moon/task/list"
        headers = {**self.common_headers, "Authorization": self.token}

        try:
            return self._extracted_from_get_tasks_9(check_task_url, headers)
        except requests.exceptions.RequestException as e:
            MoonBot.print_(f"{Fore.RED}Request failed: {e}")
        except ValueError:
            MoonBot.print_(f"{Fore.RED}Failed to decode JSON from response")

        return []

    def _extracted_from_get_tasks_9(self, check_task_url, headers):
        """
        The function extracts task details from a JSON response obtained by sending a GET request to a
        specified URL.
        
        :param check_task_url: The `check_task_url` parameter is the URL used to make a GET request to
        retrieve task information
        :param headers: The function `_extracted_from_get_tasks_9` takes three parameters: `self`,
        `check_task_url`, and `headers`. In the context of the function, `headers` is used as a
        parameter for the HTTP request headers when making a GET request to `check_task_url` to retrieve
        :return: A list of dictionaries containing details of tasks extracted from the JSON response
        fetched from the provided URL. Each dictionary includes keys for "taskId", "name", "amount", and
        "award" with corresponding values extracted from the JSON data.
        """
        response = requests.get(check_task_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "data" not in data:
            MoonBot.print_(f"{Fore.RED}Response JSON does not contain 'data' key")
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
    
    def complete_task(self, task_id, task_name, task_amount, task_award):
        """Starts and claims a task by task ID."""
        if not self.token:
            MoonBot.print_(f"{Fore.RED}Token not found")
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
            return True

        except requests.exceptions.RequestException as e:
            MoonBot.print_(f"{Fore.RED}{task_name}. Request error: {e}")
        except ValueError:
            MoonBot.print_(f"{Fore.RED}Failed to decode JSON for start task response: {response_task.text}")
        
        return False

    def _claim_task(self, task_id, headers, task_name, task_amount, task_award):
        """Claims the task and handles any request errors."""
        claim_url = f"https://moon.popp.club/moon/task/claim?taskId={task_id}"

        try:
            response_claim = requests.get(claim_url, headers=headers)
            response_claim.raise_for_status()
            
            if response_claim.status_code == 200:
                MoonBot.print_(f"{Fore.GREEN}{task_name}{Fore.YELLOW} | Amount: {Fore.MAGENTA}{task_amount}{Fore.YELLOW} | Award: {Fore.GREEN}{task_award}")
                return True

        except requests.exceptions.RequestException as e:
            MoonBot.print_(f"{Fore.RED}Failed to claim task : {Fore.WHITE}{task_name}{Fore.RED}. Request error: {e}")
        except ValueError:
            MoonBot.print_(f"{Fore.RED}Failed to decode JSON for claim task response: {response_claim.text}")

        return False
    
    # Claim reff
    def reff(self):
        """CLaims reff point"""
        claim_url = "https://moon.popp.club/moon/claim/invite"
        headers = {**self.common_headers, "Authorization": self.token}

        try:
            response = requests.get(claim_url, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                MoonBot.print_(f"{Fore.GREEN}Successfully claim reff")
                return True

        except requests.exceptions.RequestException as e:
            MoonBot.print_(f"{Fore.RED}Failed to claim reff. Request error: {e}")
        except ValueError:
            MoonBot.print_(f"{Fore.RED}Failed to decode JSON for start task response: {response.text}")

        return False

class AccountProcessor:
    """Processes each account, handles actions like login, check-in, and asset retrieval."""

    def __init__(self, account_data_file):
        """
        The function initializes an object with an account data file attribute.
        
        :param account_data_file: The `account_data_file` parameter in the `__init__` method is used to
        initialize an instance of a class with the file path or name of the file containing account
        data. This parameter allows you to specify the location or name of the file that will be used to
        store or retrieve account information
        """
        self.account_data_file = account_data_file

    def read_account_data(self):
        """Reads account data from a file, returning non-empty lines."""
        with open(self.account_data_file, "r") as file:
            return [line.strip() for line in file if line.strip()]

    def process_all_accounts(self):
        """Processes each account: logs in, performs check-in, retrieves assets, claims rewards, explores planets, and completes tasks."""
        account_list = self.read_account_data()
        total_accounts = len(account_list)

        MoonBot.print_(f"{Fore.GREEN}Total Accounts: {total_accounts}\n")

        for index, account_data in enumerate(account_list, start=1):
            self.process_single_account(account_data, index, total_accounts)

    def process_single_account(self, account_data, index, total_accounts):
        """Processes a single account with actions like login, check-in, asset retrieval, and task completion."""
        MoonBot.print_(f"{Fore.GREEN}Account: {index}/{total_accounts}")
        bot = MoonBot(account_data)

        if not bot.login():
            MoonBot.print_(f"{Fore.RED}Failed to log in.")
            return
        MoonBot.print_(f"{Fore.GREEN}Successfully logged in to Account {index}.")

        if bot.check_in():
            MoonBot.print_(f"{Fore.GREEN}Check-in completed.")

        asset_data = bot.get_asset_data()
        config = MoonBot.load_config()
        if asset_data:
            self.display_asset_data(asset_data, bot)
            if config["reff"]:
                self.claim_reff(bot)
            else:
                MoonBot.print_(f"{Fore.GREEN}Reff: {Fore.RED}Off")
            if config["achievements"]:
                self.claim_achievements(bot)
            else:
                MoonBot.print_(f"{Fore.GREEN}Achievemtns: {Fore.RED}Off")
            if config["tasks"]:
                self.complete_tasks(bot)
            else:
                MoonBot.print_(f"{Fore.GREEN}Tasks: {Fore.RED}Off")

        if index == total_accounts:
            return
        
        MoonBot.print_(f"{Fore.WHITE}------------------------------------------------------")
        MoonBot.print_(f"{Fore.YELLOW} Sleep for {config["delay_change_account"]} Second")
        time.sleep(config["delay_change_account"])  

    def claim_rewards(self, bot):
        """Claims farming rewards for an account."""
        if result := bot.claim_rewards():
            MoonBot.print_(f"{Fore.GREEN}Farming rewards successfully claimed.")
        else:
            MoonBot.print_(f"{Fore.RED}Failed to claim farming rewards.")


    def explore_planets(self, bot):
        """Initiates planet exploration for an account."""
        bot.explore_planets()

    def claim_achievements(self, bot):
        """Claims achievements for an account."""
        MoonBot.print_(f"{Fore.GREEN}Achievements: On")
        bot.get_and_send_achievements()

    def complete_tasks(self, bot):
        """Retrieves and completes tasks for an account."""
        MoonBot.print_(f"{Fore.GREEN}Tasks: On")
        tasks = bot.get_tasks()
        for task in tasks:
            task_id = task["taskId"]
            name = task.get("name")
            award_name = task.get("award")
            award_amount = task.get("amount")
            bot.complete_task(task_id,name,award_amount,award_name)
    
    def claim_reff(self, bot):
        """Claim reff point"""
        MoonBot.print_(f"{Fore.GREEN}Reff: On")
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

        MoonBot.print_(f"{Fore.GREEN}Status")
        MoonBot.print_(f"{Fore.WHITE}SD: {Fore.MAGENTA}{sd}{Style.RESET_ALL}")
        MoonBot.print_(f"{Fore.WHITE}Probe: {Fore.MAGENTA}{probe}{Style.RESET_ALL}")
        MoonBot.print_(f"{Fore.WHITE}ETH: {Fore.MAGENTA}{eth}{Style.RESET_ALL}")
        MoonBot.print_(
            (
                f"{Fore.WHITE}Remaining time: {Fore.YELLOW}{hours} hours, {minutes} minutes, "
                f"and {seconds} seconds{Style.RESET_ALL}"
            )
        )
        
        config = MoonBot.load_config()
        if config["farming"]:
            MoonBot.print_(f"{Fore.GREEN}Farming: On")
            if remaining_time_ms == 0:
                bot.claim_rewards()
        else:
            MoonBot.print_(f"{Fore.GREEN}Farming: {Fore.RED}Off")
        if config["planet"]:
            MoonBot.print_(f"{Fore.GREEN}Explore Planet: On")
            if probe > 0:
                bot.explore_planets()
        else:
            MoonBot.print_(f"{Fore.GREEN}Explore Planet: {Fore.RED}Off")

    @staticmethod
    def convert_ms_to_time(ms):
        """Converts milliseconds to hours, minutes, and seconds."""
        total_seconds = ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return hours, minutes, seconds

def main():
    """
    The main function processes account data and waits for a specified time before re-processing.
    """
    Display.welcome_message()
    processor = AccountProcessor("query.txt")
    while True:
        processor.process_all_accounts()
        MoonBot.print_(f"{Fore.WHITE}------------------------------------------------------\n")
        config = MoonBot.load_config()
        MoonBot.print_(f"{Fore.YELLOW}Waiting {config["delay_iteration"]} Seconds before re-processing...")
        time.sleep(config["delay_iteration"])

if __name__ == "__main__":
    main()
