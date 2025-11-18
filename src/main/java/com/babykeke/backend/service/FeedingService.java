package com.babykeke.backend.service;

import com.babykeke.backend.dto.request.CreateFeedingRecordRequest;
import com.babykeke.backend.dto.request.UpdateFeedingRecordRequest;
import com.babykeke.backend.dto.response.FeedingRecordDTO;
import com.babykeke.backend.entity.Baby;
import com.babykeke.backend.entity.FeedingRecord;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.BabyRepository;
import com.babykeke.backend.repository.FeedingRecordRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 喂养记录服务
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class FeedingService {

    private final FeedingRecordRepository feedingRecordRepository;
    private final BabyRepository babyRepository;

    /**
     * 创建喂养记录
     */
    @Transactional
    public FeedingRecordDTO createRecord(Integer babyId, CreateFeedingRecordRequest request, Integer userId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        FeedingRecord record = new FeedingRecord();
        record.setBaby(baby);
        record.setUserId(userId);
        record.setFeedingType(request.getFeedingType());
        record.setFeedingSequence(request.getFeedingSequence());
        record.setBreastSide(request.getBreastSide());
        record.setAmount(request.getAmount());
        record.setBottleContent(request.getBottleContent());
        record.setFoodName(request.getFoodName());
        record.setStartTime(request.getStartTime());
        record.setEndTime(request.getEndTime());
        record.setNotes(request.getNotes());

        record = feedingRecordRepository.save(record);

        log.info("创建喂养记录成功: babyId={}, recordId={}", babyId, record.getId());

        return convertToDTO(record);
    }

    /**
     * 获取喂养记录列表（分页）
     */
    public Page<FeedingRecordDTO> getRecords(Integer babyId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "startTime"));
        Page<FeedingRecord> records = feedingRecordRepository.findByBabyId(babyId, pageable);

        return records.map(this::convertToDTO);
    }

    /**
     * 获取喂养记录详情
     */
    public FeedingRecordDTO getRecordDetail(Integer babyId, Integer recordId) {
        FeedingRecord record = feedingRecordRepository.findById(recordId)
                .orElseThrow(() -> new ResourceNotFoundException("喂养记录不存在"));

        if (!record.getBaby().getId().equals(babyId)) {
            throw new ResourceNotFoundException("喂养记录不存在");
        }

        return convertToDTO(record);
    }

    /**
     * 更新喂养记录
     */
    @Transactional
    public FeedingRecordDTO updateRecord(Integer babyId, Integer recordId, UpdateFeedingRecordRequest request) {
        FeedingRecord record = feedingRecordRepository.findById(recordId)
                .orElseThrow(() -> new ResourceNotFoundException("喂养记录不存在"));

        if (!record.getBaby().getId().equals(babyId)) {
            throw new ResourceNotFoundException("喂养记录不存在");
        }

        // 只更新非空字段
        if (request.getFeedingType() != null) {
            record.setFeedingType(request.getFeedingType());
        }
        if (request.getFeedingSequence() != null) {
            record.setFeedingSequence(request.getFeedingSequence());
        }
        if (request.getBreastSide() != null) {
            record.setBreastSide(request.getBreastSide());
        }
        if (request.getAmount() != null) {
            record.setAmount(request.getAmount());
        }
        if (request.getBottleContent() != null) {
            record.setBottleContent(request.getBottleContent());
        }
        if (request.getFoodName() != null) {
            record.setFoodName(request.getFoodName());
        }
        if (request.getStartTime() != null) {
            record.setStartTime(request.getStartTime());
        }
        if (request.getEndTime() != null) {
            record.setEndTime(request.getEndTime());
        }
        if (request.getNotes() != null) {
            record.setNotes(request.getNotes());
        }

        record = feedingRecordRepository.save(record);

        log.info("更新喂养记录成功: babyId={}, recordId={}", babyId, recordId);

        return convertToDTO(record);
    }

    /**
     * 删除喂养记录
     */
    @Transactional
    public void deleteRecord(Integer babyId, Integer recordId) {
        FeedingRecord record = feedingRecordRepository.findById(recordId)
                .orElseThrow(() -> new ResourceNotFoundException("喂养记录不存在"));

        if (!record.getBaby().getId().equals(babyId)) {
            throw new ResourceNotFoundException("喂养记录不存在");
        }

        feedingRecordRepository.delete(record);

        log.info("删除喂养记录成功: babyId={}, recordId={}", babyId, recordId);
    }

    /**
     * 转换为 DTO
     */
    private FeedingRecordDTO convertToDTO(FeedingRecord record) {
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
}
