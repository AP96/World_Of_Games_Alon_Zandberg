(1) Run Flask App at main_score.py
(2) http://localhost:8080/job/WorldOfGamesPipeline - Build Job
(3) Jenkins Console Output: 
Started by user unknown or anonymous
Obtained Jenkinsfile from git https://github.com/AP96/World_Of_Games_Alon_Zandberg
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Declarative: Checkout SCM)
[Pipeline] checkout
Selected Git installation does not exist. Using Default
The recommended git tool is: NONE
using credential github-private-key
Cloning the remote Git repository
Cloning repository https://github.com/AP96/World_Of_Games_Alon_Zandberg
 > git.exe init C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline # timeout=10
Fetching upstream changes from https://github.com/AP96/World_Of_Games_Alon_Zandberg
 > git.exe --version # timeout=10
 > git --version # 'git version 2.41.0.windows.1'
using GIT_SSH to set credentials 
Verifying host key using known hosts file
 > git.exe fetch --tags --force --progress -- https://github.com/AP96/World_Of_Games_Alon_Zandberg +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git.exe config remote.origin.url https://github.com/AP96/World_Of_Games_Alon_Zandberg # timeout=10
 > git.exe config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10
Avoid second fetch
 > git.exe rev-parse "refs/remotes/origin/main^{commit}" # timeout=10
Checking out Revision c9270f82bace72e605170da521802709a2b74fdb (refs/remotes/origin/main)
 > git.exe config core.sparsecheckout # timeout=10
 > git.exe checkout -f c9270f82bace72e605170da521802709a2b74fdb # timeout=10
Commit message: "selenium corrected address"
 > git.exe rev-list --no-walk c9270f82bace72e605170da521802709a2b74fdb # timeout=10
[Pipeline] }
[Pipeline] // stage
[Pipeline] withEnv
[Pipeline] {
[Pipeline] withEnv
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout)
[Pipeline] echo
Checking out the repository - managed by Jenkins
[Pipeline] checkout
Selected Git installation does not exist. Using Default
The recommended git tool is: NONE
using credential github-private-key
 > git.exe rev-parse --resolve-git-dir C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline\.git # timeout=10
Fetching changes from the remote Git repository
 > git.exe config remote.origin.url https://github.com/AP96/World_Of_Games_Alon_Zandberg # timeout=10
Fetching upstream changes from https://github.com/AP96/World_Of_Games_Alon_Zandberg
 > git.exe --version # timeout=10
 > git --version # 'git version 2.41.0.windows.1'
using GIT_SSH to set credentials 
Verifying host key using known hosts file
 > git.exe fetch --tags --force --progress -- https://github.com/AP96/World_Of_Games_Alon_Zandberg +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git.exe rev-parse "refs/remotes/origin/main^{commit}" # timeout=10
Checking out Revision c9270f82bace72e605170da521802709a2b74fdb (refs/remotes/origin/main)
 > git.exe config core.sparsecheckout # timeout=10
 > git.exe checkout -f c9270f82bace72e605170da521802709a2b74fdb # timeout=10
Commit message: "selenium corrected address"
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Build)
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker build -t worldofgames:67 . 
2024/01/02 15:46:02 http2: server: error reading preface from client //./pipe/docker_engine: file has already been closed
#0 building with "default" instance using docker driver

#1 [internal] load .dockerignore
#1 transferring context: 2B done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.03kB done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/python:3.8-slim
#3 DONE 1.8s

#4 [1/8] FROM docker.io/library/python:3.8-slim@sha256:d1cba0f8754d097bd333b8f3d4c655f37c2ede9042d1e7db69561d9eae2eebfa
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 2.95kB 0.0s done
#5 DONE 0.0s

#6 [7/8] COPY scores.txt /app/scores.txt
#6 CACHED

#7 [2/8] WORKDIR /app
#7 CACHED

#8 [5/8] COPY utils.py /app/utils.py
#8 CACHED

#9 [6/8] COPY requirements.txt /app/requirements.txt
#9 CACHED

#10 [3/8] COPY main_score.py /app/main_score.py
#10 CACHED

#11 [4/8] COPY score.py /app/score.py
#11 CACHED

#12 [8/8] RUN pip install --no-cache-dir -r requirements.txt
#12 CACHED

#13 exporting to image
#13 exporting layers done
#13 writing image sha256:d3e40648a96bb98c1660740309dc8f5d471fcaaba43da0099ad3dfe6af31fcb7 done
#13 naming to docker.io/library/worldofgames:67 done
#13 DONE 0.0s

What's Next?
  1. Sign in to your Docker account â†’ docker login
  2. View a summary of image vulnerabilities and recommendations â†’ docker scout quickview
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Run Application)
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker rm -f wog_web_app   || exit 0 
Error response from daemon: No such container: wog_web_app
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker run -d --name wog_web_app -p 5001:5000 worldofgames:67 
5e89252b6b87dd521f3298940b5aae846369376fdbc7c2bc04c4754c6ee56656
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Run Selenium)
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker rm -f selenium-standalone-chrome   || exit 0 
Error response from daemon: No such container: selenium-standalone-chrome
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker run -d -p 4444:4444 --name selenium-standalone-chrome selenium/standalone-chrome:latest 
32bb410e40fc20023cd735265567aaae3be34ffcdb86083044cb6231b4e4e9b9
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Test)
[Pipeline] script
[Pipeline] {
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>curl -f http://localhost:5001/health 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100    15  100    15    0     0   1845      0 --:--:-- --:--:-- --:--:--  1875
Test Successful
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>curl -f http://localhost:4444 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (56) Recv failure: Connection was aborted
[Pipeline] echo
Waiting for Selenium server to become healthy...
[Pipeline] sleep
Sleeping for 5 sec
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>curl -f http://localhost:4444 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>python tests\e2e.py 
2024-01-02 15:46:13,518 - INFO - Starting the test.
2024-01-02 15:46:13,966 - INFO - Opening URL: http://host.docker.internal:5001/score
2024-01-02 15:46:14,093 - INFO - Waiting for the score element to be present on the page.
2024-01-02 15:46:14,180 - INFO - Score found: 136
2024-01-02 15:46:14,180 - INFO - Quitting the driver.
2024-01-02 15:46:14,251 - INFO - Test Passed Successfully!
[Pipeline] }
[Pipeline] // script
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Declarative: Post Actions)
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker stop wog_web_app   || exit 0 
wog_web_app
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker rm wog_web_app   || exit 0 
wog_web_app
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker stop selenium-standalone-chrome   || exit 0 
selenium-standalone-chrome
[Pipeline] bat

C:\Users\alons\.jenkins\workspace\WorldOfGamesPipeline>docker rm selenium-standalone-chrome   || exit 0 
selenium-standalone-chrome
[Pipeline] cleanWs
[WS-CLEANUP] Deleting project workspace...
[WS-CLEANUP] Deferred wipeout is used...
[WS-CLEANUP] done
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS
