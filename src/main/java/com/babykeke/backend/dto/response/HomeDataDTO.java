package com.babykeke.backend.dto.response;

import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 首页聚合数据响应
 */
@Data
public class HomeDataDTO {
    /**
     * 宝宝基本信息
     */
    private BabyDTO baby;

    /**
     * 最近的喂养记录
     */
    private List<FeedingRecordDTO> recentFeedings;

    /**
     * 最近的尿布记录
     */
    private List<DiaperRecordDTO> recentDiapers;

    /**
     * 最近的睡眠记录
     */
    private List<SleepRecordDTO> recentSleeps;

    /**
     * 最新的成长记录
     */
    private GrowthRecordDTO latestGrowth;

    /**
     * 今日统计
     */
    private TodayStats todayStats;

    /**
     * 今日统计数据
     */
    @Data
    public static class TodayStats {
        /**
         * 今日喂养次数
         */
        private Integer feedingCount;

        /**
         * 今日尿布次数
         */
        private Integer diaperCount;

        /**
         * 今日睡眠时长（分钟）
         */
        private Integer sleepDuration;

        /**
         * 今日睡眠次数
         */
        private Integer sleepCount;

        /**
         * 最后喂养时间
         */
        private LocalDateTime lastFeedingTime;

        /**
         * 最后换尿布时间
         */
        private LocalDateTime lastDiaperTime;

        /**
         * 最后睡眠时间
         */
        private LocalDateTime lastSleepTime;
    }
}
