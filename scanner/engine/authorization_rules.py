
SENSITIVE_ACTIONS =[
    "Kick",
    "Ban",
    "Rank",
    "Admin"
    ]

AUTHORIZATION_CHECKS = [
    "IsAdmin",
    "GetRankInGroup",
    "role",
    "rank",
    "permission"
    ]

TARGET_KEYWORDS = [
    "targetPlayer",
    "target",
    "otherPlayer"
    ]

MODIFICATION_KEYWORDS = [
    "Coins",
    "Inventory",
    "Health",
    "Rank",
    "Data"
    ]

REMOTE_KEYWORDS=[
    "OnServerEvent"
    ]


#A001
def  check_missing_rule(code):

    has_authorization_checks= any (
        check in code
        for check in AUTHORIZATION_CHECKS
    )

    lines = code.splitlines()
    for line_number , line in  enumerate(lines, start=1):
        has_sensitive_action =any(
        action in line 
        for action in SENSITIVE_ACTIONS
        )
        if has_sensitive_action and not has_authorization_checks:
            return {
            "ruleID" : "A001",
            "title" :"Missing Role Check",
            "category" : "Authorization",
            "severity" : "High",
            "line_number" :line_number,
            "code_line": line.strip(),
            "message" : " Sensitive action detected without an authorization check"
            }
    return None


#A003
def check_cross_player_modification(code):

    lines = code.splitlines()
    for line_number , line in enumerate(lines , start=1 ):
        has_target_keywords= any(
        target in line
        for target in TARGET_KEYWORDS
        )
        has_modification_keywords = any(
        modification in line
        for modification in MODIFICATION_KEYWORDS
        )
    
        if has_target_keywords and has_modification_keywords:
            return {
                "ruleID" : "A003",
                "title" :"Cross-Player Modification",
                "category" : "Authorization",
                "severity" : "Critical",
                "line_number" :line_number,
                "code_line": line.strip(),
                "message" : "Possible modification of another player's data without proper authorization."
            }
    return None

#A004
def check_privileged_remote(code):
    lines =code.splitlines()
    
    has_remote = any(
    remote in code
    for remote in REMOTE_KEYWORDS
    )
    has_authorization = any(
    check in code
    for check in AUTHORIZATION_CHECKS
    )

    for line_number, line in enumerate(lines, start=1):
        has_sensitive_action = any(
            action in line
            for action in SENSITIVE_ACTIONS
        )
        if has_remote and has_sensitive_action and not has_authorization:
            return {
                "ruleID" : "A004",
                "title" :"Privileged Remote Without Authorization",
                "category" : "Authorization",
                "severity" : "Critical",
                "line_number" :line_number,
                "code_line": line.strip(),
                "message" : "A privileged action is triggered through OnServerEvent without a clear authorization check."
            }
    return None
    
