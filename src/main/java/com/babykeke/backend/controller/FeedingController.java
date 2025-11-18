package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.CreateFeedingRecordRequest;
import com.babykeke.backend.dto.request.UpdateFeedingRecordRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.FeedingRecordDTO;
import com.babykeke.backend.security.BabyAccessValidator;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.FeedingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

/**
 * 喂养记录控制器
 */
@Slf4j
@RestController
@RequestMapping("/babies/{babyId}/feeding")
@RequiredArgsConstructor
public class FeedingController {

    private final FeedingService feedingService;
    private final BabyAccessValidator accessValidator;

    /**
     * 创建喂养记录
     */
    @PostMapping
    public ApiResponse<FeedingRecordDTO> createRecord(@PathVariable Integer babyId,
                                                      @Valid @RequestBody CreateFeedingRecordRequest request) {
        accessValidator.validateAccess(babyId);
        Integer userId = CurrentUser.getUserId();
        FeedingRecordDTO record = feedingService.createRecord(babyId, request, userId);
        return ApiResponse.success("创建喂养记录成功", record);
    }

    /**
     * 获取喂养记录列表（分页）
     */
    @GetMapping
    public ApiResponse<Page<FeedingRecordDTO>> getRecords(@PathVariable Integer babyId,
                                                          @RequestParam(defaultValue = "0") int page,
                                                          @RequestParam(defaultValue = "20") int size) {
        accessValidator.validateAccess(babyId);
        Page<FeedingRecordDTO> records = feedingService.getRecords(babyId, page, size);
        return ApiResponse.success(records);
    }

    /**
     * 获取喂养记录详情
     */
    @GetMapping("/{recordId}")
    public ApiResponse<FeedingRecordDTO> getRecordDetail(@PathVariable Integer babyId,
                                                         @PathVariable Integer recordId) {
        accessValidator.validateAccess(babyId);
        FeedingRecordDTO record = feedingService.getRecordDetail(babyId, recordId);
        return ApiResponse.success(record);
    }

    /**
     * 更新喂养记录
     */
    @PutMapping("/{recordId}")
    public ApiResponse<FeedingRecordDTO> updateRecord(@PathVariable Integer babyId,
                                                      @PathVariable Integer recordId,
                                                      @Valid @RequestBody UpdateFeedingRecordRequest request) {
        accessValidator.validateAccess(babyId);
        FeedingRecordDTO record = feedingService.updateRecord(babyId, recordId, request);
        return ApiResponse.success("更新喂养记录成功", record);
    }

    /**
     * 删除喂养记录
     */
    @DeleteMapping("/{recordId}")
    public ApiResponse<Void> deleteRecord(@PathVariable Integer babyId,
                                         @PathVariable Integer recordId) {
        accessValidator.validateAccess(babyId);
        feedingService.deleteRecord(babyId, recordId);
        return ApiResponse.success("删除喂养记录成功");
    }
}
