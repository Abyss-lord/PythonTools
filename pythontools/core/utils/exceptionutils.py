# Copyright 2024 The pythontools Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
-------------------------------------------------
@File       :   exception_util.py
@Date       :   2024/07/26
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/26
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib


class ExceptionUtil:
    @classmethod
    def get_exception_message(cls, e) -> str:
        return str(e)
