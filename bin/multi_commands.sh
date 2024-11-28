#!/bin/bash

COMMAND_FILE=$1

# commands.txt 的格式为：
# hello echo 'Hello, World'
# hello2 echo 'Greetings, Earthlings!'

# 逐行读取命令文件，并使用 exec_tmux.sh 在 tmux 会话中执行命令
while IFS= read -r line; do
    IFS=' ' read -ra COMMAND_ARGS <<<"$line"
    SESSION_NAME="${COMMAND_ARGS[0]}"

    # 创建一个新的数组，移除会话名并将剩余部分作为命令参数
    REMAINING_COMMAND_ARGS=("${COMMAND_ARGS[@]:1}")

    # 将剩余参数拼接为字符串形式的命令
    REMAINING_COMMAND=$(
        IFS=' '
        echo "${REMAINING_COMMAND_ARGS[*]}"
    )

    echo "Running command in session '$SESSION_NAME': $REMAINING_COMMAND"
    bash exec_tmux.sh "$SESSION_NAME" "$REMAINING_COMMAND"
done <"$COMMAND_FILE"
