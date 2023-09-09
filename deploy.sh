#!/bin/bash

# Variables
REMOTE_SERVER="ubuntu@ec2-18-170-44-95.eu-west-2.compute.amazonaws.com"
PEM_FILE="~/.ssh/puller.pem"
LOCAL_DIR="image_gen_hack/"
REMOTE_DIR="image_gen_hack/"
BACKUP_DIR="old/old_$(date +%Y%m%d_%H%M%S)"

# Files and folders to skip on remote and local
REMOTE_SKIP_LIST=("*.venv*" "*.env*" "*__pycache__*" "*old*" "*logs*")
LOCAL_SKIP_LIST=("deploy.sh" ".DS_Store" ".venv" "__pycache__" ".env" ".git")


# Get the base name of the current directory
CURRENT_DIR=$(basename "$(pwd)")

# Get the base name of LOCAL_DIR
LOCAL_DIR_BASE=$(basename "$LOCAL_DIR")

if [ "$CURRENT_DIR" == "$LOCAL_DIR_BASE" ]; then
    # echo "Current directory is LOCAL_DIR"
    echo ""
else
    echo "Current directory is not LOCAL_DIR"
    exit 1  
fi

# Create the exclude string for find command
REMOTE_EXCLUDES=""
for item in "${REMOTE_SKIP_LIST[@]}"; do
  REMOTE_EXCLUDES+="! -path '$item' "
done

# Create the exclude string for rsync command
LOCAL_EXCLUDES=""
for item in "${LOCAL_SKIP_LIST[@]}"; do
  LOCAL_EXCLUDES+="--exclude $item "
done

echo "Moving old files to backup directory."
# Move old files and folders to backup directory, excluding skipped files
ssh -i $PEM_FILE $REMOTE_SERVER "\
mkdir -p $REMOTE_DIR$BACKUP_DIR && \
find $REMOTE_DIR -mindepth 1 $REMOTE_EXCLUDES \
-exec mv {} $REMOTE_DIR$BACKUP_DIR \;"

# ssh -i $PEM_FILE $REMOTE_SERVER "mkdir -p $REMOTE_DIR$BACKUP_DIR && find $REMOTE_DIR -mindepth 1 $REMOTE_EXCLUDES -exec mv {} $REMOTE_DIR$BACKUP_DIR \;"

# Copy new files to remote server, excluding skipped files
rsync -avz -e "ssh -i $PEM_FILE" $LOCAL_EXCLUDES \
. $REMOTE_SERVER:$REMOTE_DIR