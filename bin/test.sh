#!/usr/bin/env bash

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
# 清理之前的覆盖率数据
coverage erase
# 运行测试并记录覆盖率
coverage run -m pytest "$TEST_DIR"
# 生成命令行报告
coverage report --omit="$TEST_DIR/*"
# 生成HTML报告
coverage html --omit="$TEST_DIR/*"
