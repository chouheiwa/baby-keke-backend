package com.babykeke.backend.controller;

import com.babykeke.backend.dto.request.CreateSleepRecordRequest;
import com.babykeke.backend.dto.response.ApiResponse;
import com.babykeke.backend.dto.response.SleepRecordDTO;
import com.babykeke.backend.security.BabyAccessValidator;
import com.babykeke.backend.security.CurrentUser;
import com.babykeke.backend.service.SleepService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/babies/{babyId}/sleep")
@RequiredArgsConstructor
public class SleepController {

    private final SleepService sleepService;
    private final BabyAccessValidator accessValidator;

    @PostMapping
    public ApiResponse<SleepRecordDTO> createRecord(@PathVariable Integer babyId,
                                                    @Valid @RequestBody CreateSleepRecordRequest request) {
        accessValidator.validateAccess(babyId);
        SleepRecordDTO record = sleepService.createRecord(babyId, request, CurrentUser.getUserId());
        return ApiResponse.success("创建睡眠记录成功", record);
    }

    @GetMapping
    public ApiResponse<Page<SleepRecordDTO>> getRecords(@PathVariable Integer babyId,
                                                        @RequestParam(defaultValue = "0") int page,
                                                        @RequestParam(defaultValue = "20") int size) {
        accessValidator.validateAccess(babyId);
        return ApiResponse.success(sleepService.getRecords(babyId, page, size));
    }

    @DeleteMapping("/{recordId}")
    public ApiResponse<Void> deleteRecord(@PathVariable Integer babyId,
                                         @PathVariable Integer recordId) {
        accessValidator.validateAccess(babyId);
        sleepService.deleteRecord(babyId, recordId);
        return ApiResponse.success("删除睡眠记录成功");
    }
}
