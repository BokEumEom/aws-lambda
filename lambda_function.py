import json
import logging
import os
import urllib3

http = urllib3.PoolManager()

# Reference
# <https://blog.nodeswat.com/simple-node-js-and-slack-webhook-integration-d87c95aa9600>
   
# Get values from Environments variables
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
HOOK_URL = os.environ['HOOK_URL']
   
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_message(message):
    
    data = json.dumps(message).encode('utf-8')

    res = http.request(
        method='POST',
        url=HOOK_URL,
        body=data
    )

    print(res.data, res.status)

   
def lambda_handler(event, context):
    
    iam_event = json.loads(event.get('Records')[0].get('Sns').get('Message'))
    
    logger.info("Event        : " + str(event))
    
    # 정보
    event_id = iam_event['detail']['eventID']
    
    
    # 주체
    source_ip = iam_event['detail']['sourceIPAddress']
    arn = iam_event['detail']['userIdentity']['arn']
    principalId = iam_event['detail']['userIdentity']['principalId'].split(':')[1]

    
    # 이벤트 내역
    event_time = iam_event['detail']['eventTime']
    event_name = iam_event['detail']['eventName']
    aws_region = iam_event['detail']['awsRegion']
    event_request_parameters = iam_event['detail']['requestParameters']
    event_source = iam_event['detail']['eventSource']
    groupId = iam_event['detail']['requestParameters']['groupId']
    
    changed_resource = ""
    if event_source == "ec2.amazonaws.com":
        changed_resource += "Security Group"
    else:
        changed_resource += "IAM"
    
    # cloudtrail url
    ct_url = f"https://{aws_region}.console.aws.amazon.com/cloudtrail/home?region={aws_region}#/events/{event_id}"
    
    print(ct_url)
    
    current_event = ""
    
    for key, value in event_request_parameters.items():
        current_event += f"{key} : {value}\n"
    
    
    logger.info("SLACK Channel: " + SLACK_CHANNEL)
    logger.info("HOOK URL     : " + HOOK_URL)
    
    check_list = ["Delete", "Detach", "Revoke"]
    if any(x in event_name for x in check_list):
        color = "#eb4034"
    else:
        color = "#0c3f7d"
    
    # color = "#eb4034" if event_name.find("delete") >= 0 else "#0c3f7d"

    slack_message = {
        "channel": SLACK_CHANNEL,
        "text": f"{changed_resource} Notice",
        "icon_url": "https://avatars.slack-edge.com/2019-11-25/848832123680_64c47103e3082b32c4fe_512.png",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": '*'+ changed_resource + ' Notice.*\n\n*Request Parameters*'
                }
            },
            # {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": current_event + '\n'
                }
            },
            {"type": "divider"}
        ],
        "attachments": [{
            "fallback": "Fallback 입니다.",
            "color": color,
            "blocks": [
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": '*SecurityGroupID*\n' + groupId
                    },
                    {
                        "type": "mrkdwn",
                        "text": '*UserName*\n' + principalId
                    },
                    {
                        "type": "mrkdwn",
                        "text": '*UserAgent*\n' + source_ip
                    },
                    {
                        "type": "mrkdwn",
                        "text": '*Event Time (UTC)*\n' + event_time
                    },
                    {
                        "type": "mrkdwn",
                        "text": '*Event Name*\n' + event_name
                    },
                    {
                        "type": "mrkdwn",
                        "text": '*Region*\n' + aws_region
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "show more  :waving_white_flag:"
                        },
                        "style": "primary",
                        "url": ct_url
                    }
                ]
            },
            {
            "type": "divider"
            }
            ]
        }]
    }
    
    logger.info("Slack Message        : " + str(slack_message))
    
    send_message(slack_message)