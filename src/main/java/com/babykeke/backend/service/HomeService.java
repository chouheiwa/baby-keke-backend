package com.babykeke.backend.service;

import com.babykeke.backend.dto.response.*;
import com.babykeke.backend.entity.*;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 首页服务
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class HomeService {

    private final BabyRepository babyRepository;
    private final BabyFamilyRepository babyFamilyRepository;
    private final FeedingRecordRepository feedingRecordRepository;
    private final DiaperRecordRepository diaperRecordRepository;
    private final SleepRecordRepository sleepRecordRepository;
    private final GrowthRecordRepository growthRecordRepository;

    /**
     * 获取首页聚合数据
     */
    public HomeDataDTO getHomeData(Integer babyId, Integer userId) {
        // 获取宝宝信息
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        BabyFamily babyFamily = babyFamilyRepository.findByBabyIdAndUserId(babyId, userId)
                .orElseThrow(() -> new ResourceNotFoundException("您不是该宝宝的家庭成员"));

        HomeDataDTO homeData = new HomeDataDTO();

        // 设置宝宝信息
        homeData.setBaby(convertBabyToDTO(baby, babyFamily));

        // 获取最近的记录（最近3条）
        Pageable pageable = PageRequest.of(0, 3, Sort.by(Sort.Direction.DESC, "startTime"));
        homeData.setRecentFeedings(feedingRecordRepository.findByBabyId(babyId, pageable)
                .stream()
                .map(this::convertFeedingToDTO)
                .collect(Collectors.toList()));

        Pageable diaperPageable = PageRequest.of(0, 3, Sort.by(Sort.Direction.DESC, "recordTime"));
        homeData.setRecentDiapers(diaperRecordRepository.findByBabyId(babyId, diaperPageable)
                .stream()
                .map(this::convertDiaperToDTO)
                .collect(Collectors.toList()));

        Pageable sleepPageable = PageRequest.of(0, 3, Sort.by(Sort.Direction.DESC, "startTime"));
        homeData.setRecentSleeps(sleepRecordRepository.findByBabyId(babyId, sleepPageable)
                .stream()
                .map(this::convertSleepToDTO)
                .collect(Collectors.toList()));

        // 获取最新的成长记录
        GrowthRecord latestGrowth = growthRecordRepository.findLatestByBabyId(babyId);
        if (latestGrowth != null) {
            homeData.setLatestGrowth(convertGrowthToDTO(latestGrowth));
        }

        // 计算今日统计
        homeData.setTodayStats(calculateTodayStats(babyId));

        return homeData;
    }

    /**
     * 计算今日统计数据
     */
    private HomeDataDTO.TodayStats calculateTodayStats(Integer babyId) {
        LocalDateTime startOfDay = LocalDateTime.of(LocalDate.now(), LocalTime.MIN);
        LocalDateTime endOfDay = LocalDateTime.of(LocalDate.now(), LocalTime.MAX);

        HomeDataDTO.TodayStats stats = new HomeDataDTO.TodayStats();

        // 今日喂养记录
        List<FeedingRecord> todayFeedings = feedingRecordRepository.findByBabyIdAndTimeRange(
                babyId, null, startOfDay, endOfDay);
        stats.setFeedingCount(todayFeedings.size());
        if (!todayFeedings.isEmpty()) {
            stats.setLastFeedingTime(todayFeedings.get(0).getStartTime());
        }

        // 今日尿布记录
        List<DiaperRecord> todayDiapers = diaperRecordRepository.findByBabyIdAndTimeRange(
                babyId, startOfDay, endOfDay);
        stats.setDiaperCount(todayDiapers.size());
        if (!todayDiapers.isEmpty()) {
            stats.setLastDiaperTime(todayDiapers.get(0).getRecordTime());
        }

        // 今日睡眠记录
        List<SleepRecord> todaySleeps = sleepRecordRepository.findByBabyIdAndTimeRange(
                babyId, startOfDay, endOfDay);
        stats.setSleepCount(todaySleeps.size());

        // 计算今日睡眠总时长
        int totalSleepDuration = todaySleeps.stream()
                .filter(s -> s.getDuration() != null)
                .mapToInt(SleepRecord::getDuration)
                .sum();
        stats.setSleepDuration(totalSleepDuration);

        if (!todaySleeps.isEmpty()) {
            stats.setLastSleepTime(todaySleeps.get(0).getStartTime());
        }

        return stats;
    }

    // ========== 转换方法 ==========

    private BabyDTO convertBabyToDTO(Baby baby, BabyFamily babyFamily) {
        BabyDTO dto = new BabyDTO();
        dto.setId(baby.getId());
        dto.setName(baby.getName());
        dto.setNickname(baby.getNickname());
        dto.setGender(baby.getGender());
        dto.setBirthday(baby.getBirthday());
        dto.setBirthWeight(baby.getBirthWeight());
        dto.setBirthHeight(baby.getBirthHeight());
        dto.setNotes(baby.getNotes());
        dto.setCreatedBy(baby.getCreatedBy());
        dto.setCreatedAt(baby.getCreatedAt());
        dto.setUpdatedAt(baby.getUpdatedAt());
        dto.setRelation(babyFamily.getRelation());
        dto.setRelationDisplay(babyFamily.getRelationDisplay());
        dto.setIsAdmin(babyFamily.getIsAdmin());
        return dto;
    }

    private FeedingRecordDTO convertFeedingToDTO(FeedingRecord record) {
        FeedingRecordDTO dto = new FeedingRecordDTO();
        dto.setId(record.getId());
        dto.setBabyId(record.getBaby().getId());
        dto.setUserId(record.getUserId());
        dto.setFeedingType(record.getFeedingType());
        dto.setFeedingSequence(record.getFeedingSequence());
        dto.setBreastSide(record.getBreastSide());
        dto.setAmount(record.getAmount());
        dto.setBottleContent(record.getBottleContent());
        dto.setFoodName(record.getFoodName());
        dto.setStartTime(record.getStartTime());
        dto.setEndTime(record.getEndTime());
        dto.setNotes(record.getNotes());
        dto.setCreatedAt(record.getCreatedAt());
        dto.setUpdatedAt(record.getUpdatedAt());
        return dto;
    }

    private DiaperRecordDTO convertDiaperToDTO(DiaperRecord record) {
        DiaperRecordDTO dto = new DiaperRecordDTO();
        dto.setId(record.getId());
        dto.setBabyId(record.getBaby().getId());
        dto.setUserId(record.getUserId());
        dto.setDiaperType(record.getDiaperType());
        dto.setPoopAmount(record.getPoopAmount());
        dto.setPoopColor(record.getPoopColor());
        dto.setPoopTexture(record.getPoopTexture());
        dto.setRecordTime(record.getRecordTime());
        dto.setNotes(record.getNotes());
        dto.setCreatedAt(record.getCreatedAt());
        dto.setUpdatedAt(record.getUpdatedAt());
        return dto;
    }

    private SleepRecordDTO convertSleepToDTO(SleepRecord record) {
        SleepRecordDTO dto = new SleepRecordDTO();
        dto.setId(record.getId());
        dto.setBabyId(record.getBaby().getId());
        dto.setUserId(record.getUserId());
        dto.setStatus(record.getStatus());
        dto.setStartTime(record.getStartTime());
        dto.setEndTime(record.getEndTime());
        dto.setDuration(record.getDuration());
        dto.setQuality(record.getQuality());
        dto.setPosition(record.getPosition());
        dto.setWakeCount(record.getWakeCount());
        dto.setNotes(record.getNotes());
        dto.setAutoClosedAt(record.getAutoClosedAt());
        dto.setSource(record.getSource());
        dto.setCreatedAt(record.getCreatedAt());
        dto.setUpdatedAt(record.getUpdatedAt());
        return dto;
    }

    private GrowthRecordDTO convertGrowthToDTO(GrowthRecord record) {
        GrowthRecordDTO dto = new GrowthRecordDTO();
        dto.setId(record.getId());
        dto.setBabyId(record.getBaby().getId());
        dto.setUserId(record.getUserId());
        dto.setRecordDate(record.getRecordDate());
        dto.setWeight(record.getWeight());
        dto.setHeight(record.getHeight());
        dto.setHeadCircumference(record.getHeadCircumference());
        dto.setNotes(record.getNotes());
        dto.setCreatedAt(record.getCreatedAt());
        dto.setUpdatedAt(record.getUpdatedAt());
        return dto;
    }
}
