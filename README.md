# aws-security-group-monitor
## How to Monitor and Alert AWS Security Group Modifications in Slack
AWS Security Group 생성, 삭제, 변경될 때  EventBridge를 통해 특정 CloudTrail API 호출에 대한 이벤트 패턴 규칙을 생성하여 모니터링하여 Slack으로 알람을 받을 수 있도록 구성한다.  
[참고]  
https://techblog.woowahan.com/2665/  
https://nyyang.tistory.com/126
![image](https://user-images.githubusercontent.com/43128571/174537673-af8366d2-b4e1-4704-94fe-63f2d7583acb.png)
