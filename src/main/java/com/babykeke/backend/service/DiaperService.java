package com.babykeke.backend.service;

import com.babykeke.backend.dto.request.CreateDiaperRecordRequest;
import com.babykeke.backend.dto.response.DiaperRecordDTO;
import com.babykeke.backend.entity.Baby;
import com.babykeke.backend.entity.DiaperRecord;
import com.babykeke.backend.exception.ResourceNotFoundException;
import com.babykeke.backend.repository.BabyRepository;
import com.babykeke.backend.repository.DiaperRecordRepository;
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
public class DiaperService {

    private final DiaperRecordRepository diaperRecordRepository;
    private final BabyRepository babyRepository;

    @Transactional
    public DiaperRecordDTO createRecord(Integer babyId, CreateDiaperRecordRequest request, Integer userId) {
        Baby baby = babyRepository.findById(babyId)
                .orElseThrow(() -> new ResourceNotFoundException("宝宝不存在"));

        DiaperRecord record = new DiaperRecord();
        record.setBaby(baby);
        record.setUserId(userId);
        record.setDiaperType(request.getDiaperType());
        record.setPoopAmount(request.getPoopAmount());
        record.setPoopColor(request.getPoopColor());
        record.setPoopTexture(request.getPoopTexture());
        record.setRecordTime(request.getRecordTime());
        record.setNotes(request.getNotes());

        record = diaperRecordRepository.save(record);
        log.info("创建尿布记录成功: babyId={}, recordId={}", babyId, record.getId());

        return convertToDTO(record);
    }

    public Page<DiaperRecordDTO> getRecords(Integer babyId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "recordTime"));
        Page<DiaperRecord> records = diaperRecordRepository.findByBabyId(babyId, pageable);
        return records.map(this::convertToDTO);
    }

    @Transactional
    public void deleteRecord(Integer babyId, Integer recordId) {
        DiaperRecord record = diaperRecordRepository.findById(recordId)
                .orElseThrow(() -> new ResourceNotFoundException("尿布记录不存在"));

        if (!record.getBaby().getId().equals(babyId)) {
            throw new ResourceNotFoundException("尿布记录不存在");
        }

        diaperRecordRepository.delete(record);
        log.info("删除尿布记录成功: babyId={}, recordId={}", babyId, recordId);
    }

    private DiaperRecordDTO convertToDTO(DiaperRecord record) {
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
}
