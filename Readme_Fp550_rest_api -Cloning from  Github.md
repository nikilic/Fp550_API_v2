pi@raspberrypi-tri:~/Public $ **cd pyProjects**/

#  Clone komanda sa url preuzet iz github:

pi@raspberrypi-tri:~/Public/pyProjects $ **git clone https://github.com/dusanvel/Fp550_rest_api.git**  
```
Cloning into 'Fp550_rest_api'...
remote: Counting objects: 119, done.
remote: Compressing objects: 100% (98/98), done.
remote: Total 119 (delta 65), reused 52 (delta 17), pack-reused 0
Receiving objects: 100% (119/119), 489.60 KiB | 0 bytes/s, done.
Resolving deltas: 100% (65/65), done.  
```


pi@raspberrypi-tri  Public/pyProjects $ **cd Fp550_rest_api/**  

pi@raspberrypi-tri  Public/pyProjects/Fp550_rest_api $ **ls**
```
app.py          config.py  README.md          static
commands.py     dv_pet.db  Requests_tests.py  swagger.yaml
commands_v1.py  orm.py     requirements.txt   test.sh
```

## Instaliranje requirements.txt

pi@raspberrypi-tri  Public/pyProjects/Fp550_rest_api $ **pip3 install -r requirements.txt**  
```
Collecting connexion (from -r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/d1/80/ccb30226af521fa22ea6e2860c11d30816bfc88b02bb25c05e9fff9e97b5/connexion-1.5.2-py2.py3-none-any.whl (1.0MB)
    100% |████████████████████████████████| 1.0MB 285kB/s 
Collecting Flask==0.10.1 (from -r requirements.txt (line 2))
  Downloading https://www.piwheels.org/simple/flask/Flask-0.10.1-py3-none-any.whl (115kB)
    100% |████████████████████████████████| 122kB 391kB/s 
Collecting SQLAlchemy>=1.0.13 (from -r requirements.txt (line 3))
  Downloading https://www.piwheels.org/simple/sqlalchemy/SQLAlchemy-1.2.10-cp35-cp35m-linux_armv7l.whl (1.1MB)
    100% |████████████████████████████████| 1.1MB 220kB/s 
Collecting Pyserial (from -r requirements.txt (line 4))
  Downloading https://files.pythonhosted.org/packages/0d/e4/2a744dd9e3be04a0c0907414e2a01a7c88bb3915cbe3c8cc06e209f59c30/pyserial-3.4-py2.py3-none-any.whl (193kB)
    100% |████████████████████████████████| 194kB 661kB/s 
Collecting PyYAML>=3.11 (from connexion->-r requirements.txt (line 1))
  Downloading https://www.piwheels.org/simple/pyyaml/PyYAML-3.13-cp35-cp35m-linux_armv7l.whl (42kB)
    100% |████████████████████████████████| 51kB 330kB/s 
Collecting typing>=3.6.1; python_version < "3.6" (from connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/05/2b/2b05bf1d5a9dd450447c9a5df3e118a465e5d3cb12b73b7220a5064a403f/typing-3.6.4-py3-none-any.whl
Collecting requests>=2.9.1 (from connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/65/47/7e02164a2a3db50ed6d8a6ab1d6d60b69c4c3fdf57a284257925dfc12bda/requests-2.19.1-py2.py3-none-any.whl (91kB)
    100% |████████████████████████████████| 92kB 1.0MB/s 
Collecting jsonschema>=2.5.1 (from connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/77/de/47e35a97b2b05c2fadbec67d44cfcdcd09b8086951b331d82de90d2912da/jsonschema-2.6.0-py2.py3-none-any.whl
Collecting clickclick>=1.2 (from connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/b6/51/2b04f7a56dcbacc0e3a7cf726e1d88d28866bf488a7a0668582306e1e643/clickclick-1.2.2-py2.py3-none-any.whl
Collecting six>=1.9 (from connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl
Collecting inflection>=0.3.1 (from connexion->-r requirements.txt (line 1))
  Downloading https://www.piwheels.org/simple/inflection/inflection-0.3.1-py3-none-any.whl
Collecting swagger-spec-validator>=2.3.1 (from connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/74/e4/0f945c923dcdb05f900426701b6d95810dc7e612045f778881dd490a38b7/swagger_spec_validator-2.3.1-py2.py3-none-any.whl
Collecting itsdangerous>=0.21 (from Flask==0.10.1->-r requirements.txt (line 2))
  Downloading https://www.piwheels.org/simple/itsdangerous/itsdangerous-0.24-py3-none-any.whl
Collecting Werkzeug>=0.7 (from Flask==0.10.1->-r requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/20/c4/12e3e56473e52375aa29c4764e70d1b8f3efa6682bef8d0aae04fe335243/Werkzeug-0.14.1-py2.py3-none-any.whl (322kB)
    100% |████████████████████████████████| 327kB 637kB/s 
Collecting Jinja2>=2.4 (from Flask==0.10.1->-r requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/7f/ff/ae64bacdfc95f27a016a7bed8e8686763ba4d277a78ca76f32659220a731/Jinja2-2.10-py2.py3-none-any.whl (126kB)
    100% |████████████████████████████████| 133kB 841kB/s 
Collecting idna<2.8,>=2.5 (from requests>=2.9.1->connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/4b/2a/0276479a4b3caeb8a8c1af2f8e4355746a97fab05a372e4a2c6a6b876165/idna-2.7-py2.py3-none-any.whl (58kB)
    100% |████████████████████████████████| 61kB 1.4MB/s 
Collecting certifi>=2017.4.17 (from requests>=2.9.1->connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/7c/e6/92ad559b7192d846975fc916b65f667c7b8c3a32bea7372340bfe9a15fa5/certifi-2018.4.16-py2.py3-none-any.whl (150kB)
    100% |████████████████████████████████| 153kB 1.3MB/s 
Collecting chardet<3.1.0,>=3.0.2 (from requests>=2.9.1->connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
    100% |████████████████████████████████| 143kB 1.3MB/s 
Collecting urllib3<1.24,>=1.21.1 (from requests>=2.9.1->connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/bd/c9/6fdd990019071a4a32a5e7cb78a1d92c53851ef4f56f62a3486e6a7d8ffb/urllib3-1.23-py2.py3-none-any.whl (133kB)
    100% |████████████████████████████████| 143kB 1.2MB/s 
Collecting click>=4.0 (from clickclick>=1.2->connexion->-r requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/34/c1/8806f99713ddb993c5366c362b2f908f18269f8d792aff1abfd700775a77/click-6.7-py2.py3-none-any.whl (71kB)
    100% |████████████████████████████████| 71kB 383kB/s 
Collecting MarkupSafe>=0.23 (from Jinja2>=2.4->Flask==0.10.1->-r requirements.txt (line 2))
  Downloading https://www.piwheels.org/simple/markupsafe/MarkupSafe-1.0-cp35-cp35m-linux_armv7l.whl
Installing collected packages: PyYAML, typing, idna, certifi, chardet, urllib3, requests, jsonschema, click, clickclick, six, itsdangerous, Werkzeug, MarkupSafe, Jinja2, Flask, inflection, swagger-spec-validator, connexion, SQLAlchemy, Pyserial
Successfully installed Flask-0.10.1 Jinja2-2.10 MarkupSafe-1.0 PyYAML-3.13 Pyserial-3.4 SQLAlchemy-1.2.10 Werkzeug-0.14.1 certifi-2018.4.16 chardet-3.0.4 click-6.7 clickclick-1.2.2 connexion-1.5.2 idna-2.7 inflection-0.3.1 itsdangerous-0.24 jsonschema-2.6.0 requests-2.19.1 six-1.11.0 swagger-spec-validator-2.3.1 typing-3.6.4 urllib3-1.23
```
## Instaliranje  programa za kameru "fswebcam"

pi@raspberrypi-tri   Public/pyProjects/Fp550_rest_api $ **sudo apt-get install fswebcam** 
```
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following NEW packages will be installed:
  fswebcam
0 upgraded, 1 newly installed, 0 to remove and 157 not upgraded.
Need to get 44.0 kB of archives.
After this operation, 105 kB of additional disk space will be used.
Get:1 http://raspbian.mirror.colo-serv.net/raspbian stretch/main armhf fswebcam armhf 20140113-1 [44.0 kB]
Fetched 44.0 kB in 0s (55.3 kB/s) 
Selecting previously unselected package fswebcam.
(Reading database ... 125304 files and directories currently installed.)
Preparing to unpack .../fswebcam_20140113-1_armhf.deb ...
Unpacking fswebcam (20140113-1) ...
Setting up fswebcam (20140113-1) ...
Processing triggers for man-db (2.7.6.1-2) ...
pi@raspberrypi-tri:~/Public/pyProjects/Fp550_rest_api $ 
```
### Startovanje python3

1. Pokrenuti na rpi3 Python 3(Idle)
2. Open file: F550_rest_api/app.py
3. Run module
4. Posmatraj rezultat u Python Shell :

WARNING:connexion.operation:... OAuth2 token info URL missing. **IGNORING SECURITY REQUIREMENTS**
INFO:werkzeug: * Running on http://0.0.0.0:8090/ (Press CTRL+C to quit)

