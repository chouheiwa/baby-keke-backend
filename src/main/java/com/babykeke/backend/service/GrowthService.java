package com.babykeke.backend.service;

import com.babykeke.backend.dto.request.CreateGrowthRecordRequest;
import com.babykeke.backend.dto.response.GrowthRecordDTO;
import com.babykeke.backend.entity.Baby;
import com.babykeke.backend.entity.GrowthRecord;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.BabyRepository;
import com.babykeke.backend.repository.GrowthRecordRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class GrowthService {

    private final GrowthRecordRepository growthRecordRepository;
    private final BabyRepository babyRepository;

    @Transactional
    public GrowthRecordDTO createRecord(Integer babyId, CreateGrowthRecordRequest request, Integer userId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        GrowthRecord record = new GrowthRecord();
        record.setBaby(baby);
        record.setUserId(userId);
        record.setRecordDate(request.getRecordDate());
        record.setWeight(request.getWeight());
        record.setHeight(request.getHeight());
        record.setHeadCircumference(request.getHeadCircumference());
        record.setNotes(request.getNotes());

        record = growthRecordRepository.save(record);
        log.info("创建成长记录成功: babyId={}, recordId={}", babyId, record.getId());

        return convertToDTO(record);
    }

    public Page<GrowthRecordDTO> getRecords(Integer babyId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "recordDate"));
        Page<GrowthRecord> records = growthRecordRepository.findByBabyId(babyId, pageable);
        return records.map(this::convertToDTO);
    }

    @Transactional
    public void deleteRecord(Integer babyId, Integer recordId) {
        GrowthRecord record = growthRecordRepository.findById(recordId)
                .orElseThrow(() -> new ResourceNotFoundException("成长记录不存在"));

        if (!record.getBaby().getId().equals(babyId)) {
            throw new ResourceNotFoundException("成长记录不存在");
        }

        growthRecordRepository.delete(record);
        log.info("删除成长记录成功: babyId={}, recordId={}", babyId, recordId);
    }

    private GrowthRecordDTO convertToDTO(GrowthRecord record) {
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
