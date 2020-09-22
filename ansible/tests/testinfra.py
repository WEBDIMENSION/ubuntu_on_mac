import os

""" This is a testinfra for ansible program."""
# vars
host_name = "develop.local"
home_path = "/home/vagrant/"


def test_passwd_file(host):
    """ Check passwd  """
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644


def test_hostname(host):
    """ Check hostname  """
    all_variables = host.ansible.get_variables()
    assert host.sysctl("kernel.hostname") == all_variables["hostname"]


def test_enable_services(host):
    enable_services = [
        "ssh",
        "docker",
    ]
    for i in range(len(enable_services)):
        service = host.service(enable_services[i])
        assert service.is_running
        assert service.is_enabled


def test_installed_pkg(host):
    installed_pkg = [
        "git",
        "gnupg2",
        "sshpass",
        "pass",
        "zip",
        "docker-ce",
        # "python",
        "ruby",
        "zsh",
        "glances",
        "neofetch",
        "ccze",
        "neovim",
        "pwgen",
        "nmap",
        # "tmux",
        "jq",
    ]
    for i in range(len(installed_pkg)):
        pkg = host.package(installed_pkg[i])
        assert pkg.is_installed


def test_pip_packages(host):
    path = os.path.dirname(__file__) + "/../requirements.txt"
    requirements = open(path, "r")
    lines = requirements.readlines()
    for i in range(len(lines)):
        words = lines[i].split()
        assert words[0] in host.pip_package.get_packages()
    requirements.close()


def test_file_exist(host):
    pathes = [
        home_path + ".bash_it",
        home_path + ".oh-my-zsh",
        "/usr/bin/ctags",
        "/usr/local/bin/gtags",
        "/usr/local/bin/circleci",
        "/usr/local/bin/vim",
        "/usr/local/bin/lazydocker",
    ]
    for path in pathes:
        assert host.file(path).exists


def test_envs(host):
    vars = host.ansible.get_variables()
    envs = {
        "python": {
            "command": "python --version",
            "result": vars["python_version"],
            "path": home_path + ".pyenv/shims/python",
        },
        "ruby": {
            "command": "ruby --version",
            "result": vars["ruby_version"],
            "path": home_path + ".rbenv/shims/ruby",
        },
        "lua": {
            "command": "lua -v",
            "result": vars["lua_version"],
            "path": home_path + ".luaenv/shims/lua",
        },
        "go": {
            "command": "go version",
            "result": vars["golang_version"],
            "path": home_path + ".luaenv/shims/lua",
        },
    }
    for key in envs:
        version = host.ansible("command", envs[key]["command"], check=False)["stdout"]
        assert envs[key]["result"] in version
        assert host.file(envs[key]["path"]).exists


def test_apps(host):
    apps = {
        "pass": {"command": "which pass", "result": "/usr/bin/pass"},
        "sshpass": {"command": "which sshpass", "result": "/usr/bin/sshpass"},
        "git": {"command": "which git", "result": "/usr/bin/git"},
        "zip": {"command": "which zip", "result": "/usr/bin/zip"},
        "tmux": {"command": "which tmux", "result": "/usr/bin/tmux"},
        "docker": {"command": "which docker", "result": "/usr/bin/docker"},
        "docker-compose": {
            "command": "which docker-compose",
            "result": "/usr/local/bin/docker-compose",
        },
        "zsh": {"command": "which zsh", "result": "/bin/zsh"},
        "ctags": {"command": "which ctags", "result": "/usr/bin/ctags"},
        "gtags": {"command": "which gtags", "result": "/usr/local/bin/gtags"},
        "circleci": {"command": "which circleci", "result": "/usr/local/bin/circleci"},
        "glances": {"command": "which glances", "result": "/usr/bin/glances"},
        "neofetch": {"command": "which neofetch", "result": "/usr/bin/neofetch"},
        "ccze": {"command": "which ccze", "result": "/usr/bin/ccze"},
        "vim8_version": {"command": "vim --version", "result": "VIM - Vi IMproved 8."},
        "vim8_pass": {"command": "which vim", "result": "/usr/local/bin/vim"},
        "nvim": {"command": "which nvim", "result": "/usr/bin/nvim"},
        "lazydocker": {
            "command": "which lazydocker",
            "result": "/usr/local/bin/lazydocker",
        },
        "pwgen": {"command": "which pwgen", "result": "/usr/bin/pwgen"},
        "nmap": {"command": "which nmap", "result": "/usr/bin/nmap"},
        "jq": {"command": "which jq", "result": "/usr/bin/jq"},
        "tmuxp": {"command": "which tmuxp", "result": home_path + ".pyenv/shims/tmuxp"},
    }
    for key in apps:
        version = host.ansible("command", apps[key]["command"], check=False)["stdout"]
        print(version)
        assert apps[key]["result"] in version


def test_open_port(host):
    """ Check ports  """
    ports = [
        "22",
        "2376",
    ]
    localhost = host.addr("localhost")
    for port in ports:
        assert localhost.port(port).is_reachable


def test_vagrant_user(host):
    users = [
        "vagrant",
    ]
    for user in users:
        u = host.user(user)
        assert u.exists
        assert u.name == user
        assert u.home == "/home/" + user
