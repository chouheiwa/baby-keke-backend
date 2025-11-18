package com.babykeke.backend.entity;

/**
 * 睡眠记录状态枚举
 */
public enum SleepStatus {
    in_progress,   // 进行中
    completed,     // 已完成
    auto_closed,   // 自动关闭
    cancelled      // 已取消
}
