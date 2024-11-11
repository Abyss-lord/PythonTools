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
COVERAGE_RUN="$ROOT_DIR/.venv/bin/coverage"

# 清理之前的覆盖率数据
$COVERAGE_RUN erase
# 运行测试并记录覆盖率
$COVERAGE_RUN run -m pytest "$TEST_DIR"
# 生成命令行报告
$COVERAGE_RUN report --omit="$TEST_DIR/*"
# 生成HTML报告
$COVERAGE_RUN html --omit="$TEST_DIR/*"
