import configparser
import requests
from pathlib import Path

DOMAIN = "bugzilla.redhat.com"
REST_URL = f"https://{DOMAIN}/rest"


def get_api_key():
    config = configparser.ConfigParser()
    paths = [
        Path(".bugzillarc"),
        # Path(Path.home(), ".config", "bugzillarc"),
        # Path(Path.home(), ".bugzillarc"),
    ]

    config.read(paths)
    return config[DOMAIN]["api_key"]


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.api_key}"
        return r


def open_session():
    session = requests.Session()
    session.auth = BearerAuth(get_api_key())
    return session


def update_bz(session, bugno, json):
    r = session.put(f"{REST_URL}/bug/{bugno}", json=json)
    r.raise_for_status()


def set_bz_flags(session, bugno, flag_dict):
    flags = [{"name": k, "status": v} for k, v in flag_dict.items()]

    print(f"Setting the following flags on {bugno}:")
    for f in flags:
        print(f"  {f['name']}: {f['status']}")

    update_bz(session, bugno, {"flags": flags})


def update_bz_keywords(session, bugno, keywords, action):
    print(f"{action} keywords {keywords} on {bugno}")

    update_bz(session, bugno, {action: keywords})


def set_bz_flag(session, bugno, flag_name, flag_val):
    set_bz_flags(session, bugno, {flag_name: flag_val})


def search_bz(session, params):
    r = session.get(f"{REST_URL}/bug", params=params)
    r.raise_for_status()
    return r.json()["bugs"]


def get_bz_bugs(session, bugs):
    bug_str = ",".join(bugs)
    return search_bz(session, {"id", bug_str})


def get_bz_bug(session, bugno):
    r = session.get(f"{REST_URL}/bug/{bugno}")
    r.raise_for_status()
    return r.json()["bugs"][0]


def add_bz_comment(session, bugno, text):
    json = {"comment": text}
    r = session.post(f"{REST_URL}/bug/{bugno}/comment", json=json)
    r.raise_for_status()


def clone_bz_bug(session, original, updates):
    # This is the list of keys that should be set when creating a new issue.
    # Copy them from the original.
    keys = [
        "product",
        "component",
        "summary",
        "version",
        "op_sys",
        "platform",
        "priority",
        "severity",
        "alias",
        "assigned_to",
        "cc",
        "groups",
        "qa_contact",
        "status",
        "target_milestone",
    ]

    clone = {k: original[k] for k in keys}
    clone.update(updates)

    # Set a custom description so that users are directed to the original
    # issue. This also helps avoid the situation where we end up turning an
    # originally-private description public.
    if "description" not in updates:
        orig_id = original["id"]
        desc = f"This is an automatically-generated clone of issue https://bugzilla.redhat.com/show_bug.cgi?id={orig_id}"
        clone["description"] = desc

    r = session.post(f"{REST_URL}/bug", json=clone)
    r.raise_for_status()

    print(r.json())

    clone_id = r.json()["id"]

    comment = f"This issue has been cloned at https://bugzilla.redhat.com/show_bug.cgi?id={clone_id}"
    add_bz_comment(session, original["id"], comment)
    return clone_id
