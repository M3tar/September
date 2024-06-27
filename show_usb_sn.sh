#!/bin/bash

# 执行ioreg命令并过滤输出，提取USB设备的序列号
ioreg -p IOUSB -l -b | grep -E "@|PortNum|USB Serial Number" | {
    while read line; do
        if [[ $line =~ "USB Serial Number" ]]; then
            # 提取并显示序列号
            serial=$(echo $line | awk -F'=' '{print $2}' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
            echo "USB Serial Number: $serial"
        fi
    done
}

