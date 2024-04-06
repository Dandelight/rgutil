#!/bin/bash

# This utility is used to run a command in a tmux session without opening a new tmux session in foreground.
# It is best utilized when running a huge number of commands with another utility like xargs.
#
# Usage:
# ❯ bash exec_tmux.sh hello echo 'Hello, World'
# Running echo Hello, World
# ❯ bash exec_tmux.sh hello2 echo Hello, World
# Running echo Hello, World

SESSION_NAME=$1
shift # remove the first arg,
# then $COMMAND contains the remaining args
COMMAND="$@"

echo "Running $COMMAND"

# Create a session ...
tmux new-session -d -s $SESSION_NAME
# ... and just run it.
tmux send-keys -t $SESSION_NAME "$COMMAND" C-m
