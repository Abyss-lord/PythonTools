#!/bin/bash

# 脚本所在目录
BIN_DIR=$(dirname "$0")
BIN_DIR=$(
    cd "$BIN_DIR" || exit 2
    pwd
)
# 项目根目录
ROOT_DIR=$(dirname "$BIN_DIR")
ROOT_DIR=$(
    cd "$ROOT_DIR" || exit 2
    pwd
)
cd "$ROOT_DIR" || exit 2

# 测试目录
TEST_DIR="$ROOT_DIR/tests"
python -m pytest "$TEST_DIR" --alluredir allure-results --clean-alluredir
allure serve allure-results
