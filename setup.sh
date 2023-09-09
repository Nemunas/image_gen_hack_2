sudo apt-get update
sudo apt-get upgrade -y

sudo apt remove needrestart -y 

sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y -qq
curl https://pyenv.run | bash

echo '# pyenv' >> ~/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

sleep 1
source ~/.bashrc
source ~/.bashrc
pyenv install 3.10.4

pyenv global 3.10.4


python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Get the current script's directory path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if the command is already in crontab
if crontab -l | grep -q "travel_backend/run.sh"; then
    echo "Command already exists in crontab."
else
    # Add the command to crontab
    (crontab -l ; echo "@reboot ${SCRIPT_DIR}/run.sh") | crontab -
    echo "Command added to crontab."
fi

!mkdir logs