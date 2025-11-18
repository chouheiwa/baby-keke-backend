package com.babykeke.backend.service;

import com.babykeke.backend.dto.request.CreateSleepRecordRequest;
import com.babykeke.backend.dto.response.SleepRecordDTO;
import com.babykeke.backend.entity.Baby;
import com.babykeke.backend.entity.SleepRecord;
import com.babykeke.backend.entity.SleepSource;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.BabyRepository;
import com.babykeke.backend.repository.SleepRecordRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Duration;

@Slf4j
@Service
@RequiredArgsConstructor
public class SleepService {

    private final SleepRecordRepository sleepRecordRepository;
    private final BabyRepository babyRepository;

    @Transactional
    public SleepRecordDTO createRecord(Integer babyId, CreateSleepRecordRequest request, Integer userId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        SleepRecord record = new SleepRecord();
        record.setBaby(baby);
        record.setUserId(userId);
        record.setStatus(request.getStatus());
        record.setStartTime(request.getStartTime());
        record.setEndTime(request.getEndTime());
        record.setQuality(request.getQuality());
        record.setPosition(request.getPosition());
        record.setWakeCount(request.getWakeCount());
        record.setNotes(request.getNotes());
        record.setSource(SleepSource.manual);

        // 计算时长（分钟）
        if (request.getStartTime() != null && request.getEndTime() != null) {
            long minutes = Duration.between(request.getStartTime(), request.getEndTime()).toMinutes();
            record.setDuration((int) minutes);
        } else if (request.getDuration() != null) {
            record.setDuration(request.getDuration());
        }

        record = sleepRecordRepository.save(record);
        log.info("创建睡眠记录成功: babyId={}, recordId={}", babyId, record.getId());

        return convertToDTO(record);
    }

    public Page<SleepRecordDTO> getRecords(Integer babyId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "startTime"));
        Page<SleepRecord> records = sleepRecordRepository.findByBabyId(babyId, pageable);
        return records.map(this::convertToDTO);
    }

    @Transactional
    public void deleteRecord(Integer babyId, Integer recordId) {
        SleepRecord record = sleepRecordRepository.findById(recordId)
                .orElseThrow(() -> new ResourceNotFoundException("睡眠记录不存在"));

        if (!record.getBaby().getId().equals(babyId)) {
            throw new ResourceNotFoundException("睡眠记录不存在");
        }

        sleepRecordRepository.delete(record);
        log.info("删除睡眠记录成功: babyId={}, recordId={}", babyId, recordId);
    }

    private SleepRecordDTO convertToDTO(SleepRecord record) {
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
}
