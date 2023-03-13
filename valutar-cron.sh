#!/usr/bin/env bash

# Check dependencies

if ! which docker; then
  echo "Docker was not found in your path"
  exit 1
fi

if ! which git; then
    echo "git was not found in your path"
    exit 1
fi

if [[ ! -s sec.py ]]; then
  echo "Secrets file does not exist!
  Create a file named sec.py with the following contents:
  Example with one receiver:

  #!/usr/bin/env python3

  email_sender = \"example_sender@gmail.com\"
  email_sender_password = \"sssenderpassword123\"
  email_receiver = \"example_receiver@gmail.com\"
  Example with multiple receivers:

  email_sender = \"example_sender@gmail.com\"
  email_sender_password = \"sssenderpassword123\"
  email_receiver = [\"example1_receiver@gmail.com\", \"example2_receiver@gmail.com\", \"example3_receiver@gmail.com\"]
  "
  exit 1
fi
# Bring the latest changes from GitHub
git pull

# Build the container and execute
docker build -t str/valutar .
docker run str/valutar
