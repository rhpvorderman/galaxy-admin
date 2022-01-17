# Copyright (c) 2021 Leiden University Medical Center
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
A script to get all e-mail addresses from users of this particular galaxy.
"""
import argparse
from typing import Callable, Dict, List

from bioblend.galaxy import GalaxyInstance

from datetime import datetime, timedelta


def print_user_emails(galaxy: GalaxyInstance) -> None:
    user_info: List[Dict[str, str]] = galaxy.users.get_users()
    for user in user_info:
        email = user.get("email")
        if email is not None:
            print(email)


def print_usage_report(galaxy: GalaxyInstance) -> None:
    current_date = datetime.now().date()
    print("                    \tNumber of jobs\tActive users")
    days_ago = (1, 7, 30, 90, 180, 365)
    for days in days_ago:
        time_point = current_date - timedelta(days=days)
        jobs = galaxy.jobs.get_jobs(date_range_min=time_point.isoformat(),
                                    user_details=True)
        unique_users = {job.get("user_email") for job in jobs}
        print(f"In the last {days:3} day(s):\t{len(jobs):6}\t{len(unique_users):4}")


COMMANDS: Dict[str, Callable[[GalaxyInstance], None]] = {
    "user_emails": print_user_emails,
    "usage_report": print_usage_report,
}
AVAILABLE_COMMANDS = list(COMMANDS.keys())


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        help="The command to execute",
        choices=AVAILABLE_COMMANDS)
    parser.add_argument("-g", "--galaxy", type=str,
                        help="URL of the galaxy instance")
    parser.add_argument("-a", "--api-key", type=str,
                        help="Admin api key for the galaxy instance.")
    parser.add_argument("-u", "--user-email", type=str,
                        )
    parser.add_argument("-p", "--password", type=str)
    parser.add_argument("--skip-verify-tls", action="store_false",
                        dest="verify")
    return parser


def main():
    args = argument_parser().parse_args()
    galaxy = GalaxyInstance(
        url=args.galaxy,
        key=args.api_key,
        email=args.user_email,
        password=args.password,
        verify=args.verify
    )
    COMMANDS[args.command](galaxy)


if __name__ == "__main__":
    main()
