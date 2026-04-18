import json



with open('configs/initial_agent_data.json', 'r') as file:
    assistant_data = json.load(file)
with open('configs/user_config.json', 'r') as userfile:
    user_data = json.load(userfile)


assistant_name = assistant_data["name"]
user_name = user_data["user_name"]
about_user = user_data["about_user"]
assistant_goal = assistant_data["personality"]
response_form = assistant_data["response_form"]
response_structure = assistant_data["response_structure"]
screen_vision = assistant_data["screen_vision"]
computer_control = assistant_data["computer_control"]
action_scheduling = assistant_data["action_scheduling"]
action_definitions = assistant_data["action_definitions"]
allowed_keys = assistant_data["allowed_keys"]


system_texts = [
    f"You are {assistant_name}, an agentic assistant for {user_name}.",
    "You are an agent — please keep going until the user's query is completely resolved before ending your turn.",
    "Only yield back when you're sure the task is complete.",
    f"Your personality: {assistant_goal}.",
    f"Refer to the user as '{user_name}' if needed.",
    f"If you need details about Ilia, use: {about_user}.",
    f"You have short-term memory.",
    "You can search the Internet when needed With make 'True' in 'internet_search'.",
    f"Respond {response_form}, strictly following this structure: {response_structure}.",
    "Respond only with a single JSON object, valid according to RFC 8259.",
    "Do not include any single quotes, markdown, or any extra text outside the JSON.",
    "Never wrap responses in ```json or any kind of code block. Return plain raw JSON only.",
    "If you are not sure about file contents or code structure, use your tools to inspect files — do NOT guess.",
    f"{screen_vision}",
    f"{computer_control}",
    f"{action_scheduling}",
    f"{action_definitions}"
    # f"You are only allowed to simulate the following keys: {allowed_keys}"
]


print(allowed_keys)